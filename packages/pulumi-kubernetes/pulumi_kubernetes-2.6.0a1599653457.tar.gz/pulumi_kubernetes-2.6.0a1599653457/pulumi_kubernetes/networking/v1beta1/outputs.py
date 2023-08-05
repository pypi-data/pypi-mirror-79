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

__all__ = [
    'HTTPIngressPath',
    'HTTPIngressRuleValue',
    'Ingress',
    'IngressBackend',
    'IngressClass',
    'IngressClassSpec',
    'IngressRule',
    'IngressSpec',
    'IngressStatus',
    'IngressTLS',
]

@pulumi.output_type
class HTTPIngressPath(dict):
    """
    HTTPIngressPath associates a path with a backend. Incoming urls matching the path are forwarded to the backend.
    """
    def __init__(__self__, *,
                 backend: 'outputs.IngressBackend',
                 path: Optional[str] = None,
                 path_type: Optional[str] = None):
        """
        HTTPIngressPath associates a path with a backend. Incoming urls matching the path are forwarded to the backend.
        :param 'IngressBackendArgs' backend: Backend defines the referenced service endpoint to which the traffic will be forwarded to.
        :param str path: Path is matched against the path of an incoming request. Currently it can contain characters disallowed from the conventional "path" part of a URL as defined by RFC 3986. Paths must begin with a '/'. When unspecified, all paths from incoming requests are matched.
        :param str path_type: PathType determines the interpretation of the Path matching. PathType can be one of the following values: * Exact: Matches the URL path exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching is
                 done on a path element by element basis. A path element refers is the
                 list of labels in the path split by the '/' separator. A request is a
                 match for path p if every p is an element-wise prefix of p of the
                 request path. Note that if the last element of the path is a substring
                 of the last element in request path, it is not a match (e.g. /foo/bar
                 matches /foo/bar/baz, but does not match /foo/barbaz).
               * ImplementationSpecific: Interpretation of the Path matching is up to
                 the IngressClass. Implementations can treat this as a separate PathType
                 or treat it identically to Prefix or Exact path types.
               Implementations are required to support all path types. Defaults to ImplementationSpecific.
        """
        pulumi.set(__self__, "backend", backend)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if path_type is not None:
            pulumi.set(__self__, "path_type", path_type)

    @property
    @pulumi.getter
    def backend(self) -> 'outputs.IngressBackend':
        """
        Backend defines the referenced service endpoint to which the traffic will be forwarded to.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        Path is matched against the path of an incoming request. Currently it can contain characters disallowed from the conventional "path" part of a URL as defined by RFC 3986. Paths must begin with a '/'. When unspecified, all paths from incoming requests are matched.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="pathType")
    def path_type(self) -> Optional[str]:
        """
        PathType determines the interpretation of the Path matching. PathType can be one of the following values: * Exact: Matches the URL path exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching is
          done on a path element by element basis. A path element refers is the
          list of labels in the path split by the '/' separator. A request is a
          match for path p if every p is an element-wise prefix of p of the
          request path. Note that if the last element of the path is a substring
          of the last element in request path, it is not a match (e.g. /foo/bar
          matches /foo/bar/baz, but does not match /foo/barbaz).
        * ImplementationSpecific: Interpretation of the Path matching is up to
          the IngressClass. Implementations can treat this as a separate PathType
          or treat it identically to Prefix or Exact path types.
        Implementations are required to support all path types. Defaults to ImplementationSpecific.
        """
        return pulumi.get(self, "path_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class HTTPIngressRuleValue(dict):
    """
    HTTPIngressRuleValue is a list of http selectors pointing to backends. In the example: http://<host>/<path>?<searchpart> -> backend where where parts of the url correspond to RFC 3986, this resource will be used to match against everything after the last '/' and before the first '?' or '#'.
    """
    def __init__(__self__, *,
                 paths: List['outputs.HTTPIngressPath']):
        """
        HTTPIngressRuleValue is a list of http selectors pointing to backends. In the example: http://<host>/<path>?<searchpart> -> backend where where parts of the url correspond to RFC 3986, this resource will be used to match against everything after the last '/' and before the first '?' or '#'.
        :param List['HTTPIngressPathArgs'] paths: A collection of paths that map requests to backends.
        """
        pulumi.set(__self__, "paths", paths)

    @property
    @pulumi.getter
    def paths(self) -> List['outputs.HTTPIngressPath']:
        """
        A collection of paths that map requests to backends.
        """
        return pulumi.get(self, "paths")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class Ingress(dict):
    """
    Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc.

    This resource waits until its status is ready before registering success
    for create/update, and populating output properties from the current state of the resource.
    The following conditions are used to determine whether the resource creation has
    succeeded or failed:

    1.  Ingress object exists.
    2.  Endpoint objects exist with matching names for each Ingress path (except when Service
        type is ExternalName).
    3.  Ingress entry exists for '.status.loadBalancer.ingress'.

    If the Ingress has not reached a Ready state after 10 minutes, it will
    time out and mark the resource update as Failed. You can override the default timeout value
    by setting the 'customTimeouts' option on the resource.
    """
    def __init__(__self__, *,
                 api_version: Optional[str] = None,
                 kind: Optional[str] = None,
                 metadata: Optional['_meta.v1.outputs.ObjectMeta'] = None,
                 spec: Optional['outputs.IngressSpec'] = None,
                 status: Optional['outputs.IngressStatus'] = None):
        """
        Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc.

        This resource waits until its status is ready before registering success
        for create/update, and populating output properties from the current state of the resource.
        The following conditions are used to determine whether the resource creation has
        succeeded or failed:

        1.  Ingress object exists.
        2.  Endpoint objects exist with matching names for each Ingress path (except when Service
            type is ExternalName).
        3.  Ingress entry exists for '.status.loadBalancer.ingress'.

        If the Ingress has not reached a Ready state after 10 minutes, it will
        time out and mark the resource update as Failed. You can override the default timeout value
        by setting the 'customTimeouts' option on the resource.
        :param str api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param str kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param '_meta.v1.ObjectMetaArgs' metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param 'IngressSpecArgs' spec: Spec is the desired state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        :param 'IngressStatusArgs' status: Status is the current state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'networking.k8s.io/v1beta1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'Ingress')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if spec is not None:
            pulumi.set(__self__, "spec", spec)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[str]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def metadata(self) -> Optional['_meta.v1.outputs.ObjectMeta']:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def spec(self) -> Optional['outputs.IngressSpec']:
        """
        Spec is the desired state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "spec")

    @property
    @pulumi.getter
    def status(self) -> Optional['outputs.IngressStatus']:
        """
        Status is the current state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressBackend(dict):
    """
    IngressBackend describes all endpoints for a given service and port.
    """
    def __init__(__self__, *,
                 service_name: str,
                 service_port: Any,
                 resource: Optional['_core.v1.outputs.TypedLocalObjectReference'] = None):
        """
        IngressBackend describes all endpoints for a given service and port.
        :param str service_name: Specifies the name of the referenced service.
        :param Union[float, str] service_port: Specifies the port of the referenced service.
        :param '_core.v1.TypedLocalObjectReferenceArgs' resource: Resource is an ObjectRef to another Kubernetes resource in the namespace of the Ingress object. If resource is specified, serviceName and servicePort must not be specified.
        """
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "service_port", service_port)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        """
        Specifies the name of the referenced service.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter(name="servicePort")
    def service_port(self) -> Any:
        """
        Specifies the port of the referenced service.
        """
        return pulumi.get(self, "service_port")

    @property
    @pulumi.getter
    def resource(self) -> Optional['_core.v1.outputs.TypedLocalObjectReference']:
        """
        Resource is an ObjectRef to another Kubernetes resource in the namespace of the Ingress object. If resource is specified, serviceName and servicePort must not be specified.
        """
        return pulumi.get(self, "resource")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressClass(dict):
    """
    IngressClass represents the class of the Ingress, referenced by the Ingress Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be used to indicate that an IngressClass should be considered default. When a single IngressClass resource has this annotation set to true, new Ingress resources without a class specified will be assigned this default class.
    """
    def __init__(__self__, *,
                 api_version: Optional[str] = None,
                 kind: Optional[str] = None,
                 metadata: Optional['_meta.v1.outputs.ObjectMeta'] = None,
                 spec: Optional['outputs.IngressClassSpec'] = None):
        """
        IngressClass represents the class of the Ingress, referenced by the Ingress Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be used to indicate that an IngressClass should be considered default. When a single IngressClass resource has this annotation set to true, new Ingress resources without a class specified will be assigned this default class.
        :param str api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param str kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param '_meta.v1.ObjectMetaArgs' metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param 'IngressClassSpecArgs' spec: Spec is the desired state of the IngressClass. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'networking.k8s.io/v1beta1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'IngressClass')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if spec is not None:
            pulumi.set(__self__, "spec", spec)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[str]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def metadata(self) -> Optional['_meta.v1.outputs.ObjectMeta']:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def spec(self) -> Optional['outputs.IngressClassSpec']:
        """
        Spec is the desired state of the IngressClass. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "spec")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressClassSpec(dict):
    """
    IngressClassSpec provides information about the class of an Ingress.
    """
    def __init__(__self__, *,
                 controller: Optional[str] = None,
                 parameters: Optional['_core.v1.outputs.TypedLocalObjectReference'] = None):
        """
        IngressClassSpec provides information about the class of an Ingress.
        :param str controller: Controller refers to the name of the controller that should handle this class. This allows for different "flavors" that are controlled by the same controller. For example, you may have different Parameters for the same implementing controller. This should be specified as a domain-prefixed path no more than 250 characters in length, e.g. "acme.io/ingress-controller". This field is immutable.
        :param '_core.v1.TypedLocalObjectReferenceArgs' parameters: Parameters is a link to a custom resource containing additional configuration for the controller. This is optional if the controller does not require extra parameters.
        """
        if controller is not None:
            pulumi.set(__self__, "controller", controller)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def controller(self) -> Optional[str]:
        """
        Controller refers to the name of the controller that should handle this class. This allows for different "flavors" that are controlled by the same controller. For example, you may have different Parameters for the same implementing controller. This should be specified as a domain-prefixed path no more than 250 characters in length, e.g. "acme.io/ingress-controller". This field is immutable.
        """
        return pulumi.get(self, "controller")

    @property
    @pulumi.getter
    def parameters(self) -> Optional['_core.v1.outputs.TypedLocalObjectReference']:
        """
        Parameters is a link to a custom resource containing additional configuration for the controller. This is optional if the controller does not require extra parameters.
        """
        return pulumi.get(self, "parameters")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressRule(dict):
    """
    IngressRule represents the rules mapping the paths under a specified host to the related backend services. Incoming requests are first evaluated for a host match, then routed to the backend associated with the matching IngressRuleValue.
    """
    def __init__(__self__, *,
                 host: Optional[str] = None,
                 http: Optional['outputs.HTTPIngressRuleValue'] = None):
        """
        IngressRule represents the rules mapping the paths under a specified host to the related backend services. Incoming requests are first evaluated for a host match, then routed to the backend associated with the matching IngressRuleValue.
        :param str host: Host is the fully qualified domain name of a network host, as defined by RFC 3986. Note the following deviations from the "host" part of the URI as defined in RFC 3986: 1. IPs are not allowed. Currently an IngressRuleValue can only apply to
                  the IP in the Spec of the parent Ingress.
               2. The `:` delimiter is not respected because ports are not allowed.
               	  Currently the port of an Ingress is implicitly :80 for http and
               	  :443 for https.
               Both these may change in the future. Incoming requests are matched against the host before the IngressRuleValue. If the host is unspecified, the Ingress routes all traffic based on the specified IngressRuleValue.
               
               Host can be "precise" which is a domain name without the terminating dot of a network host (e.g. "foo.bar.com") or "wildcard", which is a domain name prefixed with a single wildcard label (e.g. "*.foo.com"). The wildcard character '*' must appear by itself as the first DNS label and matches only a single label. You cannot have a wildcard label by itself (e.g. Host == "*"). Requests will be matched against the Host field in the following way: 1. If Host is precise, the request matches this rule if the http host header is equal to Host. 2. If Host is a wildcard, then the request matches this rule if the http host header is to equal to the suffix (removing the first label) of the wildcard rule.
        """
        if host is not None:
            pulumi.set(__self__, "host", host)
        if http is not None:
            pulumi.set(__self__, "http", http)

    @property
    @pulumi.getter
    def host(self) -> Optional[str]:
        """
        Host is the fully qualified domain name of a network host, as defined by RFC 3986. Note the following deviations from the "host" part of the URI as defined in RFC 3986: 1. IPs are not allowed. Currently an IngressRuleValue can only apply to
           the IP in the Spec of the parent Ingress.
        2. The `:` delimiter is not respected because ports are not allowed.
        	  Currently the port of an Ingress is implicitly :80 for http and
        	  :443 for https.
        Both these may change in the future. Incoming requests are matched against the host before the IngressRuleValue. If the host is unspecified, the Ingress routes all traffic based on the specified IngressRuleValue.

        Host can be "precise" which is a domain name without the terminating dot of a network host (e.g. "foo.bar.com") or "wildcard", which is a domain name prefixed with a single wildcard label (e.g. "*.foo.com"). The wildcard character '*' must appear by itself as the first DNS label and matches only a single label. You cannot have a wildcard label by itself (e.g. Host == "*"). Requests will be matched against the Host field in the following way: 1. If Host is precise, the request matches this rule if the http host header is equal to Host. 2. If Host is a wildcard, then the request matches this rule if the http host header is to equal to the suffix (removing the first label) of the wildcard rule.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def http(self) -> Optional['outputs.HTTPIngressRuleValue']:
        return pulumi.get(self, "http")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressSpec(dict):
    """
    IngressSpec describes the Ingress the user wishes to exist.
    """
    def __init__(__self__, *,
                 backend: Optional['outputs.IngressBackend'] = None,
                 ingress_class_name: Optional[str] = None,
                 rules: Optional[List['outputs.IngressRule']] = None,
                 tls: Optional[List['outputs.IngressTLS']] = None):
        """
        IngressSpec describes the Ingress the user wishes to exist.
        :param 'IngressBackendArgs' backend: A default backend capable of servicing requests that don't match any rule. At least one of 'backend' or 'rules' must be specified. This field is optional to allow the loadbalancer controller or defaulting logic to specify a global default.
        :param str ingress_class_name: IngressClassName is the name of the IngressClass cluster resource. The associated IngressClass defines which controller will implement the resource. This replaces the deprecated `kubernetes.io/ingress.class` annotation. For backwards compatibility, when that annotation is set, it must be given precedence over this field. The controller may emit a warning if the field and annotation have different values. Implementations of this API should ignore Ingresses without a class specified. An IngressClass resource may be marked as default, which can be used to set a default value for this field. For more information, refer to the IngressClass documentation.
        :param List['IngressRuleArgs'] rules: A list of host rules used to configure the Ingress. If unspecified, or no rule matches, all traffic is sent to the default backend.
        :param List['IngressTLSArgs'] tls: TLS configuration. Currently the Ingress only supports a single TLS port, 443. If multiple members of this list specify different hosts, they will be multiplexed on the same port according to the hostname specified through the SNI TLS extension, if the ingress controller fulfilling the ingress supports SNI.
        """
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if ingress_class_name is not None:
            pulumi.set(__self__, "ingress_class_name", ingress_class_name)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if tls is not None:
            pulumi.set(__self__, "tls", tls)

    @property
    @pulumi.getter
    def backend(self) -> Optional['outputs.IngressBackend']:
        """
        A default backend capable of servicing requests that don't match any rule. At least one of 'backend' or 'rules' must be specified. This field is optional to allow the loadbalancer controller or defaulting logic to specify a global default.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter(name="ingressClassName")
    def ingress_class_name(self) -> Optional[str]:
        """
        IngressClassName is the name of the IngressClass cluster resource. The associated IngressClass defines which controller will implement the resource. This replaces the deprecated `kubernetes.io/ingress.class` annotation. For backwards compatibility, when that annotation is set, it must be given precedence over this field. The controller may emit a warning if the field and annotation have different values. Implementations of this API should ignore Ingresses without a class specified. An IngressClass resource may be marked as default, which can be used to set a default value for this field. For more information, refer to the IngressClass documentation.
        """
        return pulumi.get(self, "ingress_class_name")

    @property
    @pulumi.getter
    def rules(self) -> Optional[List['outputs.IngressRule']]:
        """
        A list of host rules used to configure the Ingress. If unspecified, or no rule matches, all traffic is sent to the default backend.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def tls(self) -> Optional[List['outputs.IngressTLS']]:
        """
        TLS configuration. Currently the Ingress only supports a single TLS port, 443. If multiple members of this list specify different hosts, they will be multiplexed on the same port according to the hostname specified through the SNI TLS extension, if the ingress controller fulfilling the ingress supports SNI.
        """
        return pulumi.get(self, "tls")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressStatus(dict):
    """
    IngressStatus describe the current state of the Ingress.
    """
    def __init__(__self__, *,
                 load_balancer: Optional['_core.v1.outputs.LoadBalancerStatus'] = None):
        """
        IngressStatus describe the current state of the Ingress.
        :param '_core.v1.LoadBalancerStatusArgs' load_balancer: LoadBalancer contains the current status of the load-balancer.
        """
        if load_balancer is not None:
            pulumi.set(__self__, "load_balancer", load_balancer)

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> Optional['_core.v1.outputs.LoadBalancerStatus']:
        """
        LoadBalancer contains the current status of the load-balancer.
        """
        return pulumi.get(self, "load_balancer")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IngressTLS(dict):
    """
    IngressTLS describes the transport layer security associated with an Ingress.
    """
    def __init__(__self__, *,
                 hosts: Optional[List[str]] = None,
                 secret_name: Optional[str] = None):
        """
        IngressTLS describes the transport layer security associated with an Ingress.
        :param List[str] hosts: Hosts are a list of hosts included in the TLS certificate. The values in this list must match the name/s used in the tlsSecret. Defaults to the wildcard host setting for the loadbalancer controller fulfilling this Ingress, if left unspecified.
        :param str secret_name: SecretName is the name of the secret used to terminate TLS traffic on port 443. Field is left optional to allow TLS routing based on SNI hostname alone. If the SNI host in a listener conflicts with the "Host" header field used by an IngressRule, the SNI host is used for termination and value of the Host header is used for routing.
        """
        if hosts is not None:
            pulumi.set(__self__, "hosts", hosts)
        if secret_name is not None:
            pulumi.set(__self__, "secret_name", secret_name)

    @property
    @pulumi.getter
    def hosts(self) -> Optional[List[str]]:
        """
        Hosts are a list of hosts included in the TLS certificate. The values in this list must match the name/s used in the tlsSecret. Defaults to the wildcard host setting for the loadbalancer controller fulfilling this Ingress, if left unspecified.
        """
        return pulumi.get(self, "hosts")

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> Optional[str]:
        """
        SecretName is the name of the secret used to terminate TLS traffic on port 443. Field is left optional to allow TLS routing based on SNI hostname alone. If the SNI host in a listener conflicts with the "Host" header field used by an IngressRule, the SNI host is used for termination and value of the Host header is used for routing.
        """
        return pulumi.get(self, "secret_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


