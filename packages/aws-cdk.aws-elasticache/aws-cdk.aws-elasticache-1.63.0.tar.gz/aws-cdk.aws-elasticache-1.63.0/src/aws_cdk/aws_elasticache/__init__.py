"""
## Amazon ElastiCache Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCacheCluster(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnCacheCluster",
):
    """A CloudFormation ``AWS::ElastiCache::CacheCluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::CacheCluster
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        cache_node_type: str,
        engine: str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        az_mode: typing.Optional[str] = None,
        cache_parameter_group_name: typing.Optional[str] = None,
        cache_security_group_names: typing.Optional[typing.List[str]] = None,
        cache_subnet_group_name: typing.Optional[str] = None,
        cluster_name: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        notification_topic_arn: typing.Optional[str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[str] = None,
        preferred_availability_zones: typing.Optional[typing.List[str]] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        snapshot_arns: typing.Optional[typing.List[str]] = None,
        snapshot_name: typing.Optional[str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::CacheCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_node_type: ``AWS::ElastiCache::CacheCluster.CacheNodeType``.
        :param engine: ``AWS::ElastiCache::CacheCluster.Engine``.
        :param num_cache_nodes: ``AWS::ElastiCache::CacheCluster.NumCacheNodes``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.
        :param az_mode: ``AWS::ElastiCache::CacheCluster.AZMode``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.
        :param cluster_name: ``AWS::ElastiCache::CacheCluster.ClusterName``.
        :param engine_version: ``AWS::ElastiCache::CacheCluster.EngineVersion``.
        :param notification_topic_arn: ``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.
        :param port: ``AWS::ElastiCache::CacheCluster.Port``.
        :param preferred_availability_zone: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.
        :param preferred_availability_zones: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.
        :param snapshot_arns: ``AWS::ElastiCache::CacheCluster.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::CacheCluster.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.
        :param snapshot_window: ``AWS::ElastiCache::CacheCluster.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::CacheCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.
        """
        props = CfnCacheClusterProps(
            cache_node_type=cache_node_type,
            engine=engine,
            num_cache_nodes=num_cache_nodes,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            az_mode=az_mode,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            cluster_name=cluster_name,
            engine_version=engine_version,
            notification_topic_arn=notification_topic_arn,
            port=port,
            preferred_availability_zone=preferred_availability_zone,
            preferred_availability_zones=preferred_availability_zones,
            preferred_maintenance_window=preferred_maintenance_window,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshot_window=snapshot_window,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnCacheCluster, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndpointAddress")
    def attr_configuration_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConfigurationEndpoint.Address
        """
        return jsii.get(self, "attrConfigurationEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndpointPort")
    def attr_configuration_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConfigurationEndpoint.Port
        """
        return jsii.get(self, "attrConfigurationEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="attrRedisEndpointAddress")
    def attr_redis_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RedisEndpoint.Address
        """
        return jsii.get(self, "attrRedisEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrRedisEndpointPort")
    def attr_redis_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RedisEndpoint.Port
        """
        return jsii.get(self, "attrRedisEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElastiCache::CacheCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> str:
        """``AWS::ElastiCache::CacheCluster.CacheNodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        """
        return jsii.get(self, "cacheNodeType")

    @cache_node_type.setter
    def cache_node_type(self, value: str) -> None:
        jsii.set(self, "cacheNodeType", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> str:
        """``AWS::ElastiCache::CacheCluster.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        """
        return jsii.get(self, "engine")

    @engine.setter
    def engine(self, value: str) -> None:
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="numCacheNodes")
    def num_cache_nodes(self) -> jsii.Number:
        """``AWS::ElastiCache::CacheCluster.NumCacheNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        """
        return jsii.get(self, "numCacheNodes")

    @num_cache_nodes.setter
    def num_cache_nodes(self, value: jsii.Number) -> None:
        jsii.set(self, "numCacheNodes", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="azMode")
    def az_mode(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.AZMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        """
        return jsii.get(self, "azMode")

    @az_mode.setter
    def az_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "azMode", value)

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        """
        return jsii.get(self, "cacheParameterGroupName")

    @cache_parameter_group_name.setter
    def cache_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        """
        return jsii.get(self, "cacheSecurityGroupNames")

    @cache_security_group_names.setter
    def cache_security_group_names(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        """
        return jsii.get(self, "notificationTopicArn")

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredAvailabilityZone")
    def preferred_availability_zone(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        """
        return jsii.get(self, "preferredAvailabilityZone")

    @preferred_availability_zone.setter
    def preferred_availability_zone(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredAvailabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="preferredAvailabilityZones")
    def preferred_availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        """
        return jsii.get(self, "preferredAvailabilityZones")

    @preferred_availability_zones.setter
    def preferred_availability_zones(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "preferredAvailabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.SnapshotArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        """
        return jsii.get(self, "snapshotArns")

    @snapshot_arns.setter
    def snapshot_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "snapshotArns", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        """
        return jsii.get(self, "snapshotName")

    @snapshot_name.setter
    def snapshot_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        """
        return jsii.get(self, "snapshotRetentionLimit")

    @snapshot_retention_limit.setter
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        """
        return jsii.get(self, "snapshotWindow")

    @snapshot_window.setter
    def snapshot_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotWindow", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnCacheClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_node_type": "cacheNodeType",
        "engine": "engine",
        "num_cache_nodes": "numCacheNodes",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "az_mode": "azMode",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "cluster_name": "clusterName",
        "engine_version": "engineVersion",
        "notification_topic_arn": "notificationTopicArn",
        "port": "port",
        "preferred_availability_zone": "preferredAvailabilityZone",
        "preferred_availability_zones": "preferredAvailabilityZones",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnCacheClusterProps:
    def __init__(
        self,
        *,
        cache_node_type: str,
        engine: str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        az_mode: typing.Optional[str] = None,
        cache_parameter_group_name: typing.Optional[str] = None,
        cache_security_group_names: typing.Optional[typing.List[str]] = None,
        cache_subnet_group_name: typing.Optional[str] = None,
        cluster_name: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        notification_topic_arn: typing.Optional[str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[str] = None,
        preferred_availability_zones: typing.Optional[typing.List[str]] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        snapshot_arns: typing.Optional[typing.List[str]] = None,
        snapshot_name: typing.Optional[str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::CacheCluster``.

        :param cache_node_type: ``AWS::ElastiCache::CacheCluster.CacheNodeType``.
        :param engine: ``AWS::ElastiCache::CacheCluster.Engine``.
        :param num_cache_nodes: ``AWS::ElastiCache::CacheCluster.NumCacheNodes``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.
        :param az_mode: ``AWS::ElastiCache::CacheCluster.AZMode``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.
        :param cluster_name: ``AWS::ElastiCache::CacheCluster.ClusterName``.
        :param engine_version: ``AWS::ElastiCache::CacheCluster.EngineVersion``.
        :param notification_topic_arn: ``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.
        :param port: ``AWS::ElastiCache::CacheCluster.Port``.
        :param preferred_availability_zone: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.
        :param preferred_availability_zones: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.
        :param snapshot_arns: ``AWS::ElastiCache::CacheCluster.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::CacheCluster.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.
        :param snapshot_window: ``AWS::ElastiCache::CacheCluster.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::CacheCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
        """
        self._values = {
            "cache_node_type": cache_node_type,
            "engine": engine,
            "num_cache_nodes": num_cache_nodes,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if az_mode is not None:
            self._values["az_mode"] = az_mode
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if port is not None:
            self._values["port"] = port
        if preferred_availability_zone is not None:
            self._values["preferred_availability_zone"] = preferred_availability_zone
        if preferred_availability_zones is not None:
            self._values["preferred_availability_zones"] = preferred_availability_zones
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cache_node_type(self) -> str:
        """``AWS::ElastiCache::CacheCluster.CacheNodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        """
        return self._values.get("cache_node_type")

    @builtins.property
    def engine(self) -> str:
        """``AWS::ElastiCache::CacheCluster.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        """
        return self._values.get("engine")

    @builtins.property
    def num_cache_nodes(self) -> jsii.Number:
        """``AWS::ElastiCache::CacheCluster.NumCacheNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        """
        return self._values.get("num_cache_nodes")

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def az_mode(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.AZMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        """
        return self._values.get("az_mode")

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        """
        return self._values.get("cache_parameter_group_name")

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        """
        return self._values.get("cache_security_group_names")

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        """
        return self._values.get("cache_subnet_group_name")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        """
        return self._values.get("cluster_name")

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        """
        return self._values.get("engine_version")

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        """
        return self._values.get("notification_topic_arn")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        """
        return self._values.get("port")

    @builtins.property
    def preferred_availability_zone(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        """
        return self._values.get("preferred_availability_zone")

    @builtins.property
    def preferred_availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        """
        return self._values.get("preferred_availability_zones")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.SnapshotArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        """
        return self._values.get("snapshot_arns")

    @builtins.property
    def snapshot_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        """
        return self._values.get("snapshot_name")

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        """
        return self._values.get("snapshot_retention_limit")

    @builtins.property
    def snapshot_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        """
        return self._values.get("snapshot_window")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElastiCache::CacheCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        """
        return self._values.get("tags")

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        """
        return self._values.get("vpc_security_group_ids")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCacheClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnParameterGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnParameterGroup",
):
    """A CloudFormation ``AWS::ElastiCache::ParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::ParameterGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        cache_parameter_group_family: str,
        description: str,
        properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_parameter_group_family: ``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.
        :param description: ``AWS::ElastiCache::ParameterGroup.Description``.
        :param properties: ``AWS::ElastiCache::ParameterGroup.Properties``.
        """
        props = CfnParameterGroupProps(
            cache_parameter_group_family=cache_parameter_group_family,
            description=description,
            properties=properties,
        )

        jsii.create(CfnParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupFamily")
    def cache_parameter_group_family(self) -> str:
        """``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        """
        return jsii.get(self, "cacheParameterGroupFamily")

    @cache_parameter_group_family.setter
    def cache_parameter_group_family(self, value: str) -> None:
        jsii.set(self, "cacheParameterGroupFamily", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::ElastiCache::ParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]]:
        """``AWS::ElastiCache::ParameterGroup.Properties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        """
        return jsii.get(self, "properties")

    @properties.setter
    def properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]],
    ) -> None:
        jsii.set(self, "properties", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_parameter_group_family": "cacheParameterGroupFamily",
        "description": "description",
        "properties": "properties",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        cache_parameter_group_family: str,
        description: str,
        properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::ParameterGroup``.

        :param cache_parameter_group_family: ``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.
        :param description: ``AWS::ElastiCache::ParameterGroup.Description``.
        :param properties: ``AWS::ElastiCache::ParameterGroup.Properties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
        """
        self._values = {
            "cache_parameter_group_family": cache_parameter_group_family,
            "description": description,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def cache_parameter_group_family(self) -> str:
        """``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        """
        return self._values.get("cache_parameter_group_family")

    @builtins.property
    def description(self) -> str:
        """``AWS::ElastiCache::ParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        """
        return self._values.get("description")

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str, str]]]:
        """``AWS::ElastiCache::ParameterGroup.Properties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        """
        return self._values.get("properties")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReplicationGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroup",
):
    """A CloudFormation ``AWS::ElastiCache::ReplicationGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::ReplicationGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        replication_group_description: str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        auth_token: typing.Optional[str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        cache_node_type: typing.Optional[str] = None,
        cache_parameter_group_name: typing.Optional[str] = None,
        cache_security_group_names: typing.Optional[typing.List[str]] = None,
        cache_subnet_group_name: typing.Optional[str] = None,
        engine: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        multi_az_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        node_group_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "NodeGroupConfigurationProperty"]]]] = None,
        notification_topic_arn: typing.Optional[str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.List[str]] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        primary_cluster_id: typing.Optional[str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[str] = None,
        security_group_ids: typing.Optional[typing.List[str]] = None,
        snapshot_arns: typing.Optional[typing.List[str]] = None,
        snapshot_name: typing.Optional[str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[str] = None,
        snapshot_window: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::ReplicationGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_group_description: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.
        :param at_rest_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.
        :param auth_token: ``AWS::ElastiCache::ReplicationGroup.AuthToken``.
        :param automatic_failover_enabled: ``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.
        :param cache_node_type: ``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.
        :param engine: ``AWS::ElastiCache::ReplicationGroup.Engine``.
        :param engine_version: ``AWS::ElastiCache::ReplicationGroup.EngineVersion``.
        :param kms_key_id: ``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.
        :param multi_az_enabled: ``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.
        :param node_group_configuration: ``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.
        :param notification_topic_arn: ``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.
        :param num_cache_clusters: ``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.
        :param num_node_groups: ``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.
        :param port: ``AWS::ElastiCache::ReplicationGroup.Port``.
        :param preferred_cache_cluster_a_zs: ``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.
        :param primary_cluster_id: ``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.
        :param replicas_per_node_group: ``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.
        :param replication_group_id: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.
        :param security_group_ids: ``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.
        :param snapshot_arns: ``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::ReplicationGroup.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.
        :param snapshotting_cluster_id: ``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.
        :param snapshot_window: ``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::ReplicationGroup.Tags``.
        :param transit_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.
        """
        props = CfnReplicationGroupProps(
            replication_group_description=replication_group_description,
            at_rest_encryption_enabled=at_rest_encryption_enabled,
            auth_token=auth_token,
            automatic_failover_enabled=automatic_failover_enabled,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            cache_node_type=cache_node_type,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            engine=engine,
            engine_version=engine_version,
            kms_key_id=kms_key_id,
            multi_az_enabled=multi_az_enabled,
            node_group_configuration=node_group_configuration,
            notification_topic_arn=notification_topic_arn,
            num_cache_clusters=num_cache_clusters,
            num_node_groups=num_node_groups,
            port=port,
            preferred_cache_cluster_a_zs=preferred_cache_cluster_a_zs,
            preferred_maintenance_window=preferred_maintenance_window,
            primary_cluster_id=primary_cluster_id,
            replicas_per_node_group=replicas_per_node_group,
            replication_group_id=replication_group_id,
            security_group_ids=security_group_ids,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshotting_cluster_id=snapshotting_cluster_id,
            snapshot_window=snapshot_window,
            tags=tags,
            transit_encryption_enabled=transit_encryption_enabled,
        )

        jsii.create(CfnReplicationGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndPointAddress")
    def attr_configuration_end_point_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConfigurationEndPoint.Address
        """
        return jsii.get(self, "attrConfigurationEndPointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndPointPort")
    def attr_configuration_end_point_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConfigurationEndPoint.Port
        """
        return jsii.get(self, "attrConfigurationEndPointPort")

    @builtins.property
    @jsii.member(jsii_name="attrPrimaryEndPointAddress")
    def attr_primary_end_point_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: PrimaryEndPoint.Address
        """
        return jsii.get(self, "attrPrimaryEndPointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrPrimaryEndPointPort")
    def attr_primary_end_point_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: PrimaryEndPoint.Port
        """
        return jsii.get(self, "attrPrimaryEndPointPort")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointAddresses")
    def attr_read_end_point_addresses(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndPoint.Addresses
        """
        return jsii.get(self, "attrReadEndPointAddresses")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointAddressesList")
    def attr_read_end_point_addresses_list(self) -> typing.List[str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndPoint.Addresses.List
        """
        return jsii.get(self, "attrReadEndPointAddressesList")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointPorts")
    def attr_read_end_point_ports(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndPoint.Ports
        """
        return jsii.get(self, "attrReadEndPointPorts")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointPortsList")
    def attr_read_end_point_ports_list(self) -> typing.List[str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndPoint.Ports.List
        """
        return jsii.get(self, "attrReadEndPointPortsList")

    @builtins.property
    @jsii.member(jsii_name="attrReaderEndPointAddress")
    def attr_reader_end_point_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReaderEndPoint.Address
        """
        return jsii.get(self, "attrReaderEndPointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrReaderEndPointPort")
    def attr_reader_end_point_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReaderEndPoint.Port
        """
        return jsii.get(self, "attrReaderEndPointPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElastiCache::ReplicationGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="replicationGroupDescription")
    def replication_group_description(self) -> str:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        """
        return jsii.get(self, "replicationGroupDescription")

    @replication_group_description.setter
    def replication_group_description(self, value: str) -> None:
        jsii.set(self, "replicationGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="atRestEncryptionEnabled")
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        """
        return jsii.get(self, "atRestEncryptionEnabled")

    @at_rest_encryption_enabled.setter
    def at_rest_encryption_enabled(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "atRestEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="authToken")
    def auth_token(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.AuthToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        """
        return jsii.get(self, "authToken")

    @auth_token.setter
    def auth_token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "authToken", value)

    @builtins.property
    @jsii.member(jsii_name="automaticFailoverEnabled")
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        """
        return jsii.get(self, "automaticFailoverEnabled")

    @automatic_failover_enabled.setter
    def automatic_failover_enabled(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "automaticFailoverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        """
        return jsii.get(self, "cacheNodeType")

    @cache_node_type.setter
    def cache_node_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheNodeType", value)

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        """
        return jsii.get(self, "cacheParameterGroupName")

    @cache_parameter_group_name.setter
    def cache_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        """
        return jsii.get(self, "cacheSecurityGroupNames")

    @cache_security_group_names.setter
    def cache_security_group_names(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        """
        return jsii.get(self, "engine")

    @engine.setter
    def engine(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="multiAzEnabled")
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        """
        return jsii.get(self, "multiAzEnabled")

    @multi_az_enabled.setter
    def multi_az_enabled(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "multiAzEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="nodeGroupConfiguration")
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "NodeGroupConfigurationProperty"]]]]:
        """``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        """
        return jsii.get(self, "nodeGroupConfiguration")

    @node_group_configuration.setter
    def node_group_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "NodeGroupConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "nodeGroupConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        """
        return jsii.get(self, "notificationTopicArn")

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="numCacheClusters")
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        """
        return jsii.get(self, "numCacheClusters")

    @num_cache_clusters.setter
    def num_cache_clusters(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numCacheClusters", value)

    @builtins.property
    @jsii.member(jsii_name="numNodeGroups")
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        """
        return jsii.get(self, "numNodeGroups")

    @num_node_groups.setter
    def num_node_groups(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numNodeGroups", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredCacheClusterAZs")
    def preferred_cache_cluster_a_zs(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        """
        return jsii.get(self, "preferredCacheClusterAZs")

    @preferred_cache_cluster_a_zs.setter
    def preferred_cache_cluster_a_zs(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "preferredCacheClusterAZs", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="primaryClusterId")
    def primary_cluster_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        """
        return jsii.get(self, "primaryClusterId")

    @primary_cluster_id.setter
    def primary_cluster_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "primaryClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        """
        return jsii.get(self, "replicasPerNodeGroup")

    @replicas_per_node_group.setter
    def replicas_per_node_group(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "replicasPerNodeGroup", value)

    @builtins.property
    @jsii.member(jsii_name="replicationGroupId")
    def replication_group_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        """
        return jsii.get(self, "replicationGroupId")

    @replication_group_id.setter
    def replication_group_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "replicationGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        """
        return jsii.get(self, "snapshotArns")

    @snapshot_arns.setter
    def snapshot_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "snapshotArns", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        """
        return jsii.get(self, "snapshotName")

    @snapshot_name.setter
    def snapshot_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        """
        return jsii.get(self, "snapshotRetentionLimit")

    @snapshot_retention_limit.setter
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snapshottingClusterId")
    def snapshotting_cluster_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        """
        return jsii.get(self, "snapshottingClusterId")

    @snapshotting_cluster_id.setter
    def snapshotting_cluster_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshottingClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        """
        return jsii.get(self, "snapshotWindow")

    @snapshot_window.setter
    def snapshot_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotWindow", value)

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionEnabled")
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        """
        return jsii.get(self, "transitEncryptionEnabled")

    @transit_encryption_enabled.setter
    def transit_encryption_enabled(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "transitEncryptionEnabled", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "primary_availability_zone": "primaryAvailabilityZone",
            "replica_availability_zones": "replicaAvailabilityZones",
            "replica_count": "replicaCount",
            "slots": "slots",
        },
    )
    class NodeGroupConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[str] = None,
            primary_availability_zone: typing.Optional[str] = None,
            replica_availability_zones: typing.Optional[typing.List[str]] = None,
            replica_count: typing.Optional[jsii.Number] = None,
            slots: typing.Optional[str] = None,
        ) -> None:
            """
            :param node_group_id: ``CfnReplicationGroup.NodeGroupConfigurationProperty.NodeGroupId``.
            :param primary_availability_zone: ``CfnReplicationGroup.NodeGroupConfigurationProperty.PrimaryAvailabilityZone``.
            :param replica_availability_zones: ``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaAvailabilityZones``.
            :param replica_count: ``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaCount``.
            :param slots: ``CfnReplicationGroup.NodeGroupConfigurationProperty.Slots``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html
            """
            self._values = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if primary_availability_zone is not None:
                self._values["primary_availability_zone"] = primary_availability_zone
            if replica_availability_zones is not None:
                self._values["replica_availability_zones"] = replica_availability_zones
            if replica_count is not None:
                self._values["replica_count"] = replica_count
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def node_group_id(self) -> typing.Optional[str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.NodeGroupId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-nodegroupid
            """
            return self._values.get("node_group_id")

        @builtins.property
        def primary_availability_zone(self) -> typing.Optional[str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.PrimaryAvailabilityZone``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-primaryavailabilityzone
            """
            return self._values.get("primary_availability_zone")

        @builtins.property
        def replica_availability_zones(self) -> typing.Optional[typing.List[str]]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaAvailabilityZones``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicaavailabilityzones
            """
            return self._values.get("replica_availability_zones")

        @builtins.property
        def replica_count(self) -> typing.Optional[jsii.Number]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicacount
            """
            return self._values.get("replica_count")

        @builtins.property
        def slots(self) -> typing.Optional[str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.Slots``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-slots
            """
            return self._values.get("slots")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_group_description": "replicationGroupDescription",
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "auth_token": "authToken",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "engine": "engine",
        "engine_version": "engineVersion",
        "kms_key_id": "kmsKeyId",
        "multi_az_enabled": "multiAzEnabled",
        "node_group_configuration": "nodeGroupConfiguration",
        "notification_topic_arn": "notificationTopicArn",
        "num_cache_clusters": "numCacheClusters",
        "num_node_groups": "numNodeGroups",
        "port": "port",
        "preferred_cache_cluster_a_zs": "preferredCacheClusterAZs",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "primary_cluster_id": "primaryClusterId",
        "replicas_per_node_group": "replicasPerNodeGroup",
        "replication_group_id": "replicationGroupId",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshotting_cluster_id": "snapshottingClusterId",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
    },
)
class CfnReplicationGroupProps:
    def __init__(
        self,
        *,
        replication_group_description: str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        auth_token: typing.Optional[str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        cache_node_type: typing.Optional[str] = None,
        cache_parameter_group_name: typing.Optional[str] = None,
        cache_security_group_names: typing.Optional[typing.List[str]] = None,
        cache_subnet_group_name: typing.Optional[str] = None,
        engine: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        multi_az_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        node_group_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationGroup.NodeGroupConfigurationProperty"]]]] = None,
        notification_topic_arn: typing.Optional[str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.List[str]] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        primary_cluster_id: typing.Optional[str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[str] = None,
        security_group_ids: typing.Optional[typing.List[str]] = None,
        snapshot_arns: typing.Optional[typing.List[str]] = None,
        snapshot_name: typing.Optional[str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[str] = None,
        snapshot_window: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::ReplicationGroup``.

        :param replication_group_description: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.
        :param at_rest_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.
        :param auth_token: ``AWS::ElastiCache::ReplicationGroup.AuthToken``.
        :param automatic_failover_enabled: ``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.
        :param cache_node_type: ``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.
        :param engine: ``AWS::ElastiCache::ReplicationGroup.Engine``.
        :param engine_version: ``AWS::ElastiCache::ReplicationGroup.EngineVersion``.
        :param kms_key_id: ``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.
        :param multi_az_enabled: ``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.
        :param node_group_configuration: ``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.
        :param notification_topic_arn: ``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.
        :param num_cache_clusters: ``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.
        :param num_node_groups: ``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.
        :param port: ``AWS::ElastiCache::ReplicationGroup.Port``.
        :param preferred_cache_cluster_a_zs: ``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.
        :param primary_cluster_id: ``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.
        :param replicas_per_node_group: ``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.
        :param replication_group_id: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.
        :param security_group_ids: ``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.
        :param snapshot_arns: ``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::ReplicationGroup.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.
        :param snapshotting_cluster_id: ``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.
        :param snapshot_window: ``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::ReplicationGroup.Tags``.
        :param transit_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
        """
        self._values = {
            "replication_group_description": replication_group_description,
        }
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_az_enabled is not None:
            self._values["multi_az_enabled"] = multi_az_enabled
        if node_group_configuration is not None:
            self._values["node_group_configuration"] = node_group_configuration
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if num_cache_clusters is not None:
            self._values["num_cache_clusters"] = num_cache_clusters
        if num_node_groups is not None:
            self._values["num_node_groups"] = num_node_groups
        if port is not None:
            self._values["port"] = port
        if preferred_cache_cluster_a_zs is not None:
            self._values["preferred_cache_cluster_a_zs"] = preferred_cache_cluster_a_zs
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if primary_cluster_id is not None:
            self._values["primary_cluster_id"] = primary_cluster_id
        if replicas_per_node_group is not None:
            self._values["replicas_per_node_group"] = replicas_per_node_group
        if replication_group_id is not None:
            self._values["replication_group_id"] = replication_group_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshotting_cluster_id is not None:
            self._values["snapshotting_cluster_id"] = snapshotting_cluster_id
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled

    @builtins.property
    def replication_group_description(self) -> str:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        """
        return self._values.get("replication_group_description")

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        """
        return self._values.get("at_rest_encryption_enabled")

    @builtins.property
    def auth_token(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.AuthToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        """
        return self._values.get("auth_token")

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        """
        return self._values.get("automatic_failover_enabled")

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def cache_node_type(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        """
        return self._values.get("cache_node_type")

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        """
        return self._values.get("cache_parameter_group_name")

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        """
        return self._values.get("cache_security_group_names")

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        """
        return self._values.get("cache_subnet_group_name")

    @builtins.property
    def engine(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        """
        return self._values.get("engine")

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        """
        return self._values.get("engine_version")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        """
        return self._values.get("multi_az_enabled")

    @builtins.property
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationGroup.NodeGroupConfigurationProperty"]]]]:
        """``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        """
        return self._values.get("node_group_configuration")

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        """
        return self._values.get("notification_topic_arn")

    @builtins.property
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        """
        return self._values.get("num_cache_clusters")

    @builtins.property
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        """
        return self._values.get("num_node_groups")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        """
        return self._values.get("port")

    @builtins.property
    def preferred_cache_cluster_a_zs(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        """
        return self._values.get("preferred_cache_cluster_a_zs")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def primary_cluster_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        """
        return self._values.get("primary_cluster_id")

    @builtins.property
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        """
        return self._values.get("replicas_per_node_group")

    @builtins.property
    def replication_group_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        """
        return self._values.get("replication_group_id")

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        """
        return self._values.get("security_group_ids")

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        """
        return self._values.get("snapshot_arns")

    @builtins.property
    def snapshot_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        """
        return self._values.get("snapshot_name")

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        """
        return self._values.get("snapshot_retention_limit")

    @builtins.property
    def snapshotting_cluster_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        """
        return self._values.get("snapshotting_cluster_id")

    @builtins.property
    def snapshot_window(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        """
        return self._values.get("snapshot_window")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElastiCache::ReplicationGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        """
        return self._values.get("tags")

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        """
        return self._values.get("transit_encryption_enabled")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecurityGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroup",
):
    """A CloudFormation ``AWS::ElastiCache::SecurityGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::SecurityGroup
    """

    def __init__(
        self, scope: aws_cdk.core.Construct, id: str, *, description: str
    ) -> None:
        """Create a new ``AWS::ElastiCache::SecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::ElastiCache::SecurityGroup.Description``.
        """
        props = CfnSecurityGroupProps(description=description)

        jsii.create(CfnSecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::ElastiCache::SecurityGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecurityGroupIngress(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupIngress",
):
    """A CloudFormation ``AWS::ElastiCache::SecurityGroupIngress``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::SecurityGroupIngress
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        cache_security_group_name: str,
        ec2_security_group_name: str,
        ec2_security_group_owner_id: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::SecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.
        :param ec2_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props = CfnSecurityGroupIngressProps(
            cache_security_group_name=cache_security_group_name,
            ec2_security_group_name=ec2_security_group_name,
            ec2_security_group_owner_id=ec2_security_group_owner_id,
        )

        jsii.create(CfnSecurityGroupIngress, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupName")
    def cache_security_group_name(self) -> str:
        """``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        """
        return jsii.get(self, "cacheSecurityGroupName")

    @cache_security_group_name.setter
    def cache_security_group_name(self, value: str) -> None:
        jsii.set(self, "cacheSecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> str:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        """
        return jsii.get(self, "ec2SecurityGroupName")

    @ec2_security_group_name.setter
    def ec2_security_group_name(self, value: str) -> None:
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        """
        return jsii.get(self, "ec2SecurityGroupOwnerId")

    @ec2_security_group_owner_id.setter
    def ec2_security_group_owner_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupIngressProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_security_group_name": "cacheSecurityGroupName",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnSecurityGroupIngressProps:
    def __init__(
        self,
        *,
        cache_security_group_name: str,
        ec2_security_group_name: str,
        ec2_security_group_owner_id: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::SecurityGroupIngress``.

        :param cache_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.
        :param ec2_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
        """
        self._values = {
            "cache_security_group_name": cache_security_group_name,
            "ec2_security_group_name": ec2_security_group_name,
        }
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cache_security_group_name(self) -> str:
        """``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        """
        return self._values.get("cache_security_group_name")

    @builtins.property
    def ec2_security_group_name(self) -> str:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        """
        return self._values.get("ec2_security_group_name")

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        """
        return self._values.get("ec2_security_group_owner_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description"},
)
class CfnSecurityGroupProps:
    def __init__(self, *, description: str) -> None:
        """Properties for defining a ``AWS::ElastiCache::SecurityGroup``.

        :param description: ``AWS::ElastiCache::SecurityGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
        """
        self._values = {
            "description": description,
        }

    @builtins.property
    def description(self) -> str:
        """``AWS::ElastiCache::SecurityGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        """
        return self._values.get("description")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSubnetGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticache.CfnSubnetGroup",
):
    """A CloudFormation ``AWS::ElastiCache::SubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElastiCache::SubnetGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        description: str,
        subnet_ids: typing.List[str],
        cache_subnet_group_name: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::ElastiCache::SubnetGroup.Description``.
        :param subnet_ids: ``AWS::ElastiCache::SubnetGroup.SubnetIds``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.
        """
        props = CfnSubnetGroupProps(
            description=description,
            subnet_ids=subnet_ids,
            cache_subnet_group_name=cache_subnet_group_name,
        )

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::ElastiCache::SubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::ElastiCache::SubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticache.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_ids": "subnetIds",
        "cache_subnet_group_name": "cacheSubnetGroupName",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        description: str,
        subnet_ids: typing.List[str],
        cache_subnet_group_name: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::SubnetGroup``.

        :param description: ``AWS::ElastiCache::SubnetGroup.Description``.
        :param subnet_ids: ``AWS::ElastiCache::SubnetGroup.SubnetIds``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html
        """
        self._values = {
            "description": description,
            "subnet_ids": subnet_ids,
        }
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name

    @builtins.property
    def description(self) -> str:
        """``AWS::ElastiCache::SubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        """
        return self._values.get("description")

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::ElastiCache::SubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        """
        return self._values.get("subnet_ids")

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        """
        return self._values.get("cache_subnet_group_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCacheCluster",
    "CfnCacheClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnReplicationGroup",
    "CfnReplicationGroupProps",
    "CfnSecurityGroup",
    "CfnSecurityGroupIngress",
    "CfnSecurityGroupIngressProps",
    "CfnSecurityGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
]

publication.publish()
