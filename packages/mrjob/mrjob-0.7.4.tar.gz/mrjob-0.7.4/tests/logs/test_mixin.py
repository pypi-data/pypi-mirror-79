# Copyright 2016-2017 Yelp
# Copyright 2018 Yelp and Google Inc.
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
from copy import deepcopy

from mrjob.emr import EMRJobRunner
from mrjob.hadoop import HadoopJobRunner
from mrjob.logs.mixin import LogInterpretationMixin
from mrjob.logs.mixin import _log_parsing_task_log
from mrjob.step import _is_spark_step_type

from tests.py2 import Mock
from tests.py2 import patch
from tests.sandbox import BasicTestCase
from tests.mock_boto3 import MockBoto3TestCase
from tests.mockhadoop import MockHadoopTestCase


class LogInterpretationMixinTestCase(BasicTestCase):

    class MockRunner(Mock, LogInterpretationMixin):
        pass

    def setUp(self):
        self.runner = self.MockRunner()
        self.runner._opts = {}
        self.runner._step_type_uses_spark = _is_spark_step_type
        self.runner._spark_deploy_mode.return_value = 'client'

        self.log = self.start(patch('mrjob.logs.mixin.log'))


class InterpretHistoryLogTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(InterpretHistoryLogTestCase, self).setUp()

        self.runner._ls_history_logs = Mock()
        self._interpret_history_log = (
            self.start(patch('mrjob.logs.mixin._interpret_history_log')))

    def test_history_interpretation_already_filled(self):
        log_interpretation = dict(history={})

        self.runner._interpret_history_log(log_interpretation)

        self.assertEqual(
            log_interpretation, dict(history={}))

        self.assertFalse(self.log.warning.called)
        self.assertFalse(self._interpret_history_log.called)
        self.assertFalse(self.runner._ls_history_logs.called)

    def test_no_job_id(self):
        log_interpretation = dict(step={})

        self.runner._interpret_history_log(log_interpretation)

        self.assertEqual(
            log_interpretation, dict(step={}))

        self.assertTrue(self.log.warning.called)
        self.assertFalse(self._interpret_history_log.called)
        self.assertFalse(self.runner._ls_history_logs.called)

    def test_with_job_id(self):
        self._interpret_history_log.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(step=dict(job_id='job_1'))

        self.runner._interpret_history_log(log_interpretation)

        self.assertEqual(
            log_interpretation,
            dict(step=dict(job_id='job_1'),
                 history=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_history_logs.assert_called_once_with(
            job_id='job_1', output_dir=None)
        self._interpret_history_log.assert_called_once_with(
            self.runner.fs, self.runner._ls_history_logs.return_value)

    def test_with_job_id_and_output_dir(self):
        self._interpret_history_log.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(
            step=dict(job_id='job_1', output_dir='hdfs:///path/'))

        self.runner._interpret_history_log(log_interpretation)

        self.assertEqual(
            log_interpretation,
            dict(step=dict(job_id='job_1', output_dir='hdfs:///path/'),
                 history=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_history_logs.assert_called_once_with(
            job_id='job_1', output_dir='hdfs:///path/')
        self._interpret_history_log.assert_called_once_with(
            self.runner.fs, self.runner._ls_history_logs.return_value)

    def test_no_read_logs(self):
        self.runner._opts['read_logs'] = False

        self._interpret_history_log.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(
            step=dict(job_id='job_1', output_dir='hdfs:///path/'))

        self.runner._interpret_history_log(log_interpretation)

        # should do nothing
        self.assertFalse(self.log.warning.called)
        self.assertFalse(self._interpret_history_log.called)
        self.assertFalse(self.runner._ls_history_logs.called)

        self.assertEqual(log_interpretation, dict(
            step=dict(job_id='job_1', output_dir='hdfs:///path/')))


class InterpretStepLogTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(InterpretStepLogTestCase, self).setUp()

        self.runner._get_step_log_interpretation = Mock()

    def test_step_interpretation_already_filled(self):
        log_interpretation = dict(step={})

        self.runner._interpret_step_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation, dict(step={}))

        self.assertFalse(self.runner._get_step_log_interpretation.called)

    def test_step_interpretation(self):
        self.runner._get_step_log_interpretation.return_value = dict(
            job_id='job_1')

        log_interpretation = {}

        self.runner._interpret_step_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(job_id='job_1')))

        self.runner._get_step_log_interpretation.assert_called_once_with(
            log_interpretation, 'streaming')

    def test_spark_step_interpretation(self):
        self.runner._get_step_log_interpretation.return_value = dict(
            job_id='job_1')

        log_interpretation = {}

        self.runner._interpret_step_logs(log_interpretation, 'spark')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(job_id='job_1')))

        self.runner._get_step_log_interpretation.assert_called_once_with(
            log_interpretation, 'spark')

    def test_no_step_interpretation(self):
        self.runner._get_step_log_interpretation.return_value = None

        log_interpretation = {}

        self.runner._interpret_step_logs(log_interpretation, 'streaming')

        self.assertEqual(log_interpretation, {})

        self.runner._get_step_log_interpretation.assert_called_once_with(
            log_interpretation, 'streaming')

    def test_no_read_logs(self):
        self.runner._opts['read_logs'] = False

        self.runner._get_step_log_interpretation.return_value = dict(
            job_id='job_1')

        log_interpretation = {}

        self.runner._interpret_step_logs(log_interpretation, 'streaming')

        self.assertFalse(self.runner._get_step_log_interpretation.called)

        self.assertEqual(log_interpretation, {})


class InterpretTaskLogsTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(InterpretTaskLogsTestCase, self).setUp()

        self.runner.get_hadoop_version = Mock(return_value='2.7.1')
        self.runner._ls_task_logs = Mock()

        self._interpret_spark_logs = (
            self.start(patch('mrjob.logs.mixin._interpret_spark_logs')))
        self._interpret_task_logs = (
            self.start(patch('mrjob.logs.mixin._interpret_task_logs')))

    def _test_task_interpretation_already_filled(
            self, log_interpretation, step_type='streaming', **kwargs):
        orig_log_interpretation = deepcopy(log_interpretation)

        self.runner._interpret_task_logs(
            log_interpretation, step_type, **kwargs)

        self.assertEqual(log_interpretation, orig_log_interpretation)

        self.assertFalse(self.log.warning.called)
        self.assertFalse(self._interpret_task_logs.called)
        self.assertFalse(self.runner._ls_task_logs.called)
        self.assertFalse(self.runner._ls_spark_logs.called)

    def test_task_interpretation_already_filled(self):
        log_interpretation = dict(task={})

        self._test_task_interpretation_already_filled(log_interpretation)

    def test_spark_task_interpretation_already_filled(self):
        log_interpretation = dict(task={})

        self._test_task_interpretation_already_filled(log_interpretation,
                                                      'spark')

    def test_task_interpretation_already_partially_filled(self):
        log_interpretation = dict(task=dict(partial=True))

        self._test_task_interpretation_already_filled(log_interpretation)

    def test_task_interpretation_already_fully_filled(self):
        # if partial=False, only accept complete task interpretations
        log_interpretation = dict(task={})

        self._test_task_interpretation_already_filled(
            log_interpretation, partial=False)

    def test_replace_partial_interpretation_with_full(self):
        log_interpretation = dict(
            step=dict(application_id='app_id'),
            task=dict(partial=True))

        self.runner._interpret_task_logs(
            log_interpretation, 'streaming', partial=False)

        self.assertTrue(self.runner._ls_task_logs.called)
        self.assertTrue(self._interpret_task_logs.called)

    def test_application_id(self):
        self._interpret_task_logs.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(step=dict(application_id='app_1'))

        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(application_id='app_1'),
                 task=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_task_logs.assert_called_once_with(
            'streaming',
            attempt_to_container_id={},
            error_attempt_ids=(),
            application_id='app_1',
            job_id=None,
            output_dir=None)
        self._interpret_task_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._ls_task_logs.return_value,
            partial=True,
            log_callback=_log_parsing_task_log)

    def test_spark(self):
        # don't need to test spark with job_id, since it doesn't run
        # in Hadoop 1

        # TODO: Spark wouldn't have counters in logs
        self._interpret_spark_logs.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(step=dict(application_id='app_1'))

        self.runner._interpret_task_logs(log_interpretation, 'spark')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(application_id='app_1'),
                 task=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_task_logs.assert_called_once_with(
            'spark',
            attempt_to_container_id={},
            error_attempt_ids=(),
            application_id='app_1',
            job_id=None,
            output_dir=None)
        self._interpret_spark_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._ls_task_logs.return_value,
            partial=True,
            log_callback=_log_parsing_task_log)

    def test_job_id(self):
        self.runner.get_hadoop_version.return_value = '1.0.3'

        self._interpret_task_logs.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(step=dict(job_id='job_1'))

        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(job_id='job_1'),
                 task=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_task_logs.assert_called_once_with(
            'streaming',
            attempt_to_container_id={},
            error_attempt_ids=(),
            application_id=None,
            job_id='job_1',
            output_dir=None)
        self._interpret_task_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._ls_task_logs.return_value,
            partial=True,
            log_callback=_log_parsing_task_log)

    def test_output_dir(self):
        self._interpret_task_logs.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(
            step=dict(application_id='app_1', output_dir='hdfs:///path/'))

        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(application_id='app_1', output_dir='hdfs:///path/'),
                 task=dict(counters={'foo': {'bar': 1}})))

        self.assertFalse(self.log.warning.called)
        self.runner._ls_task_logs.assert_called_once_with(
            'streaming',
            attempt_to_container_id={},
            error_attempt_ids=(),
            application_id='app_1',
            job_id=None,
            output_dir='hdfs:///path/')
        self._interpret_task_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._ls_task_logs.return_value,
            partial=True,
            log_callback=_log_parsing_task_log)

    def test_missing_application_id(self):
        log_interpretation = dict(step=dict(job_id='job_1'))

        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation, dict(step=dict(job_id='job_1')))

        self.assertTrue(self.log.warning.called)
        self.assertFalse(self._interpret_task_logs.called)
        self.assertFalse(self.runner._ls_task_logs.called)

    def test_missing_job_id(self):
        self.runner.get_hadoop_version.return_value = '1.0.3'

        log_interpretation = dict(step=dict(app_id='app_1'))

        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertEqual(
            log_interpretation,
            dict(step=dict(app_id='app_1')))

        self.assertTrue(self.log.warning.called)
        self.assertFalse(self._interpret_task_logs.called)
        self.assertFalse(self.runner._ls_task_logs.called)

    def test_no_read_logs(self):
        self.runner._opts['read_logs'] = False

        self._interpret_task_logs.return_value = dict(
            counters={'foo': {'bar': 1}})

        log_interpretation = dict(step=dict(application_id='app_1'))

        # should do nothing
        self.runner._interpret_task_logs(log_interpretation, 'streaming')

        self.assertFalse(self.log.warning.called)
        self.assertFalse(self._interpret_task_logs.called)
        self.assertFalse(self.runner._ls_task_logs.called)

        self.assertEqual(log_interpretation,
                         dict(step=dict(application_id='app_1')))


class PickCountersTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(PickCountersTestCase, self).setUp()

        self.runner._interpret_history_log = Mock()
        self.runner._interpret_step_logs = Mock()

        # no need to mock mrjob.logs.counters._pick_counters();
        # what it does is really straightforward

    def test_counters_already_present(self):
        log_interpretation = dict(
            step=dict(counters={'foo': {'bar': 1}}))

        self.assertEqual(
            self.runner._pick_counters(log_interpretation, 'streaming'),
            {'foo': {'bar': 1}})

        # don't log anything if runner._pick_counters() doesn't have
        # to fetch any new information
        self.assertFalse(self.log.info.called)
        self.assertFalse(self.runner._interpret_step_logs.called)
        self.assertFalse(self.runner._interpret_history_log.called)

    def test_counters_from_step_logs(self):
        def mock_interpret_step_logs(log_interpretation, step_type):
            log_interpretation['step'] = dict(
                counters={'foo': {'bar': 1}})

        self.runner._interpret_step_logs = Mock(
            side_effect=mock_interpret_step_logs)

        log_interpretation = {}

        self.assertEqual(
            self.runner._pick_counters(log_interpretation, 'streaming'),
            {'foo': {'bar': 1}})

        self.assertTrue(self.log.info.called)  # 'Attempting to fetch...'
        self.assertTrue(self.runner._interpret_step_logs.called)
        self.assertFalse(self.runner._interpret_history_log.called)

    def test_counters_from_history_logs(self):
        def mock_interpret_history_log(log_interpretation):
            log_interpretation['history'] = dict(
                counters={'foo': {'bar': 1}})

        self.runner._interpret_history_log = Mock(
            side_effect=mock_interpret_history_log)

        log_interpretation = {}

        self.assertEqual(
            self.runner._pick_counters(log_interpretation, 'streaming'),
            {'foo': {'bar': 1}})

        self.assertTrue(self.log.info.called)  # 'Attempting to fetch...'
        self.assertTrue(self.runner._interpret_step_logs.called)
        self.assertTrue(self.runner._interpret_history_log.called)

    def test_do_nothing_for_spark_logs(self):
        log_interpretation = {}

        self.assertEqual(
            self.runner._pick_counters(log_interpretation, 'spark'),
            {})

        self.assertFalse(self.log.info.called)  # 'Attempting to fetch...'
        self.assertFalse(self.runner._interpret_step_logs.called)
        self.assertFalse(self.runner._interpret_history_log.called)


class LsHistoryLogsTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(LsHistoryLogsTestCase, self).setUp()

        self._ls_history_logs = self.start(patch(
            'mrjob.logs.mixin._ls_history_logs'))
        self.runner._stream_history_log_dirs = Mock()

    def test_basic(self):
        # the _ls_history_logs() method is a very thin wrapper. Just
        # verify that the keyword args get passed through and
        # that logging happens in the right order

        self._ls_history_logs.return_value = [
            dict(path='hdfs:///history/history.jhist'),
        ]

        results = self.runner._ls_history_logs(
            job_id='job_1', output_dir='hdfs:///output/')

        self.assertFalse(self.log.info.called)

        self.assertEqual(next(results),
                         dict(path='hdfs:///history/history.jhist'))

        self.runner._stream_history_log_dirs.assert_called_once_with(
            output_dir='hdfs:///output/')
        self._ls_history_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._stream_history_log_dirs.return_value,
            job_id='job_1')

        self.assertEqual(self.log.info.call_count, 1)
        self.assertIn('hdfs:///history/history.jhist',
                      self.log.info.call_args[0][0])

        self.assertRaises(StopIteration, next, results)

    def test_no_read_logs(self):
        self.runner._opts['read_logs'] = False

        self._ls_history_logs.return_value = [
            dict(path='hdfs:///history/history.jhist'),
        ]

        results = self.runner._ls_history_logs(
            job_id='job_1', output_dir='hdfs:///output/')

        self.assertRaises(StopIteration, next, results)

        self.assertFalse(self.log.info.called)
        self.assertFalse(self.runner._stream_history_log_dirs.called)
        self.assertFalse(self._ls_history_logs.called)


class LsTaskLogsTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(LsTaskLogsTestCase, self).setUp()

        self._ls_task_logs = self.start(patch(
            'mrjob.logs.mixin._ls_task_logs'))
        self._ls_spark_task_logs = self.start(patch(
            'mrjob.logs.mixin._ls_spark_task_logs'))

        self.runner._stream_task_log_dirs = Mock()

    def test_streaming_step(self):
        # the _ls_task_logs() method is a very thin wrapper. Just
        # verify that the keyword args get passed through and
        # that logging happens in the right order

        self._ls_task_logs.return_value = [
            dict(path='hdfs:///userlogs/1/syslog'),
            dict(path='hdfs:///userlogs/2/syslog'),
        ]

        results = self.runner._ls_task_logs(
            'streaming',
            application_id='app_1',
            job_id='job_1', output_dir='hdfs:///output/')

        self.assertFalse(self.log.info.called)

        self.assertEqual(next(results), dict(path='hdfs:///userlogs/1/syslog'))

        self.runner._stream_task_log_dirs.assert_called_once_with(
            application_id='app_1',
            output_dir='hdfs:///output/')

        self._ls_task_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._stream_task_log_dirs.return_value,
            attempt_to_container_id=None,
            error_attempt_ids=None,
            application_id='app_1',
            job_id='job_1')
        self.assertFalse(self._ls_spark_task_logs.called)

        self.assertEqual(
            list(results),
            [dict(path='hdfs:///userlogs/2/syslog')]
        )

        # unlike most of the _ls_*() methods, logging is handled elsewhere
        # with a callback
        self.assertFalse(self.log.info.called)

    def test_spark_step(self):
        # the _ls_task_logs() method is a very thin wrapper. Just
        # verify that the keyword args get passed through and
        # that logging happens in the right order

        self._ls_spark_task_logs.return_value = [
            dict(path='hdfs:///userlogs/1/stderr'),
            dict(path='hdfs:///userlogs/2/stderr'),
        ]

        results = self.runner._ls_task_logs(
            'spark',
            application_id='app_1',
            job_id='job_1', output_dir='hdfs:///output/')

        self.assertFalse(self.log.info.called)

        self.assertEqual(next(results), dict(path='hdfs:///userlogs/1/stderr'))

        self.runner._stream_task_log_dirs.assert_called_once_with(
            application_id='app_1',
            output_dir='hdfs:///output/')

        self._ls_spark_task_logs.assert_called_once_with(
            self.runner.fs,
            self.runner._stream_task_log_dirs.return_value,
            attempt_to_container_id=None,
            error_attempt_ids=None,
            application_id='app_1',
            job_id='job_1')
        self.assertFalse(self._ls_task_logs.called)

        self.assertEqual(
            list(results),
            [dict(path='hdfs:///userlogs/2/stderr')]
        )

        # unlike most of the _ls_*() methods, logging is handled elsewhere
        # with a callback
        self.assertFalse(self.log.info.called)

    def test_no_read_logs(self):
        self.runner._opts['read_logs'] = False

        self._ls_task_logs.return_value = [
            dict(path='hdfs:///userlogs/1/syslog'),
            dict(path='hdfs:///userlogs/2/syslog'),
        ]

        results = self.runner._ls_task_logs(
            'streaming',
            application_id='app_1',
            job_id='job_1', output_dir='hdfs:///output/')

        self.assertRaises(StopIteration, next, results)

        self.assertFalse(self.log.info.called)
        self.assertFalse(self._ls_task_logs.called)
        self.assertFalse(self._ls_spark_task_logs.called)
        self.assertFalse(self.runner._stream_task_log_dirs.called)


