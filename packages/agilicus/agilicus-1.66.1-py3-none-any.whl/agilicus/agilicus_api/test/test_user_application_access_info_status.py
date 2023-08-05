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
from agilicus_api.models.user_application_access_info_status import UserApplicationAccessInfoStatus  # noqa: E501
from agilicus_api.rest import ApiException

class TestUserApplicationAccessInfoStatus(unittest.TestCase):
    """UserApplicationAccessInfoStatus unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UserApplicationAccessInfoStatus
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.user_application_access_info_status.UserApplicationAccessInfoStatus()  # noqa: E501
        if include_optional :
            return UserApplicationAccessInfoStatus(
                user_id = 'tuU7smH86zAXMl76sua6xQ', 
                org_id = 'IAsl3dl40aSsfLKiU76', 
                org_name = 'egov', 
                parent_org_id = 'G99q3lasls29wsk', 
                parent_org_name = 'root', 
                application_name = 'parking', 
                application_url = 'https://parking.cloud.egov.city', 
                application_description = 'An application to submit parking requests', 
                application_category = 'citizen-facing', 
                icon_url = 'https://storage.googleapis.com/agilicus/logo.svg', 
                access_level = 'requested', 
                application_default_role_name = 'self', 
                application_default_role_id = 'as0Z6fXFsl23'
            )
        else :
            return UserApplicationAccessInfoStatus(
                user_id = 'tuU7smH86zAXMl76sua6xQ',
                org_id = 'IAsl3dl40aSsfLKiU76',
                org_name = 'egov',
                application_name = 'parking',
                application_url = 'https://parking.cloud.egov.city',
                access_level = 'requested',
        )

    def testUserApplicationAccessInfoStatus(self):
        """Test UserApplicationAccessInfoStatus"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
