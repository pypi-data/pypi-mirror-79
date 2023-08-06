# Copyright 2009-2015 Yelp and Contributors
# Copyright 2016-2018 Yelp
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
"""Tests of all the amazing utilities in mrjob.util"""
import os
import shutil
import sys
import tempfile
from io import BytesIO
from subprocess import PIPE
from subprocess import Popen

from mrjob.py2 import PY2
from mrjob.util import cmd_line
from mrjob.util import file_ext
from mrjob.util import random_identifier
from mrjob.util import safeeval
from mrjob.util import save_sys_std
from mrjob.util import to_lines
from mrjob.util import unarchive
from mrjob.util import unique
from mrjob.util import which

from tests.py2 import Mock
from tests.py2 import patch
from tests.sandbox import BasicTestCase
from tests.sandbox import SandboxedTestCase
from tests.sandbox import random_seed


class ToLinesTestCase(BasicTestCase):

    def test_empty(self):
        self.assertEqual(
            list(to_lines(_ for _ in ())),
            [])

    def test_buffered_lines(self):
        self.assertEqual(
            list(to_lines(iter([
                b'The quick\nbrown fox\nju',
                b'mped over\nthe lazy\ndog',
                b's.\n',
            ]))),
            [b'The quick\n', b'brown fox\n', b'jumped over\n', b'the lazy\n',
             b'dogs.\n'])

    def test_no_trailing_newline(self):
        self.assertEqual(
            list(to_lines(iter([
                b'Alouette,\ngentille',
                b' Alouette.',
            ]))),
            [b'Alouette,\n', b'gentille Alouette.'])

    def test_eof_without_trailing_newline(self):
        self.assertEqual(
            list(to_lines(iter([
                b'Alouette,\ngentille',
                b' Alouette.',
                b'',  # treated as EOF
                b'Allouette,\nje te p',
                b'lumerais.',
            ]))),
            [b'Alouette,\n', b'gentille Alouette.',
             b'Allouette,\n', b'je te plumerais.'])

    def test_long_lines(self):
        super_long_line = b'a' * 10000 + b'\n' + b'b' * 1000 + b'\nlast\n'
        self.assertEqual(
            list(to_lines(
                super_long_line[0 + i:1024 + i]
                for i in range(0, len(super_long_line), 1024)
            )),
            [b'a' * 10000 + b'\n', b'b' * 1000 + b'\n', b'last\n'])


class CmdLineTestCase(BasicTestCase):

    def test_cmd_line(self):
        self.assertEqual(cmd_line(['cut', '-f', 2, '-d', ' ']),
                         "cut -f 2 -d ' '")
        self.assertIn(cmd_line(['grep', '-e', "# DON'T USE$"]),
                      ("grep -e \"# DON'T USE\\$\"",
                       'grep -e \'# DON\'"\'"\'T USE$\''))


# expand_path() is tested by tests.test_conf.CombineAndExpandPathsTestCase


class FileExtTestCase(BasicTestCase):

    def test_file_ext(self):
        self.assertEqual(file_ext('foo.zip'), '.zip')
        self.assertEqual(file_ext('foo.Z'), '.Z')
        self.assertEqual(file_ext('foo.tar.gz'), '.tar.gz')
        self.assertEqual(file_ext('README'), '')
        self.assertEqual(file_ext('README,v'), '')
        self.assertEqual(file_ext('README.txt,v'), '.txt,v')

    def ignore_initial_dots(self):
        self.assertEqual(file_ext('.emacs'), '')
        self.assertEqual(file_ext('.mrjob.conf'), '.conf')
        self.assertEqual(file_ext('...dots.txt'), '.txt')


class SafeEvalTestCase(BasicTestCase):

    def test_simple_data_structures(self):
        # try unrepr-ing a bunch of simple data structures
        for x in True, None, 1, [0, 1, 2, 3, 4], {'foo': False, 'bar': 2}:
            self.assertEqual(x, safeeval(repr(x)))

    def test_no_mischief(self):
        # make sure we can't do mischief
        self.assertRaises(NameError, safeeval, "open('/tmp')")

    def test_globals_and_locals(self):
        # test passing in globals, locals
        a = -0.2
        self.assertEqual(
            abs(a),
            safeeval('abs(a)', globals={'abs': abs}, locals={'a': a}))

    def test_range_type(self):
        # ranges have different reprs on Python 2 vs. Python 3, and
        # can't be checked for equality until Python 3.3+

        if PY2:
            range_type = xrange
        else:
            range_type = range

        self.assertEqual(repr(safeeval(repr(range_type(3)))),
                         repr(range_type(3)))

        if sys.version_info >= (3, 3):
            self.assertEqual(safeeval(repr(range_type(3))),
                             range_type(3))


