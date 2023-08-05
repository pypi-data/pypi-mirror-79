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
                 enable_stackdriver_logging: Optional[pulumi.Input[bool]] = None,
                 enable_stackdriver_monitoring: Optional[pulumi.Input[bool]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input[pulumi.InputType['InstanceNetworkConfigArgs']]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 private_instance: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a Data Fusion instance.

        To get more information about Instance, see:

        * [API documentation](https://cloud.google.com/data-fusion/docs/reference/rest/v1beta1/projects.locations.instances)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/data-fusion/docs/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of the instance.
        :param pulumi.Input[bool] enable_stackdriver_logging: Option to enable Stackdriver Logging.
        :param pulumi.Input[bool] enable_stackdriver_monitoring: Option to enable Stackdriver Monitoring.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The resource labels for instance to use to annotate any related underlying resources,
               such as Compute Engine VMs.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[pulumi.InputType['InstanceNetworkConfigArgs']] network_config: Network configuration options. These are required when a private Data Fusion instance is to be created.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Map of additional options used to configure the behavior of Data Fusion instance.
        :param pulumi.Input[bool] private_instance: Specifies whether the Data Fusion instance should be private. If set to
               true, all Data Fusion nodes will have private IP addresses and will not be
               able to access the public internet.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        :param pulumi.Input[str] type: Represents the type of Data Fusion instance. Each type is configured with
               the default settings for processing and memory.
               - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines
               using point and click UI. However, there are certain limitations, such as fewer number
               of concurrent pipelines, no support for streaming pipelines, etc.
               - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features
               available, such as support for streaming pipelines, higher number of concurrent pipelines, etc.
               Possible values are `BASIC` and `ENTERPRISE`.
        :param pulumi.Input[str] version: Current version of the Data Fusion.
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
            __props__['enable_stackdriver_logging'] = enable_stackdriver_logging
            __props__['enable_stackdriver_monitoring'] = enable_stackdriver_monitoring
            __props__['labels'] = labels
            __props__['name'] = name
            __props__['network_config'] = network_config
            __props__['options'] = options
            __props__['private_instance'] = private_instance
            __props__['project'] = project
            __props__['region'] = region
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['version'] = version
            __props__['create_time'] = None
            __props__['service_account'] = None
            __props__['service_endpoint'] = None
            __props__['state'] = None
            __props__['state_message'] = None
            __props__['update_time'] = None
        super(Instance, __self__).__init__(
            'gcp:datafusion/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enable_stackdriver_logging: Optional[pulumi.Input[bool]] = None,
            enable_stackdriver_monitoring: Optional[pulumi.Input[bool]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network_config: Optional[pulumi.Input[pulumi.InputType['InstanceNetworkConfigArgs']]] = None,
            options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            private_instance: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            service_account: Optional[pulumi.Input[str]] = None,
            service_endpoint: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            state_message: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[str]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: The time the instance was created in RFC3339 UTC "Zulu" format, accurate to nanoseconds.
        :param pulumi.Input[str] description: An optional description of the instance.
        :param pulumi.Input[bool] enable_stackdriver_logging: Option to enable Stackdriver Logging.
        :param pulumi.Input[bool] enable_stackdriver_monitoring: Option to enable Stackdriver Monitoring.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: The resource labels for instance to use to annotate any related underlying resources,
               such as Compute Engine VMs.
        :param pulumi.Input[str] name: The ID of the instance or a fully qualified identifier for the instance.
        :param pulumi.Input[pulumi.InputType['InstanceNetworkConfigArgs']] network_config: Network configuration options. These are required when a private Data Fusion instance is to be created.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: Map of additional options used to configure the behavior of Data Fusion instance.
        :param pulumi.Input[bool] private_instance: Specifies whether the Data Fusion instance should be private. If set to
               true, all Data Fusion nodes will have private IP addresses and will not be
               able to access the public internet.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the Data Fusion instance.
        :param pulumi.Input[str] service_account: Service account which will be used to access resources in the customer project.
        :param pulumi.Input[str] service_endpoint: Endpoint on which the Data Fusion UI and REST APIs are accessible.
        :param pulumi.Input[str] state: The current state of this Data Fusion instance. - CREATING: Instance is being created - RUNNING: Instance is running and
               ready for requests - FAILED: Instance creation failed - DELETING: Instance is being deleted - UPGRADING: Instance is
               being upgraded - RESTARTING: Instance is being restarted
        :param pulumi.Input[str] state_message: Additional information about the current state of this Data Fusion instance if available.
        :param pulumi.Input[str] type: Represents the type of Data Fusion instance. Each type is configured with
               the default settings for processing and memory.
               - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines
               using point and click UI. However, there are certain limitations, such as fewer number
               of concurrent pipelines, no support for streaming pipelines, etc.
               - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features
               available, such as support for streaming pipelines, higher number of concurrent pipelines, etc.
               Possible values are `BASIC` and `ENTERPRISE`.
        :param pulumi.Input[str] update_time: The time the instance was last updated in RFC3339 UTC "Zulu" format, accurate to nanoseconds.
        :param pulumi.Input[str] version: Current version of the Data Fusion.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["create_time"] = create_time
        __props__["description"] = description
        __props__["enable_stackdriver_logging"] = enable_stackdriver_logging
        __props__["enable_stackdriver_monitoring"] = enable_stackdriver_monitoring
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["network_config"] = network_config
        __props__["options"] = options
        __props__["private_instance"] = private_instance
        __props__["project"] = project
        __props__["region"] = region
        __props__["service_account"] = service_account
        __props__["service_endpoint"] = service_endpoint
        __props__["state"] = state
        __props__["state_message"] = state_message
        __props__["type"] = type
        __props__["update_time"] = update_time
        __props__["version"] = version
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time the instance was created in RFC3339 UTC "Zulu" format, accurate to nanoseconds.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of the instance.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableStackdriverLogging")
    def enable_stackdriver_logging(self) -> pulumi.Output[Optional[bool]]:
        """
        Option to enable Stackdriver Logging.
        """
        return pulumi.get(self, "enable_stackdriver_logging")

    @property
    @pulumi.getter(name="enableStackdriverMonitoring")
    def enable_stackdriver_monitoring(self) -> pulumi.Output[Optional[bool]]:
        """
        Option to enable Stackdriver Monitoring.
        """
        return pulumi.get(self, "enable_stackdriver_monitoring")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource labels for instance to use to annotate any related underlying resources,
        such as Compute Engine VMs.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The ID of the instance or a fully qualified identifier for the instance.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> pulumi.Output[Optional['outputs.InstanceNetworkConfig']]:
        """
        Network configuration options. These are required when a private Data Fusion instance is to be created.
        Structure is documented below.
        """
        return pulumi.get(self, "network_config")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of additional options used to configure the behavior of Data Fusion instance.
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter(name="privateInstance")
    def private_instance(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the Data Fusion instance should be private. If set to
        true, all Data Fusion nodes will have private IP addresses and will not be
        able to access the public internet.
        """
        return pulumi.get(self, "private_instance")

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
    def region(self) -> pulumi.Output[str]:
        """
        The region of the Data Fusion instance.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Output[str]:
        """
        Service account which will be used to access resources in the customer project.
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter(name="serviceEndpoint")
    def service_endpoint(self) -> pulumi.Output[str]:
        """
        Endpoint on which the Data Fusion UI and REST APIs are accessible.
        """
        return pulumi.get(self, "service_endpoint")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of this Data Fusion instance. - CREATING: Instance is being created - RUNNING: Instance is running and
        ready for requests - FAILED: Instance creation failed - DELETING: Instance is being deleted - UPGRADING: Instance is
        being upgraded - RESTARTING: Instance is being restarted
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateMessage")
    def state_message(self) -> pulumi.Output[str]:
        """
        Additional information about the current state of this Data Fusion instance if available.
        """
        return pulumi.get(self, "state_message")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Represents the type of Data Fusion instance. Each type is configured with
        the default settings for processing and memory.
        - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines
        using point and click UI. However, there are certain limitations, such as fewer number
        of concurrent pipelines, no support for streaming pipelines, etc.
        - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features
        available, such as support for streaming pipelines, higher number of concurrent pipelines, etc.
        Possible values are `BASIC` and `ENTERPRISE`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time the instance was last updated in RFC3339 UTC "Zulu" format, accurate to nanoseconds.
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        Current version of the Data Fusion.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

