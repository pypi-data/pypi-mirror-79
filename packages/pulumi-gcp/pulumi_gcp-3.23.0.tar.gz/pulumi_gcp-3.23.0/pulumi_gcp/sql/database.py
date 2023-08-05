# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['Database']


class Database(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 charset: Optional[pulumi.Input[str]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a SQL database inside the Cloud SQL instance, hosted in
        Google's cloud.

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] charset: The charset value. See MySQL's
               [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
               and Postgres' [Character Set Support](https://www.postgresql.org/docs/9.6/static/multibyte.html)
               for more details and supported values. Postgres databases only support
               a value of `UTF8` at creation time.
        :param pulumi.Input[str] collation: The collation value. See MySQL's
               [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
               and Postgres' [Collation Support](https://www.postgresql.org/docs/9.6/static/collation.html)
               for more details and supported values. Postgres databases only support
               a value of `en_US.UTF8` at creation time.
        :param pulumi.Input[str] instance: The name of the Cloud SQL instance. This does not include the project
               ID.
        :param pulumi.Input[str] name: The name of the database in the Cloud SQL instance.
               This does not include the project ID or instance name.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['charset'] = charset
            __props__['collation'] = collation
            if instance is None:
                raise TypeError("Missing required property 'instance'")
            __props__['instance'] = instance
            __props__['name'] = name
            __props__['project'] = project
            __props__['self_link'] = None
        super(Database, __self__).__init__(
            'gcp:sql/database:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            charset: Optional[pulumi.Input[str]] = None,
            collation: Optional[pulumi.Input[str]] = None,
            instance: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] charset: The charset value. See MySQL's
               [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
               and Postgres' [Character Set Support](https://www.postgresql.org/docs/9.6/static/multibyte.html)
               for more details and supported values. Postgres databases only support
               a value of `UTF8` at creation time.
        :param pulumi.Input[str] collation: The collation value. See MySQL's
               [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
               and Postgres' [Collation Support](https://www.postgresql.org/docs/9.6/static/collation.html)
               for more details and supported values. Postgres databases only support
               a value of `en_US.UTF8` at creation time.
        :param pulumi.Input[str] instance: The name of the Cloud SQL instance. This does not include the project
               ID.
        :param pulumi.Input[str] name: The name of the database in the Cloud SQL instance.
               This does not include the project ID or instance name.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["charset"] = charset
        __props__["collation"] = collation
        __props__["instance"] = instance
        __props__["name"] = name
        __props__["project"] = project
        __props__["self_link"] = self_link
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def charset(self) -> pulumi.Output[str]:
        """
        The charset value. See MySQL's
        [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
        and Postgres' [Character Set Support](https://www.postgresql.org/docs/9.6/static/multibyte.html)
        for more details and supported values. Postgres databases only support
        a value of `UTF8` at creation time.
        """
        return pulumi.get(self, "charset")

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[str]:
        """
        The collation value. See MySQL's
        [Supported Character Sets and Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html)
        and Postgres' [Collation Support](https://www.postgresql.org/docs/9.6/static/collation.html)
        for more details and supported values. Postgres databases only support
        a value of `en_US.UTF8` at creation time.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter
    def instance(self) -> pulumi.Output[str]:
        """
        The name of the Cloud SQL instance. This does not include the project
        ID.
        """
        return pulumi.get(self, "instance")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the database in the Cloud SQL instance.
        This does not include the project ID or instance name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

