# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'InstanceNetworkConfig',
]

@pulumi.output_type
class InstanceNetworkConfig(dict):
    def __init__(__self__, *,
                 ip_allocation: str,
                 network: str):
        """
        :param str ip_allocation: The IP range in CIDR notation to use for the managed Data Fusion instance
               nodes. This range must not overlap with any other ranges used in the Data Fusion instance network.
        :param str network: Name of the network in the project with which the tenant project
               will be peered for executing pipelines. In case of shared VPC where the network resides in another host
               project the network should specified in the form of projects/{host-project-id}/global/networks/{network}
        """
        pulumi.set(__self__, "ip_allocation", ip_allocation)
        pulumi.set(__self__, "network", network)

    @property
    @pulumi.getter(name="ipAllocation")
    def ip_allocation(self) -> str:
        """
        The IP range in CIDR notation to use for the managed Data Fusion instance
        nodes. This range must not overlap with any other ranges used in the Data Fusion instance network.
        """
        return pulumi.get(self, "ip_allocation")

    @property
    @pulumi.getter
    def network(self) -> str:
        """
        Name of the network in the project with which the tenant project
        will be peered for executing pipelines. In case of shared VPC where the network resides in another host
        project the network should specified in the form of projects/{host-project-id}/global/networks/{network}
        """
        return pulumi.get(self, "network")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


