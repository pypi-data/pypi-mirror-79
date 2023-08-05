# coding: utf-8

import pprint
import re

import six





class ApplyEnterpriseRealnameAuthsReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'certificate_type': 'int',
        'corp_name': 'str',
        'customer_id': 'str',
        'enterprise_person': 'EnterprisePersonNew',
        'identify_type': 'int',
        'reg_address': 'str',
        'reg_country': 'str',
        'verified_file_url': 'list[str]',
        'verified_number': 'str',
        'xaccount_type': 'str'
    }

    attribute_map = {
        'certificate_type': 'certificate_type',
        'corp_name': 'corp_name',
        'customer_id': 'customer_id',
        'enterprise_person': 'enterprise_person',
        'identify_type': 'identify_type',
        'reg_address': 'reg_address',
        'reg_country': 'reg_country',
        'verified_file_url': 'verified_file_url',
        'verified_number': 'verified_number',
        'xaccount_type': 'xaccount_type'
    }

    def __init__(self, certificate_type=None, corp_name=None, customer_id=None, enterprise_person=None, identify_type=None, reg_address=None, reg_country=None, verified_file_url=None, verified_number=None, xaccount_type=None):
        """ApplyEnterpriseRealnameAuthsReq - a model defined in huaweicloud sdk"""
        
        

        self._certificate_type = None
        self._corp_name = None
        self._customer_id = None
        self._enterprise_person = None
        self._identify_type = None
        self._reg_address = None
        self._reg_country = None
        self._verified_file_url = None
        self._verified_number = None
        self._xaccount_type = None
        self.discriminator = None

        if certificate_type is not None:
            self.certificate_type = certificate_type
        self.corp_name = corp_name
        self.customer_id = customer_id
        if enterprise_person is not None:
            self.enterprise_person = enterprise_person
        self.identify_type = identify_type
        if reg_address is not None:
            self.reg_address = reg_address
        if reg_country is not None:
            self.reg_country = reg_country
        self.verified_file_url = verified_file_url
        self.verified_number = verified_number
        self.xaccount_type = xaccount_type

    @property
    def certificate_type(self):
        """Gets the certificate_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：企业证件类型：0：企业营业执照1：事业单位法人证书2：社会团体法人登记证书3：行政执法主体资格证4：组织机构代码证99：其他| |参数的约束及描述：企业证件类型：0：企业营业执照1：事业单位法人证书2：社会团体法人登记证书3：行政执法主体资格证4：组织机构代码证99：其他|

        :return: The certificate_type of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: int
        """
        return self._certificate_type

    @certificate_type.setter
    def certificate_type(self, certificate_type):
        """Sets the certificate_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：企业证件类型：0：企业营业执照1：事业单位法人证书2：社会团体法人登记证书3：行政执法主体资格证4：组织机构代码证99：其他| |参数的约束及描述：企业证件类型：0：企业营业执照1：事业单位法人证书2：社会团体法人登记证书3：行政执法主体资格证4：组织机构代码证99：其他|

        :param certificate_type: The certificate_type of this ApplyEnterpriseRealnameAuthsReq.
        :type: int
        """
        self._certificate_type = certificate_type

    @property
    def corp_name(self):
        """Gets the corp_name of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：单位名称。不能全是数字、特殊字符、空格。| |参数约束及描述：单位名称。不能全是数字、特殊字符、空格。|

        :return: The corp_name of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._corp_name

    @corp_name.setter
    def corp_name(self, corp_name):
        """Sets the corp_name of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：单位名称。不能全是数字、特殊字符、空格。| |参数约束及描述：单位名称。不能全是数字、特殊字符、空格。|

        :param corp_name: The corp_name of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._corp_name = corp_name

    @property
    def customer_id(self):
        """Gets the customer_id of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：客户ID。| |参数约束及描述：客户ID。|

        :return: The customer_id of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        """Sets the customer_id of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：客户ID。| |参数约束及描述：客户ID。|

        :param customer_id: The customer_id of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._customer_id = customer_id

    @property
    def enterprise_person(self):
        """Gets the enterprise_person of this ApplyEnterpriseRealnameAuthsReq.


        :return: The enterprise_person of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: EnterprisePersonNew
        """
        return self._enterprise_person

    @enterprise_person.setter
    def enterprise_person(self, enterprise_person):
        """Sets the enterprise_person of this ApplyEnterpriseRealnameAuthsReq.


        :param enterprise_person: The enterprise_person of this ApplyEnterpriseRealnameAuthsReq.
        :type: EnterprisePersonNew
        """
        self._enterprise_person = enterprise_person

    @property
    def identify_type(self):
        """Gets the identify_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：认证方案。1：企业证件扫描| |参数的约束及描述：认证方案。1：企业证件扫描|

        :return: The identify_type of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: int
        """
        return self._identify_type

    @identify_type.setter
    def identify_type(self, identify_type):
        """Sets the identify_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：认证方案。1：企业证件扫描| |参数的约束及描述：认证方案。1：企业证件扫描|

        :param identify_type: The identify_type of this ApplyEnterpriseRealnameAuthsReq.
        :type: int
        """
        self._identify_type = identify_type

    @property
    def reg_address(self):
        """Gets the reg_address of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：实名认证企业注册地址。| |参数约束及描述：实名认证企业注册地址。|

        :return: The reg_address of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._reg_address

    @reg_address.setter
    def reg_address(self, reg_address):
        """Sets the reg_address of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：实名认证企业注册地址。| |参数约束及描述：实名认证企业注册地址。|

        :param reg_address: The reg_address of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._reg_address = reg_address

    @property
    def reg_country(self):
        """Gets the reg_country of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：实名认证填写的注册国家。国家的两位字母简码。例如：注册国家为“中国”请填写“CN”。| |参数约束及描述：实名认证填写的注册国家。国家的两位字母简码。例如：注册国家为“中国”请填写“CN”。|

        :return: The reg_country of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._reg_country

    @reg_country.setter
    def reg_country(self, reg_country):
        """Sets the reg_country of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：实名认证填写的注册国家。国家的两位字母简码。例如：注册国家为“中国”请填写“CN”。| |参数约束及描述：实名认证填写的注册国家。国家的两位字母简码。例如：注册国家为“中国”请填写“CN”。|

        :param reg_country: The reg_country of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._reg_country = reg_country

    @property
    def verified_file_url(self):
        """Gets the verified_file_url of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：企业证件认证时证件附件的文件URL。附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照附件，企业人员的证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面以营业执照举例，假设存在法人的情况下，第1张上传的是营业执照扫描件abc.023，第2张是法人的身份证人像面照片def004，第3张是法人的国徽面照片gh007，那么上传顺序需要是：abc023def004gh007文件名称区分大小写附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照正面，第2张企业证件照反面，个人证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面假设不存在法人的情况下，第1张上传的是企业证件正面扫描件abc.023，第2张上传的是企业证件反面扫描件def004，那么上传顺序需要是：abc023def004文件名称区分大小写证件附件目前仅仅支持jpg、jpeg、bmp、png、gif、pdf格式，单个文件最大不超过10M。这个URL是相对URL，不需要包含桶名和download目录，只要包含download目录下的子目录和对应文件名称即可。举例如下：如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/abc023.jpg，该字段填写abc023.jpg；如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/test/abc023.jpg，该字段填写test/abc023.jpg。| |参数约束以及描述：企业证件认证时证件附件的文件URL。附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照附件，企业人员的证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面以营业执照举例，假设存在法人的情况下，第1张上传的是营业执照扫描件abc.023，第2张是法人的身份证人像面照片def004，第3张是法人的国徽面照片gh007，那么上传顺序需要是：abc023def004gh007文件名称区分大小写附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照正面，第2张企业证件照反面，个人证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面假设不存在法人的情况下，第1张上传的是企业证件正面扫描件abc.023，第2张上传的是企业证件反面扫描件def004，那么上传顺序需要是：abc023def004文件名称区分大小写证件附件目前仅仅支持jpg、jpeg、bmp、png、gif、pdf格式，单个文件最大不超过10M。这个URL是相对URL，不需要包含桶名和download目录，只要包含download目录下的子目录和对应文件名称即可。举例如下：如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/abc023.jpg，该字段填写abc023.jpg；如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/test/abc023.jpg，该字段填写test/abc023.jpg。|

        :return: The verified_file_url of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: list[str]
        """
        return self._verified_file_url

    @verified_file_url.setter
    def verified_file_url(self, verified_file_url):
        """Sets the verified_file_url of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：企业证件认证时证件附件的文件URL。附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照附件，企业人员的证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面以营业执照举例，假设存在法人的情况下，第1张上传的是营业执照扫描件abc.023，第2张是法人的身份证人像面照片def004，第3张是法人的国徽面照片gh007，那么上传顺序需要是：abc023def004gh007文件名称区分大小写附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照正面，第2张企业证件照反面，个人证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面假设不存在法人的情况下，第1张上传的是企业证件正面扫描件abc.023，第2张上传的是企业证件反面扫描件def004，那么上传顺序需要是：abc023def004文件名称区分大小写证件附件目前仅仅支持jpg、jpeg、bmp、png、gif、pdf格式，单个文件最大不超过10M。这个URL是相对URL，不需要包含桶名和download目录，只要包含download目录下的子目录和对应文件名称即可。举例如下：如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/abc023.jpg，该字段填写abc023.jpg；如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/test/abc023.jpg，该字段填写test/abc023.jpg。| |参数约束以及描述：企业证件认证时证件附件的文件URL。附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照附件，企业人员的证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面以营业执照举例，假设存在法人的情况下，第1张上传的是营业执照扫描件abc.023，第2张是法人的身份证人像面照片def004，第3张是法人的国徽面照片gh007，那么上传顺序需要是：abc023def004gh007文件名称区分大小写附件地址必须按照顺序填写，先填写企业证件的附件，如果请求中填写了企业人员信息，再填写企业人员的身份证附件。企业证件顺序为：第1张企业证件照正面，第2张企业证件照反面，个人证件顺序为：第1张个人身份证的人像面第2张个人身份证的国徽面假设不存在法人的情况下，第1张上传的是企业证件正面扫描件abc.023，第2张上传的是企业证件反面扫描件def004，那么上传顺序需要是：abc023def004文件名称区分大小写证件附件目前仅仅支持jpg、jpeg、bmp、png、gif、pdf格式，单个文件最大不超过10M。这个URL是相对URL，不需要包含桶名和download目录，只要包含download目录下的子目录和对应文件名称即可。举例如下：如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/abc023.jpg，该字段填写abc023.jpg；如果上传的证件附件在桶中的位置是：https://bucketname.obs.Endpoint.myhuaweicloud.com/download/test/abc023.jpg，该字段填写test/abc023.jpg。|

        :param verified_file_url: The verified_file_url of this ApplyEnterpriseRealnameAuthsReq.
        :type: list[str]
        """
        self._verified_file_url = verified_file_url

    @property
    def verified_number(self):
        """Gets the verified_number of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：单位证件号码。| |参数约束及描述：单位证件号码。|

        :return: The verified_number of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._verified_number

    @verified_number.setter
    def verified_number(self, verified_number):
        """Sets the verified_number of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：单位证件号码。| |参数约束及描述：单位证件号码。|

        :param verified_number: The verified_number of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._verified_number = verified_number

    @property
    def xaccount_type(self):
        """Gets the xaccount_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：华为分给合作伙伴的平台标识。该标识的具体值由华为分配。获取方法请参见如何获取xaccountType的取值| |参数约束及描述：华为分给合作伙伴的平台标识。该标识的具体值由华为分配。获取方法请参见如何获取xaccountType的取值|

        :return: The xaccount_type of this ApplyEnterpriseRealnameAuthsReq.
        :rtype: str
        """
        return self._xaccount_type

    @xaccount_type.setter
    def xaccount_type(self, xaccount_type):
        """Sets the xaccount_type of this ApplyEnterpriseRealnameAuthsReq.

        |参数名称：华为分给合作伙伴的平台标识。该标识的具体值由华为分配。获取方法请参见如何获取xaccountType的取值| |参数约束及描述：华为分给合作伙伴的平台标识。该标识的具体值由华为分配。获取方法请参见如何获取xaccountType的取值|

        :param xaccount_type: The xaccount_type of this ApplyEnterpriseRealnameAuthsReq.
        :type: str
        """
        self._xaccount_type = xaccount_type

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
        if not isinstance(other, ApplyEnterpriseRealnameAuthsReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
