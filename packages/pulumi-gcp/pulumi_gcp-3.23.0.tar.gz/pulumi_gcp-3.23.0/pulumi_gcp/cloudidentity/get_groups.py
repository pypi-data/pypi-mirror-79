# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetGroupsResult',
    'AwaitableGetGroupsResult',
    'get_groups',
]

@pulumi.output_type
class GetGroupsResult:
    """
    A collection of values returned by getGroups.
    """
    def __init__(__self__, groups=None, id=None, parent=None):
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if parent and not isinstance(parent, str):
            raise TypeError("Expected argument 'parent' to be a str")
        pulumi.set(__self__, "parent", parent)

    @property
    @pulumi.getter
    def groups(self) -> List['outputs.GetGroupsGroupResult']:
        """
        The list of groups under the provided customer or namespace. Structure is documented below.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def parent(self) -> str:
        return pulumi.get(self, "parent")


class AwaitableGetGroupsResult(GetGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupsResult(
            groups=self.groups,
            id=self.id,
            parent=self.parent)


def get_groups(parent: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupsResult:
    """
    Use this data source to get list of the Cloud Identity Groups under a customer or namespace.

    https://cloud.google.com/identity/docs/concepts/overview#groups


    :param str parent: The parent resource under which to list all Groups. Must be of the form identitysources/{identity_source_id} for external- identity-mapped groups or customers/{customer_id} for Google Groups.
    """
    __args__ = dict()
    __args__['parent'] = parent
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:cloudidentity/getGroups:getGroups', __args__, opts=opts, typ=GetGroupsResult).value

    return AwaitableGetGroupsResult(
        groups=__ret__.groups,
        id=__ret__.id,
        parent=__ret__.parent)
