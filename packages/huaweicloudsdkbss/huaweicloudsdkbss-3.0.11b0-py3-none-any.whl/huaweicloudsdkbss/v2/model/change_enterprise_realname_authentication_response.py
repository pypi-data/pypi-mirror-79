# coding: utf-8

import pprint
import re

import six


from huaweicloudsdkcore.sdk_response import SdkResponse


class ChangeEnterpriseRealnameAuthenticationResponse(SdkResponse):


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'is_review': 'int'
    }

    attribute_map = {
        'is_review': 'is_review'
    }

    def __init__(self, is_review=None):
        """ChangeEnterpriseRealnameAuthenticationResponse - a model defined in huaweicloud sdk"""
        
        super().__init__()

        self._is_review = None
        self.discriminator = None

        if is_review is not None:
            self.is_review = is_review

    @property
    def is_review(self):
        """Gets the is_review of this ChangeEnterpriseRealnameAuthenticationResponse.

        |参数名称：是否需要转人工审核，只有状态码为200才返回该参数：0：不需要1：需要| |参数的约束及描述：是否需要转人工审核，只有状态码为200才返回该参数：0：不需要1：需要|

        :return: The is_review of this ChangeEnterpriseRealnameAuthenticationResponse.
        :rtype: int
        """
        return self._is_review

    @is_review.setter
    def is_review(self, is_review):
        """Sets the is_review of this ChangeEnterpriseRealnameAuthenticationResponse.

        |参数名称：是否需要转人工审核，只有状态码为200才返回该参数：0：不需要1：需要| |参数的约束及描述：是否需要转人工审核，只有状态码为200才返回该参数：0：不需要1：需要|

        :param is_review: The is_review of this ChangeEnterpriseRealnameAuthenticationResponse.
        :type: int
        """
        self._is_review = is_review

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
        if not isinstance(other, ChangeEnterpriseRealnameAuthenticationResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
