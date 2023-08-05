# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['Domain']


class Domain(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin: Optional[pulumi.Input[str]] = None,
                 authorized_networks: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 locations: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 reserved_ip_range: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates a Microsoft AD domain

        To get more information about Domain, see:

        * [API documentation](https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains)
        * How-to Guides
            * [Managed Microsoft Active Directory Quickstart](https://cloud.google.com/managed-microsoft-ad/docs/quickstarts)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] admin: The name of delegated administrator account used to perform Active Directory operations.
               If not specified, setupadmin will be used.
        :param pulumi.Input[List[pulumi.Input[str]]] authorized_networks: The full names of the Google Compute Engine networks the domain instance is connected to. The domain is only available on networks listed in authorizedNetworks.
               If CIDR subnets overlap between networks, domain creation will fail.
        :param pulumi.Input[str] domain_name: The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions,
               https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels that can contain user-provided metadata
        :param pulumi.Input[List[pulumi.Input[str]]] locations: Locations where domain needs to be provisioned. [regions][compute/docs/regions-zones/]
               e.g. us-west1 or us-east4 Service supports up to 4 locations at once. Each location will use a /26 block.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] reserved_ip_range: The CIDR range of internal addresses that are reserved for this domain. Reserved networks must be /24 or larger.
               Ranges must be unique and non-overlapping with existing subnets in authorizedNetworks
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

            __props__['admin'] = admin
            __props__['authorized_networks'] = authorized_networks
            if domain_name is None:
                raise TypeError("Missing required property 'domain_name'")
            __props__['domain_name'] = domain_name
            __props__['labels'] = labels
            if locations is None:
                raise TypeError("Missing required property 'locations'")
            __props__['locations'] = locations
            __props__['project'] = project
            if reserved_ip_range is None:
                raise TypeError("Missing required property 'reserved_ip_range'")
            __props__['reserved_ip_range'] = reserved_ip_range
            __props__['fqdn'] = None
            __props__['name'] = None
        super(Domain, __self__).__init__(
            'gcp:activedirectory/domain:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin: Optional[pulumi.Input[str]] = None,
            authorized_networks: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            fqdn: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            locations: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            reserved_ip_range: Optional[pulumi.Input[str]] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] admin: The name of delegated administrator account used to perform Active Directory operations.
               If not specified, setupadmin will be used.
        :param pulumi.Input[List[pulumi.Input[str]]] authorized_networks: The full names of the Google Compute Engine networks the domain instance is connected to. The domain is only available on networks listed in authorizedNetworks.
               If CIDR subnets overlap between networks, domain creation will fail.
        :param pulumi.Input[str] domain_name: The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions,
               https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains.
        :param pulumi.Input[str] fqdn: The fully-qualified domain name of the exposed domain used by clients to connect to the service. Similar to what would
               be chosen for an Active Directory set up on an internal network.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels that can contain user-provided metadata
        :param pulumi.Input[List[pulumi.Input[str]]] locations: Locations where domain needs to be provisioned. [regions][compute/docs/regions-zones/]
               e.g. us-west1 or us-east4 Service supports up to 4 locations at once. Each location will use a /26 block.
        :param pulumi.Input[str] name: The unique name of the domain using the format: 'projects/{project}/locations/global/domains/{domainName}'.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] reserved_ip_range: The CIDR range of internal addresses that are reserved for this domain. Reserved networks must be /24 or larger.
               Ranges must be unique and non-overlapping with existing subnets in authorizedNetworks
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["admin"] = admin
        __props__["authorized_networks"] = authorized_networks
        __props__["domain_name"] = domain_name
        __props__["fqdn"] = fqdn
        __props__["labels"] = labels
        __props__["locations"] = locations
        __props__["name"] = name
        __props__["project"] = project
        __props__["reserved_ip_range"] = reserved_ip_range
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def admin(self) -> pulumi.Output[Optional[str]]:
        """
        The name of delegated administrator account used to perform Active Directory operations.
        If not specified, setupadmin will be used.
        """
        return pulumi.get(self, "admin")

    @property
    @pulumi.getter(name="authorizedNetworks")
    def authorized_networks(self) -> pulumi.Output[Optional[List[str]]]:
        """
        The full names of the Google Compute Engine networks the domain instance is connected to. The domain is only available on networks listed in authorizedNetworks.
        If CIDR subnets overlap between networks, domain creation will fail.
        """
        return pulumi.get(self, "authorized_networks")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name. e.g. mydomain.myorganization.com, with the restrictions,
        https://cloud.google.com/managed-microsoft-ad/reference/rest/v1/projects.locations.global.domains.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[str]:
        """
        The fully-qualified domain name of the exposed domain used by clients to connect to the service. Similar to what would
        be chosen for an Active Directory set up on an internal network.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels that can contain user-provided metadata
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Output[List[str]]:
        """
        Locations where domain needs to be provisioned. [regions][compute/docs/regions-zones/]
        e.g. us-west1 or us-east4 Service supports up to 4 locations at once. Each location will use a /26 block.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The unique name of the domain using the format: 'projects/{project}/locations/global/domains/{domainName}'.
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
    @pulumi.getter(name="reservedIpRange")
    def reserved_ip_range(self) -> pulumi.Output[str]:
        """
        The CIDR range of internal addresses that are reserved for this domain. Reserved networks must be /24 or larger.
        Ranges must be unique and non-overlapping with existing subnets in authorizedNetworks
        """
        return pulumi.get(self, "reserved_ip_range")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

