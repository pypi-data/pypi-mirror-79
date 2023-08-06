# -*- encoding: utf-8 -*-
# Copyright 2009-2013 Yelp and Contributors
# Copyright 2015-2018 Yelp
# Copyright 2019 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit testing of MRJob."""
import inspect
import logging
import os
import sys
import time
from io import BytesIO
from os.path import abspath
from os.path import dirname
from os.path import join
from subprocess import Popen
from subprocess import PIPE

from mrjob.conf import combine_envs
from mrjob.examples.mr_wc import MRWordCountUtility
from mrjob.job import MRJob
from mrjob.job import UsageError
from mrjob.job import _im_func
from mrjob.options import _RUNNER_ALIASES
from mrjob.options import _RUNNER_OPTS
from mrjob.parse import parse_mr_job_stderr
from mrjob.protocol import BytesValueProtocol
from mrjob.protocol import JSONProtocol
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import PickleProtocol
from mrjob.protocol import RawValueProtocol
from mrjob.protocol import ReprProtocol
from mrjob.protocol import ReprValueProtocol
from mrjob.protocol import StandardJSONProtocol
from mrjob.py2 import PY2
from mrjob.py2 import StringIO
from mrjob.step import JarStep
from mrjob.step import MRStep
from mrjob.step import SparkStep
from mrjob.step import StepFailedException
from mrjob.util import safeeval
from mrjob.util import to_lines

from tests.job import run_job
from tests.mr_cmd_job import MRCmdJob
from tests.mr_hadoop_format_job import MRHadoopFormatJob
from tests.mr_no_runner import MRNoRunner
from tests.mr_rot13lib import MRRot13Lib
from tests.mr_runner import MRRunner
from tests.mr_spark_method_wordcount import MRSparkMethodWordcount
from tests.mr_tower_of_powers import MRTowerOfPowers
from tests.mr_two_step_job import MRTwoStepJob
from tests.mr_upload_attrs_job import MRUploadAttrsJob
from tests.py2 import MagicMock
from tests.py2 import Mock
from tests.py2 import patch
from tests.sandbox import BasicTestCase
from tests.sandbox import EmptyMrjobConfTestCase
from tests.sandbox import mrjob_pythonpath
from tests.sandbox import SandboxedTestCase
from tests.sandbox import SingleSparkContextTestCase

try:
    import pyspark
    pyspark
except ImportError:
    pyspark = None


def _mock_context_mgr(m, return_value):
    m.return_value.__enter__.return_value = return_value

# These can't be invoked as a separate script, but they don't need to be


class MRCustomJob(MRJob):

    def configure_args(self):
        super(MRCustomJob, self).configure_args()

        self.add_passthru_arg(
            '--foo-size', '-F', type=int, dest='foo_size', default=5)
        self.add_passthru_arg(
            '--bar-name', '-B', dest='bar_name', default=None)
        self.add_passthru_arg(
            '--enable-baz-mode', '-M', action='store_true', dest='baz_mode',
            default=False)
        self.add_passthru_arg(
            '--disable-quuxing', '-Q', action='store_false', dest='quuxing',
            default=True)
        self.add_passthru_arg(
            '--pill-type', '-T', choices=(['red', 'blue']),
            default='blue')
        self.add_passthru_arg(
            '--planck-constant', '-C', type=float, default=6.626068e-34)
        self.add_passthru_arg(
            '--extra-special-arg', '-S', action='append',
            dest='extra_special_args', default=[])

        self.pass_arg_through('--runner')

        self.add_file_arg('--foo-config', dest='foo_config', default=None)
        self.add_file_arg('--accordian-file', dest='accordian_files',
                          action='append', default=[])


class MRBoringJob(MRJob):
    """It's a boring job, but somebody had to do it."""
    def mapper(self, key, value):
        yield(key, value)

    def reducer(self, key, values):
        yield(key, list(values))


class MRInitJob(MRJob):

    def __init__(self, *args, **kwargs):
        super(MRInitJob, self).__init__(*args, **kwargs)
        self.sum_amount = 0
        self.multiplier = 0
        self.combiner_multipler = 1

    def mapper_init(self):
        self.sum_amount += 10

    def mapper(self, key, value):
        yield(None, self.sum_amount)

    def reducer_init(self):
        self.multiplier += 10

    def reducer(self, key, values):
        yield(None, sum(values) * self.multiplier)

    def combiner_init(self):
        self.combiner_multiplier = 2

    def combiner(self, key, values):
        yield(None, sum(values) * self.combiner_multiplier)


### Test cases ###


class MRInitTestCase(EmptyMrjobConfTestCase):

    def test_mapper(self):
        j = MRInitJob([])
        j.mapper_init()
        self.assertEqual(next(j.mapper(None, None)), (None, j.sum_amount))

    def test_init_funcs(self):
        num_inputs = 2
        stdin = BytesIO(b"x\n" * num_inputs)
        mr_job = MRInitJob(['-r', 'inline', '-'])
        mr_job.sandbox(stdin=stdin)

        results = []
        with mr_job.make_runner() as runner:
            runner.run()
            results.extend(mr_job.parse_output(runner.cat_output()))

        # these numbers should match if mapper_init, reducer_init, and
        # combiner_init were called as expected
        self.assertEqual(results[0][1], num_inputs * 10 * 10 * 2)


class ParseOutputTestCase(BasicTestCase):

    def test_default_protocol(self):
        job = MRJob([])

        data = iter([b'1\t2', b'\n{"3": ', b'4}\t"fi', b've"\n'])
        self.assertEqual(
            list(job.parse_output(data)),
            [(1, 2), ({'3': 4}, 'five')])

    def test_bytes_value_protocol(self):
        job = MRJob([])
        job.OUTPUT_PROTOCOL = BytesValueProtocol

        data = iter([b'one\nt', b'wo\nthree\n', b'four\nfive\n'])
        self.assertEqual(
            list(job.parse_output(data)),
            [(None, b'one\n'),
             (None, b'two\n'),
             (None, b'three\n'),
             (None, b'four\n'),
             (None, b'five\n')])


class NoTzsetTestCase(BasicTestCase):

    def setUp(self):
        self.remove_time_tzset()

    def tearDown(self):
        """Test systems without time.tzset() (e.g. Windows). See Issue #46."""
        self.restore_time_tzset()

    def remove_time_tzset(self):
        if hasattr(time, 'tzset'):
            self._real_time_tzset = time.tzset
            del time.tzset

    def restore_time_tzset(self):
        if hasattr(self, '_real_time_tzset'):
            time.tzset = self._real_time_tzset

    def test_init_does_not_require_tzset(self):
        MRJob([])


class CountersAndStatusTestCase(BasicTestCase):

    def test_counters_and_status(self):
        mr_job = MRJob([]).sandbox()

        mr_job.increment_counter('Foo', 'Bar')
        mr_job.set_status('Initializing qux gradients...')
        mr_job.increment_counter('Foo', 'Bar')
        mr_job.increment_counter('Foo', 'Baz', 20)
        mr_job.set_status('Sorting metasyntactic variables...')

        parsed_stderr = parse_mr_job_stderr(mr_job.stderr.getvalue())

        self.assertEqual(parsed_stderr,
                         {'counters': {'Foo': {'Bar': 2, 'Baz': 20}},
                          'statuses': ['Initializing qux gradients...',
                                       'Sorting metasyntactic variables...'],
                          'other': []})

    def test_unicode_set_status(self):
        mr_job = MRJob([]).sandbox()
        # shouldn't raise an exception
        mr_job.set_status(u'💩')

    def test_unicode_counter(self):
        mr_job = MRJob([]).sandbox()
        # shouldn't raise an exception
        mr_job.increment_counter(u'💩', 'x', 1)

    def test_negative_and_zero_counters(self):
        mr_job = MRJob([]).sandbox()

        mr_job.increment_counter('Foo', 'Bar', -1)
        mr_job.increment_counter('Foo', 'Baz')
        mr_job.increment_counter('Foo', 'Baz', -1)
        mr_job.increment_counter('Qux', 'Quux', 0)

        parsed_stderr = parse_mr_job_stderr(mr_job.stderr.getvalue())
        self.assertEqual(parsed_stderr['counters'],
                         {'Foo': {'Bar': -1, 'Baz': 0}, 'Qux': {'Quux': 0}})

    def test_bad_counter_amounts(self):
        mr_job = MRJob([]).sandbox()

        self.assertRaises(TypeError,
                          mr_job.increment_counter, 'Foo', 'Bar', 'two')

        self.assertRaises(TypeError,
                          mr_job.increment_counter, 'Foo', 'Bar', None)

    def test_commas_in_counters(self):
        # commas should be replaced with semicolons
        mr_job = MRJob([]).sandbox()

        mr_job.increment_counter('Bad items', 'a, b, c')
        mr_job.increment_counter('girl, interrupted', 'movie')

        parsed_stderr = parse_mr_job_stderr(mr_job.stderr.getvalue())
        self.assertEqual(parsed_stderr['counters'],
                         {'Bad items': {'a; b; c': 1},
                          'girl; interrupted': {'movie': 1}})


