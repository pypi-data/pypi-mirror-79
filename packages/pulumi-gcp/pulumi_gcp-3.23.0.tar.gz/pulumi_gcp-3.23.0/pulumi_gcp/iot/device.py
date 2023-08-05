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

__all__ = ['Device']


class Device(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blocked: Optional[pulumi.Input[bool]] = None,
                 credentials: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeviceCredentialArgs']]]]] = None,
                 gateway_config: Optional[pulumi.Input[pulumi.InputType['DeviceGatewayConfigArgs']]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 registry: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Google Cloud IoT Core device.

        To get more information about Device, see:

        * [API documentation](https://cloud.google.com/iot/docs/reference/cloudiot/rest/)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/iot/docs/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] blocked: If a device is blocked, connections or requests from this device will fail.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeviceCredentialArgs']]]] credentials: The credentials used to authenticate this device.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['DeviceGatewayConfigArgs']] gateway_config: Gateway-related configuration and state.
               Structure is documented below.
        :param pulumi.Input[str] log_level: The logging verbosity for device activity.
               Possible values are `NONE`, `ERROR`, `INFO`, and `DEBUG`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: The metadata key-value pairs assigned to the device.
        :param pulumi.Input[str] name: A unique name for the resource.
        :param pulumi.Input[str] registry: The name of the device registry where this device should be created.
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

            __props__['blocked'] = blocked
            __props__['credentials'] = credentials
            __props__['gateway_config'] = gateway_config
            __props__['log_level'] = log_level
            __props__['metadata'] = metadata
            __props__['name'] = name
            if registry is None:
                raise TypeError("Missing required property 'registry'")
            __props__['registry'] = registry
            __props__['config'] = None
            __props__['last_config_ack_time'] = None
            __props__['last_config_send_time'] = None
            __props__['last_error_status'] = None
            __props__['last_error_time'] = None
            __props__['last_event_time'] = None
            __props__['last_heartbeat_time'] = None
            __props__['last_state_time'] = None
            __props__['num_id'] = None
            __props__['state'] = None
        super(Device, __self__).__init__(
            'gcp:iot/device:Device',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            blocked: Optional[pulumi.Input[bool]] = None,
            config: Optional[pulumi.Input[pulumi.InputType['DeviceConfigArgs']]] = None,
            credentials: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeviceCredentialArgs']]]]] = None,
            gateway_config: Optional[pulumi.Input[pulumi.InputType['DeviceGatewayConfigArgs']]] = None,
            last_config_ack_time: Optional[pulumi.Input[str]] = None,
            last_config_send_time: Optional[pulumi.Input[str]] = None,
            last_error_status: Optional[pulumi.Input[pulumi.InputType['DeviceLastErrorStatusArgs']]] = None,
            last_error_time: Optional[pulumi.Input[str]] = None,
            last_event_time: Optional[pulumi.Input[str]] = None,
            last_heartbeat_time: Optional[pulumi.Input[str]] = None,
            last_state_time: Optional[pulumi.Input[str]] = None,
            log_level: Optional[pulumi.Input[str]] = None,
            metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            num_id: Optional[pulumi.Input[str]] = None,
            registry: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[pulumi.InputType['DeviceStateArgs']]] = None) -> 'Device':
        """
        Get an existing Device resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] blocked: If a device is blocked, connections or requests from this device will fail.
        :param pulumi.Input[pulumi.InputType['DeviceConfigArgs']] config: The most recent device configuration, which is eventually sent from Cloud IoT Core to the device.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeviceCredentialArgs']]]] credentials: The credentials used to authenticate this device.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['DeviceGatewayConfigArgs']] gateway_config: Gateway-related configuration and state.
               Structure is documented below.
        :param pulumi.Input[str] last_config_ack_time: The last time a cloud-to-device config version acknowledgment was received from the device.
        :param pulumi.Input[str] last_config_send_time: The last time a cloud-to-device config version was sent to the device.
        :param pulumi.Input[pulumi.InputType['DeviceLastErrorStatusArgs']] last_error_status: The error message of the most recent error, such as a failure to publish to Cloud Pub/Sub.
        :param pulumi.Input[str] last_error_time: The time the most recent error occurred, such as a failure to publish to Cloud Pub/Sub.
        :param pulumi.Input[str] last_event_time: The last time a telemetry event was received.
        :param pulumi.Input[str] last_heartbeat_time: The last time an MQTT PINGREQ was received.
        :param pulumi.Input[str] last_state_time: The last time a state event was received.
        :param pulumi.Input[str] log_level: The logging verbosity for device activity.
               Possible values are `NONE`, `ERROR`, `INFO`, and `DEBUG`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: The metadata key-value pairs assigned to the device.
        :param pulumi.Input[str] name: A unique name for the resource.
        :param pulumi.Input[str] num_id: A server-defined unique numeric ID for the device. This is a more compact way to identify devices, and it is globally
               unique.
        :param pulumi.Input[str] registry: The name of the device registry where this device should be created.
        :param pulumi.Input[pulumi.InputType['DeviceStateArgs']] state: The state most recently received from the device.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["blocked"] = blocked
        __props__["config"] = config
        __props__["credentials"] = credentials
        __props__["gateway_config"] = gateway_config
        __props__["last_config_ack_time"] = last_config_ack_time
        __props__["last_config_send_time"] = last_config_send_time
        __props__["last_error_status"] = last_error_status
        __props__["last_error_time"] = last_error_time
        __props__["last_event_time"] = last_event_time
        __props__["last_heartbeat_time"] = last_heartbeat_time
        __props__["last_state_time"] = last_state_time
        __props__["log_level"] = log_level
        __props__["metadata"] = metadata
        __props__["name"] = name
        __props__["num_id"] = num_id
        __props__["registry"] = registry
        __props__["state"] = state
        return Device(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def blocked(self) -> pulumi.Output[Optional[bool]]:
        """
        If a device is blocked, connections or requests from this device will fail.
        """
        return pulumi.get(self, "blocked")

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output['outputs.DeviceConfig']:
        """
        The most recent device configuration, which is eventually sent from Cloud IoT Core to the device.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional[List['outputs.DeviceCredential']]]:
        """
        The credentials used to authenticate this device.
        Structure is documented below.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="gatewayConfig")
    def gateway_config(self) -> pulumi.Output[Optional['outputs.DeviceGatewayConfig']]:
        """
        Gateway-related configuration and state.
        Structure is documented below.
        """
        return pulumi.get(self, "gateway_config")

    @property
    @pulumi.getter(name="lastConfigAckTime")
    def last_config_ack_time(self) -> pulumi.Output[str]:
        """
        The last time a cloud-to-device config version acknowledgment was received from the device.
        """
        return pulumi.get(self, "last_config_ack_time")

    @property
    @pulumi.getter(name="lastConfigSendTime")
    def last_config_send_time(self) -> pulumi.Output[str]:
        """
        The last time a cloud-to-device config version was sent to the device.
        """
        return pulumi.get(self, "last_config_send_time")

    @property
    @pulumi.getter(name="lastErrorStatus")
    def last_error_status(self) -> pulumi.Output['outputs.DeviceLastErrorStatus']:
        """
        The error message of the most recent error, such as a failure to publish to Cloud Pub/Sub.
        """
        return pulumi.get(self, "last_error_status")

    @property
    @pulumi.getter(name="lastErrorTime")
    def last_error_time(self) -> pulumi.Output[str]:
        """
        The time the most recent error occurred, such as a failure to publish to Cloud Pub/Sub.
        """
        return pulumi.get(self, "last_error_time")

    @property
    @pulumi.getter(name="lastEventTime")
    def last_event_time(self) -> pulumi.Output[str]:
        """
        The last time a telemetry event was received.
        """
        return pulumi.get(self, "last_event_time")

    @property
    @pulumi.getter(name="lastHeartbeatTime")
    def last_heartbeat_time(self) -> pulumi.Output[str]:
        """
        The last time an MQTT PINGREQ was received.
        """
        return pulumi.get(self, "last_heartbeat_time")

    @property
    @pulumi.getter(name="lastStateTime")
    def last_state_time(self) -> pulumi.Output[str]:
        """
        The last time a state event was received.
        """
        return pulumi.get(self, "last_state_time")

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> pulumi.Output[Optional[str]]:
        """
        The logging verbosity for device activity.
        Possible values are `NONE`, `ERROR`, `INFO`, and `DEBUG`.
        """
        return pulumi.get(self, "log_level")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The metadata key-value pairs assigned to the device.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name for the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numId")
    def num_id(self) -> pulumi.Output[str]:
        """
        A server-defined unique numeric ID for the device. This is a more compact way to identify devices, and it is globally
        unique.
        """
        return pulumi.get(self, "num_id")

    @property
    @pulumi.getter
    def registry(self) -> pulumi.Output[str]:
        """
        The name of the device registry where this device should be created.
        """
        return pulumi.get(self, "registry")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output['outputs.DeviceState']:
        """
        The state most recently received from the device.
        """
        return pulumi.get(self, "state")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

