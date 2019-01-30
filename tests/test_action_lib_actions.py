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

from packer_base_action_test_case import PackerBaseActionTestCase
from st2common.runners.base_action import Action
from lib.actions import BaseAction

from build import BuildAction

__all__ = [
    'BaseActionTestCase'
]


class BaseActionTestCase(PackerBaseActionTestCase):
    __test__ = True
    action_cls = BuildAction

    def test_init(self):
        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    def test__get_vars_global_and_input(self):
        action = self.get_action_instance()
        action._global_vars = {'test': 'test_value'}
        test_dict = {'test2': 'test_value2'}
        expected_result = {'test': 'test_value',
                          'test2': 'test_value2'}

        result = action._get_vars(test_dict)
        self.assertEqual(result, expected_result)

    def test__get_vars_just_global(self):
        action = self.get_action_instance()
        action._global_vars = {'test': 'test_value'}
        expected_result = {'test': 'test_value'}

        result = action._get_vars(None)
        self.assertEqual(result, expected_result)

    def test__get_vars_no_global(self):
        action = self.get_action_instance()
        action._global_vars = None
        test_dict = {'test2': 'test_value2'}
        expected_result = {'test2': 'test_value2'}

        result = action._get_vars(test_dict)
        self.assertEqual(result, expected_result)

    @mock.patch('lib.actions.os')
    def test_set_dir(self, mock_os):
        action = self.get_action_instance()
        test_dir = "test_dir"

        mock_os.chdir.return_value = "Success"

        action.set_dir(test_dir)
        mock_os.chdir.assert_called_once_with(test_dir)

    @mock.patch('lib.actions.packer')
    def test_packer(self, mock_packer):
        action = self.get_action_instance()
        action._exec_path = "test/path"
        test_dict = {'packerfile': 'test/file/packer'}
        expected_result = "Expected Result"

        mock_packer.Packer.return_value = expected_result

        result = action.packer(**test_dict)
        self.assertEqual(result, expected_result)
        mock_packer.Packer.assert_called_once_with(test_dict['packerfile'],
                                                  exc=None,
                                                  only=None,
                                                  vars=None,
                                                  vars_file=None,
                                                  exec_path="test/path")

    @mock.patch('lib.actions.packer')
    def test_packer_with_input_overrides(self, mock_packer):
        action = self.get_action_instance()
        action._exec_path = "test/path"
        test_dict = {'packerfile': 'test/file/packer',
                    'exc': True,
                    'variables': {'test': 'test'}}
        expected_result = "Expected Result"

        mock_packer.Packer.return_value = expected_result

        result = action.packer(**test_dict)
        self.assertEqual(result, expected_result)
        mock_packer.Packer.assert_called_once_with(test_dict['packerfile'],
                                                  exc=True,
                                                  only=None,
                                                  vars=test_dict['variables'],
                                                  vars_file=None,
                                                  exec_path="test/path")