class ProtocolsTestCase(BasicTestCase):
    # not putting these in their own files because we're not going to invoke
    # it as a script anyway.

    class MRBoringJob2(MRBoringJob):
        INPUT_PROTOCOL = StandardJSONProtocol
        INTERNAL_PROTOCOL = PickleProtocol
        OUTPUT_PROTOCOL = ReprProtocol

    class MRBoringJob3(MRBoringJob):

        def internal_protocol(self):
            return ReprProtocol()

    class MRBoringJob4(MRBoringJob):
        INTERNAL_PROTOCOL = ReprProtocol

    class MRTrivialJob(MRJob):
        OUTPUT_PROTOCOL = RawValueProtocol

        def mapper(self, key, value):
            yield key, value

    def assertMethodsEqual(self, fs, gs):
        # we're going to use this to match bound against unbound methods
        self.assertEqual([_im_func(f) for f in fs],
                         [_im_func(g) for g in gs])

    def test_default_protocols(self):
        mr_job = MRBoringJob([])

        self.assertMethodsEqual(
            mr_job.pick_protocols(0, 'mapper'),
            (RawValueProtocol.read, JSONProtocol.write))

        self.assertMethodsEqual(
            mr_job.pick_protocols(0, 'reducer'),
            (StandardJSONProtocol.read, JSONProtocol.write))

    def test_explicit_default_protocols(self):
        mr_job2 = self.MRBoringJob2().sandbox()
        self.assertMethodsEqual(mr_job2.pick_protocols(0, 'mapper'),
                                (JSONProtocol.read, PickleProtocol.write))
        self.assertMethodsEqual(mr_job2.pick_protocols(0, 'reducer'),
                                (PickleProtocol.read, ReprProtocol.write))

        mr_job3 = self.MRBoringJob3()
        self.assertMethodsEqual(mr_job3.pick_protocols(0, 'mapper'),
                                (RawValueProtocol.read, ReprProtocol.write))
        # output protocol should default to JSON
        self.assertMethodsEqual(mr_job3.pick_protocols(0, 'reducer'),
                                (ReprProtocol.read, JSONProtocol.write))

        mr_job4 = self.MRBoringJob4()
        self.assertMethodsEqual(mr_job4.pick_protocols(0, 'mapper'),
                                (RawValueProtocol.read, ReprProtocol.write))
        # output protocol should default to JSON
        self.assertMethodsEqual(mr_job4.pick_protocols(0, 'reducer'),
                                (ReprProtocol.read, JSONProtocol.write))

    def test_mapper_raw_value_to_json(self):
        RAW_INPUT = BytesIO(b'foo\nbar\nbaz\n')

        mr_job = MRBoringJob(['--mapper'])
        mr_job.sandbox(stdin=RAW_INPUT)
        mr_job.run_mapper()

        self.assertEqual(mr_job.stdout.getvalue(),
                         b'null\t"foo"\n' +
                         b'null\t"bar"\n' +
                         b'null\t"baz"\n')

    def test_reducer_json_to_json(self):
        JSON_INPUT = BytesIO(b'"foo"\t"bar"\n' +
                             b'"foo"\t"baz"\n' +
                             b'"bar"\t"qux"\n')

        mr_job = MRBoringJob(args=['--reducer'])
        mr_job.sandbox(stdin=JSON_INPUT)
        mr_job.run_reducer()

        # ujson doesn't add whitespace to JSON
        self.assertEqual(mr_job.stdout.getvalue().replace(b' ', b''),
                         (b'"foo"\t["bar","baz"]\n' +
                          b'"bar"\t["qux"]\n'))

    def test_output_protocol_with_no_final_reducer(self):
        # if there's no reducer, the last mapper should use the
        # output protocol (in this case, repr)
        RAW_INPUT = BytesIO(b'foo\nbar\nbaz\n')

        mr_job = self.MRTrivialJob(['--mapper'])
        mr_job.sandbox(stdin=RAW_INPUT)
        mr_job.run_mapper()

        self.assertEqual(mr_job.stdout.getvalue(),
                         RAW_INPUT.getvalue())


class ProtocolErrorsTestCase(EmptyMrjobConfTestCase):

    class MRBoringReprAndJSONJob(MRBoringJob):
        # allowing reading in bytes that can't be JSON-encoded
        INPUT_PROTOCOL = ReprValueProtocol
        INTERNAL_PROTOCOL = StandardJSONProtocol
        OUTPUT_PROTOCOL = StandardJSONProtocol

    class MRBoringJSONJob(MRJob):
        INPUT_PROTOCOL = StandardJSONProtocol
        INTERNAL_PROTOCOL = StandardJSONProtocol
        OUTPUT_PROTOCOL = StandardJSONProtocol

        def reducer(self, key, values):
            yield(key, list(values))

    BAD_JSON_INPUT = (b'BAD\tJSON\n' +
                      b'"foo"\t"bar"\n' +
                      b'"too"\t"many"\t"tabs"\n' +
                      b'"notabs"\n')

    UNENCODABLE_REPR_INPUT = (b"'foo'\n" +
                              b'set()\n' +
                              b"'bar'\n")

    def assertJobHandlesUndecodableInput(self, job_args=()):
        job = self.MRBoringJSONJob(job_args)
        job.sandbox(stdin=BytesIO(self.BAD_JSON_INPUT))

        with job.make_runner() as r:
            r.run()

            # good data should still get through
            self.assertEqual(b''.join(r.cat_output()), b'"foo"\t["bar"]\n')

            # exception type varies between JSON implementations,
            # so just make sure there were three exceptions of some sort
            counters = r.counters()[0]
            self.assertEqual(sorted(counters), ['Undecodable input'])
            self.assertEqual(
                sum(counters['Undecodable input'].values()), 3)

    def assertJobRaisesExceptionOnUndecodableInput(self, job_args=()):
        job = self.MRBoringJSONJob(job_args)
        job.sandbox(stdin=BytesIO(self.BAD_JSON_INPUT))

        with job.make_runner() as r:
            self.assertRaises(Exception, r.run)

    def assertJobHandlesUnencodableOutput(self, job_args=()):
        job = self.MRBoringReprAndJSONJob(job_args)
        job.sandbox(stdin=BytesIO(self.UNENCODABLE_REPR_INPUT))

        with job.make_runner() as r:
            r.run()

            # good data should still get through
            self.assertEqual(b''.join(r.cat_output()),
                             b'null\t["bar", "foo"]\n')

            counters = r.counters()[0]

            # there should be one Unencodable output error. Exception
            # type may vary by json implementation
            self.assertEqual(
                list(counters), ['Unencodable output'])
            self.assertEqual(
                list(counters['Unencodable output'].values()), [1])

    def assertJobRaisesExceptionOnUnencodableOutput(self, job_args=()):
        job = self.MRBoringReprAndJSONJob(job_args)
        job.sandbox(stdin=BytesIO(self.UNENCODABLE_REPR_INPUT))

        with job.make_runner() as r:
            self.assertRaises(Exception, r.run)

    def test_undecodable_input(self):
        self.assertJobRaisesExceptionOnUndecodableInput()

    def test_unencodable_output(self):
        self.assertJobRaisesExceptionOnUnencodableOutput()


