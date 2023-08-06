# Copyright 2017-2018 Yelp
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
from io import BytesIO
import gzip
import os
import stat
from os.path import join
from shutil import make_archive

from mrjob import conf
from mrjob.examples.mr_word_freq_count import MRWordFreqCount
from mrjob.inline import InlineMRJobRunner
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep

from tests.mr_group import MRGroup
from tests.mr_no_mapper import MRNoMapper
from tests.mr_os_walk_job import MROSWalkJob
from tests.mr_sort_and_group import MRSortAndGroup
from tests.mr_test_jobconf import MRTestJobConf
from tests.mr_test_per_step_jobconf import MRTestPerStepJobConf
from tests.mr_word_count import MRWordCount
from tests.py2 import patch
from tests.sandbox import BasicTestCase
from tests.sandbox import SandboxedTestCase


# these jobs don't need to be in their own file because they'll be run inline

class MRIncrementerJob(MRJob):
    """A terribly silly way to add a positive integer to values."""

    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def configure_args(self):
        super(MRIncrementerJob, self).configure_args()

        self.add_passthru_arg('--times', type=int, default=1)

    def mapper(self, _, value):
        yield None, value + 1

    def steps(self):
        return [MRStep(mapper=self.mapper)] * self.options.times


class MRFilePermissionsJob(MRJob):
    """A way to check file permissions."""

    def mapper(self, _, value):
        pass

    def mapper_final(self):
        yield None, None

    def reducer(self, _, __):
        for path in os.listdir('.'):
            yield path, os.stat(path).st_mode


class SortValuesTestCase(SandboxedTestCase):
    # inline runner doesn't have its own sorting logic
    RUNNER = 'inline'

    _INPUT = b'alligator\nactuary\nbowling\nartichoke\nballoon\nbaby\n'

    def test_no_sort_values(self):
        # don't sort values if not requested (#660)

        job = MRGroup(['-r', self.RUNNER])
        job.sandbox(stdin=BytesIO(self._INPUT))

        with job.make_runner() as runner:
            runner.run()
            output = list(job.parse_output(runner.cat_output()))

            self.assertEqual(
                sorted(output),
                [('a', ['alligator', 'actuary', 'artichoke']),
                 ('b', ['bowling', 'balloon', 'baby'])])

    def test_sort_values(self):
        job = MRSortAndGroup(['-r', self.RUNNER])
        job.sandbox(stdin=BytesIO(self._INPUT))

        with job.make_runner() as runner:
            runner.run()
            output = list(job.parse_output(runner.cat_output()))

            self.assertEqual(
                sorted(output),
                [('a', ['actuary', 'alligator', 'artichoke']),
                 ('b', ['baby', 'balloon', 'bowling'])])

    def test_sorting_is_case_sensitive(self):
        job = MRSortAndGroup(['-r', self.RUNNER])
        job.sandbox(stdin=BytesIO(b'Aaron\naardvark\nABC\n'))

        with job.make_runner() as runner:
            runner.run()
            output = list(job.parse_output(runner.cat_output()))

            self.assertEqual(
                sorted(output),
                [('A', ['ABC', 'Aaron']),
                 ('a', ['aardvark'])])


class MRJobFileOptionsTestCase(SandboxedTestCase):

    def setUp(self):
        super(MRJobFileOptionsTestCase, self).setUp()

        self.input_file_path = join(self.tmp_dir, 'input_file.txt')
        with open(self.input_file_path, 'wb') as f:
            f.write(b'2\n')

    def test_with_input_file_option(self):
        mr_job = MRCustomFileOptionJob(
            ['-r', 'inline', '--platform-file', self.input_file_path])
        mr_job.sandbox(stdin=BytesIO(b'1\n'))

        with mr_job.make_runner() as runner:
            runner.run()
            output = sorted(
                v for k, v in mr_job.parse_output(runner.cat_output()))

            self.assertEqual(output, [2])


class NoMRJobConfTestCase(BasicTestCase):

    def test_no_mrjob_confs(self):
        with patch.object(
                conf, '_expanded_mrjob_conf_path', return_value=None):

            mr_job = MRIncrementerJob(['-r', 'inline', '--times', '2'])
            mr_job.sandbox(stdin=BytesIO(b'0\n1\n2\n'))

            with mr_job.make_runner() as runner:
                runner.run()
                output = sorted(
                    v for k, v in mr_job.parse_output(runner.cat_output()))
                self.assertEqual(output, [2, 3, 4])


class MRCustomFileOptionJob(MRJob):
    """ A simple MRJob that uses the input file option."""

    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    multiplier = 1

    def configure_args(self):
        super(MRCustomFileOptionJob, self).configure_args()
        self.add_file_arg('--platform-file')

    def mapper_init(self):
        with open(self.options.platform_file) as f:
            self.multiplier = int(f.read())

    def mapper(self, _, value):
        yield None, value * self.multiplier