class ArchiveTestCase(BasicTestCase):

    def setUp(self):
        self.setup_tmp_dir()

    def tearDown(self):
        self.rm_tmp_dir()

    def setup_tmp_dir(self):
        join = os.path.join

        self.tmp_dir = tempfile.mkdtemp()

        os.mkdir(join(self.tmp_dir, 'a'))  # contains files to archive

        # create a/foo
        with open(join(self.tmp_dir, 'a', 'foo'), 'w') as foo:
            foo.write('FOO\n')

        # a/bar symlinks to a/foo
        os.symlink('foo', join(self.tmp_dir, 'a', 'bar'))

        # create a/baz; going to filter this out
        with open(join(self.tmp_dir, 'a', 'baz'), 'w') as baz:
            baz.write('BAZ\n')

        # create a/qux/quux
        os.mkdir(join(self.tmp_dir, 'a', 'qux'))
        with open(join(self.tmp_dir, 'a', 'qux', 'quux'), 'w') as quux:
            quux.write('QUUX\n')

    def rm_tmp_dir(self):
        shutil.rmtree(self.tmp_dir)

    def ensure_expected_results(self, added_files=[], excluded_files=[]):
        join = os.path.join

        # make sure the files we expect are there
        expected_files = ['bar', 'baz', 'foo', 'qux']
        expected_files = (set(expected_files + added_files) -
                          set(excluded_files))

        self.assertEqual(
            sorted(os.listdir(join(self.tmp_dir, 'b'))),
            sorted(expected_files))

        self.assertEqual(
            list(os.listdir(join(self.tmp_dir, 'b', 'qux'))), ['quux'])

        # make sure their contents are intact
        with open(join(self.tmp_dir, 'b', 'foo')) as foo:
            self.assertEqual(foo.read(), 'FOO\n')

        with open(join(self.tmp_dir, 'b', 'bar')) as bar:
            self.assertEqual(bar.read(), 'FOO\n')

        with open(join(self.tmp_dir, 'b', 'qux', 'quux')) as quux:
            self.assertEqual(quux.read(), 'QUUX\n')

        # make sure symlinks are converted to files
        assert os.path.isfile(join(self.tmp_dir, 'b', 'bar'))
        assert not os.path.islink(join(self.tmp_dir, 'b', 'bar'))

    def archive_and_unarchive(self, extension, archive_template,
                              added_files=[]):
        join = os.path.join

        # archive it up
        archive_name = 'a.' + extension
        variables = dict(archive_name=join('..', archive_name),
                         files_to_archive='.')
        archive_command = [arg % variables for arg in archive_template]

        # sometime the relevant command isn't available or doesn't work;
        # if so, skip the test
        try:
            proc = Popen(archive_command, cwd=join(self.tmp_dir, 'a'),
                         stdout=PIPE, stderr=PIPE)
        except OSError as e:
            if e.errno == 2:
                self.skipTest("No %s command" % archive_command[0])
            else:
                raise
        proc.communicate()  # discard output
        if proc.returncode != 0:
            self.skipTest("Can't run `%s` to create archive." %
                          cmd_line(archive_command))

        # unarchive it into b/
        unarchive(join(self.tmp_dir, archive_name), join(self.tmp_dir, 'b'))

        self.ensure_expected_results(added_files=added_files)

    def test_unarchive_tar(self):
        # this test requires that tar is present
        self.archive_and_unarchive(
            'tar',
            ['tar', 'chf', '%(archive_name)s', '%(files_to_archive)s'])

    def test_unarchive_tar_gz(self):
        # this test requires that tar is present and supports the "z" option
        self.archive_and_unarchive(
            'tar.gz',
            ['tar', 'czhf', '%(archive_name)s', '%(files_to_archive)s'])

    def test_unarchive_tar_bz2(self):
        # this test requires that tar is present and supports the "j" option
        self.archive_and_unarchive(
            'tar.bz2',
            ['tar', 'cjhf', '%(archive_name)s', '%(files_to_archive)s'])

    def test_unarchive_jar(self):
        # this test requires that jar is present
        self.archive_and_unarchive(
            'jar',
            ['jar', 'cf', '%(archive_name)s', '%(files_to_archive)s'],
            added_files=['META-INF'])

    def test_unarchive_zip(self):
        # this test requires that zip is present
        self.archive_and_unarchive('zip', ['zip', '-qr',
                                   '%(archive_name)s', '%(files_to_archive)s'])

    def test_unarchive_non_archive(self):
        join = os.path.join

        self.assertRaises(
            IOError,
            unarchive, join(self.tmp_dir, 'a', 'foo'), join(self.tmp_dir, 'b'))