class PickProtocolsTestCase(BasicTestCase):

    def _yield_none(self, *args, **kwargs):
        yield None

    def _make_job(self, steps):

        class CustomJob(MRJob):

            INPUT_PROTOCOL = PickleProtocol
            INTERNAL_PROTOCOL = JSONProtocol
            OUTPUT_PROTOCOL = JSONValueProtocol

            def steps(self):
                return steps

        args = ['--no-conf']

        return CustomJob(args)

    def _assert_script_protocols(self, steps, expected_protocols):
        """Given a list of (read_protocol_class, write_protocol_class) tuples
        for *each substep*, assert that the given _steps_desc() output for each
        substep matches the protocols in order
        """
        j = self._make_job(steps)
        for i, step in enumerate(steps):
            expected_step = expected_protocols[i]
            step_desc = step.description(i)

            if step_desc['type'] == 'jar':
                # step_type for a non-script step is undefined
                self.assertIsNone(expected_step)
            else:
                for substep_key in ('mapper', 'combiner', 'reducer'):
                    if substep_key in step_desc:
                        self.assertIn(substep_key, expected_step)
                        expected_substep = expected_step[substep_key]

                        try:
                            actual_read, actual_write = (
                                j._pick_protocol_instances(i, substep_key))
                        except ValueError:
                            self.assertIsNone(expected_substep)
                        else:
                            expected_read, expected_write = expected_substep
                            self.assertIsInstance(actual_read, expected_read)
                            self.assertIsInstance(actual_write, expected_write)
                    else:
                        self.assertNotIn(substep_key, expected_step)

    def test_single_mapper(self):
        self._assert_script_protocols(
            [MRStep(mapper=self._yield_none)],
            [dict(mapper=(PickleProtocol, JSONValueProtocol))])

    def test_single_reducer(self):
        # MRStep transparently adds mapper
        self._assert_script_protocols(
            [MRStep(reducer=self._yield_none)],
            [dict(mapper=(PickleProtocol, JSONProtocol),
                  reducer=(JSONProtocol, JSONValueProtocol))])

    def test_mapper_combiner(self):
        self._assert_script_protocols(
            [MRStep(mapper=self._yield_none,
                    combiner=self._yield_none)],
            [dict(mapper=(PickleProtocol, JSONValueProtocol),
                  combiner=(JSONValueProtocol, JSONValueProtocol))])

    def test_mapper_combiner_reducer(self):
        self._assert_script_protocols(
            [MRStep(
                mapper=self._yield_none,
                combiner=self._yield_none,
                reducer=self._yield_none)],
            [dict(mapper=(PickleProtocol, JSONProtocol),
                  combiner=(JSONProtocol, JSONProtocol),
                  reducer=(JSONProtocol, JSONValueProtocol))])

    def test_begin_jar_step(self):
        self._assert_script_protocols(
            [JarStep(jar='binks_jar.jar'),
             MRStep(
                 mapper=self._yield_none,
                 combiner=self._yield_none,
                 reducer=self._yield_none)],
            [None,
             dict(mapper=(PickleProtocol, JSONProtocol),
                  combiner=(JSONProtocol, JSONProtocol),
                  reducer=(JSONProtocol, JSONValueProtocol))])

    def test_end_jar_step(self):
        self._assert_script_protocols(
            [MRStep(
                mapper=self._yield_none,
                combiner=self._yield_none,
                reducer=self._yield_none),
             JarStep(jar='binks_jar.jar')],
            [dict(mapper=(PickleProtocol, JSONProtocol),
                  combiner=(JSONProtocol, JSONProtocol),
                  reducer=(JSONProtocol, JSONValueProtocol)),
             None])

    def test_middle_jar_step(self):
        self._assert_script_protocols(
            [MRStep(
                mapper=self._yield_none,
                combiner=self._yield_none),
             JarStep(jar='binks_jar.jar'),
             MRStep(reducer=self._yield_none)],
            [dict(mapper=(PickleProtocol, JSONProtocol),
                  combiner=(JSONProtocol, JSONProtocol)),
             None,
             dict(reducer=(JSONProtocol, JSONValueProtocol))])

    def test_single_mapper_cmd(self):
        self._assert_script_protocols(
            [MRStep(mapper_cmd='cat')],
            [dict(mapper=None)])

    def test_single_mapper_cmd_with_script_combiner(self):
        self._assert_script_protocols(
            [MRStep(
                mapper_cmd='cat',
                combiner=self._yield_none)],
            [dict(mapper=None,
                  combiner=(RawValueProtocol, RawValueProtocol))])

    def test_single_mapper_cmd_with_script_reducer(self):
        # reducer is only script step so it uses INPUT_PROTOCOL and
        # OUTPUT_PROTOCOL
        self._assert_script_protocols(
            [MRStep(
                mapper_cmd='cat',
                reducer=self._yield_none)],
            [dict(mapper=None,
                  reducer=(PickleProtocol, JSONValueProtocol))])

    def test_multistep(self):
        # reducer is only script step so it uses INPUT_PROTOCOL and
        # OUTPUT_PROTOCOL
        self._assert_script_protocols(
            [MRStep(mapper_cmd='cat',
                    reducer=self._yield_none),
             JarStep(jar='binks_jar.jar'),
             MRStep(mapper=self._yield_none)],
            [dict(mapper=None,
                  reducer=(PickleProtocol, JSONProtocol)),
             None,
             dict(mapper=(JSONProtocol, JSONValueProtocol))])


class JobConfTestCase(BasicTestCase):

    class MRJobConfJob(MRJob):
        JOBCONF = {'mapred.foo': 'garply',
                   'mapred.bar.bar.baz': 'foo'}

    class MRJobConfMethodJob(MRJob):
        def jobconf(self):
            return {'mapred.baz': 'bar'}

    class MRBoolJobConfJob(MRJob):
        JOBCONF = {'true_value': True,
                   'false_value': False}

    def test_empty(self):
        mr_job = MRJob([])

        self.assertEqual(mr_job._runner_kwargs()['jobconf'], {})

    def test_cmd_line_options(self):
        mr_job = MRJob([
            '-D', 'mapred.foo=bar',
            '-D', 'mapred.foo=baz',
            # --jobconf is the long name for -D
            '--jobconf', 'mapred.qux=quux',
        ])

        self.assertEqual(mr_job._runner_kwargs()['jobconf'],
                         {'mapred.foo': 'baz',  # second option takes priority
                          'mapred.qux': 'quux'})

    def test_bool_options_are_unchanged(self):
        # translating True to 'true' is now handled in the runner
        mr_job = self.MRBoolJobConfJob([])
        self.assertEqual(mr_job.jobconf()['true_value'], True)
        self.assertEqual(mr_job.jobconf()['false_value'], False)

    def test_jobconf_method(self):
        mr_job = self.MRJobConfJob([])

        self.assertEqual(mr_job._runner_kwargs()['jobconf'],
                         {'mapred.foo': 'garply',
                          'mapred.bar.bar.baz': 'foo'})

    def test_jobconf_attr_and_cmd_line_options(self):
        mr_job = self.MRJobConfJob([
            '-D', 'mapred.foo=bar',
            '-D', 'mapred.foo=baz',
            '-D', 'mapred.qux=quux',
        ])

        self.assertEqual(mr_job._runner_kwargs()['jobconf'],
                         {'mapred.bar.bar.baz': 'foo',
                          'mapred.foo': 'baz',  # command line takes priority
                          'mapred.qux': 'quux'})

    def test_redefined_jobconf_method(self):
        mr_job = self.MRJobConfMethodJob([])

        self.assertEqual(mr_job._runner_kwargs()['jobconf'],
                         {'mapred.baz': 'bar'})

    def test_redefined_jobconf_method_doesnt_override_cmd_line(self):
        mr_job = self.MRJobConfMethodJob([
            '-D', 'mapred.foo=bar',
            '-D', 'mapred.baz=foo',
        ])

        # -D is ignored because that's the way we defined jobconf()
        self.assertEqual(mr_job._runner_kwargs()['jobconf'],
                         {'mapred.foo': 'bar',
                          'mapred.baz': 'foo'})


class LibjarsTestCase(BasicTestCase):

    def test_default(self):
        job = MRJob([])

        self.assertEqual(job._runner_kwargs()['libjars'], [])

    def test_libjars_switch(self):
        job = MRJob(['--libjars', 'honey.jar,dora.jar'])

        self.assertEqual(job._runner_kwargs()['libjars'],
                         ['honey.jar', 'dora.jar'])

    def test_libjars_attr(self):
        with patch.object(MRJob, 'LIBJARS', ['/left/dora.jar']):
            job = MRJob([])

            self.assertEqual(job._runner_kwargs()['libjars'],
                             ['/left/dora.jar'])

    def test_libjars_attr_plus_option(self):
        with patch.object(MRJob, 'LIBJARS', ['/left/dora.jar']):
            job = MRJob(['--libjars', 'honey.jar'])

            self.assertEqual(job._runner_kwargs()['libjars'],
                             ['/left/dora.jar', 'honey.jar'])

    def test_libjars_attr_relative_path(self):
        job_dir = dirname(MRJob.mr_job_script())

        with patch.object(MRJob, 'LIBJARS', ['cookie.jar', '/left/dora.jar']):
            job = MRJob([])

            self.assertEqual(
                job._runner_kwargs()['libjars'],
                [join(job_dir, 'cookie.jar'), '/left/dora.jar'])

    def test_libjars_environment_variables(self):
        job_dir = dirname(MRJob.mr_job_script())

        with patch.dict('os.environ', A='/path/to/a', B='b'):
            with patch.object(MRJob, 'LIBJARS',
                              ['$A/cookie.jar', '$B/honey.jar']):
                job = MRJob([])

                # libjars() peeks into envvars to figure out if the path
                # is relative or absolute
                self.assertEqual(
                    job._runner_kwargs()['libjars'],
                    ['$A/cookie.jar', join(job_dir, '$B/honey.jar')])

    def test_cant_override_libjars_on_command_line(self):
        with patch.object(MRJob, 'libjars', return_value=['honey.jar']):
            job = MRJob(['--libjars', 'cookie.jar'])

            # ignore switch, don't resolve relative path
            self.assertEqual(job._runner_kwargs()['libjars'],
                             ['honey.jar', 'cookie.jar'])


