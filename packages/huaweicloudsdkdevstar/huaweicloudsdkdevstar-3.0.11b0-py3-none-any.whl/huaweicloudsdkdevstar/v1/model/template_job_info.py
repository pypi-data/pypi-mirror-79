# coding: utf-8

import pprint
import re

import six





class TemplateJobInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'application_name': 'str',
        'template_id': 'str',
        'repo_type': 'int',
        'properties': 'object',
        'repo_info': 'RepositoryInfo'
    }

    attribute_map = {
        'application_name': 'application_name',
        'template_id': 'template_id',
        'repo_type': 'repo_type',
        'properties': 'properties',
        'repo_info': 'repo_info'
    }

    def __init__(self, application_name=None, template_id=None, repo_type=None, properties=None, repo_info=None):
        """TemplateJobInfo - a model defined in huaweicloud sdk"""
        
        

        self._application_name = None
        self._template_id = None
        self._repo_type = None
        self._properties = None
        self._repo_info = None
        self.discriminator = None

        if application_name is not None:
            self.application_name = application_name
        self.template_id = template_id
        if repo_type is not None:
            self.repo_type = repo_type
        if properties is not None:
            self.properties = properties
        if repo_info is not None:
            self.repo_info = repo_info

    @property
    def application_name(self):
        """Gets the application_name of this TemplateJobInfo.

        应用名称

        :return: The application_name of this TemplateJobInfo.
        :rtype: str
        """
        return self._application_name

    @application_name.setter
    def application_name(self, application_name):
        """Sets the application_name of this TemplateJobInfo.

        应用名称

        :param application_name: The application_name of this TemplateJobInfo.
        :type: str
        """
        self._application_name = application_name

    @property
    def template_id(self):
        """Gets the template_id of this TemplateJobInfo.

        任务依赖的模板id

        :return: The template_id of this TemplateJobInfo.
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this TemplateJobInfo.

        任务依赖的模板id

        :param template_id: The template_id of this TemplateJobInfo.
        :type: str
        """
        self._template_id = template_id

    @property
    def repo_type(self):
        """Gets the repo_type of this TemplateJobInfo.

        应用代码生成后的地址类型，目前支持0：codehub地址

        :return: The repo_type of this TemplateJobInfo.
        :rtype: int
        """
        return self._repo_type

    @repo_type.setter
    def repo_type(self, repo_type):
        """Sets the repo_type of this TemplateJobInfo.

        应用代码生成后的地址类型，目前支持0：codehub地址

        :param repo_type: The repo_type of this TemplateJobInfo.
        :type: int
        """
        self._repo_type = repo_type

    @property
    def properties(self):
        """Gets the properties of this TemplateJobInfo.

        应用的动态参数json

        :return: The properties of this TemplateJobInfo.
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this TemplateJobInfo.

        应用的动态参数json

        :param properties: The properties of this TemplateJobInfo.
        :type: object
        """
        self._properties = properties

    @property
    def repo_info(self):
        """Gets the repo_info of this TemplateJobInfo.


        :return: The repo_info of this TemplateJobInfo.
        :rtype: RepositoryInfo
        """
        return self._repo_info

    @repo_info.setter
    def repo_info(self, repo_info):
        """Sets the repo_info of this TemplateJobInfo.


        :param repo_info: The repo_info of this TemplateJobInfo.
        :type: RepositoryInfo
        """
        self._repo_info = repo_info

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
        if not isinstance(other, TemplateJobInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
