# Copyright 2009-2013 Yelp
# Copyright 2015 Yelp
# Copyright 2017 Yelp
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
import bz2
import gzip
import os
from os.path import join

from mrjob.fs.local import LocalFilesystem

from tests.sandbox import SandboxedTestCase


class CatTestCase(SandboxedTestCase):

    def setUp(self):
        super(CatTestCase, self).setUp()
        self.fs = LocalFilesystem()

    def test_cat_uncompressed(self):
        path = self.makefile('f', b'bar\nfoo\n')

        self.assertEqual(
            b''.join(self.fs._cat_file(path)),
            b'bar\nfoo\n')

    def test_cat_file_uri(self):
        uri = 'file://' + self.makefile('f', b'bar\nfoo\n')

        self.assertEqual(
            b''.join(self.fs._cat_file(uri)),
            b'bar\nfoo\n')

    def test_yields_lines(self):
        # since it's just opening the fileobj directly
        path = self.makefile('f', b'bar\nfoo\n')

        self.assertEqual(list(self.fs._cat_file(path)),
                         [b'bar\n', b'foo\n'])

    def test_cat_gz(self):
        input_gz_path = join(self.tmp_dir, 'input.gz')
        with gzip.GzipFile(input_gz_path, 'wb') as input_gz:
            input_gz.write(b'foo\nbar\n')

        self.assertEqual(
            b''.join(self.fs._cat_file(input_gz_path)),
            b'foo\nbar\n')

    def test_cat_bz2(self):
        input_bz2_path = join(self.tmp_dir, 'input.bz2')

        with bz2.BZ2File(input_bz2_path, 'wb') as input_bz2:
            input_bz2.write(b'bar\nbar\nfoo\n')

        self.assertEqual(
            b''.join(self.fs._cat_file(input_bz2_path)),
            b'bar\nbar\nfoo\n')


class LocalFSTestCase(SandboxedTestCase):

    def setUp(self):
        super(LocalFSTestCase, self).setUp()
        self.fs = LocalFilesystem()

    def test_can_handle_local_paths(self):
        self.assertEqual(self.fs.can_handle_path('/dem/bitties'), True)
        # relative paths
        self.assertEqual(self.fs.can_handle_path('garden'), True)

    def test_can_handle_file_uris(self):
        self.assertEqual(self.fs.can_handle_path('file:///dem/bitties'), True)

    def test_cant_handle_other_uris(self):
        self.assertEqual(self.fs.can_handle_path('http://yelp.com/'), False)

    def test_du(self):
        data_path_1 = self.makefile('data1', 'abcd')
        data_path_2 = self.makefile('more/data2', 'defg')

        self.assertEqual(self.fs.du(self.tmp_dir), 8)
        self.assertEqual(self.fs.du(data_path_1), 4)
        self.assertEqual(self.fs.du('file://' + data_path_2), 4)

    def test_ls_empty(self):
        self.assertEqual(list(self.fs.ls(self.tmp_dir)), [])

    def test_ls_basic(self):
        self.makefile('f', 'contents')
        self.assertEqual(sorted(self.fs.ls(self.tmp_dir)),
                         sorted(self.abs_paths('f')))

    def test_ls_basic_2(self):
        self.makefile('f', 'contents')
        self.makefile('f2', 'contents')
        self.assertEqual(sorted(self.fs.ls(self.tmp_dir)),
                         sorted(self.abs_paths('f', 'f2')))

    def test_ls_recurse(self):
        self.makefile('f', 'contents')
        self.makefile(join('d', 'f2'), 'contents')
        self.assertEqual(sorted(list(self.fs.ls(self.tmp_dir))),
                         sorted(self.abs_paths('f', 'd/f2')))

    def test_ls_with_file_uri(self):
        f_path = self.makefile('f', 'contents')
        f_uri = 'file://' + f_path

        self.assertEqual(list(self.fs.ls(f_uri)), [f_uri])

    def test_ls_dir_with_file_uri(self):
        self.makefile('f', 'contents')
        self.makefile('f2', 'contents')
        tmp_dir_uri = 'file://' + self.tmp_dir

        self.assertEqual(sorted(list(self.fs.ls(tmp_dir_uri))),
                         [tmp_dir_uri + '/f', tmp_dir_uri + '/f2'])

    def test_mkdir(self):
        path = join(self.tmp_dir, 'dir')
        self.fs.mkdir(path)
        self.assertEqual(os.path.isdir(path), True)

    def test_mkdir_file_uri(self):
        path = join(self.tmp_dir, 'dir')
        self.fs.mkdir('file://' + path)
        self.assertEqual(os.path.isdir(path), True)

    def test_exists_no(self):
        path = join(self.tmp_dir, 'f')
        self.assertEqual(self.fs.exists(path), False)
        self.assertEqual(self.fs.exists('file://' + path), False)

    def test_exists_yes(self):
        path = self.makefile('f', 'contents')
        self.assertEqual(self.fs.exists(path), True)
        self.assertEqual(self.fs.exists('file://' + path), True)

    def test_put(self):
        src = self.makefile('f', 'contents')
        dest1 = join(self.tmp_dir, 'g')
        dest2 = join(self.tmp_dir, 'h')

        self.fs.put(src, dest1)
        self.assertEqual(b''.join(self.fs.cat(dest1)), b'contents')

        # test put()-ing to a URI. *src* has to be an actual path
        self.fs.put(src, 'file://' + dest2)
        self.assertEqual(b''.join(self.fs.cat(dest1)), b'contents')

    def test_rm_file(self):
        path = self.makefile('f', 'contents')
        self.assertEqual(self.fs.exists(path), True)

        self.fs.rm(path)
        self.assertEqual(self.fs.exists(path), False)

    def test_rm_file_by_uri(self):
        path = self.makefile('f', 'contents')
        self.assertEqual(self.fs.exists(path), True)

        self.fs.rm('file://' + path)
        self.assertEqual(self.fs.exists(path), False)

    def test_rm_dir(self):
        path = self.makedirs('foobar')
        self.assertEqual(self.fs.exists(path), True)

        self.fs.rm(path)
        self.assertEqual(self.fs.exists(path), False)

    def test_touchz(self):
        path = join(self.tmp_dir, 'f')

        self.assertEqual(self.fs.exists(path), False)

        self.fs.touchz(path)
        self.assertEqual(self.fs.exists(path), True)

        # okay to touchz() an empty file
        self.fs.touchz(path)

        with open(path, 'w') as f:
            f.write('not empty anymore')

        # not okay to touchz() a non-empty file
        self.assertRaises(OSError, self.fs.touchz, path)

    def test_touchz_file_uri(self):
        uri = 'file://' + join(self.tmp_dir, 'f')

        self.assertEqual(self.fs.exists(uri), False)

        self.fs.touchz(uri)
        self.assertEqual(self.fs.exists(uri), True)

    def test_md5sum(self):
        path = self.makefile('f', 'abcd')

        self.assertEqual(self.fs.md5sum(path),
                         'e2fc714c4727ee9395f324cd2e7f331f')

        self.assertEqual(self.fs.md5sum('file://' + path),
                         'e2fc714c4727ee9395f324cd2e7f331f')