class HadoopFormatTestCase(BasicTestCase):

    # MRHadoopFormatJob is imported above

    class MRHadoopFormatMethodJob(MRJob):

        def hadoop_input_format(self):
            return 'mapred.ReasonableInputFormat'

        def hadoop_output_format(self):
            # not a real Java class, thank god :)
            return 'mapred.EbcdicDb2EnterpriseXmlOutputFormat'

    def test_empty(self):
        mr_job = MRJob([])

        self.assertEqual(mr_job._runner_kwargs()['hadoop_input_format'],
                         None)
        self.assertEqual(mr_job._runner_kwargs()['hadoop_output_format'],
                         None)

    def test_hadoop_format_attributes(self):
        mr_job = MRHadoopFormatJob([])

        self.assertEqual(mr_job._runner_kwargs()['hadoop_input_format'],
                         'mapred.FooInputFormat')
        self.assertEqual(mr_job._runner_kwargs()['hadoop_output_format'],
                         'mapred.BarOutputFormat')

    def test_hadoop_format_methods(self):
        mr_job = self.MRHadoopFormatMethodJob([])

        self.assertEqual(mr_job._runner_kwargs()['hadoop_input_format'],
                         'mapred.ReasonableInputFormat')
        self.assertEqual(mr_job._runner_kwargs()['hadoop_output_format'],
                         'mapred.EbcdicDb2EnterpriseXmlOutputFormat')


class PartitionerTestCase(BasicTestCase):

    class MRPartitionerJob(MRJob):
        PARTITIONER = 'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner'

    def test_empty(self):
        mr_job = MRJob([])

        self.assertEqual(mr_job._runner_kwargs()['partitioner'], None)

    def test_partitioner_attr(self):
        mr_job = self.MRPartitionerJob([])

        self.assertEqual(
            mr_job._runner_kwargs()['partitioner'],
            'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner')


class IsTaskTestCase(BasicTestCase):

    def test_is_task(self):
        self.assertEqual(MRJob([]).is_task(), False)
        self.assertEqual(MRJob(['--mapper']).is_task(), True)
        self.assertEqual(MRJob(['--reducer']).is_task(), True)
        self.assertEqual(MRJob(['--combiner']).is_task(), True)
        self.assertEqual(MRJob(['--spark']).is_task(), True)


class StepNumTestCase(BasicTestCase):

    def test_two_step_job_end_to_end(self):
        # represent input as a list so we can reuse it
        # also, leave off newline (MRJobRunner should fix it)
        mapper0_input_lines = [b'foo', b'bar']

        def test_mapper0(mr_job, input_lines):
            mr_job.sandbox(input_lines)
            mr_job.run_mapper(0)
            self.assertEqual(mr_job.stdout.getvalue(),
                             b'null\t"foo"\n' + b'"foo"\tnull\n' +
                             b'null\t"bar"\n' + b'"bar"\tnull\n')

        mapper0 = MRTwoStepJob([])
        test_mapper0(mapper0, mapper0_input_lines)

        # --step-num=0 shouldn't actually be necessary
        mapper0_no_step_num = MRTwoStepJob(['--mapper'])
        test_mapper0(mapper0_no_step_num, mapper0_input_lines)

        # sort output of mapper0
        mapper0_output_input_lines = BytesIO(mapper0.stdout.getvalue())
        reducer0_input_lines = sorted(mapper0_output_input_lines,
                                      key=lambda line: line.split(b'\t'))

        def test_reducer0(mr_job, input_lines):
            mr_job.sandbox(input_lines)
            mr_job.run_reducer(0)
            self.assertEqual(mr_job.stdout.getvalue(),
                             b'"bar"\t1\n' + b'"foo"\t1\n' + b'null\t2\n')

        reducer0 = MRTwoStepJob([])
        test_reducer0(reducer0, reducer0_input_lines)

        # --step-num=0 shouldn't actually be necessary
        reducer0_no_step_num = MRTwoStepJob(['--reducer'])
        test_reducer0(reducer0_no_step_num, reducer0_input_lines)

        # mapper can use reducer0's output as-is
        mapper1_input_lines = BytesIO(reducer0.stdout.getvalue())

        def test_mapper1(mr_job, input_lines):
            mr_job.sandbox(input_lines)
            mr_job.run_mapper(1)
            self.assertEqual(mr_job.stdout.getvalue(),
                             b'1\t"bar"\n' + b'1\t"foo"\n' + b'2\tnull\n')

        mapper1 = MRTwoStepJob([])
        test_mapper1(mapper1, mapper1_input_lines)

    def test_nonexistent_steps(self):
        mr_job = MRTwoStepJob([])
        mr_job.sandbox()
        self.assertRaises(ValueError, mr_job.run_reducer, 1)
        self.assertRaises(ValueError, mr_job.run_mapper, 2)
        self.assertRaises(ValueError, mr_job.run_reducer, -1)

    def test_wrong_type_of_step(self):
        mr_job = MRJob([])
        mr_job.spark = MagicMock()

        self.assertRaises((TypeError, ValueError), mr_job.run_mapper)
        self.assertRaises((TypeError, ValueError), mr_job.run_combiner)
        self.assertRaises((TypeError, ValueError), mr_job.run_reducer)


class FileOptionsTestCase(SandboxedTestCase):

    def test_end_to_end(self):
        n_file_path = join(self.tmp_dir, 'n_file')

        with open(n_file_path, 'w') as f:
            f.write('3')

        os.environ['LOCAL_N_FILE_PATH'] = n_file_path

        stdin = [b'0\n', b'1\n', b'2\n']

        # use local runner so that the file is actually sent somewhere
        mr_job = MRTowerOfPowers(
            ['-v', '--cleanup=NONE', '--n-file', n_file_path,
             '--runner=local'])
        self.assertEqual(len(mr_job.steps()), 3)

        mr_job.sandbox(stdin=stdin)

        with mr_job.make_runner() as runner:
            # make sure our file gets placed in the working dir
            self.assertIn(n_file_path, runner._working_dir_mgr.paths())

            runner.run()
            output = set()
            for _, value in mr_job.parse_output(runner.cat_output()):
                output.add(value)

        self.assertEqual(set(output), set([0, 1, ((2 ** 3) ** 3) ** 3]))


class RunJobTestCase(SandboxedTestCase):

    def run_job(self, args=()):
        args = ([sys.executable, MRTwoStepJob.mr_job_script()] +
                list(args) + ['--no-conf'])
        # add . to PYTHONPATH (in case mrjob isn't actually installed)
        env = combine_envs(os.environ,
                           {'PYTHONPATH': abspath('.')})
        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
        stdout, stderr = proc.communicate(input=b'foo\nbar\nbar\n')
        return stdout, stderr, proc.returncode

    def test_quiet(self):
        stdout, stderr, returncode = self.run_job(['-q'])
        self.assertEqual(sorted(BytesIO(stdout)),
                         [b'1\t"foo"\n', b'2\t"bar"\n', b'3\tnull\n'])

        self.assertEqual(stderr, b'')
        self.assertEqual(returncode, 0)

    def test_verbose(self):
        stdout, stderr, returncode = self.run_job()
        self.assertEqual(sorted(BytesIO(stdout)),
                         [b'1\t"foo"\n', b'2\t"bar"\n', b'3\tnull\n'])

        self.assertNotEqual(stderr, '')
        self.assertEqual(returncode, 0)
        normal_stderr = stderr

        stdout, stderr, returncode = self.run_job(['-v'])
        self.assertEqual(sorted(BytesIO(stdout)),
                         [b'1\t"foo"\n', b'2\t"bar"\n', b'3\tnull\n'])

        self.assertNotEqual(stderr, b'')
        self.assertEqual(returncode, 0)
        self.assertGreater(len(stderr), len(normal_stderr))

    def test_output_dir(self):
        self.assertEqual(os.listdir(self.tmp_dir), [])  # sanity check

        stdout, stderr, returncode = self.run_job(
            ['--output-dir', self.tmp_dir])
        self.assertEqual(stdout, b'')
        self.assertNotEqual(stderr, b'')
        self.assertEqual(returncode, 0)

        # make sure the correct output is in the temp dir
        self.assertNotEqual(os.listdir(self.tmp_dir), [])
        output_lines = []
        for dirpath, _, filenames in os.walk(self.tmp_dir):
            for filename in filenames:
                with open(join(dirpath, filename), 'rb') as output_f:
                    output_lines.extend(output_f)

        self.assertEqual(sorted(output_lines),
                         [b'1\t"foo"\n', b'2\t"bar"\n', b'3\tnull\n'])

    def test_no_cat_output(self):
        stdout, stderr, returncode = self.run_job(['--no-cat-output'])
        self.assertEqual(stdout, b'')
        self.assertNotEqual(stderr, b'')
        self.assertEqual(returncode, 0)

    def test_output_dir_and_cat_output(self):
        self.assertEqual(os.listdir(self.tmp_dir), [])  # sanity check

        stdout, stderr, returncode = self.run_job(
            ['--output-dir', self.tmp_dir, '--cat-output'])
        self.assertNotEqual(stdout, b'')
        self.assertNotEqual(stderr, b'')
        self.assertEqual(returncode, 0)

        # make sure the correct output is in the temp dir
        self.assertNotEqual(os.listdir(self.tmp_dir), [])


