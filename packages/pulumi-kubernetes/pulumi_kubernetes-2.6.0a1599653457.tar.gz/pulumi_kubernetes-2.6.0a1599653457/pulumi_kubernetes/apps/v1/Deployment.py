# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from ... import _utilities, _tables
from . import outputs
from ... import core as _core
from ... import meta as _meta
from ._inputs import *

__all__ = ['Deployment']


class Deployment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 spec: Optional[pulumi.Input[pulumi.InputType['DeploymentSpecArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Deployment enables declarative updates for Pods and ReplicaSets.

        This resource waits until its status is ready before registering success
        for create/update, and populating output properties from the current state of the resource.
        The following conditions are used to determine whether the resource creation has
        succeeded or failed:

        1. The Deployment has begun to be updated by the Deployment controller. If the current
           generation of the Deployment is > 1, then this means that the current generation must
           be different from the generation reported by the last outputs.
        2. There exists a ReplicaSet whose revision is equal to the current revision of the
           Deployment.
        3. The Deployment's '.status.conditions' has a status of type 'Available' whose 'status'
           member is set to 'True'.
        4. If the Deployment has generation > 1, then '.status.conditions' has a status of type
           'Progressing', whose 'status' member is set to 'True', and whose 'reason' is
           'NewReplicaSetAvailable'. For generation <= 1, this status field does not exist,
           because it doesn't do a rollout (i.e., it simply creates the Deployment and
           corresponding ReplicaSet), and therefore there is no rollout to mark as 'Progressing'.

        If the Deployment has not reached a Ready state after 10 minutes, it will
        time out and mark the resource update as Failed. You can override the default timeout value
        by setting the 'customTimeouts' option on the resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']] metadata: Standard object metadata.
        :param pulumi.Input[pulumi.InputType['DeploymentSpecArgs']] spec: Specification of the desired behavior of the Deployment.
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

            __props__['api_version'] = 'apps/v1'
            __props__['kind'] = 'Deployment'
            __props__['metadata'] = metadata
            __props__['spec'] = spec
            __props__['status'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="kubernetes:apps/v1beta1:Deployment"), pulumi.Alias(type_="kubernetes:apps/v1beta2:Deployment"), pulumi.Alias(type_="kubernetes:extensions/v1beta1:Deployment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Deployment, __self__).__init__(
            'kubernetes:apps/v1:Deployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Deployment':
        """
        Get an existing Deployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Deployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional['_meta.v1.outputs.ObjectMeta']]:
        """
        Standard object metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def spec(self) -> pulumi.Output[Optional['outputs.DeploymentSpec']]:
        """
        Specification of the desired behavior of the Deployment.
        """
        return pulumi.get(self, "spec")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional['outputs.DeploymentStatus']]:
        """
        Most recently observed status of the Deployment.
        """
        return pulumi.get(self, "status")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

