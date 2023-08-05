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
from agilicus_api.models.list_application_summary_response import ListApplicationSummaryResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListApplicationSummaryResponse(unittest.TestCase):
    """ListApplicationSummaryResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListApplicationSummaryResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_application_summary_response.ListApplicationSummaryResponse()  # noqa: E501
        if include_optional :
            return ListApplicationSummaryResponse(
                application_summaries = [
                    agilicus_api.models.application_summary.ApplicationSummary(
                        status = agilicus_api.models.application_summary_status.ApplicationSummaryStatus(
                            application_id = '39dl4dDJGdjgud8', 
                            application_name = 'parking', 
                            assigned_org_id = 'as9f9adfDFwEE9', 
                            published = 'no', 
                            description = 'An application to submit parking requests', 
                            category = 'citizen-facing', 
                            icon_url = 'https://storage.googleapis.com/agilicus/logo.svg', 
                            default_role_name = 'self', 
                            default_role_id = 'as0Z6fXFsl23', ), )
                    ], 
                limit = 56
            )
        else :
            return ListApplicationSummaryResponse(
                application_summaries = [
                    agilicus_api.models.application_summary.ApplicationSummary(
                        status = agilicus_api.models.application_summary_status.ApplicationSummaryStatus(
                            application_id = '39dl4dDJGdjgud8', 
                            application_name = 'parking', 
                            assigned_org_id = 'as9f9adfDFwEE9', 
                            published = 'no', 
                            description = 'An application to submit parking requests', 
                            category = 'citizen-facing', 
                            icon_url = 'https://storage.googleapis.com/agilicus/logo.svg', 
                            default_role_name = 'self', 
                            default_role_id = 'as0Z6fXFsl23', ), )
                    ],
                limit = 56,
        )

    def testListApplicationSummaryResponse(self):
        """Test ListApplicationSummaryResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