class BadMainTestCase(BasicTestCase):
    """Ensure that the user cannot do anything but just call MRYourJob.run()
    from __main__()"""

    def test_bad_main_catch(self):
        sys.argv.append('--mapper')
        self.assertRaises(UsageError, MRBoringJob([]).make_runner)
        sys.argv = sys.argv[:-1]


class ProtocolTypeTestCase(BasicTestCase):

    class StrangeJob(MRJob):

        def INPUT_PROTOCOL(self):
            return JSONProtocol()

        def INTERNAL_PROTOCOL(self):
            return JSONProtocol()

        def OUTPUT_PROTOCOL(self):
            return JSONProtocol()

    def test_attrs_should_be_classes(self):
        log = self.start(patch('mrjob.job.log'))

        job = self.StrangeJob([])
        self.assertIsInstance(job.input_protocol(), JSONProtocol)
        self.assertIsInstance(job.internal_protocol(), JSONProtocol)
        self.assertIsInstance(job.output_protocol(), JSONProtocol)

        warnings = [args[0] for args, kwargs in log.warning.call_args_list]

        self.assertTrue(
            warnings[0].startswith('INPUT_PROTOCOL should be a class'))
        self.assertTrue(
            warnings[1].startswith('INTERNAL_PROTOCOL should be a class'))
        self.assertTrue(
            warnings[2].startswith('OUTPUT_PROTOCOL should be a class'))


class StepsTestCase(BasicTestCase):

    class SteppyJob(MRJob):

        def _yield_none(self, *args, **kwargs):
            yield None

        def steps(self):
            return [
                MRStep(mapper_init=self._yield_none, mapper_pre_filter='cat',
                       reducer_cmd='wc -l'),
                JarStep(jar='s3://bookat/binks_jar.jar')]

    class SingleSteppyCommandJob(MRJob):

        def mapper_cmd(self):
            return 'cat'

        def combiner_cmd(self):
            return 'cat'

        def reducer_cmd(self):
            return 'wc -l'

    class SingleStepJobConfMethodJob(MRJob):
        def mapper(self, key, value):
            return None

        def jobconf(self):
            return {'mapred.baz': 'bar'}

    class PreMRFilterJob(MRJob):

        def mapper_pre_filter(self):
            return 'grep m'

        def combiner_pre_filter(self):
            return 'grep c'

        def reducer_pre_filter(self):
            return 'grep r'

    # for spark testing used mock methods instead

    def test_steps(self):
        j = self.SteppyJob(['--no-conf'])
        self.assertEqual(
            j.steps()[0],
            MRStep(
                mapper_init=j._yield_none,
                mapper_pre_filter='cat',
                reducer_cmd='wc -l'))
        self.assertEqual(
            j.steps()[1], JarStep(jar='s3://bookat/binks_jar.jar'))

    def test_cmd_steps(self):
        j = self.SingleSteppyCommandJob(['--no-conf'])
        self.assertEqual(
            j._steps_desc(),
            [{
                'type': 'streaming',
                'mapper': {'type': 'command', 'command': 'cat'},
                'combiner': {'type': 'command', 'command': 'cat'},
                'reducer': {'type': 'command', 'command': 'wc -l'}}])

    def test_can_override_jobconf_method(self):
        # regression test for #656
        j = self.SingleStepJobConfMethodJob(['--no-conf'])

        # overriding jobconf() should affect _runner_kwargs()
        # but not step definitions
        self.assertEqual(j._runner_kwargs()['jobconf'],
                         {'mapred.baz': 'bar'})

        self.assertEqual(
            j.steps()[0],
            MRStep(mapper=j.mapper))

    def test_pre_filters(self):
        j = self.PreMRFilterJob(['--no-conf'])
        self.assertEqual(
            j._steps_desc(),
            [
                dict(
                    type='streaming',
                    mapper=dict(type='script', pre_filter='grep m'),
                    combiner=dict(type='script', pre_filter='grep c'),
                    reducer=dict(type='script', pre_filter='grep r'),
                )
            ])

    def test_spark_method(self):
        j = MRJob(['--no-conf'])
        j.spark = MagicMock()

        self.assertEqual(
            j.steps(),
            [SparkStep(j.spark)]
        )

        self.assertEqual(
            j._steps_desc(),
            [dict(type='spark', jobconf={}, spark_args=[])]
        )

    def test_spark_and_spark_args_methods(self):
        j = MRJob(['--no-conf'])
        j.spark = MagicMock()
        j.spark_args = MagicMock(return_value=['argh', 'ARRRRGH!'])

        self.assertEqual(
            j.steps(),
            [SparkStep(j.spark, spark_args=['argh', 'ARRRRGH!'])]
        )

        self.assertEqual(
            j._steps_desc(),
            [dict(type='spark', jobconf={}, spark_args=['argh', 'ARRRRGH!'])]
        )

    def test_spark_and_streaming_dont_mix(self):
        j = MRJob(['--no-conf'])
        j.mapper = MagicMock()
        j.spark = MagicMock()

        self.assertRaises(ValueError, j.steps)

    def test_spark_args_ignored_without_spark(self):
        j = MRJob(['--no-conf'])
        j.reducer = MagicMock()
        j.spark_args = MagicMock(spark_args=['argh', 'ARRRRGH!'])

        self.assertEqual(j.steps(), [MRStep(reducer=j.reducer)])


class RunSparkTestCase(BasicTestCase):

    def test_spark(self):
        job = MRJob(['--spark', 'input_dir', 'output_dir'])
        job.spark = MagicMock()

        job.execute()

        job.spark.assert_called_once_with('input_dir', 'output_dir')

    def test_spark_with_step_num(self):
        job = MRJob(['--step-num=1', '--spark', 'input_dir', 'output_dir'])

        mapper = MagicMock()
        spark = MagicMock()

        job.steps = Mock(
            return_value=[MRStep(mapper=mapper), SparkStep(spark)])

        job.execute()

        spark.assert_called_once_with('input_dir', 'output_dir')
        self.assertFalse(mapper.called)

    def test_wrong_step_type(self):
        job = MRJob(['--spark', 'input_dir', 'output_dir'])
        job.mapper = MagicMock()

        self.assertRaises(TypeError, job.execute)

    def test_wrong_step_num(self):
        job = MRJob(['--step-num=1', '--spark', 'input_dir', 'output_dir'])
        job.spark = MagicMock()

        self.assertRaises(ValueError, job.execute)

    def test_too_few_args(self):
        job = MRJob(['--spark'])
        job.spark = MagicMock()

        self.assertRaises(ValueError, job.execute)

    def test_too_many_args(self):
        job = MRJob(['--spark', 'input_dir', 'output_dir', 'error_dir'])
        job.spark = MagicMock()

        self.assertRaises(ValueError, job.execute)


