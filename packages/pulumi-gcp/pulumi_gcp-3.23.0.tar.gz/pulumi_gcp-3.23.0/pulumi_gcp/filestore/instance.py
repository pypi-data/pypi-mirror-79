# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Instance']


class Instance(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 file_shares: Optional[pulumi.Input[pulumi.InputType['InstanceFileSharesArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Google Cloud Filestore instance.

        To get more information about Instance, see:

        * [API documentation](https://cloud.google.com/filestore/docs/reference/rest/v1beta1/projects.locations.instances/create)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/filestore/docs/creating-instances)
            * [Use with Kubernetes](https://cloud.google.com/filestore/docs/accessing-fileshares)
            * [Copying Data In/Out](https://cloud.google.com/filestore/docs/copying-data)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the instance.
        :param pulumi.Input[pulumi.InputType['InstanceFileSharesArgs']] file_shares: File system shares on the instance. For this version, only a
               single file share is supported.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] name: The name of the fileshare (16 characters or less)
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkArgs']]]] networks: VPC networks to which the instance is connected. For this version,
               only a single network is supported.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] tier: The service tier of the instance.
               Possible values are `TIER_UNSPECIFIED`, `STANDARD`, `PREMIUM`, `BASIC_HDD`, `BASIC_SSD`, and `HIGH_SCALE_SSD`.
        :param pulumi.Input[str] zone: The name of the Filestore zone of the instance.
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

            __props__['description'] = description
            if file_shares is None:
                raise TypeError("Missing required property 'file_shares'")
            __props__['file_shares'] = file_shares
            __props__['labels'] = labels
            __props__['name'] = name
            if networks is None:
                raise TypeError("Missing required property 'networks'")
            __props__['networks'] = networks
            __props__['project'] = project
            if tier is None:
                raise TypeError("Missing required property 'tier'")
            __props__['tier'] = tier
            if zone is None:
                raise TypeError("Missing required property 'zone'")
            __props__['zone'] = zone
            __props__['create_time'] = None
            __props__['etag'] = None
        super(Instance, __self__).__init__(
            'gcp:filestore/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            file_shares: Optional[pulumi.Input[pulumi.InputType['InstanceFileSharesArgs']]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            networks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkArgs']]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            tier: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: A description of the instance.
        :param pulumi.Input[str] etag: Server-specified ETag for the instance resource to prevent simultaneous updates from overwriting each other.
        :param pulumi.Input[pulumi.InputType['InstanceFileSharesArgs']] file_shares: File system shares on the instance. For this version, only a
               single file share is supported.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] name: The name of the fileshare (16 characters or less)
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkArgs']]]] networks: VPC networks to which the instance is connected. For this version,
               only a single network is supported.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] tier: The service tier of the instance.
               Possible values are `TIER_UNSPECIFIED`, `STANDARD`, `PREMIUM`, `BASIC_HDD`, `BASIC_SSD`, and `HIGH_SCALE_SSD`.
        :param pulumi.Input[str] zone: The name of the Filestore zone of the instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["create_time"] = create_time
        __props__["description"] = description
        __props__["etag"] = etag
        __props__["file_shares"] = file_shares
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["networks"] = networks
        __props__["project"] = project
        __props__["tier"] = tier
        __props__["zone"] = zone
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the instance.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Server-specified ETag for the instance resource to prevent simultaneous updates from overwriting each other.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="fileShares")
    def file_shares(self) -> pulumi.Output['outputs.InstanceFileShares']:
        """
        File system shares on the instance. For this version, only a
        single file share is supported.
        Structure is documented below.
        """
        return pulumi.get(self, "file_shares")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the fileshare (16 characters or less)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def networks(self) -> pulumi.Output[List['outputs.InstanceNetwork']]:
        """
        VPC networks to which the instance is connected. For this version,
        only a single network is supported.
        Structure is documented below.
        """
        return pulumi.get(self, "networks")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Output[str]:
        """
        The service tier of the instance.
        Possible values are `TIER_UNSPECIFIED`, `STANDARD`, `PREMIUM`, `BASIC_HDD`, `BASIC_SSD`, and `HIGH_SCALE_SSD`.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        """
        The name of the Filestore zone of the instance.
        """
        return pulumi.get(self, "zone")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

