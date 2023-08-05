# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.09.08
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import agilicus_api
from agilicus_api.models.environment import Environment  # noqa: E501
from agilicus_api.rest import ApiException

class TestEnvironment(unittest.TestCase):
    """Environment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Environment
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.environment.Environment()  # noqa: E501
        if include_optional :
            return Environment(
                created = '2015-07-07T15:49:51.230+02:00', 
                name = '0', 
                maintenance_org_id = '0', 
                version_tag = '0', 
                config_mount_path = '0', 
                config_as_mount = '0', 
                config_as_env = '0', 
                secrets_mount_path = '0', 
                secrets_as_mount = '0', 
                secrets_as_env = '0', 
                application_services = [
                    agilicus_api.models.application_service.ApplicationService(
                        created = '2015-07-07T15:49:51.230+02:00', 
                        id = '123', 
                        name = '0', 
                        org_id = '0', 
                        hostname = 'db.example.com', 
                        ipv4_addresses = [
                            '192.0.2.1'
                            ], 
                        name_resolution = 'static', 
                        port = 56, 
                        protocol = 'tcp', 
                        assignments = [
                            agilicus_api.models.application_service_assignment.ApplicationServiceAssignment(
                                app_id = '0', 
                                environment_name = '0', 
                                org_id = '0', )
                            ], 
                        updated = '2015-07-07T15:49:51.230+02:00', )
                    ], 
                serverless_image = '0', 
                status = agilicus_api.models.environment_status.EnvironmentStatus(
                    runtime_status = agilicus_api.models.runtime_status.RuntimeStatus(
                        overall_status = 'good', 
                        running_replicas = 2, 
                        error_message = 'CrashLoopBackoff', 
                        restarts = 5, 
                        cpu = 0.6, 
                        memory = 45.2, 
                        last_apply_time = '2020-06-19T15:35:08Z', 
                        updated = '2015-07-07T15:49:51.230+02:00', 
                        running_image = 'cr.agilicus.com/applications/iomad:v1.13.0', 
                        running_hash = 'sha256:2fb759c1adfe40863b89a4076111af8f210e7342d2240f09b08fc445b357112e', 
                        org_id = '123', ), ), 
                updated = '2015-07-07T15:49:51.230+02:00'
            )
        else :
            return Environment(
                name = '0',
                version_tag = '0',
        )

    def testEnvironment(self):
        """Test Environment"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
