# Copyright 2012 Yelp
# Copyright 2013 David Marin
# Copyright 2014-2018 Yelp
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
from mrjob import cmd
from mrjob.tools import diagnose
from mrjob.tools import spark_submit
from mrjob.tools.emr import audit_usage
from mrjob.tools.emr import create_cluster
from mrjob.tools.emr import report_long_jobs
from mrjob.tools.emr import s3_tmpwatch
from mrjob.tools.emr import terminate_cluster
from mrjob.tools.emr import terminate_idle_clusters

from tests.py2 import patch
from tests.sandbox import BasicTestCase


class CommandTestCase(BasicTestCase):

    def setUp(self):
        def error(msg=None):
            if msg:
                raise ValueError(msg)
            else:
                raise ValueError

        p = patch.object(cmd, '_error', side_effect=error)
        p.start()
        self.addCleanup(p.stop)

    def _test_main_call(self, module, cmd_name):
        with patch.object(module, 'main') as m_main:
            cmd.main(args=['mrjob', cmd_name])
            m_main.assert_called_once_with([])

    def test_audit_usage(self):
        self._test_main_call(audit_usage, 'audit-emr-usage')

    def test_diagnose(self):
        self._test_main_call(diagnose, 'diagnose')

    def test_create_cluster(self):
        self._test_main_call(create_cluster, 'create-cluster')

    def test_report_long_jobs(self):
        self._test_main_call(report_long_jobs, 'report-long-jobs')

    def test_s3_tmpwatch(self):
        self._test_main_call(s3_tmpwatch, 's3-tmpwatch')

    def test_spark_submit(self):
        self._test_main_call(spark_submit, 'spark-submit')

    def test_terminate_idle_clusters(self):
        self._test_main_call(terminate_idle_clusters,
                             'terminate-idle-clusters')

    def test_terminate_cluster(self):
        self._test_main_call(terminate_cluster, 'terminate-cluster')
