# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['JobIAMPolicy']


class JobIAMPolicy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 job_id: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Three different resources help you manage IAM policies on dataproc jobs. Each of these resources serves a different use case:

        * `dataproc.JobIAMPolicy`: Authoritative. Sets the IAM policy for the job and replaces any existing policy already attached.
        * `dataproc.JobIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the job are preserved.
        * `dataproc.JobIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the job are preserved.

        > **Note:** `dataproc.JobIAMPolicy` **cannot** be used in conjunction with `dataproc.JobIAMBinding` and `dataproc.JobIAMMember` or they will fight over what your policy should be. In addition, be careful not to accidentally unset ownership of the job as `dataproc.JobIAMPolicy` replaces the entire policy.

        > **Note:** `dataproc.JobIAMBinding` resources **can be** used in conjunction with `dataproc.JobIAMMember` resources **only if** they do not grant privilege to the same role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_data: The policy data generated by a `organizations.getIAMPolicy` data source.
        :param pulumi.Input[str] project: The project in which the job belongs. If it
               is not provided, the provider will use a default.
        :param pulumi.Input[str] region: The region in which the job belongs. If it
               is not provided, the provider will use a default.
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

            if job_id is None:
                raise TypeError("Missing required property 'job_id'")
            __props__['job_id'] = job_id
            if policy_data is None:
                raise TypeError("Missing required property 'policy_data'")
            __props__['policy_data'] = policy_data
            __props__['project'] = project
            __props__['region'] = region
            __props__['etag'] = None
        super(JobIAMPolicy, __self__).__init__(
            'gcp:dataproc/jobIAMPolicy:JobIAMPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            etag: Optional[pulumi.Input[str]] = None,
            job_id: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None) -> 'JobIAMPolicy':
        """
        Get an existing JobIAMPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the jobs's IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by a `organizations.getIAMPolicy` data source.
        :param pulumi.Input[str] project: The project in which the job belongs. If it
               is not provided, the provider will use a default.
        :param pulumi.Input[str] region: The region in which the job belongs. If it
               is not provided, the provider will use a default.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["etag"] = etag
        __props__["job_id"] = job_id
        __props__["policy_data"] = policy_data
        __props__["project"] = project
        __props__["region"] = region
        return JobIAMPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the jobs's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="jobId")
    def job_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "job_id")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Output[str]:
        """
        The policy data generated by a `organizations.getIAMPolicy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project in which the job belongs. If it
        is not provided, the provider will use a default.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region in which the job belongs. If it
        is not provided, the provider will use a default.
        """
        return pulumi.get(self, "region")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

