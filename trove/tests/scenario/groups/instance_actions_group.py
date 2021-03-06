# Copyright 2015 Tesora Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from proboscis import test

from trove.tests.scenario import groups
from trove.tests.scenario.groups.test_group import TestGroup
from trove.tests.scenario.runners import test_runners


GROUP = "scenario.instance_actions_group"


class InstanceActionsRunnerFactory(test_runners.RunnerFactory):

    _runner_ns = 'instance_actions_runners'
    _runner_cls = 'InstanceActionsRunner'


@test(depends_on_groups=[groups.INST_LOG],
      groups=[GROUP, groups.INST_ACTIONS])
class InstanceActionsGroup(TestGroup):
    """Test Instance Actions functionality."""

    def __init__(self):
        super(InstanceActionsGroup, self).__init__(
            InstanceActionsRunnerFactory.instance())

    @test
    def add_test_data(self):
        """Add test data."""
        self.test_runner.run_add_test_data()

    @test(depends_on=[add_test_data])
    def verify_test_data(self):
        """Verify test data."""
        self.test_runner.run_verify_test_data()

    @test(runs_after=[verify_test_data])
    def instance_restart(self):
        """Restart an existing instance."""
        self.test_runner.run_instance_restart()

    @test(depends_on=[verify_test_data, instance_restart])
    def verify_test_data_after_restart(self):
        """Verify test data after restart."""
        self.test_runner.run_verify_test_data()

    @test(depends_on=[instance_restart],
          runs_after=[verify_test_data_after_restart])
    def instance_resize_volume(self):
        """Resize attached volume."""
        self.test_runner.run_instance_resize_volume()

    @test(depends_on=[verify_test_data, instance_resize_volume])
    def verify_test_data_after_volume_resize(self):
        """Verify test data after volume resize."""
        self.test_runner.run_verify_test_data()

    @test(depends_on=[add_test_data],
          runs_after=[verify_test_data_after_volume_resize])
    def remove_test_data(self):
        """Remove test data."""
        self.test_runner.run_remove_test_data()


@test(depends_on_classes=[InstanceActionsGroup],
      groups=[GROUP, groups.INST_ACTIONS_RESIZE])
class InstanceActionsResizeGroup(TestGroup):
    """Test Instance Actions Resize functionality."""

    def __init__(self):
        super(InstanceActionsResizeGroup, self).__init__(
            InstanceActionsRunnerFactory.instance())

    @test
    def add_test_data(self):
        """Add test data."""
        self.test_runner.run_add_test_data()

    @test(depends_on=[add_test_data])
    def verify_test_data(self):
        """Verify test data."""
        self.test_runner.run_verify_test_data()

    @test(runs_after=[verify_test_data])
    def instance_resize_flavor(self):
        """Resize instance flavor."""
        self.test_runner.run_instance_resize_flavor()


@test(depends_on_classes=[InstanceActionsResizeGroup],
      groups=[GROUP, groups.INST_ACTIONS_RESIZE_WAIT])
class InstanceActionsResizeWaitGroup(TestGroup):
    """Test that Instance Actions Resize Completes."""

    def __init__(self):
        super(InstanceActionsResizeWaitGroup, self).__init__(
            InstanceActionsRunnerFactory.instance())

    @test
    def wait_for_instance_resize_flavor(self):
        """Wait for resize instance flavor to complete."""
        self.test_runner.run_wait_for_instance_resize_flavor()

    @test(depends_on=[wait_for_instance_resize_flavor])
    def verify_test_data_after_flavor_resize(self):
        """Verify test data after flavor resize."""
        self.test_runner.run_verify_test_data()

    @test(runs_after=[verify_test_data_after_flavor_resize])
    def remove_test_data(self):
        """Remove test data."""
        self.test_runner.run_remove_test_data()