class SimRunnerJobConfTestCase(SandboxedTestCase):

    # this class is also used to test local mode
    RUNNER = 'inline'

    def test_input_files(self):
        input_path = join(self.tmp_dir, 'input')
        with open(input_path, 'wb') as input_file:
            input_file.write(b'bar\nqux\nfoo\n')

        input_gz_path = join(self.tmp_dir, 'input.gz')
        with gzip.GzipFile(input_gz_path, 'wb') as input_gz:
            input_gz.write(b'foo\n')

        mr_job = MRWordCount(['-r', self.RUNNER,
                              input_path, input_gz_path])
        mr_job.sandbox()

        results = []

        with mr_job.make_runner() as runner:
            runner.run()

            results.extend(mr_job.parse_output(runner.cat_output()))

            self.assertGreater(runner.counters()[0]['count']['combiners'], 2)

        self.assertEqual(sorted(results),
                         [('file://' + input_path, 3),
                          ('file://' + input_gz_path, 1)])

    def _extra_expected_local_files(self, runner):
        """A list of additional local files expected, as tuples
        of (path, name). Hook for dealing with cat.py in local mode."""
        return []

    def test_jobconf_simulated_by_runner(self):
        # use a .gz file so there's only one split
        input_gz_path = join(self.tmp_dir, 'input.gz')
        with gzip.GzipFile(input_gz_path, 'wb') as input_gz:
            input_gz.write(b'foo\n')
        input_gz_size = os.stat(input_gz_path)[stat.ST_SIZE]

        upload_path = join(self.tmp_dir, 'upload')
        with open(upload_path, 'wb') as upload_file:
            upload_file.write(b'PAYLOAD')

        # use --no-bootstrap-mrjob so we don't have to worry about
        # mrjob.tar.gz and the setup wrapper script
        self.add_mrjob_to_pythonpath()
        mr_job = MRTestJobConf(['-r', self.RUNNER,
                                '--no-bootstrap-mrjob',
                                '-D=user.defined=something',
                                '--files', upload_path,
                               input_gz_path])

        mr_job.sandbox()

        results = {}

        # between the single line of input and setting mapred.map.tasks to 1,
        # we should be restricted to only one task, which will give more
        # predictable results

        with mr_job.make_runner() as runner:
            script_path = runner._script_path

            runner.run()

            results.update(dict(mr_job.parse_output(runner.cat_output())))

        working_dir = results['mapreduce.job.local.dir']
        self.assertEqual(working_dir,
                         join(runner._get_local_tmp_dir(),
                              'step', '000', 'mapper', '00000', 'wd'))

        self.assertEqual(results['mapreduce.job.cache.archives'], '')

        expected_cache_files = [
            script_path + '#mr_test_jobconf.py',
            upload_path + '#upload'
        ] + [
            '%s#%s' % (path, name)
            for path, name in self._extra_expected_local_files(runner)
        ]
        self.assertEqual(
            sorted(results['mapreduce.job.cache.files'].split(',')),
            sorted(expected_cache_files))

        self.assertEqual(results['mapreduce.job.cache.local.archives'], '')
        expected_local_files = [
            join(working_dir, 'mr_test_jobconf.py'),
            join(working_dir, 'upload')
        ] + [
            join(working_dir, name)
            for path, name in self._extra_expected_local_files(runner)
        ]
        self.assertEqual(
            sorted(results['mapreduce.job.cache.local.files'].split(',')),
            sorted(expected_local_files))
        self.assertEqual(results['mapreduce.job.id'], runner._job_key)

        self.assertEqual(results['mapreduce.map.input.file'],
                         'file://' + input_gz_path)
        self.assertEqual(results['mapreduce.map.input.length'],
                         str(input_gz_size))
        self.assertEqual(results['mapreduce.map.input.start'], '0')
        self.assertEqual(results['mapreduce.task.attempt.id'],
                         'attempt_%s_mapper_00000_0' % runner._job_key)
        self.assertEqual(results['mapreduce.task.id'],
                         'task_%s_mapper_00000' % runner._job_key)
        self.assertEqual(results['mapreduce.task.ismap'], 'true')
        self.assertEqual(results['mapreduce.task.output.dir'],
                         runner._output_dir)
        self.assertEqual(results['mapreduce.task.partition'], '0')
        self.assertEqual(results['user.defined'], 'something')

    def test_per_step_jobconf(self):
        mr_job = MRTestPerStepJobConf([
            '-r', self.RUNNER, '-D', 'user.defined=something'])
        mr_job.sandbox()

        results = {}

        with mr_job.make_runner() as runner:
            runner.run()

            for key, value in mr_job.parse_output(runner.cat_output()):
                results[tuple(key)] = value

        # user.defined gets re-defined in the second step
        self.assertEqual(results[(0, 'user.defined')], 'something')
        self.assertEqual(results[(1, 'user.defined')], 'nothing')


