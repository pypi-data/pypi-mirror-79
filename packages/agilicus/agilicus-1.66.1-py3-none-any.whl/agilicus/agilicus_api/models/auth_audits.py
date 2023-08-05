# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.09.08
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class AuthAudits(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'user_id': 'str',
        'upstream_user_id': 'str',
        'org_id': 'str',
        'org_name': 'str',
        'time': 'datetime',
        'event': 'str',
        'source_ip': 'str',
        'token_id': 'str',
        'trace_id': 'str',
        'session': 'str',
        'issuer': 'str',
        'client_id': 'str',
        'application_name': 'str',
        'login_org_id': 'str',
        'login_org_name': 'str',
        'upstream_idp': 'str',
        'stage': 'str',
        'user_agent': 'str'
    }

    attribute_map = {
        'user_id': 'user_id',
        'upstream_user_id': 'upstream_user_id',
        'org_id': 'org_id',
        'org_name': 'org_name',
        'time': 'time',
        'event': 'event',
        'source_ip': 'source_ip',
        'token_id': 'token_id',
        'trace_id': 'trace_id',
        'session': 'session',
        'issuer': 'issuer',
        'client_id': 'client_id',
        'application_name': 'application_name',
        'login_org_id': 'login_org_id',
        'login_org_name': 'login_org_name',
        'upstream_idp': 'upstream_idp',
        'stage': 'stage',
        'user_agent': 'user_agent'
    }

    def __init__(self, user_id=None, upstream_user_id=None, org_id=None, org_name=None, time=None, event=None, source_ip=None, token_id=None, trace_id=None, session=None, issuer=None, client_id=None, application_name=None, login_org_id=None, login_org_name=None, upstream_idp=None, stage=None, user_agent=None, local_vars_configuration=None):  # noqa: E501
        """AuthAudits - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._user_id = None
        self._upstream_user_id = None
        self._org_id = None
        self._org_name = None
        self._time = None
        self._event = None
        self._source_ip = None
        self._token_id = None
        self._trace_id = None
        self._session = None
        self._issuer = None
        self._client_id = None
        self._application_name = None
        self._login_org_id = None
        self._login_org_name = None
        self._upstream_idp = None
        self._stage = None
        self._user_agent = None
        self.discriminator = None

        if user_id is not None:
            self.user_id = user_id
        if upstream_user_id is not None:
            self.upstream_user_id = upstream_user_id
        if org_id is not None:
            self.org_id = org_id
        if org_name is not None:
            self.org_name = org_name
        if time is not None:
            self.time = time
        if event is not None:
            self.event = event
        if source_ip is not None:
            self.source_ip = source_ip
        if token_id is not None:
            self.token_id = token_id
        if trace_id is not None:
            self.trace_id = trace_id
        if session is not None:
            self.session = session
        if issuer is not None:
            self.issuer = issuer
        if client_id is not None:
            self.client_id = client_id
        if application_name is not None:
            self.application_name = application_name
        if login_org_id is not None:
            self.login_org_id = login_org_id
        if login_org_name is not None:
            self.login_org_name = login_org_name
        if upstream_idp is not None:
            self.upstream_idp = upstream_idp
        if stage is not None:
            self.stage = stage
        if user_agent is not None:
            self.user_agent = user_agent

    @property
    def user_id(self):
        """Gets the user_id of this AuthAudits.  # noqa: E501

        The system-local id of the user performing the action.  # noqa: E501

        :return: The user_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this AuthAudits.

        The system-local id of the user performing the action.  # noqa: E501

        :param user_id: The user_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def upstream_user_id(self):
        """Gets the upstream_user_id of this AuthAudits.  # noqa: E501

        The id of the user in the upstream system, if available.  # noqa: E501

        :return: The upstream_user_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._upstream_user_id

    @upstream_user_id.setter
    def upstream_user_id(self, upstream_user_id):
        """Sets the upstream_user_id of this AuthAudits.

        The id of the user in the upstream system, if available.  # noqa: E501

        :param upstream_user_id: The upstream_user_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._upstream_user_id = upstream_user_id

    @property
    def org_id(self):
        """Gets the org_id of this AuthAudits.  # noqa: E501

        The id of the organisation of the issuer against which the user is authenticating.   # noqa: E501

        :return: The org_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this AuthAudits.

        The id of the organisation of the issuer against which the user is authenticating.   # noqa: E501

        :param org_id: The org_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def org_name(self):
        """Gets the org_name of this AuthAudits.  # noqa: E501

        The name of the organisation of the issuer against which the user is authenticating.   # noqa: E501

        :return: The org_name of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._org_name

    @org_name.setter
    def org_name(self, org_name):
        """Sets the org_name of this AuthAudits.

        The name of the organisation of the issuer against which the user is authenticating.   # noqa: E501

        :param org_name: The org_name of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._org_name = org_name

    @property
    def time(self):
        """Gets the time of this AuthAudits.  # noqa: E501

        the time at which the record was generated.  # noqa: E501

        :return: The time of this AuthAudits.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this AuthAudits.

        the time at which the record was generated.  # noqa: E501

        :param time: The time of this AuthAudits.  # noqa: E501
        :type: datetime
        """

        self._time = time

    @property
    def event(self):
        """Gets the event of this AuthAudits.  # noqa: E501

        The event which generated the record. The meaning of the event depends on the stage where it occured.   # noqa: E501

        :return: The event of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this AuthAudits.

        The event which generated the record. The meaning of the event depends on the stage where it occured.   # noqa: E501

        :param event: The event of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._event = event

    @property
    def source_ip(self):
        """Gets the source_ip of this AuthAudits.  # noqa: E501

        The IP address of the host initiating the action  # noqa: E501

        :return: The source_ip of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._source_ip

    @source_ip.setter
    def source_ip(self, source_ip):
        """Sets the source_ip of this AuthAudits.

        The IP address of the host initiating the action  # noqa: E501

        :param source_ip: The source_ip of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._source_ip = source_ip

    @property
    def token_id(self):
        """Gets the token_id of this AuthAudits.  # noqa: E501

        The id of the token issued or reissued as part of the authentication.  # noqa: E501

        :return: The token_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._token_id

    @token_id.setter
    def token_id(self, token_id):
        """Sets the token_id of this AuthAudits.

        The id of the token issued or reissued as part of the authentication.  # noqa: E501

        :param token_id: The token_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._token_id = token_id

    @property
    def trace_id(self):
        """Gets the trace_id of this AuthAudits.  # noqa: E501

        A correlation ID associated with requests related to this event  # noqa: E501

        :return: The trace_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._trace_id

    @trace_id.setter
    def trace_id(self, trace_id):
        """Sets the trace_id of this AuthAudits.

        A correlation ID associated with requests related to this event  # noqa: E501

        :param trace_id: The trace_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._trace_id = trace_id

    @property
    def session(self):
        """Gets the session of this AuthAudits.  # noqa: E501

        The session associated with tokens related to this event. This can be used to tie the actions undertaking by requests bearing tokens with the same session back to the authentication events which created the tokens.   # noqa: E501

        :return: The session of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._session

    @session.setter
    def session(self, session):
        """Sets the session of this AuthAudits.

        The session associated with tokens related to this event. This can be used to tie the actions undertaking by requests bearing tokens with the same session back to the authentication events which created the tokens.   # noqa: E501

        :param session: The session of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._session = session

    @property
    def issuer(self):
        """Gets the issuer of this AuthAudits.  # noqa: E501

        The issuer the user logged in to.  # noqa: E501

        :return: The issuer of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this AuthAudits.

        The issuer the user logged in to.  # noqa: E501

        :param issuer: The issuer of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._issuer = issuer

    @property
    def client_id(self):
        """Gets the client_id of this AuthAudits.  # noqa: E501

        The client id of the web application, client, etc. that the user is logging in with. Note that this is not the id of the `IssuerClient`, but rather the id presented to the authentication system to identify that client. This corresponds to `name` in the `IssuerClient`.   # noqa: E501

        :return: The client_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this AuthAudits.

        The client id of the web application, client, etc. that the user is logging in with. Note that this is not the id of the `IssuerClient`, but rather the id presented to the authentication system to identify that client. This corresponds to `name` in the `IssuerClient`.   # noqa: E501

        :param client_id: The client_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def application_name(self):
        """Gets the application_name of this AuthAudits.  # noqa: E501

        The name of the application within the system the user is logging in to.  # noqa: E501

        :return: The application_name of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._application_name

    @application_name.setter
    def application_name(self, application_name):
        """Sets the application_name of this AuthAudits.

        The name of the application within the system the user is logging in to.  # noqa: E501

        :param application_name: The application_name of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._application_name = application_name

    @property
    def login_org_id(self):
        """Gets the login_org_id of this AuthAudits.  # noqa: E501

        The id of the organisation that the user is logging in to. Note that this is disctinct from the `org_id` field, which is tied to the issuer. This id is tied to the application.   # noqa: E501

        :return: The login_org_id of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._login_org_id

    @login_org_id.setter
    def login_org_id(self, login_org_id):
        """Sets the login_org_id of this AuthAudits.

        The id of the organisation that the user is logging in to. Note that this is disctinct from the `org_id` field, which is tied to the issuer. This id is tied to the application.   # noqa: E501

        :param login_org_id: The login_org_id of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._login_org_id = login_org_id

    @property
    def login_org_name(self):
        """Gets the login_org_name of this AuthAudits.  # noqa: E501

        The name of the organisation that the user is logging in to. This corresponds to `login_org_id`.   # noqa: E501

        :return: The login_org_name of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._login_org_name

    @login_org_name.setter
    def login_org_name(self, login_org_name):
        """Sets the login_org_name of this AuthAudits.

        The name of the organisation that the user is logging in to. This corresponds to `login_org_id`.   # noqa: E501

        :param login_org_name: The login_org_name of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._login_org_name = login_org_name

    @property
    def upstream_idp(self):
        """Gets the upstream_idp of this AuthAudits.  # noqa: E501

        The name of the identity provider proving the identity of the user.   # noqa: E501

        :return: The upstream_idp of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._upstream_idp

    @upstream_idp.setter
    def upstream_idp(self, upstream_idp):
        """Sets the upstream_idp of this AuthAudits.

        The name of the identity provider proving the identity of the user.   # noqa: E501

        :param upstream_idp: The upstream_idp of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._upstream_idp = upstream_idp

    @property
    def stage(self):
        """Gets the stage of this AuthAudits.  # noqa: E501

        The stage of the login process. This identifies where in the pipeline the event was generated.   # noqa: E501

        :return: The stage of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Sets the stage of this AuthAudits.

        The stage of the login process. This identifies where in the pipeline the event was generated.   # noqa: E501

        :param stage: The stage of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._stage = stage

    @property
    def user_agent(self):
        """Gets the user_agent of this AuthAudits.  # noqa: E501

        The user agent of the client used to perform the login.   # noqa: E501

        :return: The user_agent of this AuthAudits.  # noqa: E501
        :rtype: str
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        """Sets the user_agent of this AuthAudits.

        The user agent of the client used to perform the login.   # noqa: E501

        :param user_agent: The user_agent of this AuthAudits.  # noqa: E501
        :type: str
        """

        self._user_agent = user_agent

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AuthAudits):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AuthAudits):
            return True

        return self.to_dict() != other.to_dict()
