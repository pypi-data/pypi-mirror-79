# coding: utf-8

import pprint
import re

import six





class ListSignatureKeysBindedToApiV2Request:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'instance_id': 'str',
        'api_id': 'str',
        'sign_id': 'str',
        'sign_name': 'str',
        'env_id': 'str',
        'offset': 'int',
        'limit': 'int'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'api_id': 'api_id',
        'sign_id': 'sign_id',
        'sign_name': 'sign_name',
        'env_id': 'env_id',
        'offset': 'offset',
        'limit': 'limit'
    }

    def __init__(self, instance_id=None, api_id=None, sign_id=None, sign_name=None, env_id=None, offset=0, limit=20):
        """ListSignatureKeysBindedToApiV2Request - a model defined in huaweicloud sdk"""
        
        

        self._instance_id = None
        self._api_id = None
        self._sign_id = None
        self._sign_name = None
        self._env_id = None
        self._offset = None
        self._limit = None
        self.discriminator = None

        self.instance_id = instance_id
        self.api_id = api_id
        if sign_id is not None:
            self.sign_id = sign_id
        if sign_name is not None:
            self.sign_name = sign_name
        if env_id is not None:
            self.env_id = env_id
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit

    @property
    def instance_id(self):
        """Gets the instance_id of this ListSignatureKeysBindedToApiV2Request.


        :return: The instance_id of this ListSignatureKeysBindedToApiV2Request.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ListSignatureKeysBindedToApiV2Request.


        :param instance_id: The instance_id of this ListSignatureKeysBindedToApiV2Request.
        :type: str
        """
        self._instance_id = instance_id

    @property
    def api_id(self):
        """Gets the api_id of this ListSignatureKeysBindedToApiV2Request.


        :return: The api_id of this ListSignatureKeysBindedToApiV2Request.
        :rtype: str
        """
        return self._api_id

    @api_id.setter
    def api_id(self, api_id):
        """Sets the api_id of this ListSignatureKeysBindedToApiV2Request.


        :param api_id: The api_id of this ListSignatureKeysBindedToApiV2Request.
        :type: str
        """
        self._api_id = api_id

    @property
    def sign_id(self):
        """Gets the sign_id of this ListSignatureKeysBindedToApiV2Request.


        :return: The sign_id of this ListSignatureKeysBindedToApiV2Request.
        :rtype: str
        """
        return self._sign_id

    @sign_id.setter
    def sign_id(self, sign_id):
        """Sets the sign_id of this ListSignatureKeysBindedToApiV2Request.


        :param sign_id: The sign_id of this ListSignatureKeysBindedToApiV2Request.
        :type: str
        """
        self._sign_id = sign_id

    @property
    def sign_name(self):
        """Gets the sign_name of this ListSignatureKeysBindedToApiV2Request.


        :return: The sign_name of this ListSignatureKeysBindedToApiV2Request.
        :rtype: str
        """
        return self._sign_name

    @sign_name.setter
    def sign_name(self, sign_name):
        """Sets the sign_name of this ListSignatureKeysBindedToApiV2Request.


        :param sign_name: The sign_name of this ListSignatureKeysBindedToApiV2Request.
        :type: str
        """
        self._sign_name = sign_name

    @property
    def env_id(self):
        """Gets the env_id of this ListSignatureKeysBindedToApiV2Request.


        :return: The env_id of this ListSignatureKeysBindedToApiV2Request.
        :rtype: str
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """Sets the env_id of this ListSignatureKeysBindedToApiV2Request.


        :param env_id: The env_id of this ListSignatureKeysBindedToApiV2Request.
        :type: str
        """
        self._env_id = env_id

    @property
    def offset(self):
        """Gets the offset of this ListSignatureKeysBindedToApiV2Request.


        :return: The offset of this ListSignatureKeysBindedToApiV2Request.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListSignatureKeysBindedToApiV2Request.


        :param offset: The offset of this ListSignatureKeysBindedToApiV2Request.
        :type: int
        """
        self._offset = offset

    @property
    def limit(self):
        """Gets the limit of this ListSignatureKeysBindedToApiV2Request.


        :return: The limit of this ListSignatureKeysBindedToApiV2Request.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListSignatureKeysBindedToApiV2Request.


        :param limit: The limit of this ListSignatureKeysBindedToApiV2Request.
        :type: int
        """
        self._limit = limit

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
        if not isinstance(other, ListSignatureKeysBindedToApiV2Request):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