class SimRunnerNoMapperTestCase(SandboxedTestCase):

    RUNNER = 'inline'

     # tests #1141. Also used by local mapper

    def test_step_with_no_mapper(self):
        mr_job = MRNoMapper(['-r', self.RUNNER])

        mr_job.sandbox(stdin=BytesIO(
            b'one fish two fish\nred fish blue fish\n'))

        with mr_job.make_runner() as runner:
            runner.run()

            self.assertEqual(
                sorted(mr_job.parse_output(runner.cat_output())),
                [(1, ['blue', 'one', 'red', 'two']),
                 (4, ['fish'])])


class LocalFSTestCase(SandboxedTestCase):

    def setUp(self):
        super(LocalFSTestCase, self).setUp()
        self.runner = InlineMRJobRunner()

    def test_can_handle_paths(self):
        self.assertEqual(
            self.runner.fs.exists(join(self.tmp_dir, 'foo')), False)

    def test_can_handle_file_uris(self):
        self.assertEqual(
            self.runner.fs.exists(
                'file://' + join(self.tmp_dir, 'foo')),
            False)

    def test_cant_handle_other_uris(self):
        self.assertRaises(IOError, self.runner.fs.ls, 's3://walrus/foo')


class DistributedCachePermissionsTestCase(SandboxedTestCase):
    # test #1619

    def test_file_permissions(self):
        data_path = self.makefile('data')

        job = MRFilePermissionsJob(['--files', data_path])
        job.sandbox()

        with job.make_runner() as runner:
            runner.run()

            perms = dict(job.parse_output(runner.cat_output()))

        self.assertIn('data', perms)
        data_perms = perms['data']

        self.assertTrue(data_perms & stat.S_IXUSR)
        self.assertFalse(data_perms & stat.S_IXGRP)
        self.assertFalse(data_perms & stat.S_IXOTH)


class FSOnlyHandlesFileURIsTestCase(SandboxedTestCase):
    # regression test for #1185

    # updated for #1986 (file:// URIs)
    def test_file_uris_only(self):
        runner = InlineMRJobRunner()

        # sanity check
        foo_path = self.makefile('foo')
        bar_path = join(self.tmp_dir, 'bar')
        self.assertTrue(runner.fs.exists(foo_path))
        self.assertFalse(runner.fs.exists('file://' + bar_path))

        # non-file:/// URI should raise IOError, not return False
        self.assertRaises(IOError,
                          runner.fs.exists, 's3://walrus/fish')


class FileURIsAsInputTestCase(SandboxedTestCase):
    # regression test for #1986

    def test_file_uris_as_input(self):
        input1 = self.makefile('input1.txt', b'cat rat bat')
        input2 = 'file://' + self.makefile('input2.txt', b'dog dog dog')

        job = MRWordFreqCount([input1, input2])
        job.sandbox()

        with job.make_runner() as runner:
            runner.run()

            self.assertEqual(dict(job.parse_output(runner.cat_output())),
                             dict(bat=1, cat=1, dog=3, rat=1))


class FileUploadTestCase(SandboxedTestCase):

    # SetupTestCase in test_bin.py covers a lot of this. added this test
    # so we can ensure that sim runners correctly handle file URIs.
    # Should probably make this more comprehensive, see #2114

    def test_file_uris(self):
        f1_path = self.makefile('f1', b'contents')
        f2_uri = 'file://' + self.makefile('f2', b'stuff')

        job = MROSWalkJob(['--files', '%s,%s' % (f1_path, f2_uri)])
        job.sandbox()

        with job.make_runner() as runner:
            runner.run()

            path_to_size = dict(job.parse_output(runner.cat_output()))

            self.assertEqual(path_to_size.get('./f1'), 8)
            self.assertEqual(path_to_size.get('./f2'), 5)

    def test_archive_uris(self):
        qux_dir = self.makedirs('qux')
        self.makefile(join(qux_dir, 'bar'), b'baz')

        qux_tar_gz = make_archive(join(self.tmp_dir, 'qux'), 'gztar', qux_dir)
        qux_tar_gz_uri = 'file://' + qux_tar_gz

        job = MROSWalkJob(
            ['--archives', '%s#qux,%s#qux2' % (qux_tar_gz, qux_tar_gz_uri)])
        job.sandbox()

        with job.make_runner() as runner:
            runner.run()

            path_to_size = dict(job.parse_output(runner.cat_output()))

            self.assertEqual(path_to_size.get('./qux/bar'), 3)
            self.assertEqual(path_to_size.get('./qux2/bar'), 3)
