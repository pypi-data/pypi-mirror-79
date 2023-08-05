# coding: utf-8

import pprint
import re

import six





class AccessPassword:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'user': 'str',
        'password': 'str'
    }

    attribute_map = {
        'name': 'name',
        'user': 'user',
        'password': 'password'
    }

    def __init__(self, name=None, user=None, password=None):
        """AccessPassword - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._user = None
        self._password = None
        self.discriminator = None

        self.name = name
        self.user = user
        self.password = password

    @property
    def name(self):
        """Gets the name of this AccessPassword.

        授权名称。

        :return: The name of this AccessPassword.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AccessPassword.

        授权名称。

        :param name: The name of this AccessPassword.
        :type: str
        """
        self._name = name

    @property
    def user(self):
        """Gets the user of this AccessPassword.

        仓库用户名。

        :return: The user of this AccessPassword.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this AccessPassword.

        仓库用户名。

        :param user: The user of this AccessPassword.
        :type: str
        """
        self._user = user

    @property
    def password(self):
        """Gets the password of this AccessPassword.

        仓库密码。

        :return: The password of this AccessPassword.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this AccessPassword.

        仓库密码。

        :param password: The password of this AccessPassword.
        :type: str
        """
        self._password = password

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
        if not isinstance(other, AccessPassword):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