class PickErrorTestCase(LogInterpretationMixinTestCase):

    def setUp(self):
        super(PickErrorTestCase, self).setUp()

        self.runner._interpret_history_log = Mock()
        self.runner._interpret_step_logs = Mock()
        self.runner._interpret_task_logs = Mock()

        self._pick_error = self.start(
            patch('mrjob.logs.mixin._pick_error'))

    def test_logs_already_interpreted(self):
        log_interpretation = dict(
            history={}, step={}, task={})

        self.assertEqual(
            self.runner._pick_error(log_interpretation, 'streaming'),
            self._pick_error.return_value)

        # don't log a message or interpret logs
        self.assertFalse(self.log.info.called)
        self.assertFalse(self.runner._interpret_history_log.called)
        self.assertFalse(self.runner._interpret_step_logs.called)
        self.assertFalse(self.runner._interpret_task_logs.called)

    def _test_interpret_all_logs(self, log_interpretation):
        self.assertEqual(
            self.runner._pick_error(log_interpretation, 'streaming'),
            self._pick_error.return_value)

        # log a message ('Scanning logs...') and call _interpret() methods
        self.assertTrue(self.log.info.called)
        self.assertTrue(self.runner._interpret_history_log.called)
        self.assertTrue(self.runner._interpret_step_logs.called)
        self.assertTrue(self.runner._interpret_task_logs.called)

    def test_empty_log_interpretation(self):
        self._test_interpret_all_logs({})

    def test_step_log_only(self):
        self._test_interpret_all_logs(dict(step={}))

    def test_step_and_history_logs_only(self):
        self._test_interpret_all_logs(dict(step={}, history={}))

    def test_step_and_task_logs_only(self):
        self._test_interpret_all_logs(dict(step={}, task={}))

    def test_spark_client_mode(self):
        log_interpretation = {}

        self.assertEqual(
            self.runner._pick_error(log_interpretation, 'spark'),
            self._pick_error.return_value)

        self.assertTrue(self.log.info.called)
        self.assertFalse(self.runner._interpret_history_log.called)
        self.assertTrue(self.runner._interpret_step_logs.called)
        self.assertFalse(self.runner._interpret_task_logs.called)

    def test_spark_cluster_mode(self):
        log_interpretation = {}

        self.runner._spark_deploy_mode.return_value = 'cluster'

        self.assertEqual(
            self.runner._pick_error(log_interpretation, 'spark'),
            self._pick_error.return_value)

        self.assertTrue(self.log.info.called)
        self.assertFalse(self.runner._interpret_history_log.called)
        self.assertTrue(self.runner._interpret_step_logs.called)
        self.assertTrue(self.runner._interpret_task_logs.called)

    def test_logs_needed_to_pick_error_used(self):
        log_interpretation = {}

        self.runner._logs_needed_to_pick_error = Mock(
            return_value=('history', 'task'))

        self.assertEqual(
            self.runner._pick_error(log_interpretation, 'streaming'),
            self._pick_error.return_value)

        self.assertTrue(self.runner._logs_needed_to_pick_error.called)

        self.assertTrue(self.log.info.called)
        self.assertTrue(self.runner._interpret_history_log.called)
        self.assertFalse(self.runner._interpret_step_logs.called)
        self.assertTrue(self.runner._interpret_task_logs.called)


class LogsNeededToPickErrorTestCase(MockBoto3TestCase, MockHadoopTestCase):

    def test_emr_runner(self):
        # EMR runner is always in cluster mode
        runner = EMRJobRunner()

        self.assertEqual(runner._logs_needed_to_pick_error('streaming'),
                         ('step', 'history', 'task'))
        self.assertEqual(runner._logs_needed_to_pick_error('spark'),
                         ('step', 'task'))

    def test_hadoop_runner_client_mode(self):
        runner = HadoopJobRunner()

        self.assertEqual(runner._logs_needed_to_pick_error('streaming'),
                         ('step', 'history', 'task'))
        self.assertEqual(runner._logs_needed_to_pick_error('spark'),
                         ('step',))

    def test_hadoop_runner_cluster_mode(self):
        runner = HadoopJobRunner(spark_deploy_mode='cluster')

        self.assertEqual(runner._logs_needed_to_pick_error('streaming'),
                         ('step', 'history', 'task'))
        self.assertEqual(runner._logs_needed_to_pick_error('spark'),
                         ('step', 'task'))
