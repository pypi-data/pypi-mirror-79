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

__all__ = ['Subnetwork']


class Subnetwork(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 log_config: Optional[pulumi.Input[pulumi.InputType['SubnetworkLogConfigArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 private_ip_google_access: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 secondary_ip_ranges: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['SubnetworkSecondaryIpRangeArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A VPC network is a virtual version of the traditional physical networks
        that exist within and between physical data centers. A VPC network
        provides connectivity for your Compute Engine virtual machine (VM)
        instances, Container Engine containers, App Engine Flex services, and
        other network-related resources.

        Each GCP project contains one or more VPC networks. Each VPC network is a
        global entity spanning all GCP regions. This global VPC network allows VM
        instances and other resources to communicate with each other via internal,
        private IP addresses.

        Each VPC network is subdivided into subnets, and each subnet is contained
        within a single region. You can have more than one subnet in a region for
        a given VPC network. Each subnet has a contiguous private RFC1918 IP
        space. You create instances, containers, and the like in these subnets.
        When you create an instance, you must create it in a subnet, and the
        instance draws its internal IP address from that subnet.

        Virtual machine (VM) instances in a VPC network can communicate with
        instances in all other subnets of the same VPC network, regardless of
        region, using their RFC1918 private IP addresses. You can isolate portions
        of the network, even entire subnets, using firewall rules.

        To get more information about Subnetwork, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/subnetworks)
        * How-to Guides
            * [Private Google Access](https://cloud.google.com/vpc/docs/configure-private-google-access)
            * [Cloud Networking](https://cloud.google.com/vpc/docs/using-vpc)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when
               you create the resource. This field can be set only at resource
               creation time.
        :param pulumi.Input[str] ip_cidr_range: The range of IP addresses belonging to this subnetwork secondary
               range. Provide this property when you create the subnetwork.
               Ranges must be unique and non-overlapping with all primary and
               secondary IP ranges within a network. Only IPv4 is supported.
        :param pulumi.Input[pulumi.InputType['SubnetworkLogConfigArgs']] log_config: Denotes the logging options for the subnetwork flow logs. If logging is enabled
               logs will be exported to Stackdriver. This field cannot be set if the `purpose` of this
               subnetwork is `INTERNAL_HTTPS_LOAD_BALANCER`
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the resource, provided by the client when initially
               creating the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?` which
               means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] network: The network this subnet belongs to.
               Only networks that are in the distributed mode can have subnetworks.
        :param pulumi.Input[bool] private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can
               access Google APIs and services by using Private Google Access.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] purpose: The purpose of the resource. This field can be either PRIVATE
               or INTERNAL_HTTPS_LOAD_BALANCER. A subnetwork with purpose set to
               INTERNAL_HTTPS_LOAD_BALANCER is a user-created subnetwork that is
               reserved for Internal HTTP(S) Load Balancing. If unspecified, the
               purpose defaults to PRIVATE.
               If set to INTERNAL_HTTPS_LOAD_BALANCER you must also set the role.
               Possible values are `INTERNAL_HTTPS_LOAD_BALANCER` and `PRIVATE`.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
        :param pulumi.Input[str] role: The role of subnetwork. Currently, this field is only used when
               purpose = INTERNAL_HTTPS_LOAD_BALANCER. The value can be set to ACTIVE
               or BACKUP. An ACTIVE subnetwork is one that is currently being used
               for Internal HTTP(S) Load Balancing. A BACKUP subnetwork is one that
               is ready to be promoted to ACTIVE or is currently draining.
               Possible values are `ACTIVE` and `BACKUP`.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['SubnetworkSecondaryIpRangeArgs']]]] secondary_ip_ranges: An array of configurations for secondary IP ranges for VM instances
               contained in this subnetwork. The primary IP of such VM must belong
               to the primary ipCidrRange of the subnetwork. The alias IPs may belong
               to either primary or secondary ranges. Structure is documented below.
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
            if ip_cidr_range is None:
                raise TypeError("Missing required property 'ip_cidr_range'")
            __props__['ip_cidr_range'] = ip_cidr_range
            __props__['log_config'] = log_config
            __props__['name'] = name
            if network is None:
                raise TypeError("Missing required property 'network'")
            __props__['network'] = network
            __props__['private_ip_google_access'] = private_ip_google_access
            __props__['project'] = project
            __props__['purpose'] = purpose
            __props__['region'] = region
            __props__['role'] = role
            __props__['secondary_ip_ranges'] = secondary_ip_ranges
            __props__['creation_timestamp'] = None
            __props__['fingerprint'] = None
            __props__['gateway_address'] = None
            __props__['self_link'] = None
        super(Subnetwork, __self__).__init__(
            'gcp:compute/subnetwork:Subnetwork',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            fingerprint: Optional[pulumi.Input[str]] = None,
            gateway_address: Optional[pulumi.Input[str]] = None,
            ip_cidr_range: Optional[pulumi.Input[str]] = None,
            log_config: Optional[pulumi.Input[pulumi.InputType['SubnetworkLogConfigArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            private_ip_google_access: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            purpose: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            secondary_ip_ranges: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['SubnetworkSecondaryIpRangeArgs']]]]] = None,
            self_link: Optional[pulumi.Input[str]] = None) -> 'Subnetwork':
        """
        Get an existing Subnetwork resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when
               you create the resource. This field can be set only at resource
               creation time.
        :param pulumi.Input[str] fingerprint: Fingerprint of this resource. This field is used internally during updates of this resource.
        :param pulumi.Input[str] gateway_address: The gateway address for default routes to reach destination addresses outside this subnetwork.
        :param pulumi.Input[str] ip_cidr_range: The range of IP addresses belonging to this subnetwork secondary
               range. Provide this property when you create the subnetwork.
               Ranges must be unique and non-overlapping with all primary and
               secondary IP ranges within a network. Only IPv4 is supported.
        :param pulumi.Input[pulumi.InputType['SubnetworkLogConfigArgs']] log_config: Denotes the logging options for the subnetwork flow logs. If logging is enabled
               logs will be exported to Stackdriver. This field cannot be set if the `purpose` of this
               subnetwork is `INTERNAL_HTTPS_LOAD_BALANCER`
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the resource, provided by the client when initially
               creating the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?` which
               means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] network: The network this subnet belongs to.
               Only networks that are in the distributed mode can have subnetworks.
        :param pulumi.Input[bool] private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can
               access Google APIs and services by using Private Google Access.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] purpose: The purpose of the resource. This field can be either PRIVATE
               or INTERNAL_HTTPS_LOAD_BALANCER. A subnetwork with purpose set to
               INTERNAL_HTTPS_LOAD_BALANCER is a user-created subnetwork that is
               reserved for Internal HTTP(S) Load Balancing. If unspecified, the
               purpose defaults to PRIVATE.
               If set to INTERNAL_HTTPS_LOAD_BALANCER you must also set the role.
               Possible values are `INTERNAL_HTTPS_LOAD_BALANCER` and `PRIVATE`.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
        :param pulumi.Input[str] role: The role of subnetwork. Currently, this field is only used when
               purpose = INTERNAL_HTTPS_LOAD_BALANCER. The value can be set to ACTIVE
               or BACKUP. An ACTIVE subnetwork is one that is currently being used
               for Internal HTTP(S) Load Balancing. A BACKUP subnetwork is one that
               is ready to be promoted to ACTIVE or is currently draining.
               Possible values are `ACTIVE` and `BACKUP`.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['SubnetworkSecondaryIpRangeArgs']]]] secondary_ip_ranges: An array of configurations for secondary IP ranges for VM instances
               contained in this subnetwork. The primary IP of such VM must belong
               to the primary ipCidrRange of the subnetwork. The alias IPs may belong
               to either primary or secondary ranges. Structure is documented below.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["creation_timestamp"] = creation_timestamp
        __props__["description"] = description
        __props__["fingerprint"] = fingerprint
        __props__["gateway_address"] = gateway_address
        __props__["ip_cidr_range"] = ip_cidr_range
        __props__["log_config"] = log_config
        __props__["name"] = name
        __props__["network"] = network
        __props__["private_ip_google_access"] = private_ip_google_access
        __props__["project"] = project
        __props__["purpose"] = purpose
        __props__["region"] = region
        __props__["role"] = role
        __props__["secondary_ip_ranges"] = secondary_ip_ranges
        __props__["self_link"] = self_link
        return Subnetwork(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of this resource. Provide this property when
        you create the resource. This field can be set only at resource
        creation time.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of this resource. This field is used internally during updates of this resource.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="gatewayAddress")
    def gateway_address(self) -> pulumi.Output[str]:
        """
        The gateway address for default routes to reach destination addresses outside this subnetwork.
        """
        return pulumi.get(self, "gateway_address")

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> pulumi.Output[str]:
        """
        The range of IP addresses belonging to this subnetwork secondary
        range. Provide this property when you create the subnetwork.
        Ranges must be unique and non-overlapping with all primary and
        secondary IP ranges within a network. Only IPv4 is supported.
        """
        return pulumi.get(self, "ip_cidr_range")

    @property
    @pulumi.getter(name="logConfig")
    def log_config(self) -> pulumi.Output[Optional['outputs.SubnetworkLogConfig']]:
        """
        Denotes the logging options for the subnetwork flow logs. If logging is enabled
        logs will be exported to Stackdriver. This field cannot be set if the `purpose` of this
        subnetwork is `INTERNAL_HTTPS_LOAD_BALANCER`
        Structure is documented below.
        """
        return pulumi.get(self, "log_config")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource, provided by the client when initially
        creating the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?` which
        means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The network this subnet belongs to.
        Only networks that are in the distributed mode can have subnetworks.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="privateIpGoogleAccess")
    def private_ip_google_access(self) -> pulumi.Output[Optional[bool]]:
        """
        When enabled, VMs in this subnetwork without external IP addresses can
        access Google APIs and services by using Private Google Access.
        """
        return pulumi.get(self, "private_ip_google_access")

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
    def purpose(self) -> pulumi.Output[str]:
        """
        The purpose of the resource. This field can be either PRIVATE
        or INTERNAL_HTTPS_LOAD_BALANCER. A subnetwork with purpose set to
        INTERNAL_HTTPS_LOAD_BALANCER is a user-created subnetwork that is
        reserved for Internal HTTP(S) Load Balancing. If unspecified, the
        purpose defaults to PRIVATE.
        If set to INTERNAL_HTTPS_LOAD_BALANCER you must also set the role.
        Possible values are `INTERNAL_HTTPS_LOAD_BALANCER` and `PRIVATE`.
        """
        return pulumi.get(self, "purpose")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The GCP region for this subnetwork.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[Optional[str]]:
        """
        The role of subnetwork. Currently, this field is only used when
        purpose = INTERNAL_HTTPS_LOAD_BALANCER. The value can be set to ACTIVE
        or BACKUP. An ACTIVE subnetwork is one that is currently being used
        for Internal HTTP(S) Load Balancing. A BACKUP subnetwork is one that
        is ready to be promoted to ACTIVE or is currently draining.
        Possible values are `ACTIVE` and `BACKUP`.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="secondaryIpRanges")
    def secondary_ip_ranges(self) -> pulumi.Output[List['outputs.SubnetworkSecondaryIpRange']]:
        """
        An array of configurations for secondary IP ranges for VM instances
        contained in this subnetwork. The primary IP of such VM must belong
        to the primary ipCidrRange of the subnetwork. The alias IPs may belong
        to either primary or secondary ranges. Structure is documented below.
        """
        return pulumi.get(self, "secondary_ip_ranges")

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

