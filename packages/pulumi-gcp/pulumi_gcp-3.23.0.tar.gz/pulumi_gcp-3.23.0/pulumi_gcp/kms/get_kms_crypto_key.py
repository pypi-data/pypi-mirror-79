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
    'GetKMSCryptoKeyResult',
    'AwaitableGetKMSCryptoKeyResult',
    'get_kms_crypto_key',
]

@pulumi.output_type
class GetKMSCryptoKeyResult:
    """
    A collection of values returned by getKMSCryptoKey.
    """
    def __init__(__self__, id=None, key_ring=None, labels=None, name=None, purpose=None, rotation_period=None, self_link=None, version_templates=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_ring and not isinstance(key_ring, str):
            raise TypeError("Expected argument 'key_ring' to be a str")
        pulumi.set(__self__, "key_ring", key_ring)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if purpose and not isinstance(purpose, str):
            raise TypeError("Expected argument 'purpose' to be a str")
        pulumi.set(__self__, "purpose", purpose)
        if rotation_period and not isinstance(rotation_period, str):
            raise TypeError("Expected argument 'rotation_period' to be a str")
        pulumi.set(__self__, "rotation_period", rotation_period)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if version_templates and not isinstance(version_templates, list):
            raise TypeError("Expected argument 'version_templates' to be a list")
        pulumi.set(__self__, "version_templates", version_templates)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyRing")
    def key_ring(self) -> str:
        return pulumi.get(self, "key_ring")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def purpose(self) -> str:
        """
        Defines the cryptographic capabilities of the key.
        """
        return pulumi.get(self, "purpose")

    @property
    @pulumi.getter(name="rotationPeriod")
    def rotation_period(self) -> str:
        """
        Every time this period passes, generate a new CryptoKeyVersion and set it as
        the primary. The first rotation will take place after the specified period. The rotation period has the format
        of a decimal number with up to 9 fractional digits, followed by the letter s (seconds).
        """
        return pulumi.get(self, "rotation_period")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        The self link of the created CryptoKey. Its format is `projects/{projectId}/locations/{location}/keyRings/{keyRingName}/cryptoKeys/{cryptoKeyName}`.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="versionTemplates")
    def version_templates(self) -> List['outputs.GetKMSCryptoKeyVersionTemplateResult']:
        return pulumi.get(self, "version_templates")


class AwaitableGetKMSCryptoKeyResult(GetKMSCryptoKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKMSCryptoKeyResult(
            id=self.id,
            key_ring=self.key_ring,
            labels=self.labels,
            name=self.name,
            purpose=self.purpose,
            rotation_period=self.rotation_period,
            self_link=self.self_link,
            version_templates=self.version_templates)


def get_kms_crypto_key(key_ring: Optional[str] = None,
                       name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKMSCryptoKeyResult:
    """
    Provides access to a Google Cloud Platform KMS CryptoKey. For more information see
    [the official documentation](https://cloud.google.com/kms/docs/object-hierarchy#key)
    and
    [API](https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys).

    A CryptoKey is an interface to key material which can be used to encrypt and decrypt data. A CryptoKey belongs to a
    Google Cloud KMS KeyRing.


    :param str key_ring: The `self_link` of the Google Cloud Platform KeyRing to which the key belongs.
    :param str name: The CryptoKey's name.
           A CryptoKey’s name belonging to the specified Google Cloud Platform KeyRing and match the regular expression `[a-zA-Z0-9_-]{1,63}`
    """
    __args__ = dict()
    __args__['keyRing'] = key_ring
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:kms/getKMSCryptoKey:getKMSCryptoKey', __args__, opts=opts, typ=GetKMSCryptoKeyResult).value

    return AwaitableGetKMSCryptoKeyResult(
        id=__ret__.id,
        key_ring=__ret__.key_ring,
        labels=__ret__.labels,
        name=__ret__.name,
        purpose=__ret__.purpose,
        rotation_period=__ret__.rotation_period,
        self_link=__ret__.self_link,
        version_templates=__ret__.version_templates)
