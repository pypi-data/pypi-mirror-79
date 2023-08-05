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


class PolicyRuleSpec(object):
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
        'action': 'str',
        'org_id': 'str',
        'priority': 'int',
        'conditions': 'list[PolicyCondition]'
    }

    attribute_map = {
        'action': 'action',
        'org_id': 'org_id',
        'priority': 'priority',
        'conditions': 'conditions'
    }

    def __init__(self, action=None, org_id=None, priority=None, conditions=None, local_vars_configuration=None):  # noqa: E501
        """PolicyRuleSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._action = None
        self._org_id = None
        self._priority = None
        self._conditions = None
        self.discriminator = None

        self.action = action
        if org_id is not None:
            self.org_id = org_id
        self.priority = priority
        self.conditions = conditions

    @property
    def action(self):
        """Gets the action of this PolicyRuleSpec.  # noqa: E501

        The action to take if the conditions are evaluated to true. Actions are case sensitive.  # noqa: E501

        :return: The action of this PolicyRuleSpec.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this PolicyRuleSpec.

        The action to take if the conditions are evaluated to true. Actions are case sensitive.  # noqa: E501

        :param action: The action of this PolicyRuleSpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and action is None:  # noqa: E501
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                action is not None and len(action) > 100):
            raise ValueError("Invalid value for `action`, length must be less than or equal to `100`")  # noqa: E501

        self._action = action

    @property
    def org_id(self):
        """Gets the org_id of this PolicyRuleSpec.  # noqa: E501

        The org id corresponding to the issuer whose policy you are updating  # noqa: E501

        :return: The org_id of this PolicyRuleSpec.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this PolicyRuleSpec.

        The org id corresponding to the issuer whose policy you are updating  # noqa: E501

        :param org_id: The org_id of this PolicyRuleSpec.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                org_id is not None and len(org_id) > 40):
            raise ValueError("Invalid value for `org_id`, length must be less than or equal to `40`")  # noqa: E501

        self._org_id = org_id

    @property
    def priority(self):
        """Gets the priority of this PolicyRuleSpec.  # noqa: E501

        The priority of this rule relative to other rules. Rules of a higher priority will be evaluated first and if the condition evaluates to true the action will be taken. 1 is the highest priority.  # noqa: E501

        :return: The priority of this PolicyRuleSpec.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this PolicyRuleSpec.

        The priority of this rule relative to other rules. Rules of a higher priority will be evaluated first and if the condition evaluates to true the action will be taken. 1 is the highest priority.  # noqa: E501

        :param priority: The priority of this PolicyRuleSpec.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and priority is None:  # noqa: E501
            raise ValueError("Invalid value for `priority`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                priority is not None and priority < 1):  # noqa: E501
            raise ValueError("Invalid value for `priority`, must be a value greater than or equal to `1`")  # noqa: E501

        self._priority = priority

    @property
    def conditions(self):
        """Gets the conditions of this PolicyRuleSpec.  # noqa: E501

        An array mapping a condition type to a condition.  # noqa: E501

        :return: The conditions of this PolicyRuleSpec.  # noqa: E501
        :rtype: list[PolicyCondition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """Sets the conditions of this PolicyRuleSpec.

        An array mapping a condition type to a condition.  # noqa: E501

        :param conditions: The conditions of this PolicyRuleSpec.  # noqa: E501
        :type: list[PolicyCondition]
        """
        if self.local_vars_configuration.client_side_validation and conditions is None:  # noqa: E501
            raise ValueError("Invalid value for `conditions`, must not be `None`")  # noqa: E501

        self._conditions = conditions

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
        if not isinstance(other, PolicyRuleSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PolicyRuleSpec):
            return True

        return self.to_dict() != other.to_dict()
