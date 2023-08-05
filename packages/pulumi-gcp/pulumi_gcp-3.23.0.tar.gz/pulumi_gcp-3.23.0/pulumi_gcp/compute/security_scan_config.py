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

__all__ = ['SecurityScanConfig']


class SecurityScanConfig(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[pulumi.InputType['SecurityScanConfigAuthenticationArgs']]] = None,
                 blacklist_patterns: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 export_to_security_command_center: Optional[pulumi.Input[str]] = None,
                 max_qps: Optional[pulumi.Input[float]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['SecurityScanConfigScheduleArgs']]] = None,
                 starting_urls: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 target_platforms: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 user_agent: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A ScanConfig resource contains the configurations to launch a scan.

        To get more information about ScanConfig, see:

        * [API documentation](https://cloud.google.com/security-scanner/docs/reference/rest/v1beta/projects.scanConfigs)
        * How-to Guides
            * [Using Cloud Security Scanner](https://cloud.google.com/security-scanner/docs/scanning)

        > **Warning:** All arguments including `authentication.google_account.password` and `authentication.custom_account.password` will be stored in the raw
        state as plain-text.[Read more about secrets in state](https://www.pulumi.com/docs/intro/concepts/programming-model/#secrets)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SecurityScanConfigAuthenticationArgs']] authentication: The authentication configuration.
               If specified, service will use the authentication configuration during scanning.
               Structure is documented below.
        :param pulumi.Input[List[pulumi.Input[str]]] blacklist_patterns: The blacklist URL patterns as described in
               https://cloud.google.com/security-scanner/docs/excluded-urls
        :param pulumi.Input[str] display_name: The user provider display name of the ScanConfig.
        :param pulumi.Input[str] export_to_security_command_center: Controls export of scan configurations and results to Cloud Security Command Center.
               Default value is `ENABLED`.
               Possible values are `ENABLED` and `DISABLED`.
        :param pulumi.Input[float] max_qps: The maximum QPS during scanning. A valid value ranges from 5 to 20 inclusively.
               Defaults to 15.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[pulumi.InputType['SecurityScanConfigScheduleArgs']] schedule: The schedule of the ScanConfig
               Structure is documented below.
        :param pulumi.Input[List[pulumi.Input[str]]] starting_urls: The starting URLs from which the scanner finds site pages.
        :param pulumi.Input[List[pulumi.Input[str]]] target_platforms: Set of Cloud Platforms targeted by the scan. If empty, APP_ENGINE will be used as a default.
               Each value may be one of `APP_ENGINE` and `COMPUTE`.
        :param pulumi.Input[str] user_agent: Type of the user agents used for scanning
               Default value is `CHROME_LINUX`.
               Possible values are `USER_AGENT_UNSPECIFIED`, `CHROME_LINUX`, `CHROME_ANDROID`, and `SAFARI_IPHONE`.
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

            __props__['authentication'] = authentication
            __props__['blacklist_patterns'] = blacklist_patterns
            if display_name is None:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            __props__['export_to_security_command_center'] = export_to_security_command_center
            __props__['max_qps'] = max_qps
            __props__['project'] = project
            __props__['schedule'] = schedule
            if starting_urls is None:
                raise TypeError("Missing required property 'starting_urls'")
            __props__['starting_urls'] = starting_urls
            __props__['target_platforms'] = target_platforms
            __props__['user_agent'] = user_agent
            __props__['name'] = None
        super(SecurityScanConfig, __self__).__init__(
            'gcp:compute/securityScanConfig:SecurityScanConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authentication: Optional[pulumi.Input[pulumi.InputType['SecurityScanConfigAuthenticationArgs']]] = None,
            blacklist_patterns: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            export_to_security_command_center: Optional[pulumi.Input[str]] = None,
            max_qps: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            schedule: Optional[pulumi.Input[pulumi.InputType['SecurityScanConfigScheduleArgs']]] = None,
            starting_urls: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            target_platforms: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            user_agent: Optional[pulumi.Input[str]] = None) -> 'SecurityScanConfig':
        """
        Get an existing SecurityScanConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SecurityScanConfigAuthenticationArgs']] authentication: The authentication configuration.
               If specified, service will use the authentication configuration during scanning.
               Structure is documented below.
        :param pulumi.Input[List[pulumi.Input[str]]] blacklist_patterns: The blacklist URL patterns as described in
               https://cloud.google.com/security-scanner/docs/excluded-urls
        :param pulumi.Input[str] display_name: The user provider display name of the ScanConfig.
        :param pulumi.Input[str] export_to_security_command_center: Controls export of scan configurations and results to Cloud Security Command Center.
               Default value is `ENABLED`.
               Possible values are `ENABLED` and `DISABLED`.
        :param pulumi.Input[float] max_qps: The maximum QPS during scanning. A valid value ranges from 5 to 20 inclusively.
               Defaults to 15.
        :param pulumi.Input[str] name: A server defined name for this index. Format: 'projects/{{project}}/scanConfigs/{{server_generated_id}}'
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[pulumi.InputType['SecurityScanConfigScheduleArgs']] schedule: The schedule of the ScanConfig
               Structure is documented below.
        :param pulumi.Input[List[pulumi.Input[str]]] starting_urls: The starting URLs from which the scanner finds site pages.
        :param pulumi.Input[List[pulumi.Input[str]]] target_platforms: Set of Cloud Platforms targeted by the scan. If empty, APP_ENGINE will be used as a default.
               Each value may be one of `APP_ENGINE` and `COMPUTE`.
        :param pulumi.Input[str] user_agent: Type of the user agents used for scanning
               Default value is `CHROME_LINUX`.
               Possible values are `USER_AGENT_UNSPECIFIED`, `CHROME_LINUX`, `CHROME_ANDROID`, and `SAFARI_IPHONE`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["authentication"] = authentication
        __props__["blacklist_patterns"] = blacklist_patterns
        __props__["display_name"] = display_name
        __props__["export_to_security_command_center"] = export_to_security_command_center
        __props__["max_qps"] = max_qps
        __props__["name"] = name
        __props__["project"] = project
        __props__["schedule"] = schedule
        __props__["starting_urls"] = starting_urls
        __props__["target_platforms"] = target_platforms
        __props__["user_agent"] = user_agent
        return SecurityScanConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Output[Optional['outputs.SecurityScanConfigAuthentication']]:
        """
        The authentication configuration.
        If specified, service will use the authentication configuration during scanning.
        Structure is documented below.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="blacklistPatterns")
    def blacklist_patterns(self) -> pulumi.Output[Optional[List[str]]]:
        """
        The blacklist URL patterns as described in
        https://cloud.google.com/security-scanner/docs/excluded-urls
        """
        return pulumi.get(self, "blacklist_patterns")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The user provider display name of the ScanConfig.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="exportToSecurityCommandCenter")
    def export_to_security_command_center(self) -> pulumi.Output[Optional[str]]:
        """
        Controls export of scan configurations and results to Cloud Security Command Center.
        Default value is `ENABLED`.
        Possible values are `ENABLED` and `DISABLED`.
        """
        return pulumi.get(self, "export_to_security_command_center")

    @property
    @pulumi.getter(name="maxQps")
    def max_qps(self) -> pulumi.Output[Optional[float]]:
        """
        The maximum QPS during scanning. A valid value ranges from 5 to 20 inclusively.
        Defaults to 15.
        """
        return pulumi.get(self, "max_qps")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A server defined name for this index. Format: 'projects/{{project}}/scanConfigs/{{server_generated_id}}'
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
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional['outputs.SecurityScanConfigSchedule']]:
        """
        The schedule of the ScanConfig
        Structure is documented below.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="startingUrls")
    def starting_urls(self) -> pulumi.Output[List[str]]:
        """
        The starting URLs from which the scanner finds site pages.
        """
        return pulumi.get(self, "starting_urls")

    @property
    @pulumi.getter(name="targetPlatforms")
    def target_platforms(self) -> pulumi.Output[Optional[List[str]]]:
        """
        Set of Cloud Platforms targeted by the scan. If empty, APP_ENGINE will be used as a default.
        Each value may be one of `APP_ENGINE` and `COMPUTE`.
        """
        return pulumi.get(self, "target_platforms")

    @property
    @pulumi.getter(name="userAgent")
    def user_agent(self) -> pulumi.Output[Optional[str]]:
        """
        Type of the user agents used for scanning
        Default value is `CHROME_LINUX`.
        Possible values are `USER_AGENT_UNSPECIFIED`, `CHROME_LINUX`, `CHROME_ANDROID`, and `SAFARI_IPHONE`.
        """
        return pulumi.get(self, "user_agent")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

