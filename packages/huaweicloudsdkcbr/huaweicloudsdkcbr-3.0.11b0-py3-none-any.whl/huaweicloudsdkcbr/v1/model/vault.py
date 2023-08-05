# coding: utf-8

import pprint
import re

import six





class Vault:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'billing': 'Billing',
        'description': 'str',
        'id': 'str',
        'name': 'str',
        'project_id': 'str',
        'provider_id': 'str',
        'resources': 'list[ResourceResp]',
        'tags': 'list[Tag]',
        'enterprise_project_id': 'str',
        'auto_bind': 'bool',
        'bind_rules': 'VaultBindRules',
        'auto_expand': 'bool',
        'user_id': 'str',
        'created_at': 'str'
    }

    attribute_map = {
        'billing': 'billing',
        'description': 'description',
        'id': 'id',
        'name': 'name',
        'project_id': 'project_id',
        'provider_id': 'provider_id',
        'resources': 'resources',
        'tags': 'tags',
        'enterprise_project_id': 'enterprise_project_id',
        'auto_bind': 'auto_bind',
        'bind_rules': 'bind_rules',
        'auto_expand': 'auto_expand',
        'user_id': 'user_id',
        'created_at': 'created_at'
    }

    def __init__(self, billing=None, description=None, id=None, name=None, project_id=None, provider_id=None, resources=None, tags=None, enterprise_project_id=None, auto_bind=None, bind_rules=None, auto_expand=None, user_id=None, created_at=None):
        """Vault - a model defined in huaweicloud sdk"""
        
        

        self._billing = None
        self._description = None
        self._id = None
        self._name = None
        self._project_id = None
        self._provider_id = None
        self._resources = None
        self._tags = None
        self._enterprise_project_id = None
        self._auto_bind = None
        self._bind_rules = None
        self._auto_expand = None
        self._user_id = None
        self._created_at = None
        self.discriminator = None

        self.billing = billing
        if description is not None:
            self.description = description
        self.id = id
        self.name = name
        self.project_id = project_id
        self.provider_id = provider_id
        self.resources = resources
        if tags is not None:
            self.tags = tags
        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        if auto_bind is not None:
            self.auto_bind = auto_bind
        if bind_rules is not None:
            self.bind_rules = bind_rules
        if auto_expand is not None:
            self.auto_expand = auto_expand
        if user_id is not None:
            self.user_id = user_id
        if created_at is not None:
            self.created_at = created_at

    @property
    def billing(self):
        """Gets the billing of this Vault.


        :return: The billing of this Vault.
        :rtype: Billing
        """
        return self._billing

    @billing.setter
    def billing(self, billing):
        """Sets the billing of this Vault.


        :param billing: The billing of this Vault.
        :type: Billing
        """
        self._billing = billing

    @property
    def description(self):
        """Gets the description of this Vault.

        存储库自定义描述信息。

        :return: The description of this Vault.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Vault.

        存储库自定义描述信息。

        :param description: The description of this Vault.
        :type: str
        """
        self._description = description

    @property
    def id(self):
        """Gets the id of this Vault.

        保管库ID

        :return: The id of this Vault.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Vault.

        保管库ID

        :param id: The id of this Vault.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """Gets the name of this Vault.

        保管库名称

        :return: The name of this Vault.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Vault.

        保管库名称

        :param name: The name of this Vault.
        :type: str
        """
        self._name = name

    @property
    def project_id(self):
        """Gets the project_id of this Vault.

        项目ID

        :return: The project_id of this Vault.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Vault.

        项目ID

        :param project_id: The project_id of this Vault.
        :type: str
        """
        self._project_id = project_id

    @property
    def provider_id(self):
        """Gets the provider_id of this Vault.

        保管库类型

        :return: The provider_id of this Vault.
        :rtype: str
        """
        return self._provider_id

    @provider_id.setter
    def provider_id(self, provider_id):
        """Sets the provider_id of this Vault.

        保管库类型

        :param provider_id: The provider_id of this Vault.
        :type: str
        """
        self._provider_id = provider_id

    @property
    def resources(self):
        """Gets the resources of this Vault.

        存储库资源

        :return: The resources of this Vault.
        :rtype: list[ResourceResp]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this Vault.

        存储库资源

        :param resources: The resources of this Vault.
        :type: list[ResourceResp]
        """
        self._resources = resources

    @property
    def tags(self):
        """Gets the tags of this Vault.

        存储库标签

        :return: The tags of this Vault.
        :rtype: list[Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this Vault.

        存储库标签

        :param tags: The tags of this Vault.
        :type: list[Tag]
        """
        self._tags = tags

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this Vault.

        企业项目id，默认为‘0’。

        :return: The enterprise_project_id of this Vault.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this Vault.

        企业项目id，默认为‘0’。

        :param enterprise_project_id: The enterprise_project_id of this Vault.
        :type: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def auto_bind(self):
        """Gets the auto_bind of this Vault.

        是否自动绑定，默认为false，不支持。

        :return: The auto_bind of this Vault.
        :rtype: bool
        """
        return self._auto_bind

    @auto_bind.setter
    def auto_bind(self, auto_bind):
        """Sets the auto_bind of this Vault.

        是否自动绑定，默认为false，不支持。

        :param auto_bind: The auto_bind of this Vault.
        :type: bool
        """
        self._auto_bind = auto_bind

    @property
    def bind_rules(self):
        """Gets the bind_rules of this Vault.


        :return: The bind_rules of this Vault.
        :rtype: VaultBindRules
        """
        return self._bind_rules

    @bind_rules.setter
    def bind_rules(self, bind_rules):
        """Sets the bind_rules of this Vault.


        :param bind_rules: The bind_rules of this Vault.
        :type: VaultBindRules
        """
        self._bind_rules = bind_rules

    @property
    def auto_expand(self):
        """Gets the auto_expand of this Vault.

        是否开启存储库自动扩容能力（只支持按需存储库）。

        :return: The auto_expand of this Vault.
        :rtype: bool
        """
        return self._auto_expand

    @auto_expand.setter
    def auto_expand(self, auto_expand):
        """Sets the auto_expand of this Vault.

        是否开启存储库自动扩容能力（只支持按需存储库）。

        :param auto_expand: The auto_expand of this Vault.
        :type: bool
        """
        self._auto_expand = auto_expand

    @property
    def user_id(self):
        """Gets the user_id of this Vault.

        用户id

        :return: The user_id of this Vault.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this Vault.

        用户id

        :param user_id: The user_id of this Vault.
        :type: str
        """
        self._user_id = user_id

    @property
    def created_at(self):
        """Gets the created_at of this Vault.

        创建时间

        :return: The created_at of this Vault.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Vault.

        创建时间

        :param created_at: The created_at of this Vault.
        :type: str
        """
        self._created_at = created_at

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
        if not isinstance(other, Vault):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
