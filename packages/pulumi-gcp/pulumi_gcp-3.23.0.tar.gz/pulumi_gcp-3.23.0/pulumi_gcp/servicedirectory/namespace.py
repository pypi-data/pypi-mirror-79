# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['Namespace']


class Namespace(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 namespace_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A container for `services`. Namespaces allow administrators to group services
        together and define permissions for a collection of services.

        To get more information about Namespace, see:

        * [API documentation](https://cloud.google.com/service-directory/docs/reference/rest/v1beta1/projects.locations.namespaces)
        * How-to Guides
            * [Configuring a namespace](https://cloud.google.com/service-directory/docs/configuring-service-directory#configuring_a_namespace)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels associated with this Namespace. No more than 64 user
               labels can be associated with a given resource. Label keys and values can
               be no longer than 63 characters.
        :param pulumi.Input[str] location: The location for the Namespace.
               A full list of valid locations can be found by running
               `gcloud beta service-directory locations list`.
        :param pulumi.Input[str] namespace_id: The Resource ID must be 1-63 characters long, including digits,
               lowercase letters or the hyphen character.
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

            __props__['labels'] = labels
            if location is None:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if namespace_id is None:
                raise TypeError("Missing required property 'namespace_id'")
            __props__['namespace_id'] = namespace_id
            __props__['project'] = project
            __props__['name'] = None
        super(Namespace, __self__).__init__(
            'gcp:servicedirectory/namespace:Namespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace_id: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'Namespace':
        """
        Get an existing Namespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels associated with this Namespace. No more than 64 user
               labels can be associated with a given resource. Label keys and values can
               be no longer than 63 characters.
        :param pulumi.Input[str] location: The location for the Namespace.
               A full list of valid locations can be found by running
               `gcloud beta service-directory locations list`.
        :param pulumi.Input[str] name: The resource name for the namespace in the format 'projects/*/locations/*/namespaces/*'.
        :param pulumi.Input[str] namespace_id: The Resource ID must be 1-63 characters long, including digits,
               lowercase letters or the hyphen character.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["labels"] = labels
        __props__["location"] = location
        __props__["name"] = name
        __props__["namespace_id"] = namespace_id
        __props__["project"] = project
        return Namespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels associated with this Namespace. No more than 64 user
        labels can be associated with a given resource. Label keys and values can
        be no longer than 63 characters.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location for the Namespace.
        A full list of valid locations can be found by running
        `gcloud beta service-directory locations list`.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name for the namespace in the format 'projects/*/locations/*/namespaces/*'.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespaceId")
    def namespace_id(self) -> pulumi.Output[str]:
        """
        The Resource ID must be 1-63 characters long, including digits,
        lowercase letters or the hyphen character.
        """
        return pulumi.get(self, "namespace_id")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