class OnlyReadWrapper(object):
    """Restrict a file object to only the read() method (used by
    ReadFileTestCase)."""

    def __init__(self, fp):
        self.fp = fp

    def read(self, *args, **kwargs):
        return self.fp.read(*args, **kwargs)


class RandomIdentifierTestCase(BasicTestCase):

    def test_format(self):
        with random_seed(0):
            random_id = random_identifier()
        self.assertEqual(len(random_id), 16)
        self.assertFalse(set(random_id) - set('0123456789abcdef'))

    def test_no_collisions_possible_ever(self):
        # heh
        with random_seed(0):
            self.assertNotEqual(random_identifier(), random_identifier())


class SaveSysStdTestCase(BasicTestCase):

    def setUp(self):
        # if save_sys_std() *doesn't* work, don't mess up other tests
        super(SaveSysStdTestCase, self).setUp()

        self.stdin = self.start(patch('sys.stdin'))
        self.stdout = self.start(patch('sys.stdout'))
        self.stderr = self.start(patch('sys.stderr'))

    def test_basic(self):
        fake_stdin = BytesIO(b'HI')
        fake_stdout = BytesIO()
        fake_stderr = BytesIO()

        with save_sys_std():
            sys.stdin = fake_stdin
            self.assertEqual(sys.stdin.read(), b'HI')

            sys.stdout = fake_stdout
            sys.stdout.write(b'Hello!\n')

            sys.stderr = fake_stderr
            sys.stderr.write(b'!!!')

        self.assertEqual(sys.stdin, self.stdin)
        self.assertEqual(sys.stdout, self.stdout)
        self.assertEqual(sys.stderr, self.stderr)

        self.assertFalse(self.stdin.read.called)
        self.assertFalse(self.stdout.write.called)
        self.assertFalse(self.stderr.write.called)

        self.assertEqual(fake_stdout.getvalue(), b'Hello!\n')
        self.assertEqual(fake_stderr.getvalue(), b'!!!')

    def test_flushing(self):
        fake_stderr = Mock()

        with save_sys_std():
            sys.stderr = fake_stderr
            sys.stderr.write(b'Hello!\n')

        self.assertEqual(self.stderr.flush.call_count, 1)
        self.assertEqual(fake_stderr.flush.call_count, 1)

        # stdout was never patched, so it gets flushed twice
        self.assertEqual(self.stdout.flush.call_count, 2)

        # we don't flush stdin
        self.assertFalse(self.stdin.flush.called)

    def test_bad_flush(self):
        fake_stdout = "LOOK AT ME I'M STDOUT"
        self.assertFalse(hasattr(fake_stdout, 'flush'))

        with save_sys_std():
            sys.stdout = fake_stdout

        self.assertEqual(sys.stdout, self.stdout)
        self.assertEqual(self.stdout.flush.call_count, 1)

        # sys.stderr, which was not patched, should be flushed twice
        self.assertEqual(self.stderr.flush.call_count, 2)


class UniqueTestCase(BasicTestCase):

    def test_empty(self):
        self.assertEqual(list(unique([])), [])

    def test_de_duplication(self):
        self.assertEqual(list(unique([1, 2, 1, 5, 1])),
                         [1, 2, 5])

    def test_preserves_order(self):
        self.assertEqual(list(unique([6, 7, 2, 0, 7, 1])),
                         [6, 7, 2, 0, 1])

    def test_mixed_types_ok(self):
        self.assertEqual(list(unique(['a', None, 33, 'a'])),
                         ['a', None, 33])


class WhichTestCase(SandboxedTestCase):

    # which() is just a passthrough to shutil.which() and
    # distutils.spawn.find_executable, so we're really just
    # testing for consistent behavior across versions

    def setUp(self):
        super(WhichTestCase, self).setUp()

        self.shekondar_path = self.makefile('shekondar', executable=True)

    def test_explicit_path(self):
        self.assertEqual(which('shekondar', path=self.tmp_dir),
                         self.shekondar_path)

    def test_path_from_environment(self):
        with patch.dict(os.environ, PATH=self.tmp_dir):
            self.assertEqual(which('shekondar'), self.shekondar_path)

    def test_not_found(self):
        self.assertEqual(which('shekondar-the-fearsome', self.tmp_dir), None)

    def test_no_path(self):
        with patch.dict(os.environ, clear=True):
            # make sure we protect find_executable() from missing $PATH
            # on Python 2.
            self.assertEqual(which('shekondar'), None)
