# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['FirewallRule']


class FirewallRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[float]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_range: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A single firewall rule that is evaluated against incoming traffic
        and provides an action to take on matched requests.

        To get more information about FirewallRule, see:

        * [API documentation](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.firewall.ingressRules)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/appengine/docs/standard/python/creating-firewalls#creating_firewall_rules)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[float] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
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

            if action is None:
                raise TypeError("Missing required property 'action'")
            __props__['action'] = action
            __props__['description'] = description
            __props__['priority'] = priority
            __props__['project'] = project
            if source_range is None:
                raise TypeError("Missing required property 'source_range'")
            __props__['source_range'] = source_range
        super(FirewallRule, __self__).__init__(
            'gcp:appengine/firewallRule:FirewallRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            priority: Optional[pulumi.Input[float]] = None,
            project: Optional[pulumi.Input[str]] = None,
            source_range: Optional[pulumi.Input[str]] = None) -> 'FirewallRule':
        """
        Get an existing FirewallRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[float] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["action"] = action
        __props__["description"] = description
        __props__["priority"] = priority
        __props__["project"] = project
        __props__["source_range"] = source_range
        return FirewallRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        The action to take if this rule matches.
        Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional string description of this rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[float]]:
        """
        A positive integer that defines the order of rule evaluation.
        Rules with the lowest priority are evaluated first.
        A default rule at priority Int32.MaxValue matches all IPv4 and
        IPv6 traffic when no previous rule matches. Only the action of
        this rule can be modified by the user.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="sourceRange")
    def source_range(self) -> pulumi.Output[str]:
        """
        IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        return pulumi.get(self, "source_range")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

