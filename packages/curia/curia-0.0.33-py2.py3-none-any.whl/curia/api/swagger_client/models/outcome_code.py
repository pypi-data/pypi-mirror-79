# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class OutcomeCode(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'outcome_query_id': 'str',
        'project_id': 'str',
        'code_id': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'outcome_query_id': 'outcomeQueryId',
        'project_id': 'projectId',
        'code_id': 'codeId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, outcome_query_id=None, project_id=None, code_id=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """OutcomeCode - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._outcome_query_id = None
        self._project_id = None
        self._code_id = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.outcome_query_id = outcome_query_id
        self.project_id = project_id
        self.code_id = code_id
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this OutcomeCode.  # noqa: E501


        :return: The id of this OutcomeCode.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OutcomeCode.


        :param id: The id of this OutcomeCode.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def outcome_query_id(self):
        """Gets the outcome_query_id of this OutcomeCode.  # noqa: E501


        :return: The outcome_query_id of this OutcomeCode.  # noqa: E501
        :rtype: str
        """
        return self._outcome_query_id

    @outcome_query_id.setter
    def outcome_query_id(self, outcome_query_id):
        """Sets the outcome_query_id of this OutcomeCode.


        :param outcome_query_id: The outcome_query_id of this OutcomeCode.  # noqa: E501
        :type: str
        """
        if outcome_query_id is None:
            raise ValueError("Invalid value for `outcome_query_id`, must not be `None`")  # noqa: E501

        self._outcome_query_id = outcome_query_id

    @property
    def project_id(self):
        """Gets the project_id of this OutcomeCode.  # noqa: E501


        :return: The project_id of this OutcomeCode.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this OutcomeCode.


        :param project_id: The project_id of this OutcomeCode.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def code_id(self):
        """Gets the code_id of this OutcomeCode.  # noqa: E501


        :return: The code_id of this OutcomeCode.  # noqa: E501
        :rtype: str
        """
        return self._code_id

    @code_id.setter
    def code_id(self, code_id):
        """Sets the code_id of this OutcomeCode.


        :param code_id: The code_id of this OutcomeCode.  # noqa: E501
        :type: str
        """
        if code_id is None:
            raise ValueError("Invalid value for `code_id`, must not be `None`")  # noqa: E501

        self._code_id = code_id

    @property
    def created_at(self):
        """Gets the created_at of this OutcomeCode.  # noqa: E501


        :return: The created_at of this OutcomeCode.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this OutcomeCode.


        :param created_at: The created_at of this OutcomeCode.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this OutcomeCode.  # noqa: E501


        :return: The updated_at of this OutcomeCode.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this OutcomeCode.


        :param updated_at: The updated_at of this OutcomeCode.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this OutcomeCode.  # noqa: E501


        :return: The version of this OutcomeCode.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this OutcomeCode.


        :param version: The version of this OutcomeCode.  # noqa: E501
        :type: float
        """

        self._version = version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(OutcomeCode, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OutcomeCode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
