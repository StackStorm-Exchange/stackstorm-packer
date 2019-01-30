# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import mock
from sh import ErrorReturnCode

from packer_base_action_test_case import PackerBaseActionTestCase
from st2common.runners.base_action import Action
from lib.actions import BaseAction

from build import BuildAction

__all__ = [
    'BuildActionTestCase'
]


class BuildActionTestCase(PackerBaseActionTestCase):
    __test__ = True
    action_cls = BuildAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, BuildAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    @mock.patch('lib.actions.BaseAction.packer')
    def test_run_success(self, mock_packer):
        action = self.get_action_instance(self.blank_config)
        test_dict = {'packerfile': 'test/file/packer'}

        expected_result = "Test Build"
        mock_build_return = mock.Mock(stdout=expected_result, status="success")
        mock_packer.return_value.build.return_value = mock_build_return

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_packer.assert_called_once_with(test_dict['packerfile'],
                                            exc=None,
                                            only=None,
                                            variables=None,
                                            vars_file=None)
        mock_packer.return_value.build.assert_called_once_with(parallel=True,
                                                              debug=False,
                                                              force=False)

    @mock.patch('lib.actions.BaseAction.packer')
    def test_run_success_with_input_overrides(self, mock_packer):
        action = self.get_action_instance(self.blank_config)
        test_dict = {'packerfile': 'test/file/packer',
                    'debug': True,
                    'exclude': True,
                    'variables': {'test': 'test'}}

        expected_result = "Test Build"
        mock_build_return = mock.Mock(stdout=expected_result, status="success")
        mock_packer.return_value.build.return_value = mock_build_return

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_packer.assert_called_once_with(test_dict['packerfile'],
                                            exc=True,
                                            only=None,
                                            variables=test_dict['variables'],
                                            vars_file=None)
        mock_packer.return_value.build.assert_called_once_with(parallel=True,
                                                              debug=True,
                                                              force=False)

    @mock.patch('lib.actions.BaseAction.packer')
    def test_run_error(self, mock_packer):
        action = self.get_action_instance(self.blank_config)
        test_dict = {'packerfile': 'test/file/packer'}

        expected_result = "Test Build"
        mock_error = ErrorReturnCode(stdout=expected_result,
                                    full_cmd="Test_cmd",
                                    stderr="Test_stderr")

        mock_packer.return_value.build.side_effect = mock_error

        result = action.run(**test_dict)
        self.assertEqual(result, (False, expected_result))
        mock_packer.assert_called_once_with(test_dict['packerfile'],
                                            exc=None,
                                            only=None,
                                            variables=None,
                                            vars_file=None)

    def test_format_results_success(self):
        action = self.get_action_instance()
        test_string = "\x1b[1;32mTest_string\x1b[0m"
        expected_result = "Test_string"

        result = action.format_results(test_string)
        self.assertEqual(result, expected_result)

    def test_format_results_failed(self):
        action = self.get_action_instance()
        test_string = ("\x1b[0;32mvsphere-iso: \x1b[38;5;41m "
                      "System Package lnav should be installed\x1b[0m\x1b[0m\n")
        expected_result = 'vsphere-iso:  System Package lnav should be installed\n'

        result = action.format_results(test_string)
        self.assertEqual(result, expected_result)