class PrintHelpTestCase(SandboxedTestCase):

    def setUp(self):
        super(PrintHelpTestCase, self).setUp()

        self.exit = self.start(patch('sys.exit'))
        self.stdout = self.start(patch.object(sys, 'stdout', StringIO()))

    def test_basic_help(self):
        MRJob(['--help'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # basic option
        self.assertIn('--conf-path', output)

        # not basic options
        self.assertNotIn('--step-num', output)
        self.assertNotIn('--s3-endpoint', output)

        # deprecated options
        self.assertIn('add --deprecated', output)
        self.assertNotIn('--deprecated DEPRECATED', output)

    def test_basic_help_deprecated(self):
        MRJob(['--help', '--deprecated'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # basic option
        self.assertIn('--conf-path', output)

        # not basic options
        self.assertNotIn('--step-num', output)
        self.assertNotIn('--s3-endpoint', output)

        # deprecated options
        self.assertNotIn('add --deprecated', output)
        self.assertIn('--deprecated', output)

    def test_runner_help(self):
        MRJob(['--help', '-r', 'emr'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # EMR runner option
        self.assertIn('--s3-endpoint', output)

        # not runner options
        self.assertNotIn('--conf-path', output)
        self.assertNotIn('--step-num', output)

        # a runner option, but not for EMR
        self.assertNotIn('--gcp-project', output)

        # deprecated options (none as of v0.7.0, probably more to come)
        # self.assertNotIn('--some-deprecated-switch', output)  # noqa

    def test_deprecated_runner_help(self):
        MRJob(['--help', '-r', 'emr', '--deprecated'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # EMR runner option
        self.assertIn('--s3-endpoint', output)

        # not runner options
        self.assertNotIn('--conf-path', output)
        self.assertNotIn('--step-num', output)

        # a runner option, but not for EMR
        self.assertNotIn('--gcp-project', output)

        # deprecated options (none as of v0.7.0, probably more to come)
        # self.assertIn('--some-deprecated-switch', output)

    def test_runner_help_works_for_all_runners(self):
        for alias in _RUNNER_ALIASES:
            MRJob(['--help', '-r', alias])

    def test_spark_runner_help_includes_max_output_files(self):
        MRJob(['--help', '-r', 'spark'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # not a proper opt, but should appear with spark runner switches
        self.assertIn('--max-output-files', output)

    def test_steps_help(self):
        MRJob(['--help', '-v'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        # step option included
        self.assertIn('--step-num', output)

        # runner option not included
        self.assertNotIn('--s3-endpoint', output)

        # general job option also included
        self.assertIn('--conf-path', output)

    def test_passthrough_options(self):
        MRCmdJob(['--help'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        self.assertIn('--reducer-cmd-2', output)

    def test_dont_print_usage_usage(self):
        # regression test for #1866
        MRCmdJob(['--help'])
        self.exit.assert_called_once_with(0)

        output = self.stdout.getvalue()
        first_line = output.split('\n')[0]

        self.assertTrue(first_line.startswith('usage: '))
        self.assertNotIn('usage', first_line[len('usage: '):])


class RunnerKwargsTestCase(BasicTestCase):
    # ensure that switches exist for every option passed to runners

    NON_OPTION_KWARGS = set([
        'conf_paths',
        'extra_args',
        'hadoop_input_format',
        'hadoop_output_format',
        'input_paths',
        'mr_job_script',
        'output_dir',
        'partitioner',
        'sort_values',
        'stdin',
        'steps',
        'step_output_dir',
    ])

    CONF_ONLY_OPTIONS = set([
        'aws_access_key_id',
        'aws_secret_access_key',
        'aws_session_token',
    ])

    def _test_runner_kwargs(self, runner_alias):
        launcher = MRJob(args=['/path/to/script', '-r', runner_alias])

        kwargs = launcher._runner_kwargs()

        option_names = set(kwargs) - self.NON_OPTION_KWARGS - {'mrjob_cls'}

        self.assertEqual(
            option_names,
            # libjars can be set by the job
            (set(_RUNNER_OPTS) -
             self.CONF_ONLY_OPTIONS)
        )

    def test_dataproc(self):
        self._test_runner_kwargs('dataproc')

    def test_emr(self):
        self._test_runner_kwargs('emr')

    def test_hadoop(self):
        self._test_runner_kwargs('hadoop')

    def test_inline(self):
        self._test_runner_kwargs('inline')

    def test_local(self):
        self._test_runner_kwargs('local')


class UploadAttrsTestCase(SandboxedTestCase):

    def setUp(self):
        super(UploadAttrsTestCase, self).setUp()

        self.log = self.start(patch('mrjob.job.log'))

    def test_relative_files(self):
        class TestJob(MRJob):
            FILES = ['sandbox.py', 'quiet.py#q.py']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            [
                join(dirname(__file__), 'sandbox.py'),
                join(dirname(__file__), 'quiet.py#q.py'),
            ]
        )

    def test_absolute_files(self):
        class TestJob(MRJob):
            FILES = [abspath(__file__)]

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            job.FILES
        )

    def test_files_attr_combines_with_cmd_line(self):
        class TestJob(MRJob):
            FILES = ['/tmp/foo.db']

        job = TestJob(['--files', 'foo/bar.txt'])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            ['foo/bar.txt', '/tmp/foo.db']
        )

    def test_envvar_files(self):
        class TestJob(MRJob):
            FILES = ['$ABSPATH', '$RELPATH#b.txt', '~/$RELPATH']

        # verify that we check if the path will be relative or
        # absolute after expansion
        os.environ['ABSPATH'] = '/var/foo.db'
        os.environ['RELPATH'] = 'bar.txt'

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            [
                '$ABSPATH',
                join(dirname(__file__), '$RELPATH#b.txt'),
                '~/$RELPATH',
            ]
        )

    def test_files_attr_relative_subdir_warning(self):
        class TestJob(MRJob):
            FILES = ['fs/test_s3.py']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            [
                join(dirname(__file__), 'fs/test_s3.py'),
            ]
        )

        self.assertTrue(self.log.warning.called)

    def test_files_attr_no_relative_subdir_warning_with_hash(self):
        class TestJob(MRJob):
            FILES = ['fs/test_s3.py#test_s3.py']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            [
                join(dirname(__file__), 'fs/test_s3.py#test_s3.py'),
            ]
        )

        self.assertFalse(self.log.warning.called)

    def test_files_method_doesnt_qualify_path(self):
        class TestJob(MRJob):
            def files(self):
                return ['foo/bar.txt']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            ['foo/bar.txt'],
        )

    def test_files_method_can_return_string(self):
        class TestJob(MRJob):
            def files(self):
                return '/var/foo.db'

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            ['/var/foo.db'],
        )

    def test_files_method_can_return_none(self):
        class TestJob(MRJob):
            def files(self):
                pass

        job = TestJob([])

        self.assertEqual(job._runner_kwargs()['upload_files'], [])

    def test_files_method_overrides_files_attr(self):
        class TestJob(MRJob):
            FILES = ['test_runner.py']

            def files(self):
                return ['/var/foo.db']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            ['/var/foo.db'],
        )

    def test_files_method_combines_with_cmd_line(self):
        class TestJob(MRJob):
            def files(self):
                return ['foo/bar.txt']

        job = TestJob(['--files', 'baz.txt'])

        self.assertEqual(
            job._runner_kwargs()['upload_files'],
            ['baz.txt', 'foo/bar.txt'],
        )

    # DIRS and ARCHIVES use _upload_attr() too, so we don't need
    # to test them as extensively

    def test_dirs_attr(self):
        class TestJob(MRJob):
            DIRS = ['/tmp', 'fs', 'logs']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            [
                '/tmp',
                join(dirname(__file__), 'fs'),
                join(dirname(__file__), 'logs'),
            ],
        )

    def test_dirs_attr_combines_with_cmd_line(self):
        class TestJob(MRJob):
            DIRS = ['/tmp']

        job = TestJob(['--dirs', 'foo'])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            ['foo', '/tmp']
        )

    def test_dirs_method_doesnt_qualify_path(self):
        class TestJob(MRJob):
            def dirs(self):
                return ['logs']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            ['logs'],
        )

    def test_dirs_method_can_return_string(self):
        class TestJob(MRJob):
            def dirs(self):
                return '/tmp'

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            ['/tmp'],
        )

    def test_dirs_method_can_return_none(self):
        class TestJob(MRJob):

            def dirs(self):
                pass

        job = TestJob([])

        self.assertEqual(job._runner_kwargs()['upload_dirs'], [])

    def test_dirs_method_overrides_dirs_attr(self):
        class TestJob(MRJob):
            DIRS = ['logs']

            def dirs(self):
                return ['/tmp']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            ['/tmp'],
        )

    def test_dirs_method_combines_with_cmd_line(self):
        class TestJob(MRJob):
            def dirs(self):
                return ['/tmp']

        job = TestJob(['--dirs', 'stuff_dir'])

        self.assertEqual(
            job._runner_kwargs()['upload_dirs'],
            ['stuff_dir', '/tmp'],
        )

    def test_archives_attr(self):
        class TestJob(MRJob):
            ARCHIVES = ['/tmp/dir.tar.gz', 'foo.zip']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            [
                '/tmp/dir.tar.gz',
                join(dirname(__file__), 'foo.zip'),
            ],
        )

    def test_archives_attr_combines_with_cmd_line(self):
        class TestJob(MRJob):
            ARCHIVES = ['/tmp/dir.tar.gz']

        job = TestJob(['--archives', 'foo.zip'])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            ['foo.zip', '/tmp/dir.tar.gz']
        )

    def test_archives_method_doesnt_qualify_path(self):
        class TestJob(MRJob):

            def archives(self):
                return ['logs.tar.gz']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            ['logs.tar.gz'],
        )

    def test_archives_method_can_return_string(self):
        class TestJob(MRJob):

            def archives(self):
                return '/tmp/dir.tar.gz'

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            ['/tmp/dir.tar.gz'],
        )

    def test_archives_method_can_return_none(self):
        class TestJob(MRJob):

            def archives(self):
                pass

        job = TestJob([])

        self.assertEqual(job._runner_kwargs()['upload_archives'], [])

    def test_archives_method_overrides_dirs_attr(self):
        class TestJob(MRJob):
            ARCHIVES = ['logs.tar.gz']

            def archives(self):
                return ['/tmp/dirs.tar.gz']

        job = TestJob([])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            ['/tmp/dirs.tar.gz'],
        )

    def test_archives_method_combines_with_cmd_line(self):
        class TestJob(MRJob):
            def archives(self):
                return ['/tmp/dir.tar.gz']

        job = TestJob(['--archives', 'stuff.zip'])

        self.assertEqual(
            job._runner_kwargs()['upload_archives'],
            ['stuff.zip', '/tmp/dir.tar.gz'],
        )

    def test_attrs_with_real_job(self):
        # MRUploadAttrsJob uses FILES, DIRS, and ARCHIVES to upload
        # a static set of files
        self.assertEqual(
            set(run_job(MRUploadAttrsJob([]))),
            {
                '.',
                './empty',
                './empty.tar.gz',
                './mr_upload_attrs_job',
                './mr_upload_attrs_job.py',
                './mr_upload_attrs_job/empty.tar.gz',
                './mr_upload_attrs_job/README.txt',
                './README.txt',
            }
        )

    def test_use_dirs_to_import_code(self):
        self.assertEqual(
            run_job(MRRot13Lib([]), b'The quick brown fox'),
            {None: 'Gur dhvpx oebja sbk\n'}
        )


