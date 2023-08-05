# coding: utf-8

import pprint
import re

import six





class GlanceCreateTagRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'image_id': 'str',
        'tag': 'str'
    }

    attribute_map = {
        'image_id': 'image_id',
        'tag': 'tag'
    }

    def __init__(self, image_id=None, tag=None):
        """GlanceCreateTagRequest - a model defined in huaweicloud sdk"""
        
        

        self._image_id = None
        self._tag = None
        self.discriminator = None

        self.image_id = image_id
        self.tag = tag

    @property
    def image_id(self):
        """Gets the image_id of this GlanceCreateTagRequest.


        :return: The image_id of this GlanceCreateTagRequest.
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this GlanceCreateTagRequest.


        :param image_id: The image_id of this GlanceCreateTagRequest.
        :type: str
        """
        self._image_id = image_id

    @property
    def tag(self):
        """Gets the tag of this GlanceCreateTagRequest.


        :return: The tag of this GlanceCreateTagRequest.
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this GlanceCreateTagRequest.


        :param tag: The tag of this GlanceCreateTagRequest.
        :type: str
        """
        self._tag = tag

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
        if not isinstance(other, GlanceCreateTagRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
