# coding: utf-8

import pprint
import re

import six





class CreateHookRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'x_repo_auth': 'str',
        'namespace': 'str',
        'project': 'str',
        'body': 'HookCreate'
    }

    attribute_map = {
        'x_repo_auth': 'X-Repo-Auth',
        'namespace': 'namespace',
        'project': 'project',
        'body': 'body'
    }

    def __init__(self, x_repo_auth=None, namespace=None, project=None, body=None):
        """CreateHookRequest - a model defined in huaweicloud sdk"""
        
        

        self._x_repo_auth = None
        self._namespace = None
        self._project = None
        self._body = None
        self.discriminator = None

        self.x_repo_auth = x_repo_auth
        self.namespace = namespace
        self.project = project
        if body is not None:
            self.body = body

    @property
    def x_repo_auth(self):
        """Gets the x_repo_auth of this CreateHookRequest.


        :return: The x_repo_auth of this CreateHookRequest.
        :rtype: str
        """
        return self._x_repo_auth

    @x_repo_auth.setter
    def x_repo_auth(self, x_repo_auth):
        """Sets the x_repo_auth of this CreateHookRequest.


        :param x_repo_auth: The x_repo_auth of this CreateHookRequest.
        :type: str
        """
        self._x_repo_auth = x_repo_auth

    @property
    def namespace(self):
        """Gets the namespace of this CreateHookRequest.


        :return: The namespace of this CreateHookRequest.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this CreateHookRequest.


        :param namespace: The namespace of this CreateHookRequest.
        :type: str
        """
        self._namespace = namespace

    @property
    def project(self):
        """Gets the project of this CreateHookRequest.


        :return: The project of this CreateHookRequest.
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this CreateHookRequest.


        :param project: The project of this CreateHookRequest.
        :type: str
        """
        self._project = project

    @property
    def body(self):
        """Gets the body of this CreateHookRequest.


        :return: The body of this CreateHookRequest.
        :rtype: HookCreate
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this CreateHookRequest.


        :param body: The body of this CreateHookRequest.
        :type: HookCreate
        """
        self._body = body

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
        if not isinstance(other, CreateHookRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
