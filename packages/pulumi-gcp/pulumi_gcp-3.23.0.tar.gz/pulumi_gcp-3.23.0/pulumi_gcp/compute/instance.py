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
                 allow_stopping_for_update: Optional[pulumi.Input[bool]] = None,
                 attached_disks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceAttachedDiskArgs']]]]] = None,
                 boot_disk: Optional[pulumi.Input[pulumi.InputType['InstanceBootDiskArgs']]] = None,
                 can_ip_forward: Optional[pulumi.Input[bool]] = None,
                 confidential_instance_config: Optional[pulumi.Input[pulumi.InputType['InstanceConfidentialInstanceConfigArgs']]] = None,
                 deletion_protection: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 desired_status: Optional[pulumi.Input[str]] = None,
                 enable_display: Optional[pulumi.Input[bool]] = None,
                 guest_accelerators: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceGuestAcceleratorArgs']]]]] = None,
                 hostname: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 metadata_startup_script: Optional[pulumi.Input[str]] = None,
                 min_cpu_platform: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_interfaces: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkInterfaceArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 resource_policies: Optional[pulumi.Input[str]] = None,
                 scheduling: Optional[pulumi.Input[pulumi.InputType['InstanceSchedulingArgs']]] = None,
                 scratch_disks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceScratchDiskArgs']]]]] = None,
                 service_account: Optional[pulumi.Input[pulumi.InputType['InstanceServiceAccountArgs']]] = None,
                 shielded_instance_config: Optional[pulumi.Input[pulumi.InputType['InstanceShieldedInstanceConfigArgs']]] = None,
                 tags: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a VM instance resource within GCE. For more information see
        [the official documentation](https://cloud.google.com/compute/docs/instances)
        and
        [API](https://cloud.google.com/compute/docs/reference/latest/instances).

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_stopping_for_update: If true, allows this prvider to stop the instance to update its properties.
               If you try to update a property that requires stopping the instance without setting this field, the update will fail.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceAttachedDiskArgs']]]] attached_disks: Additional disks to attach to the instance. Can be repeated multiple times for multiple disks. Structure is documented below.
        :param pulumi.Input[pulumi.InputType['InstanceBootDiskArgs']] boot_disk: The boot disk for the instance.
               Structure is documented below.
        :param pulumi.Input[bool] can_ip_forward: Whether to allow sending and receiving of
               packets with non-matching source or destination IPs.
               This defaults to false.
        :param pulumi.Input[pulumi.InputType['InstanceConfidentialInstanceConfigArgs']] confidential_instance_config: The Confidential VM config being used by the instance. on_host_maintenance has to be set to TERMINATE or this will fail
               to create.
        :param pulumi.Input[bool] deletion_protection: Enable deletion protection on this instance. Defaults to false.
               **Note:** you must disable deletion protection before removing the resource (e.g., via `pulumi destroy`), or the instance cannot be deleted and the provider run will not complete successfully.
        :param pulumi.Input[str] description: A brief description of this resource.
        :param pulumi.Input[str] desired_status: Desired status of the instance. Either
               `"RUNNING"` or `"TERMINATED"`.
        :param pulumi.Input[bool] enable_display: Enable [Virtual Displays](https://cloud.google.com/compute/docs/instances/enable-instance-virtual-display#verify_display_driver) on this instance.
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceGuestAcceleratorArgs']]]] guest_accelerators: List of the type and count of accelerator cards attached to the instance. Structure documented below.
               **Note:** GPU accelerators can only be used with `on_host_maintenance` option set to TERMINATE.
        :param pulumi.Input[str] hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid.
               Valid format is a series of labels 1-63 characters long matching the regular expression `a-z`, concatenated with periods.
               The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A map of key/value label pairs to assign to the instance.
        :param pulumi.Input[str] machine_type: The machine type to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: Metadata key/value pairs to make available from
               within the instance. Ssh keys attached in the Cloud Console will be removed.
               Add them to your config in order to keep them attached to your instance.
        :param pulumi.Input[str] metadata_startup_script: An alternative to using the
               startup-script metadata key, except this one forces the instance to be
               recreated (thus re-running the script) if it is changed. This replaces the
               startup-script metadata key on the created instance and thus the two
               mechanisms are not allowed to be used simultaneously.  Users are free to use
               either mechanism - the only distinction is that this separate attribute
               willl cause a recreate on modification.  On import, `metadata_startup_script`
               will be set, but `metadata.startup-script` will not - if you choose to use the
               other mechanism, you will see a diff immediately after import, which will cause a
               destroy/recreate operation.  You may want to modify your state file manually
               using `pulumi stack` commands, depending on your use case.
        :param pulumi.Input[str] min_cpu_platform: Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as
               `Intel Haswell` or `Intel Skylake`. See the complete list [here](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform).
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[str] name: A unique name for the resource, required by GCE.
               Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkInterfaceArgs']]]] network_interfaces: Networks to attach to the instance. This can
               be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] resource_policies: -- A list of short names or self_links of resource policies to attach to the instance. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported.
        :param pulumi.Input[pulumi.InputType['InstanceSchedulingArgs']] scheduling: The scheduling strategy to use. More details about
               this configuration option are detailed below.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceScratchDiskArgs']]]] scratch_disks: Scratch disks to attach to the instance. This can be
               specified multiple times for multiple scratch disks. Structure is documented below.
        :param pulumi.Input[pulumi.InputType['InstanceServiceAccountArgs']] service_account: Service account to attach to the instance.
               Structure is documented below.
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[pulumi.InputType['InstanceShieldedInstanceConfigArgs']] shielded_instance_config: Enable [Shielded VM](https://cloud.google.com/security/shielded-cloud/shielded-vm) on this instance. Shielded VM provides verifiable integrity to prevent against malware and rootkits. Defaults to disabled. Structure is documented below.
               **Note**: `shielded_instance_config` can only be used with boot images with shielded vm support. See the complete list [here](https://cloud.google.com/compute/docs/images#shielded-images).
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[List[pulumi.Input[str]]] tags: A list of network tags to attach to the instance.
        :param pulumi.Input[str] zone: The zone that the machine should be created in.
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

            __props__['allow_stopping_for_update'] = allow_stopping_for_update
            __props__['attached_disks'] = attached_disks
            if boot_disk is None:
                raise TypeError("Missing required property 'boot_disk'")
            __props__['boot_disk'] = boot_disk
            __props__['can_ip_forward'] = can_ip_forward
            __props__['confidential_instance_config'] = confidential_instance_config
            __props__['deletion_protection'] = deletion_protection
            __props__['description'] = description
            __props__['desired_status'] = desired_status
            __props__['enable_display'] = enable_display
            __props__['guest_accelerators'] = guest_accelerators
            __props__['hostname'] = hostname
            __props__['labels'] = labels
            if machine_type is None:
                raise TypeError("Missing required property 'machine_type'")
            __props__['machine_type'] = machine_type
            __props__['metadata'] = metadata
            __props__['metadata_startup_script'] = metadata_startup_script
            __props__['min_cpu_platform'] = min_cpu_platform
            __props__['name'] = name
            if network_interfaces is None:
                raise TypeError("Missing required property 'network_interfaces'")
            __props__['network_interfaces'] = network_interfaces
            __props__['project'] = project
            __props__['resource_policies'] = resource_policies
            __props__['scheduling'] = scheduling
            __props__['scratch_disks'] = scratch_disks
            __props__['service_account'] = service_account
            __props__['shielded_instance_config'] = shielded_instance_config
            __props__['tags'] = tags
            __props__['zone'] = zone
            __props__['cpu_platform'] = None
            __props__['current_status'] = None
            __props__['instance_id'] = None
            __props__['label_fingerprint'] = None
            __props__['metadata_fingerprint'] = None
            __props__['self_link'] = None
            __props__['tags_fingerprint'] = None
        super(Instance, __self__).__init__(
            'gcp:compute/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_stopping_for_update: Optional[pulumi.Input[bool]] = None,
            attached_disks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceAttachedDiskArgs']]]]] = None,
            boot_disk: Optional[pulumi.Input[pulumi.InputType['InstanceBootDiskArgs']]] = None,
            can_ip_forward: Optional[pulumi.Input[bool]] = None,
            confidential_instance_config: Optional[pulumi.Input[pulumi.InputType['InstanceConfidentialInstanceConfigArgs']]] = None,
            cpu_platform: Optional[pulumi.Input[str]] = None,
            current_status: Optional[pulumi.Input[str]] = None,
            deletion_protection: Optional[pulumi.Input[bool]] = None,
            description: Optional[pulumi.Input[str]] = None,
            desired_status: Optional[pulumi.Input[str]] = None,
            enable_display: Optional[pulumi.Input[bool]] = None,
            guest_accelerators: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceGuestAcceleratorArgs']]]]] = None,
            hostname: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            label_fingerprint: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            machine_type: Optional[pulumi.Input[str]] = None,
            metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            metadata_fingerprint: Optional[pulumi.Input[str]] = None,
            metadata_startup_script: Optional[pulumi.Input[str]] = None,
            min_cpu_platform: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network_interfaces: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkInterfaceArgs']]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            resource_policies: Optional[pulumi.Input[str]] = None,
            scheduling: Optional[pulumi.Input[pulumi.InputType['InstanceSchedulingArgs']]] = None,
            scratch_disks: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceScratchDiskArgs']]]]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            service_account: Optional[pulumi.Input[pulumi.InputType['InstanceServiceAccountArgs']]] = None,
            shielded_instance_config: Optional[pulumi.Input[pulumi.InputType['InstanceShieldedInstanceConfigArgs']]] = None,
            tags: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            tags_fingerprint: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_stopping_for_update: If true, allows this prvider to stop the instance to update its properties.
               If you try to update a property that requires stopping the instance without setting this field, the update will fail.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceAttachedDiskArgs']]]] attached_disks: Additional disks to attach to the instance. Can be repeated multiple times for multiple disks. Structure is documented below.
        :param pulumi.Input[pulumi.InputType['InstanceBootDiskArgs']] boot_disk: The boot disk for the instance.
               Structure is documented below.
        :param pulumi.Input[bool] can_ip_forward: Whether to allow sending and receiving of
               packets with non-matching source or destination IPs.
               This defaults to false.
        :param pulumi.Input[pulumi.InputType['InstanceConfidentialInstanceConfigArgs']] confidential_instance_config: The Confidential VM config being used by the instance. on_host_maintenance has to be set to TERMINATE or this will fail
               to create.
        :param pulumi.Input[str] cpu_platform: The CPU platform used by this instance.
        :param pulumi.Input[str] current_status: Current status of the instance.
        :param pulumi.Input[bool] deletion_protection: Enable deletion protection on this instance. Defaults to false.
               **Note:** you must disable deletion protection before removing the resource (e.g., via `pulumi destroy`), or the instance cannot be deleted and the provider run will not complete successfully.
        :param pulumi.Input[str] description: A brief description of this resource.
        :param pulumi.Input[str] desired_status: Desired status of the instance. Either
               `"RUNNING"` or `"TERMINATED"`.
        :param pulumi.Input[bool] enable_display: Enable [Virtual Displays](https://cloud.google.com/compute/docs/instances/enable-instance-virtual-display#verify_display_driver) on this instance.
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceGuestAcceleratorArgs']]]] guest_accelerators: List of the type and count of accelerator cards attached to the instance. Structure documented below.
               **Note:** GPU accelerators can only be used with `on_host_maintenance` option set to TERMINATE.
        :param pulumi.Input[str] hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid.
               Valid format is a series of labels 1-63 characters long matching the regular expression `a-z`, concatenated with periods.
               The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created.
        :param pulumi.Input[str] instance_id: The server-assigned unique identifier of this instance.
        :param pulumi.Input[str] label_fingerprint: The unique fingerprint of the labels.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: A map of key/value label pairs to assign to the instance.
        :param pulumi.Input[str] machine_type: The machine type to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: Metadata key/value pairs to make available from
               within the instance. Ssh keys attached in the Cloud Console will be removed.
               Add them to your config in order to keep them attached to your instance.
        :param pulumi.Input[str] metadata_fingerprint: The unique fingerprint of the metadata.
        :param pulumi.Input[str] metadata_startup_script: An alternative to using the
               startup-script metadata key, except this one forces the instance to be
               recreated (thus re-running the script) if it is changed. This replaces the
               startup-script metadata key on the created instance and thus the two
               mechanisms are not allowed to be used simultaneously.  Users are free to use
               either mechanism - the only distinction is that this separate attribute
               willl cause a recreate on modification.  On import, `metadata_startup_script`
               will be set, but `metadata.startup-script` will not - if you choose to use the
               other mechanism, you will see a diff immediately after import, which will cause a
               destroy/recreate operation.  You may want to modify your state file manually
               using `pulumi stack` commands, depending on your use case.
        :param pulumi.Input[str] min_cpu_platform: Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as
               `Intel Haswell` or `Intel Skylake`. See the complete list [here](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform).
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[str] name: A unique name for the resource, required by GCE.
               Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceNetworkInterfaceArgs']]]] network_interfaces: Networks to attach to the instance. This can
               be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] resource_policies: -- A list of short names or self_links of resource policies to attach to the instance. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported.
        :param pulumi.Input[pulumi.InputType['InstanceSchedulingArgs']] scheduling: The scheduling strategy to use. More details about
               this configuration option are detailed below.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['InstanceScratchDiskArgs']]]] scratch_disks: Scratch disks to attach to the instance. This can be
               specified multiple times for multiple scratch disks. Structure is documented below.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[pulumi.InputType['InstanceServiceAccountArgs']] service_account: Service account to attach to the instance.
               Structure is documented below.
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[pulumi.InputType['InstanceShieldedInstanceConfigArgs']] shielded_instance_config: Enable [Shielded VM](https://cloud.google.com/security/shielded-cloud/shielded-vm) on this instance. Shielded VM provides verifiable integrity to prevent against malware and rootkits. Defaults to disabled. Structure is documented below.
               **Note**: `shielded_instance_config` can only be used with boot images with shielded vm support. See the complete list [here](https://cloud.google.com/compute/docs/images#shielded-images).
               **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        :param pulumi.Input[List[pulumi.Input[str]]] tags: A list of network tags to attach to the instance.
        :param pulumi.Input[str] tags_fingerprint: The unique fingerprint of the tags.
        :param pulumi.Input[str] zone: The zone that the machine should be created in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allow_stopping_for_update"] = allow_stopping_for_update
        __props__["attached_disks"] = attached_disks
        __props__["boot_disk"] = boot_disk
        __props__["can_ip_forward"] = can_ip_forward
        __props__["confidential_instance_config"] = confidential_instance_config
        __props__["cpu_platform"] = cpu_platform
        __props__["current_status"] = current_status
        __props__["deletion_protection"] = deletion_protection
        __props__["description"] = description
        __props__["desired_status"] = desired_status
        __props__["enable_display"] = enable_display
        __props__["guest_accelerators"] = guest_accelerators
        __props__["hostname"] = hostname
        __props__["instance_id"] = instance_id
        __props__["label_fingerprint"] = label_fingerprint
        __props__["labels"] = labels
        __props__["machine_type"] = machine_type
        __props__["metadata"] = metadata
        __props__["metadata_fingerprint"] = metadata_fingerprint
        __props__["metadata_startup_script"] = metadata_startup_script
        __props__["min_cpu_platform"] = min_cpu_platform
        __props__["name"] = name
        __props__["network_interfaces"] = network_interfaces
        __props__["project"] = project
        __props__["resource_policies"] = resource_policies
        __props__["scheduling"] = scheduling
        __props__["scratch_disks"] = scratch_disks
        __props__["self_link"] = self_link
        __props__["service_account"] = service_account
        __props__["shielded_instance_config"] = shielded_instance_config
        __props__["tags"] = tags
        __props__["tags_fingerprint"] = tags_fingerprint
        __props__["zone"] = zone
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowStoppingForUpdate")
    def allow_stopping_for_update(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, allows this prvider to stop the instance to update its properties.
        If you try to update a property that requires stopping the instance without setting this field, the update will fail.
        """
        return pulumi.get(self, "allow_stopping_for_update")

    @property
    @pulumi.getter(name="attachedDisks")
    def attached_disks(self) -> pulumi.Output[Optional[List['outputs.InstanceAttachedDisk']]]:
        """
        Additional disks to attach to the instance. Can be repeated multiple times for multiple disks. Structure is documented below.
        """
        return pulumi.get(self, "attached_disks")

    @property
    @pulumi.getter(name="bootDisk")
    def boot_disk(self) -> pulumi.Output['outputs.InstanceBootDisk']:
        """
        The boot disk for the instance.
        Structure is documented below.
        """
        return pulumi.get(self, "boot_disk")

    @property
    @pulumi.getter(name="canIpForward")
    def can_ip_forward(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to allow sending and receiving of
        packets with non-matching source or destination IPs.
        This defaults to false.
        """
        return pulumi.get(self, "can_ip_forward")

    @property
    @pulumi.getter(name="confidentialInstanceConfig")
    def confidential_instance_config(self) -> pulumi.Output['outputs.InstanceConfidentialInstanceConfig']:
        """
        The Confidential VM config being used by the instance. on_host_maintenance has to be set to TERMINATE or this will fail
        to create.
        """
        return pulumi.get(self, "confidential_instance_config")

    @property
    @pulumi.getter(name="cpuPlatform")
    def cpu_platform(self) -> pulumi.Output[str]:
        """
        The CPU platform used by this instance.
        """
        return pulumi.get(self, "cpu_platform")

    @property
    @pulumi.getter(name="currentStatus")
    def current_status(self) -> pulumi.Output[str]:
        """
        Current status of the instance.
        """
        return pulumi.get(self, "current_status")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable deletion protection on this instance. Defaults to false.
        **Note:** you must disable deletion protection before removing the resource (e.g., via `pulumi destroy`), or the instance cannot be deleted and the provider run will not complete successfully.
        """
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A brief description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="desiredStatus")
    def desired_status(self) -> pulumi.Output[Optional[str]]:
        """
        Desired status of the instance. Either
        `"RUNNING"` or `"TERMINATED"`.
        """
        return pulumi.get(self, "desired_status")

    @property
    @pulumi.getter(name="enableDisplay")
    def enable_display(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable [Virtual Displays](https://cloud.google.com/compute/docs/instances/enable-instance-virtual-display#verify_display_driver) on this instance.
        **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        """
        return pulumi.get(self, "enable_display")

    @property
    @pulumi.getter(name="guestAccelerators")
    def guest_accelerators(self) -> pulumi.Output[List['outputs.InstanceGuestAccelerator']]:
        """
        List of the type and count of accelerator cards attached to the instance. Structure documented below.
        **Note:** GPU accelerators can only be used with `on_host_maintenance` option set to TERMINATE.
        """
        return pulumi.get(self, "guest_accelerators")

    @property
    @pulumi.getter
    def hostname(self) -> pulumi.Output[Optional[str]]:
        """
        A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid.
        Valid format is a series of labels 1-63 characters long matching the regular expression `a-z`, concatenated with periods.
        The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The server-assigned unique identifier of this instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="labelFingerprint")
    def label_fingerprint(self) -> pulumi.Output[str]:
        """
        The unique fingerprint of the labels.
        """
        return pulumi.get(self, "label_fingerprint")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of key/value label pairs to assign to the instance.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> pulumi.Output[str]:
        """
        The machine type to create.
        """
        return pulumi.get(self, "machine_type")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Metadata key/value pairs to make available from
        within the instance. Ssh keys attached in the Cloud Console will be removed.
        Add them to your config in order to keep them attached to your instance.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter(name="metadataFingerprint")
    def metadata_fingerprint(self) -> pulumi.Output[str]:
        """
        The unique fingerprint of the metadata.
        """
        return pulumi.get(self, "metadata_fingerprint")

    @property
    @pulumi.getter(name="metadataStartupScript")
    def metadata_startup_script(self) -> pulumi.Output[Optional[str]]:
        """
        An alternative to using the
        startup-script metadata key, except this one forces the instance to be
        recreated (thus re-running the script) if it is changed. This replaces the
        startup-script metadata key on the created instance and thus the two
        mechanisms are not allowed to be used simultaneously.  Users are free to use
        either mechanism - the only distinction is that this separate attribute
        willl cause a recreate on modification.  On import, `metadata_startup_script`
        will be set, but `metadata.startup-script` will not - if you choose to use the
        other mechanism, you will see a diff immediately after import, which will cause a
        destroy/recreate operation.  You may want to modify your state file manually
        using `pulumi stack` commands, depending on your use case.
        """
        return pulumi.get(self, "metadata_startup_script")

    @property
    @pulumi.getter(name="minCpuPlatform")
    def min_cpu_platform(self) -> pulumi.Output[str]:
        """
        Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as
        `Intel Haswell` or `Intel Skylake`. See the complete list [here](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform).
        **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        """
        return pulumi.get(self, "min_cpu_platform")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name for the resource, required by GCE.
        Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> pulumi.Output[List['outputs.InstanceNetworkInterface']]:
        """
        Networks to attach to the instance. This can
        be specified multiple times. Structure is documented below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="resourcePolicies")
    def resource_policies(self) -> pulumi.Output[Optional[str]]:
        """
        -- A list of short names or self_links of resource policies to attach to the instance. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported.
        """
        return pulumi.get(self, "resource_policies")

    @property
    @pulumi.getter
    def scheduling(self) -> pulumi.Output['outputs.InstanceScheduling']:
        """
        The scheduling strategy to use. More details about
        this configuration option are detailed below.
        """
        return pulumi.get(self, "scheduling")

    @property
    @pulumi.getter(name="scratchDisks")
    def scratch_disks(self) -> pulumi.Output[Optional[List['outputs.InstanceScratchDisk']]]:
        """
        Scratch disks to attach to the instance. This can be
        specified multiple times for multiple scratch disks. Structure is documented below.
        """
        return pulumi.get(self, "scratch_disks")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Output[Optional['outputs.InstanceServiceAccount']]:
        """
        Service account to attach to the instance.
        Structure is documented below.
        **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter(name="shieldedInstanceConfig")
    def shielded_instance_config(self) -> pulumi.Output['outputs.InstanceShieldedInstanceConfig']:
        """
        Enable [Shielded VM](https://cloud.google.com/security/shielded-cloud/shielded-vm) on this instance. Shielded VM provides verifiable integrity to prevent against malware and rootkits. Defaults to disabled. Structure is documented below.
        **Note**: `shielded_instance_config` can only be used with boot images with shielded vm support. See the complete list [here](https://cloud.google.com/compute/docs/images#shielded-images).
        **Note**: `allow_stopping_for_update` must be set to true or your instance must have a `desired_status` of `TERMINATED` in order to update this field.
        """
        return pulumi.get(self, "shielded_instance_config")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[List[str]]]:
        """
        A list of network tags to attach to the instance.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsFingerprint")
    def tags_fingerprint(self) -> pulumi.Output[str]:
        """
        The unique fingerprint of the tags.
        """
        return pulumi.get(self, "tags_fingerprint")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        """
        The zone that the machine should be created in.
        """
        return pulumi.get(self, "zone")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

