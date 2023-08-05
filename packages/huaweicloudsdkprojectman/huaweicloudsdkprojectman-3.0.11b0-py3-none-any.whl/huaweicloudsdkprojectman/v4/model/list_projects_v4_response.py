# coding: utf-8

import pprint
import re

import six


from huaweicloudsdkcore.sdk_response import SdkResponse


class ListProjectsV4Response(SdkResponse):


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'projects': 'list[ListProjectsV4ResponseBodyProjects]',
        'total': 'int'
    }

    attribute_map = {
        'projects': 'projects',
        'total': 'total'
    }

    def __init__(self, projects=None, total=None):
        """ListProjectsV4Response - a model defined in huaweicloud sdk"""
        
        super().__init__()

        self._projects = None
        self._total = None
        self.discriminator = None

        if projects is not None:
            self.projects = projects
        if total is not None:
            self.total = total

    @property
    def projects(self):
        """Gets the projects of this ListProjectsV4Response.

        项目信息列表

        :return: The projects of this ListProjectsV4Response.
        :rtype: list[ListProjectsV4ResponseBodyProjects]
        """
        return self._projects

    @projects.setter
    def projects(self, projects):
        """Sets the projects of this ListProjectsV4Response.

        项目信息列表

        :param projects: The projects of this ListProjectsV4Response.
        :type: list[ListProjectsV4ResponseBodyProjects]
        """
        self._projects = projects

    @property
    def total(self):
        """Gets the total of this ListProjectsV4Response.

        项目总数

        :return: The total of this ListProjectsV4Response.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ListProjectsV4Response.

        项目总数

        :param total: The total of this ListProjectsV4Response.
        :type: int
        """
        self._total = total

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
        if not isinstance(other, ListProjectsV4Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
