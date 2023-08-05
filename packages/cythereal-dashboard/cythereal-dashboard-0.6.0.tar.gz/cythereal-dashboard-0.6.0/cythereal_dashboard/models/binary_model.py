# coding: utf-8

"""
    Cythereal Dashboard API

     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/alerts` endpoint should return a response object with `data.alerts`. This property SHOULD  contain a list of the returned objects. For the `/alerts` endpoint, the `data.alerts` property contains a list of MagicAlerts objects. See the `/alerts` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class BinaryModel(object):
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
        'sha1': 'Sha1',
        'md5': 'str',
        'sha256': 'str',
        'sha512': 'str',
        'unpacked_sha1': 'str',
        'object_class': 'str',
        'file_type': 'str',
        'upload_timestamp': 'Timestamp',
        'first_seen': 'Timestamp',
        'num_matches': 'int',
        'num_sim_pack_sim_pay': 'int',
        'num_sim_pack_diff_pay': 'int',
        'num_diff_pack_sim_pay': 'int',
        'categories': 'Categories',
        'investigations': 'list[str]',
        'tokens': 'list[str]',
        'avlabels': 'list[str]',
        'packed_campaign_size': 'int',
        'payload_campaign_size': 'int',
        'yara_id': 'YaraId',
        'yara_id_unpacked': 'YaraId',
        'color': 'Color'
    }

    attribute_map = {
        'sha1': 'sha1',
        'md5': 'md5',
        'sha256': 'sha256',
        'sha512': 'sha512',
        'unpacked_sha1': 'unpacked_sha1',
        'object_class': 'object_class',
        'file_type': 'file_type',
        'upload_timestamp': 'upload_timestamp',
        'first_seen': 'first_seen',
        'num_matches': 'num_matches',
        'num_sim_pack_sim_pay': 'num_sim_pack_sim_pay',
        'num_sim_pack_diff_pay': 'num_sim_pack_diff_pay',
        'num_diff_pack_sim_pay': 'num_diff_pack_sim_pay',
        'categories': 'categories',
        'investigations': 'investigations',
        'tokens': 'tokens',
        'avlabels': 'avlabels',
        'packed_campaign_size': 'packed_campaign_size',
        'payload_campaign_size': 'payload_campaign_size',
        'yara_id': 'yara_id',
        'yara_id_unpacked': 'yara_id_unpacked',
        'color': 'color'
    }

    def __init__(self, sha1=None, md5=None, sha256=None, sha512=None, unpacked_sha1=None, object_class=None, file_type=None, upload_timestamp=None, first_seen=None, num_matches=None, num_sim_pack_sim_pay=None, num_sim_pack_diff_pay=None, num_diff_pack_sim_pay=None, categories=None, investigations=None, tokens=None, avlabels=None, packed_campaign_size=None, payload_campaign_size=None, yara_id=None, yara_id_unpacked=None, color=None):  # noqa: E501
        """BinaryModel - a model defined in Swagger"""  # noqa: E501

        self._sha1 = None
        self._md5 = None
        self._sha256 = None
        self._sha512 = None
        self._unpacked_sha1 = None
        self._object_class = None
        self._file_type = None
        self._upload_timestamp = None
        self._first_seen = None
        self._num_matches = None
        self._num_sim_pack_sim_pay = None
        self._num_sim_pack_diff_pay = None
        self._num_diff_pack_sim_pay = None
        self._categories = None
        self._investigations = None
        self._tokens = None
        self._avlabels = None
        self._packed_campaign_size = None
        self._payload_campaign_size = None
        self._yara_id = None
        self._yara_id_unpacked = None
        self._color = None
        self.discriminator = None

        if sha1 is not None:
            self.sha1 = sha1
        if md5 is not None:
            self.md5 = md5
        if sha256 is not None:
            self.sha256 = sha256
        if sha512 is not None:
            self.sha512 = sha512
        if unpacked_sha1 is not None:
            self.unpacked_sha1 = unpacked_sha1
        if object_class is not None:
            self.object_class = object_class
        if file_type is not None:
            self.file_type = file_type
        if upload_timestamp is not None:
            self.upload_timestamp = upload_timestamp
        if first_seen is not None:
            self.first_seen = first_seen
        if num_matches is not None:
            self.num_matches = num_matches
        if num_sim_pack_sim_pay is not None:
            self.num_sim_pack_sim_pay = num_sim_pack_sim_pay
        if num_sim_pack_diff_pay is not None:
            self.num_sim_pack_diff_pay = num_sim_pack_diff_pay
        if num_diff_pack_sim_pay is not None:
            self.num_diff_pack_sim_pay = num_diff_pack_sim_pay
        if categories is not None:
            self.categories = categories
        if investigations is not None:
            self.investigations = investigations
        if tokens is not None:
            self.tokens = tokens
        if avlabels is not None:
            self.avlabels = avlabels
        if packed_campaign_size is not None:
            self.packed_campaign_size = packed_campaign_size
        if payload_campaign_size is not None:
            self.payload_campaign_size = payload_campaign_size
        if yara_id is not None:
            self.yara_id = yara_id
        if yara_id_unpacked is not None:
            self.yara_id_unpacked = yara_id_unpacked
        if color is not None:
            self.color = color

    @property
    def sha1(self):
        """Gets the sha1 of this BinaryModel.  # noqa: E501


        :return: The sha1 of this BinaryModel.  # noqa: E501
        :rtype: Sha1
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1):
        """Sets the sha1 of this BinaryModel.


        :param sha1: The sha1 of this BinaryModel.  # noqa: E501
        :type: Sha1
        """

        self._sha1 = sha1

    @property
    def md5(self):
        """Gets the md5 of this BinaryModel.  # noqa: E501

        A unique md5 representation of the file  # noqa: E501

        :return: The md5 of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this BinaryModel.

        A unique md5 representation of the file  # noqa: E501

        :param md5: The md5 of this BinaryModel.  # noqa: E501
        :type: str
        """
        if md5 is not None and not re.search(r'[a-fA-F0-9]{32}', md5):  # noqa: E501
            raise ValueError(r"Invalid value for `md5`, must be a follow pattern or equal to `/[a-fA-F0-9]{32}/`")  # noqa: E501

        self._md5 = md5

    @property
    def sha256(self):
        """Gets the sha256 of this BinaryModel.  # noqa: E501

        A unique sha256 representation of the file  # noqa: E501

        :return: The sha256 of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """Sets the sha256 of this BinaryModel.

        A unique sha256 representation of the file  # noqa: E501

        :param sha256: The sha256 of this BinaryModel.  # noqa: E501
        :type: str
        """
        if sha256 is not None and not re.search(r'[a-fA-F0-9]{64}', sha256):  # noqa: E501
            raise ValueError(r"Invalid value for `sha256`, must be a follow pattern or equal to `/[a-fA-F0-9]{64}/`")  # noqa: E501

        self._sha256 = sha256

    @property
    def sha512(self):
        """Gets the sha512 of this BinaryModel.  # noqa: E501

        A unique sha512 representation of the file.  # noqa: E501

        :return: The sha512 of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._sha512

    @sha512.setter
    def sha512(self, sha512):
        """Sets the sha512 of this BinaryModel.

        A unique sha512 representation of the file.  # noqa: E501

        :param sha512: The sha512 of this BinaryModel.  # noqa: E501
        :type: str
        """
        if sha512 is not None and not re.search(r'[a-fA-F0-9]{128}', sha512):  # noqa: E501
            raise ValueError(r"Invalid value for `sha512`, must be a follow pattern or equal to `/[a-fA-F0-9]{128}/`")  # noqa: E501

        self._sha512 = sha512

    @property
    def unpacked_sha1(self):
        """Gets the unpacked_sha1 of this BinaryModel.  # noqa: E501

        A unique sha1 representation of the file produced by unpacking this file. If one exists, otherwise empty.  # noqa: E501

        :return: The unpacked_sha1 of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._unpacked_sha1

    @unpacked_sha1.setter
    def unpacked_sha1(self, unpacked_sha1):
        """Sets the unpacked_sha1 of this BinaryModel.

        A unique sha1 representation of the file produced by unpacking this file. If one exists, otherwise empty.  # noqa: E501

        :param unpacked_sha1: The unpacked_sha1 of this BinaryModel.  # noqa: E501
        :type: str
        """

        self._unpacked_sha1 = unpacked_sha1

    @property
    def object_class(self):
        """Gets the object_class of this BinaryModel.  # noqa: E501

        Unique in-house class type of the file.  # noqa: E501

        :return: The object_class of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._object_class

    @object_class.setter
    def object_class(self, object_class):
        """Sets the object_class of this BinaryModel.

        Unique in-house class type of the file.  # noqa: E501

        :param object_class: The object_class of this BinaryModel.  # noqa: E501
        :type: str
        """

        self._object_class = object_class

    @property
    def file_type(self):
        """Gets the file_type of this BinaryModel.  # noqa: E501

        A more precise description of the file. The result of running the `file` command on the command line  # noqa: E501

        :return: The file_type of this BinaryModel.  # noqa: E501
        :rtype: str
        """
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        """Sets the file_type of this BinaryModel.

        A more precise description of the file. The result of running the `file` command on the command line  # noqa: E501

        :param file_type: The file_type of this BinaryModel.  # noqa: E501
        :type: str
        """

        self._file_type = file_type

    @property
    def upload_timestamp(self):
        """Gets the upload_timestamp of this BinaryModel.  # noqa: E501


        :return: The upload_timestamp of this BinaryModel.  # noqa: E501
        :rtype: Timestamp
        """
        return self._upload_timestamp

    @upload_timestamp.setter
    def upload_timestamp(self, upload_timestamp):
        """Sets the upload_timestamp of this BinaryModel.


        :param upload_timestamp: The upload_timestamp of this BinaryModel.  # noqa: E501
        :type: Timestamp
        """

        self._upload_timestamp = upload_timestamp

    @property
    def first_seen(self):
        """Gets the first_seen of this BinaryModel.  # noqa: E501


        :return: The first_seen of this BinaryModel.  # noqa: E501
        :rtype: Timestamp
        """
        return self._first_seen

    @first_seen.setter
    def first_seen(self, first_seen):
        """Sets the first_seen of this BinaryModel.


        :param first_seen: The first_seen of this BinaryModel.  # noqa: E501
        :type: Timestamp
        """

        self._first_seen = first_seen

    @property
    def num_matches(self):
        """Gets the num_matches of this BinaryModel.  # noqa: E501

        The number of similar files to this one.  # noqa: E501

        :return: The num_matches of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._num_matches

    @num_matches.setter
    def num_matches(self, num_matches):
        """Sets the num_matches of this BinaryModel.

        The number of similar files to this one.  # noqa: E501

        :param num_matches: The num_matches of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._num_matches = num_matches

    @property
    def num_sim_pack_sim_pay(self):
        """Gets the num_sim_pack_sim_pay of this BinaryModel.  # noqa: E501

        The number of matches with a similar packer and a similar payload  # noqa: E501

        :return: The num_sim_pack_sim_pay of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._num_sim_pack_sim_pay

    @num_sim_pack_sim_pay.setter
    def num_sim_pack_sim_pay(self, num_sim_pack_sim_pay):
        """Sets the num_sim_pack_sim_pay of this BinaryModel.

        The number of matches with a similar packer and a similar payload  # noqa: E501

        :param num_sim_pack_sim_pay: The num_sim_pack_sim_pay of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._num_sim_pack_sim_pay = num_sim_pack_sim_pay

    @property
    def num_sim_pack_diff_pay(self):
        """Gets the num_sim_pack_diff_pay of this BinaryModel.  # noqa: E501

        The number of matches with a similar packer, but a different payload  # noqa: E501

        :return: The num_sim_pack_diff_pay of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._num_sim_pack_diff_pay

    @num_sim_pack_diff_pay.setter
    def num_sim_pack_diff_pay(self, num_sim_pack_diff_pay):
        """Sets the num_sim_pack_diff_pay of this BinaryModel.

        The number of matches with a similar packer, but a different payload  # noqa: E501

        :param num_sim_pack_diff_pay: The num_sim_pack_diff_pay of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._num_sim_pack_diff_pay = num_sim_pack_diff_pay

    @property
    def num_diff_pack_sim_pay(self):
        """Gets the num_diff_pack_sim_pay of this BinaryModel.  # noqa: E501

        The number of matches with a different packer, but a similar payload.  # noqa: E501

        :return: The num_diff_pack_sim_pay of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._num_diff_pack_sim_pay

    @num_diff_pack_sim_pay.setter
    def num_diff_pack_sim_pay(self, num_diff_pack_sim_pay):
        """Sets the num_diff_pack_sim_pay of this BinaryModel.

        The number of matches with a different packer, but a similar payload.  # noqa: E501

        :param num_diff_pack_sim_pay: The num_diff_pack_sim_pay of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._num_diff_pack_sim_pay = num_diff_pack_sim_pay

    @property
    def categories(self):
        """Gets the categories of this BinaryModel.  # noqa: E501


        :return: The categories of this BinaryModel.  # noqa: E501
        :rtype: Categories
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this BinaryModel.


        :param categories: The categories of this BinaryModel.  # noqa: E501
        :type: Categories
        """

        self._categories = categories

    @property
    def investigations(self):
        """Gets the investigations of this BinaryModel.  # noqa: E501

        A list of the investigations that this file belongs to.  # noqa: E501

        :return: The investigations of this BinaryModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._investigations

    @investigations.setter
    def investigations(self, investigations):
        """Sets the investigations of this BinaryModel.

        A list of the investigations that this file belongs to.  # noqa: E501

        :param investigations: The investigations of this BinaryModel.  # noqa: E501
        :type: list[str]
        """

        self._investigations = investigations

    @property
    def tokens(self):
        """Gets the tokens of this BinaryModel.  # noqa: E501

        A list of tokens associated with this file.  # noqa: E501

        :return: The tokens of this BinaryModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        """Sets the tokens of this BinaryModel.

        A list of tokens associated with this file.  # noqa: E501

        :param tokens: The tokens of this BinaryModel.  # noqa: E501
        :type: list[str]
        """

        self._tokens = tokens

    @property
    def avlabels(self):
        """Gets the avlabels of this BinaryModel.  # noqa: E501

        A list of avlabels associated with this file.  # noqa: E501

        :return: The avlabels of this BinaryModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._avlabels

    @avlabels.setter
    def avlabels(self, avlabels):
        """Sets the avlabels of this BinaryModel.

        A list of avlabels associated with this file.  # noqa: E501

        :param avlabels: The avlabels of this BinaryModel.  # noqa: E501
        :type: list[str]
        """

        self._avlabels = avlabels

    @property
    def packed_campaign_size(self):
        """Gets the packed_campaign_size of this BinaryModel.  # noqa: E501

        The size of the campaign that the packed binary belongs to  # noqa: E501

        :return: The packed_campaign_size of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._packed_campaign_size

    @packed_campaign_size.setter
    def packed_campaign_size(self, packed_campaign_size):
        """Sets the packed_campaign_size of this BinaryModel.

        The size of the campaign that the packed binary belongs to  # noqa: E501

        :param packed_campaign_size: The packed_campaign_size of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._packed_campaign_size = packed_campaign_size

    @property
    def payload_campaign_size(self):
        """Gets the payload_campaign_size of this BinaryModel.  # noqa: E501

        The size of the campaign that the payload binary belongs to, if one exists  # noqa: E501

        :return: The payload_campaign_size of this BinaryModel.  # noqa: E501
        :rtype: int
        """
        return self._payload_campaign_size

    @payload_campaign_size.setter
    def payload_campaign_size(self, payload_campaign_size):
        """Sets the payload_campaign_size of this BinaryModel.

        The size of the campaign that the payload binary belongs to, if one exists  # noqa: E501

        :param payload_campaign_size: The payload_campaign_size of this BinaryModel.  # noqa: E501
        :type: int
        """

        self._payload_campaign_size = payload_campaign_size

    @property
    def yara_id(self):
        """Gets the yara_id of this BinaryModel.  # noqa: E501


        :return: The yara_id of this BinaryModel.  # noqa: E501
        :rtype: YaraId
        """
        return self._yara_id

    @yara_id.setter
    def yara_id(self, yara_id):
        """Sets the yara_id of this BinaryModel.


        :param yara_id: The yara_id of this BinaryModel.  # noqa: E501
        :type: YaraId
        """

        self._yara_id = yara_id

    @property
    def yara_id_unpacked(self):
        """Gets the yara_id_unpacked of this BinaryModel.  # noqa: E501


        :return: The yara_id_unpacked of this BinaryModel.  # noqa: E501
        :rtype: YaraId
        """
        return self._yara_id_unpacked

    @yara_id_unpacked.setter
    def yara_id_unpacked(self, yara_id_unpacked):
        """Sets the yara_id_unpacked of this BinaryModel.


        :param yara_id_unpacked: The yara_id_unpacked of this BinaryModel.  # noqa: E501
        :type: YaraId
        """

        self._yara_id_unpacked = yara_id_unpacked

    @property
    def color(self):
        """Gets the color of this BinaryModel.  # noqa: E501


        :return: The color of this BinaryModel.  # noqa: E501
        :rtype: Color
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this BinaryModel.


        :param color: The color of this BinaryModel.  # noqa: E501
        :type: Color
        """

        self._color = color

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
        if issubclass(BinaryModel, dict):
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
        if not isinstance(other, BinaryModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
