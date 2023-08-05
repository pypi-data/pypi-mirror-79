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
from agilicus_api.models.list_tokens_response import ListTokensResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListTokensResponse(unittest.TestCase):
    """ListTokensResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListTokensResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_tokens_response.ListTokensResponse()  # noqa: E501
        if include_optional :
            return ListTokensResponse(
                tokens = [
                    agilicus_api.models.token.Token(
                        sub = '123', 
                        sub_email = 'foo@example.com', 
                        org = '123', 
                        root_org = '123', 
                        roles = {"app-1":["viewer"],"app-2":["owner"]}, 
                        jti = '123', 
                        iat = '0', 
                        exp = '0', 
                        hosts = [
                            agilicus_api.models.host_permissions.HostPermissions(
                                upstream_host = '0', 
                                app_id = '123', 
                                admin_org_id = '123', 
                                allowed_list = [
                                    agilicus_api.models.rendered_rule.RenderedRule(
                                        methods = [
                                            'get'
                                            ], 
                                        paths = [
                                            '0'
                                            ], 
                                        query_parameters = [
                                            agilicus_api.models.rendered_query_parameter.RenderedQueryParameter(
                                                name = '0', 
                                                exact_match = '0', )
                                            ], 
                                        body = agilicus_api.models.rendered_rule_body.RenderedRuleBody(
                                            json = [
                                                agilicus_api.models.json_body_constraint.JSONBodyConstraint(
                                                    name = '0', 
                                                    exact_match = '0', 
                                                    match_type = 'string', 
                                                    pointer = '/foo/0/a~1b/2', )
                                                ], ), )
                                    ], )
                            ], 
                        aud = [
                            '0'
                            ], 
                        session = '123', 
                        scopes = [
                            'urn:agilicus:users:owner'
                            ], )
                    ], 
                limit = 56
            )
        else :
            return ListTokensResponse(
                limit = 56,
        )

    def testListTokensResponse(self):
        """Test ListTokensResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
