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

from inspect_action import InspectAction

__all__ = [
    'InspectActionTestCase'
]


class InspectActionTestCase(PackerBaseActionTestCase):
    __test__ = True
    action_cls = InspectAction

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, InspectAction)
        self.assertIsInstance(action, BaseAction)
        self.assertIsInstance(action, Action)

    @mock.patch('lib.actions.BaseAction.packer')
    def test_run_success(self, mock_packer):
        action = self.get_action_instance(self.blank_config)
        test_dict = {'packerfile': 'test/file/packer'}

        expected_result = "Expected Result"
        mock_inspect_return = mock.Mock(parsed_output=expected_result)
        mock_packer.return_value.inspect.return_value = mock_inspect_return

        result = action.run(**test_dict)
        self.assertEqual(result, expected_result)
        mock_packer.assert_called_once_with(test_dict['packerfile'])
        mock_packer.return_value.inspect.assert_called_once_with(mrf=True)

    @mock.patch('lib.actions.BaseAction.packer')
    def test_run_error(self, mock_packer):
        action = self.get_action_instance(self.blank_config)
        test_dict = {'packerfile': 'test/file/packer'}

        mock_packer.return_value.inspect.side_effect = Exception("ERROR")

        with self.assertRaises(Exception):
            action.run(**test_dict)
        mock_packer.assert_called_once_with(test_dict['packerfile'])
        mock_packer.return_value.inspect.assert_called_once_with(mrf=True)
