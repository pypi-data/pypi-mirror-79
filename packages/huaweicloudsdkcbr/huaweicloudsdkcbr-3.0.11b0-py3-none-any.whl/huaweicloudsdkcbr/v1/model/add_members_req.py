# coding: utf-8

import pprint
import re

import six





class AddMembersReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'members': 'list[str]'
    }

    attribute_map = {
        'members': 'members'
    }

    def __init__(self, members=None):
        """AddMembersReq - a model defined in huaweicloud sdk"""
        
        

        self._members = None
        self.discriminator = None

        self.members = members

    @property
    def members(self):
        """Gets the members of this AddMembersReq.

        列表，待添加备份共享成员的project_id。

        :return: The members of this AddMembersReq.
        :rtype: list[str]
        """
        return self._members

    @members.setter
    def members(self, members):
        """Sets the members of this AddMembersReq.

        列表，待添加备份共享成员的project_id。

        :param members: The members of this AddMembersReq.
        :type: list[str]
        """
        self._members = members

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
                if attr in self.sensitive_list:
                    result[attr] = "****"
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
        if not isinstance(other, AddMembersReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