# SingleSparkContextTestCase is skipped if there's no pyspark
class SparkJobMethodsTestCase(SandboxedTestCase, SingleSparkContextTestCase):
    # regression test for #2039

    def setUp(self):
        super(SparkJobMethodsTestCase, self).setUp()

        import warnings
        warnings.filterwarnings('error')

        # ensure that we aren't sandboxing the job. This used to be
        # the way we made Spark jobs serializable; see #2039
        self.job_sandbox = self.start(
            patch('mrjob.job.MRJob.sandbox'))

    def test_job_can_be_pickled_and_unpicked(self):
        job = MRJob([])

        pickled_job = pyspark.cloudpickle.dumps(job)
        pyspark.cloudpickle.loads(pickled_job)

    def test_spark_can_serialize_job_methods(self):
        input_path = self.makefile(
            'input', b'one fish\ntwo fish\nred fish\nblue fish\n')

        job = MRSparkMethodWordcount(['-r', 'inline', input_path])
        # don't sandbox; we want to see if Spark can handle an un-sandboxed job

        counts = {}

        with job.make_runner() as runner:
            runner.run()

            for line in to_lines(runner.cat_output()):
                k, v = safeeval(line)
                counts[k] = v

        self.assertEqual(counts, dict(
            blue=1, fish=4, one=1, red=1, two=1))

        # check that we didn't alter the job to make it serializable
        self.assertFalse(self.job_sandbox.called)


class IntermixedArgsTestCase(SandboxedTestCase):

    def test_intermixed_args(self):
        # test of #1701

        file1 = self.makefile('file1', b'the quick brown fox')
        file2 = self.makefile('file2', b'jumped over\nthe lazy dogs')
        args = [file1, '-v', file2]

        if sys.version_info < (3, 7):
            # argparse can't do this before Python 3.7
            self.assertRaises(ValueError, MRWordCountUtility, args)
        else:
            job = MRWordCountUtility(args)

            with job.make_runner() as runner:
                runner.run()
                output = dict(job.parse_output(runner.cat_output()))

                self.assertEqual(output, dict(chars=46, words=9, lines=3))


class LaunchJobTestCase(SandboxedTestCase):

    def _make_launcher(self, *args):
        """Make a launcher, add a mock runner (``launcher.mock_runner``), and
        set it up so that ``launcher.make_runner().__enter__()`` returns
        ``launcher.mock_runner()``.
        """
        launcher = MRJob(args=['--no-conf', ''] + list(args))
        launcher.sandbox()

        launcher.mock_runner = Mock()
        launcher.mock_runner.cat_output.return_value = [b'a line\n']

        launcher.make_runner = MagicMock()  # include __enter__
        launcher.make_runner.return_value.__enter__.return_value = (
            launcher.mock_runner)

        return launcher

    def test_output(self):
        launcher = self._make_launcher()

        launcher.run_job()

        self.assertEqual(launcher.stdout.getvalue(), b'a line\n')
        self.assertEqual(launcher.stderr.getvalue(), b'')

    def test_no_cat_output(self):
        launcher = self._make_launcher('--no-cat-output')

        launcher.run_job()

        self.assertEqual(launcher.stdout.getvalue(), b'')
        self.assertEqual(launcher.stderr.getvalue(), b'')

    def test_output_dir_implies_no_cat_output(self):
        launcher = self._make_launcher('--output-dir', self.tmp_dir)

        launcher.run_job()

        self.assertEqual(launcher.stdout.getvalue(), b'')
        self.assertEqual(launcher.stderr.getvalue(), b'')

    def test_output_dir_with_explicit_cat_output(self):
        launcher = self._make_launcher(
            '--output-dir', self.tmp_dir, '--cat-output')

        launcher.run_job()

        self.assertEqual(launcher.stdout.getvalue(), b'a line\n')
        self.assertEqual(launcher.stderr.getvalue(), b'')

    def test_exit_on_step_failure(self):
        launcher = self._make_launcher()
        launcher.mock_runner.run.side_effect = StepFailedException

        self.assertRaises(SystemExit, launcher.run_job)

        self.assertEqual(launcher.stdout.getvalue(), b'')
        self.assertIn(b'Step failed', launcher.stderr.getvalue())

    def test_pass_through_other_exceptions(self):
        launcher = self._make_launcher()
        launcher.mock_runner.run.side_effect = OSError

        self.assertRaises(OSError, launcher.run_job)

        self.assertEqual(launcher.stdout.getvalue(), b'')
        self.assertEqual(launcher.stderr.getvalue(), b'')


