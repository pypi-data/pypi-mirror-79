# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['Job']


class Job(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_experiments: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 ip_configuration: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 max_workers: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 on_delete: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 service_account_email: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 temp_gcs_location: Optional[pulumi.Input[str]] = None,
                 template_gcs_path: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates a job on Dataflow, which is an implementation of Apache Beam running on Google Compute Engine. For more information see
        the official documentation for
        [Beam](https://beam.apache.org) and [Dataflow](https://cloud.google.com/dataflow/).

        ## Note on "destroy" / "apply"

        There are many types of Dataflow jobs.  Some Dataflow jobs run constantly, getting new data from (e.g.) a GCS bucket, and outputting data continuously.  Some jobs process a set amount of data then terminate.  All jobs can fail while running due to programming errors or other issues.  In this way, Dataflow jobs are different from most other Google resources.

        The Dataflow resource is considered 'existing' while it is in a nonterminal state.  If it reaches a terminal state (e.g. 'FAILED', 'COMPLETE', 'CANCELLED'), it will be recreated on the next 'apply'.  This is as expected for jobs which run continuously, but may surprise users who use this resource for other kinds of Dataflow jobs.

        A Dataflow job which is 'destroyed' may be "cancelled" or "drained".  If "cancelled", the job terminates - any data written remains where it is, but no new data will be processed.  If "drained", no new data will enter the pipeline, but any data currently in the pipeline will finish being processed.  The default is "cancelled", but if a user sets `on_delete` to `"drain"` in the configuration, you may experience a long wait for your `pulumi destroy` to complete.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] additional_experiments: List of experiments that should be used by the job. An example value is `["enable_stackdriver_agent_metrics"]`.
        :param pulumi.Input[str] ip_configuration: The configuration for VM IPs.  Options are `"WORKER_IP_PUBLIC"` or `"WORKER_IP_PRIVATE"`.
        :param pulumi.Input[Mapping[str, Any]] labels: User labels to be specified for the job. Keys and values should follow the restrictions
               specified in the [labeling restrictions](https://cloud.google.com/compute/docs/labeling-resources#restrictions) page.
               **NOTE**: Google-provided Dataflow templates often provide default labels that begin with `goog-dataflow-provided`.
               Unless explicitly set in config, these labels will be ignored to prevent diffs on re-apply.
        :param pulumi.Input[str] machine_type: The machine type to use for the job.
        :param pulumi.Input[float] max_workers: The number of workers permitted to work on the job.  More workers may improve processing speed at additional cost.
        :param pulumi.Input[str] name: A unique name for the resource, required by Dataflow.
        :param pulumi.Input[str] network: The network to which VMs will be assigned. If it is not provided, "default" will be used.
        :param pulumi.Input[str] on_delete: One of "drain" or "cancel".  Specifies behavior of deletion during `pulumi destroy`.  See above note.
        :param pulumi.Input[Mapping[str, Any]] parameters: Key/Value pairs to be passed to the Dataflow job (as used in the template).
        :param pulumi.Input[str] project: The project in which the resource belongs. If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region in which the created job should run.
        :param pulumi.Input[str] service_account_email: The Service Account email used to create the job.
        :param pulumi.Input[str] subnetwork: The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK".
        :param pulumi.Input[str] temp_gcs_location: A writeable location on GCS for the Dataflow job to dump its temporary data.
        :param pulumi.Input[str] template_gcs_path: The GCS path to the Dataflow job template.
        :param pulumi.Input[str] zone: The zone in which the created job should run. If it is not provided, the provider zone is used.
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

            __props__['additional_experiments'] = additional_experiments
            __props__['ip_configuration'] = ip_configuration
            __props__['labels'] = labels
            __props__['machine_type'] = machine_type
            __props__['max_workers'] = max_workers
            __props__['name'] = name
            __props__['network'] = network
            __props__['on_delete'] = on_delete
            __props__['parameters'] = parameters
            __props__['project'] = project
            __props__['region'] = region
            __props__['service_account_email'] = service_account_email
            __props__['subnetwork'] = subnetwork
            if temp_gcs_location is None:
                raise TypeError("Missing required property 'temp_gcs_location'")
            __props__['temp_gcs_location'] = temp_gcs_location
            if template_gcs_path is None:
                raise TypeError("Missing required property 'template_gcs_path'")
            __props__['template_gcs_path'] = template_gcs_path
            __props__['zone'] = zone
            __props__['job_id'] = None
            __props__['state'] = None
            __props__['type'] = None
        super(Job, __self__).__init__(
            'gcp:dataflow/job:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            additional_experiments: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            ip_configuration: Optional[pulumi.Input[str]] = None,
            job_id: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            machine_type: Optional[pulumi.Input[str]] = None,
            max_workers: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            on_delete: Optional[pulumi.Input[str]] = None,
            parameters: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            service_account_email: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            subnetwork: Optional[pulumi.Input[str]] = None,
            temp_gcs_location: Optional[pulumi.Input[str]] = None,
            template_gcs_path: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] additional_experiments: List of experiments that should be used by the job. An example value is `["enable_stackdriver_agent_metrics"]`.
        :param pulumi.Input[str] ip_configuration: The configuration for VM IPs.  Options are `"WORKER_IP_PUBLIC"` or `"WORKER_IP_PRIVATE"`.
        :param pulumi.Input[str] job_id: The unique ID of this job.
        :param pulumi.Input[Mapping[str, Any]] labels: User labels to be specified for the job. Keys and values should follow the restrictions
               specified in the [labeling restrictions](https://cloud.google.com/compute/docs/labeling-resources#restrictions) page.
               **NOTE**: Google-provided Dataflow templates often provide default labels that begin with `goog-dataflow-provided`.
               Unless explicitly set in config, these labels will be ignored to prevent diffs on re-apply.
        :param pulumi.Input[str] machine_type: The machine type to use for the job.
        :param pulumi.Input[float] max_workers: The number of workers permitted to work on the job.  More workers may improve processing speed at additional cost.
        :param pulumi.Input[str] name: A unique name for the resource, required by Dataflow.
        :param pulumi.Input[str] network: The network to which VMs will be assigned. If it is not provided, "default" will be used.
        :param pulumi.Input[str] on_delete: One of "drain" or "cancel".  Specifies behavior of deletion during `pulumi destroy`.  See above note.
        :param pulumi.Input[Mapping[str, Any]] parameters: Key/Value pairs to be passed to the Dataflow job (as used in the template).
        :param pulumi.Input[str] project: The project in which the resource belongs. If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region in which the created job should run.
        :param pulumi.Input[str] service_account_email: The Service Account email used to create the job.
        :param pulumi.Input[str] state: The current state of the resource, selected from the [JobState enum](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobState)
        :param pulumi.Input[str] subnetwork: The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK".
        :param pulumi.Input[str] temp_gcs_location: A writeable location on GCS for the Dataflow job to dump its temporary data.
        :param pulumi.Input[str] template_gcs_path: The GCS path to the Dataflow job template.
        :param pulumi.Input[str] type: The type of this job, selected from the [JobType enum](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobType)
        :param pulumi.Input[str] zone: The zone in which the created job should run. If it is not provided, the provider zone is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["additional_experiments"] = additional_experiments
        __props__["ip_configuration"] = ip_configuration
        __props__["job_id"] = job_id
        __props__["labels"] = labels
        __props__["machine_type"] = machine_type
        __props__["max_workers"] = max_workers
        __props__["name"] = name
        __props__["network"] = network
        __props__["on_delete"] = on_delete
        __props__["parameters"] = parameters
        __props__["project"] = project
        __props__["region"] = region
        __props__["service_account_email"] = service_account_email
        __props__["state"] = state
        __props__["subnetwork"] = subnetwork
        __props__["temp_gcs_location"] = temp_gcs_location
        __props__["template_gcs_path"] = template_gcs_path
        __props__["type"] = type
        __props__["zone"] = zone
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="additionalExperiments")
    def additional_experiments(self) -> pulumi.Output[Optional[List[str]]]:
        """
        List of experiments that should be used by the job. An example value is `["enable_stackdriver_agent_metrics"]`.
        """
        return pulumi.get(self, "additional_experiments")

    @property
    @pulumi.getter(name="ipConfiguration")
    def ip_configuration(self) -> pulumi.Output[Optional[str]]:
        """
        The configuration for VM IPs.  Options are `"WORKER_IP_PUBLIC"` or `"WORKER_IP_PRIVATE"`.
        """
        return pulumi.get(self, "ip_configuration")

    @property
    @pulumi.getter(name="jobId")
    def job_id(self) -> pulumi.Output[str]:
        """
        The unique ID of this job.
        """
        return pulumi.get(self, "job_id")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        User labels to be specified for the job. Keys and values should follow the restrictions
        specified in the [labeling restrictions](https://cloud.google.com/compute/docs/labeling-resources#restrictions) page.
        **NOTE**: Google-provided Dataflow templates often provide default labels that begin with `goog-dataflow-provided`.
        Unless explicitly set in config, these labels will be ignored to prevent diffs on re-apply.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> pulumi.Output[Optional[str]]:
        """
        The machine type to use for the job.
        """
        return pulumi.get(self, "machine_type")

    @property
    @pulumi.getter(name="maxWorkers")
    def max_workers(self) -> pulumi.Output[Optional[float]]:
        """
        The number of workers permitted to work on the job.  More workers may improve processing speed at additional cost.
        """
        return pulumi.get(self, "max_workers")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name for the resource, required by Dataflow.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[Optional[str]]:
        """
        The network to which VMs will be assigned. If it is not provided, "default" will be used.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="onDelete")
    def on_delete(self) -> pulumi.Output[Optional[str]]:
        """
        One of "drain" or "cancel".  Specifies behavior of deletion during `pulumi destroy`.  See above note.
        """
        return pulumi.get(self, "on_delete")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        Key/Value pairs to be passed to the Dataflow job (as used in the template).
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project in which the resource belongs. If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        The region in which the created job should run.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="serviceAccountEmail")
    def service_account_email(self) -> pulumi.Output[Optional[str]]:
        """
        The Service Account email used to create the job.
        """
        return pulumi.get(self, "service_account_email")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the resource, selected from the [JobState enum](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobState)
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def subnetwork(self) -> pulumi.Output[Optional[str]]:
        """
        The subnetwork to which VMs will be assigned. Should be of the form "regions/REGION/subnetworks/SUBNETWORK".
        """
        return pulumi.get(self, "subnetwork")

    @property
    @pulumi.getter(name="tempGcsLocation")
    def temp_gcs_location(self) -> pulumi.Output[str]:
        """
        A writeable location on GCS for the Dataflow job to dump its temporary data.
        """
        return pulumi.get(self, "temp_gcs_location")

    @property
    @pulumi.getter(name="templateGcsPath")
    def template_gcs_path(self) -> pulumi.Output[str]:
        """
        The GCS path to the Dataflow job template.
        """
        return pulumi.get(self, "template_gcs_path")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of this job, selected from the [JobType enum](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobType)
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[Optional[str]]:
        """
        The zone in which the created job should run. If it is not provided, the provider zone is used.
        """
        return pulumi.get(self, "zone")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