class CommandLineArgsTestCase(BasicTestCase):

    def test_shouldnt_exit_when_invoked_as_object(self):
        self.assertRaises(ValueError, MRJob, args=['--quux', 'baz'])

    def test_should_exit_when_invoked_as_script(self):
        args = [sys.executable, inspect.getsourcefile(MRJob),
                '--quux', 'baz']

        # add . to PYTHONPATH (in case mrjob isn't actually installed)
        env = combine_envs(os.environ,
                           {'PYTHONPATH': mrjob_pythonpath()})
        proc = Popen(args, stderr=PIPE, stdout=PIPE, env=env)
        _, err = proc.communicate()
        self.assertEqual(proc.returncode, 2, err)

    def test_custom_key_value_option_parsing(self):
        # simple example
        mr_job = MRJob(args=['--cmdenv', 'FOO=bar', ''])
        self.assertEqual(mr_job.options.cmdenv, {'FOO': 'bar'})

        # trickier example
        mr_job = MRJob(args=[
            '--cmdenv', 'FOO=bar',
            '--cmdenv', 'FOO=baz',
            '--cmdenv', 'BAZ=qux=quux'])
        self.assertEqual(mr_job.options.cmdenv,
                         {'FOO': 'baz', 'BAZ': 'qux=quux'})

        # must have KEY=VALUE
        self.assertRaises(ValueError, MRJob,
                          args=['--cmdenv', 'FOO', ''])

    def test_passthrough_options_defaults(self):
        mr_job = MRCustomJob(args=[])

        self.assertEqual(mr_job.options.foo_size, 5)
        self.assertEqual(mr_job.options.bar_name, None)
        self.assertEqual(mr_job.options.baz_mode, False)
        self.assertEqual(mr_job.options.quuxing, True)
        self.assertEqual(mr_job.options.pill_type, 'blue')
        self.assertEqual(mr_job.options.planck_constant, 6.626068e-34)
        self.assertEqual(mr_job.options.extra_special_args, [])
        self.assertEqual(mr_job.options.runner, None)
        # should include all --protocol options
        # should include default value of --num-items
        # should use long option names (--protocol, not -p)
        # shouldn't include --limit because it's None
        # items should be in the order they were instantiated
        self.assertEqual(mr_job._non_option_kwargs()['extra_args'], [])

    def test_explicit_passthrough_options(self):
        mr_job = MRCustomJob(args=[
            '-v',
            '--foo-size=9',
            '--bar-name', 'Alembic',
            '--enable-baz-mode', '--disable-quuxing',
            '--pill-type', 'red',
            '--planck-constant', '1',
            '--planck-constant', '42',
            '--extra-special-arg', 'you',
            '--extra-special-arg', 'me',
            '--runner', 'inline',
        ])

        self.assertEqual(mr_job.options.foo_size, 9)
        self.assertEqual(mr_job.options.bar_name, 'Alembic')
        self.assertEqual(mr_job.options.baz_mode, True)
        self.assertEqual(mr_job.options.quuxing, False)
        self.assertEqual(mr_job.options.pill_type, 'red')
        self.assertEqual(mr_job.options.planck_constant, 42)
        self.assertEqual(mr_job.options.extra_special_args, ['you', 'me'])
        self.assertEqual(
            mr_job._non_option_kwargs()['extra_args'],
            [
                '--foo-size', '9',
                '--bar-name', 'Alembic',
                '--enable-baz-mode',
                '--disable-quuxing',
                '--pill-type', 'red',
                '--planck-constant', '1',
                '--planck-constant', '42',
                '--extra-special-arg', 'you',
                '--extra-special-arg', 'me',
                '--runner', 'inline',
            ]
        )

    def test_explicit_passthrough_options_short(self):
        mr_job = MRCustomJob(args=[
            '-v',
            '-F9', '-BAlembic', '-MQ', '-T', 'red', '-C1', '-C42',
            '--extra-special-arg', 'you',
            '--extra-special-arg', 'me',
            '-r', 'inline',
        ])

        self.assertEqual(mr_job.options.foo_size, 9)
        self.assertEqual(mr_job.options.bar_name, 'Alembic')
        self.assertEqual(mr_job.options.baz_mode, True)
        self.assertEqual(mr_job.options.quuxing, False)
        self.assertEqual(mr_job.options.pill_type, 'red')
        self.assertEqual(mr_job.options.planck_constant, 42)
        self.assertEqual(mr_job.options.extra_special_args, ['you', 'me'])
        self.assertEqual(
            mr_job._non_option_kwargs()['extra_args'],
            # order is preserved, but args are separated from switches
            [
                '-F', '9',
                '-B', 'Alembic',
                '-M', '-Q',
                '-T', 'red',
                '-C', '1',
                '-C', '42',
                '--extra-special-arg', 'you',
                '--extra-special-arg', 'me',
                '-r', 'inline',
            ]
        )

    def test_bad_custom_options(self):
        self.assertRaises(ValueError,
                          MRCustomJob,
                          args=['--planck-constant', 'c'])
        self.assertRaises(ValueError, MRCustomJob,
                          args=['--pill-type=green'])

    def test_bad_option_types(self):
        mr_job = MRJob(args=[])
        self.assertRaises(
            ValueError, mr_job.add_passthru_arg,
            '--stop-words', dest='stop_words', type='set', default=None)
        self.assertRaises(
            ValueError, mr_job.add_passthru_arg,
            '--leave-a-msg', dest='leave_a_msg', action='callback',
            default=None)

    def test_incorrect_option_types(self):
        self.assertRaises(ValueError, MRJob, args=['--cmdenv', 'cats'])
        self.assertRaises(ValueError, MRJob,
                          args=['--ssh-bind-ports', 'athens'])

    def test_default_file_options(self):
        mr_job = MRCustomJob(args=[])
        self.assertEqual(mr_job.options.foo_config, None)
        self.assertEqual(mr_job.options.accordian_files, [])
        self.assertEqual(mr_job._non_option_kwargs()['extra_args'], [])

    def test_explicit_file_options(self):
        mr_job = MRCustomJob(args=[
            '--foo-config', '/tmp/.fooconf#dot-fooconf',
            '--foo-config', '/etc/fooconf',
            '--accordian-file', 'WeirdAl.mp3',
            '--accordian-file', '/home/dave/JohnLinnell.ogg'])
        self.assertEqual(mr_job.options.foo_config, '/etc/fooconf')
        self.assertEqual(mr_job.options.accordian_files, [
            'WeirdAl.mp3', '/home/dave/JohnLinnell.ogg'])
        self.assertEqual(mr_job._non_option_kwargs()['extra_args'], [
            '--foo-config', dict(
                path='/tmp/.fooconf', name='dot-fooconf', type='file'),
            '--foo-config', dict(
                path='/etc/fooconf', name=None, type='file'),
            '--accordian-file', dict(
                path='WeirdAl.mp3', name=None, type='file'),
            '--accordian-file', dict(
                path='/home/dave/JohnLinnell.ogg', name=None, type='file')
        ])

    def test_str_type_with_file_arg(self):
        # regression test for #1858
        class MRGoodFileArgTypeJob(MRJob):
            def configure_args(self):
                super(MRGoodFileArgTypeJob, self).configure_args()
                self.add_file_arg(
                    '--bibliophile', dest='bibliophiles', type=str)

        mr_job = MRGoodFileArgTypeJob(
            args=['--bibliophile', '/var/bookworm'])

        self.assertEqual(mr_job.options.bibliophiles, '/var/bookworm')

    def test_no_conf_overrides(self):
        mr_job = MRCustomJob(args=['-c', 'blah.conf', '--no-conf'])
        self.assertEqual(mr_job.options.conf_paths, [])

    def test_no_conf_overridden(self):
        mr_job = MRCustomJob(args=['--no-conf', '-c', 'blah.conf'])
        self.assertEqual(mr_job.options.conf_paths, ['blah.conf'])


class TestToolLogging(BasicTestCase):
    """ Verify the behavior of logging configuration for CLI tools
    """
    def test_default_options(self):
        with patch.object(sys, 'stderr', StringIO()) as stderr:
            MRJob.set_up_logging()
            log = logging.getLogger('__main__')
            log.info('INFO')
            log.debug('DEBUG')
            self.assertEqual(stderr.getvalue(), 'INFO\n')

    def test_verbose(self):
        with patch.object(sys, 'stderr', StringIO()) as stderr:
            MRJob.set_up_logging(verbose=True)
            log = logging.getLogger('__main__')
            log.info('INFO')
            log.debug('DEBUG')
            self.assertEqual(stderr.getvalue(), 'INFO\nDEBUG\n')


class TestPassThroughRunner(BasicTestCase):

    def get_value(self, job):
        job.sandbox()

        with job.make_runner() as runner:
            runner.run()

            for _, value in job.parse_output(runner.cat_output()):
                return value

    def test_no_pass_through(self):
        self.assertEqual(self.get_value(MRNoRunner([])), None)
        self.assertEqual(self.get_value(MRNoRunner(['-r', 'inline'])), None)
        self.assertEqual(self.get_value(MRNoRunner(['-r', 'local'])), None)

    def test_pass_through(self):
        self.assertEqual(self.get_value(MRRunner([])), None)
        self.assertEqual(self.get_value(MRRunner(['-r', 'inline'])), 'inline')
        self.assertEqual(self.get_value(MRRunner(['-r', 'local'])), 'local')


class StdStreamTestCase(BasicTestCase):

    def test_normal_python(self):
        job = MRJob([])

        if PY2:
            self.assertEqual(job.stdin, sys.stdin)
            self.assertEqual(job.stdout, sys.stdout)
            self.assertEqual(job.stderr, sys.stderr)
        else:
            self.assertEqual(job.stdin, sys.stdin.buffer)
            self.assertEqual(job.stdout, sys.stdout.buffer)
            self.assertEqual(job.stderr, sys.stderr.buffer)

    def test_python3_jupyter_notebook(self):
        # regression test for #1441

        # this test actually works on any Python platform, since we use mocks
        mock_stdin = Mock()
        mock_stdin.buffer = Mock()

        mock_stdout = Mock()
        del mock_stdout.buffer

        mock_stderr = Mock()
        del mock_stderr.buffer

        with patch.multiple(sys, stdin=mock_stdin,
                            stdout=mock_stdout, stderr=mock_stderr):
            job = MRJob([])

            self.assertEqual(job.stdin, mock_stdin.buffer)
            self.assertEqual(job.stdout, mock_stdout)
            self.assertEqual(job.stderr, mock_stderr)
