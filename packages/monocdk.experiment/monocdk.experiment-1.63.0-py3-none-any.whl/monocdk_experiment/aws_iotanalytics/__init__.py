import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_7760e8e4,
    CfnTag as _CfnTag_b4661f1a,
    Construct as _Construct_f50a3f53,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)


@jsii.implements(_IInspectable_051e6ed8)
class CfnChannel(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannel",
):
    """A CloudFormation ``AWS::IoTAnalytics::Channel``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTAnalytics::Channel
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        channel_name: typing.Optional[str] = None,
        channel_storage: typing.Optional[typing.Union["ChannelStorageProperty", _IResolvable_9ceae33e]] = None,
        retention_period: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::IoTAnalytics::Channel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_name: ``AWS::IoTAnalytics::Channel.ChannelName``.
        :param channel_storage: ``AWS::IoTAnalytics::Channel.ChannelStorage``.
        :param retention_period: ``AWS::IoTAnalytics::Channel.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Channel.Tags``.
        """
        props = CfnChannelProps(
            channel_name=channel_name,
            channel_storage=channel_storage,
            retention_period=retention_period,
            tags=tags,
        )

        jsii.create(CfnChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::IoTAnalytics::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Channel.ChannelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelname
        """
        return jsii.get(self, "channelName")

    @channel_name.setter
    def channel_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "channelName", value)

    @builtins.property
    @jsii.member(jsii_name="channelStorage")
    def channel_storage(
        self,
    ) -> typing.Optional[typing.Union["ChannelStorageProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Channel.ChannelStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelstorage
        """
        return jsii.get(self, "channelStorage")

    @channel_storage.setter
    def channel_storage(
        self,
        value: typing.Optional[typing.Union["ChannelStorageProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "channelStorage", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Channel.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-retentionperiod
        """
        return jsii.get(self, "retentionPeriod")

    @retention_period.setter
    def retention_period(
        self,
        value: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "retentionPeriod", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannel.ChannelStorageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed_s3": "customerManagedS3",
            "service_managed_s3": "serviceManagedS3",
        },
    )
    class ChannelStorageProperty:
        def __init__(
            self,
            *,
            customer_managed_s3: typing.Optional[typing.Union["CfnChannel.CustomerManagedS3Property", _IResolvable_9ceae33e]] = None,
            service_managed_s3: typing.Optional[typing.Union["CfnChannel.ServiceManagedS3Property", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param customer_managed_s3: ``CfnChannel.ChannelStorageProperty.CustomerManagedS3``.
            :param service_managed_s3: ``CfnChannel.ChannelStorageProperty.ServiceManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html
            """
            self._values = {}
            if customer_managed_s3 is not None:
                self._values["customer_managed_s3"] = customer_managed_s3
            if service_managed_s3 is not None:
                self._values["service_managed_s3"] = service_managed_s3

        @builtins.property
        def customer_managed_s3(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.CustomerManagedS3Property", _IResolvable_9ceae33e]]:
            """``CfnChannel.ChannelStorageProperty.CustomerManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html#cfn-iotanalytics-channel-channelstorage-customermanageds3
            """
            return self._values.get("customer_managed_s3")

        @builtins.property
        def service_managed_s3(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.ServiceManagedS3Property", _IResolvable_9ceae33e]]:
            """``CfnChannel.ChannelStorageProperty.ServiceManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-channelstorage.html#cfn-iotanalytics-channel-channelstorage-servicemanageds3
            """
            return self._values.get("service_managed_s3")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannel.CustomerManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "role_arn": "roleArn",
            "key_prefix": "keyPrefix",
        },
    )
    class CustomerManagedS3Property:
        def __init__(
            self,
            *,
            bucket: str,
            role_arn: str,
            key_prefix: typing.Optional[str] = None,
        ) -> None:
            """
            :param bucket: ``CfnChannel.CustomerManagedS3Property.Bucket``.
            :param role_arn: ``CfnChannel.CustomerManagedS3Property.RoleArn``.
            :param key_prefix: ``CfnChannel.CustomerManagedS3Property.KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html
            """
            self._values = {
                "bucket": bucket,
                "role_arn": role_arn,
            }
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix

        @builtins.property
        def bucket(self) -> str:
            """``CfnChannel.CustomerManagedS3Property.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-bucket
            """
            return self._values.get("bucket")

        @builtins.property
        def role_arn(self) -> str:
            """``CfnChannel.CustomerManagedS3Property.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def key_prefix(self) -> typing.Optional[str]:
            """``CfnChannel.CustomerManagedS3Property.KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-customermanageds3.html#cfn-iotanalytics-channel-customermanageds3-keyprefix
            """
            return self._values.get("key_prefix")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannel.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param number_of_days: ``CfnChannel.RetentionPeriodProperty.NumberOfDays``.
            :param unlimited: ``CfnChannel.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html
            """
            self._values = {}
            if number_of_days is not None:
                self._values["number_of_days"] = number_of_days
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def number_of_days(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.RetentionPeriodProperty.NumberOfDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-numberofdays
            """
            return self._values.get("number_of_days")

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnChannel.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-unlimited
            """
            return self._values.get("unlimited")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannel.ServiceManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ServiceManagedS3Property:
        def __init__(self) -> None:
            """
            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-servicemanageds3.html
            """
            self._values = {}

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "channel_storage": "channelStorage",
        "retention_period": "retentionPeriod",
        "tags": "tags",
    },
)
class CfnChannelProps:
    def __init__(
        self,
        *,
        channel_name: typing.Optional[str] = None,
        channel_storage: typing.Optional[typing.Union["CfnChannel.ChannelStorageProperty", _IResolvable_9ceae33e]] = None,
        retention_period: typing.Optional[typing.Union["CfnChannel.RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTAnalytics::Channel``.

        :param channel_name: ``AWS::IoTAnalytics::Channel.ChannelName``.
        :param channel_storage: ``AWS::IoTAnalytics::Channel.ChannelStorage``.
        :param retention_period: ``AWS::IoTAnalytics::Channel.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
        """
        self._values = {}
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if channel_storage is not None:
            self._values["channel_storage"] = channel_storage
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Channel.ChannelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelname
        """
        return self._values.get("channel_name")

    @builtins.property
    def channel_storage(
        self,
    ) -> typing.Optional[typing.Union["CfnChannel.ChannelStorageProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Channel.ChannelStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelstorage
        """
        return self._values.get("channel_storage")

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["CfnChannel.RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Channel.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-retentionperiod
        """
        return self._values.get("retention_period")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::IoTAnalytics::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDataset(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset",
):
    """A CloudFormation ``AWS::IoTAnalytics::Dataset``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTAnalytics::Dataset
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        actions: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActionProperty", _IResolvable_9ceae33e]]],
        content_delivery_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DatasetContentDeliveryRuleProperty", _IResolvable_9ceae33e]]]] = None,
        dataset_name: typing.Optional[str] = None,
        retention_period: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        triggers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerProperty", _IResolvable_9ceae33e]]]] = None,
        versioning_configuration: typing.Optional[typing.Union["VersioningConfigurationProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::IoTAnalytics::Dataset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: ``AWS::IoTAnalytics::Dataset.Actions``.
        :param content_delivery_rules: ``AWS::IoTAnalytics::Dataset.ContentDeliveryRules``.
        :param dataset_name: ``AWS::IoTAnalytics::Dataset.DatasetName``.
        :param retention_period: ``AWS::IoTAnalytics::Dataset.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Dataset.Tags``.
        :param triggers: ``AWS::IoTAnalytics::Dataset.Triggers``.
        :param versioning_configuration: ``AWS::IoTAnalytics::Dataset.VersioningConfiguration``.
        """
        props = CfnDatasetProps(
            actions=actions,
            content_delivery_rules=content_delivery_rules,
            dataset_name=dataset_name,
            retention_period=retention_period,
            tags=tags,
            triggers=triggers,
            versioning_configuration=versioning_configuration,
        )

        jsii.create(CfnDataset, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::IoTAnalytics::Dataset.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActionProperty", _IResolvable_9ceae33e]]]:
        """``AWS::IoTAnalytics::Dataset.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-actions
        """
        return jsii.get(self, "actions")

    @actions.setter
    def actions(
        self,
        value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActionProperty", _IResolvable_9ceae33e]]],
    ) -> None:
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="contentDeliveryRules")
    def content_delivery_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DatasetContentDeliveryRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::IoTAnalytics::Dataset.ContentDeliveryRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-contentdeliveryrules
        """
        return jsii.get(self, "contentDeliveryRules")

    @content_delivery_rules.setter
    def content_delivery_rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DatasetContentDeliveryRuleProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "contentDeliveryRules", value)

    @builtins.property
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Dataset.DatasetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-datasetname
        """
        return jsii.get(self, "datasetName")

    @dataset_name.setter
    def dataset_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "datasetName", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Dataset.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-retentionperiod
        """
        return jsii.get(self, "retentionPeriod")

    @retention_period.setter
    def retention_period(
        self,
        value: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "retentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::IoTAnalytics::Dataset.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-triggers
        """
        return jsii.get(self, "triggers")

    @triggers.setter
    def triggers(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "triggers", value)

    @builtins.property
    @jsii.member(jsii_name="versioningConfiguration")
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union["VersioningConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Dataset.VersioningConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-versioningconfiguration
        """
        return jsii.get(self, "versioningConfiguration")

    @versioning_configuration.setter
    def versioning_configuration(
        self,
        value: typing.Optional[typing.Union["VersioningConfigurationProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "versioningConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_name": "actionName",
            "container_action": "containerAction",
            "query_action": "queryAction",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            action_name: str,
            container_action: typing.Optional[typing.Union["CfnDataset.ContainerActionProperty", _IResolvable_9ceae33e]] = None,
            query_action: typing.Optional[typing.Union["CfnDataset.QueryActionProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param action_name: ``CfnDataset.ActionProperty.ActionName``.
            :param container_action: ``CfnDataset.ActionProperty.ContainerAction``.
            :param query_action: ``CfnDataset.ActionProperty.QueryAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html
            """
            self._values = {
                "action_name": action_name,
            }
            if container_action is not None:
                self._values["container_action"] = container_action
            if query_action is not None:
                self._values["query_action"] = query_action

        @builtins.property
        def action_name(self) -> str:
            """``CfnDataset.ActionProperty.ActionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-actionname
            """
            return self._values.get("action_name")

        @builtins.property
        def container_action(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.ContainerActionProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.ActionProperty.ContainerAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-containeraction
            """
            return self._values.get("container_action")

        @builtins.property
        def query_action(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.QueryActionProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.ActionProperty.QueryAction``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-queryaction
            """
            return self._values.get("query_action")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.ContainerActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execution_role_arn": "executionRoleArn",
            "image": "image",
            "resource_configuration": "resourceConfiguration",
            "variables": "variables",
        },
    )
    class ContainerActionProperty:
        def __init__(
            self,
            *,
            execution_role_arn: str,
            image: str,
            resource_configuration: typing.Union["CfnDataset.ResourceConfigurationProperty", _IResolvable_9ceae33e],
            variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.VariableProperty", _IResolvable_9ceae33e]]]] = None,
        ) -> None:
            """
            :param execution_role_arn: ``CfnDataset.ContainerActionProperty.ExecutionRoleArn``.
            :param image: ``CfnDataset.ContainerActionProperty.Image``.
            :param resource_configuration: ``CfnDataset.ContainerActionProperty.ResourceConfiguration``.
            :param variables: ``CfnDataset.ContainerActionProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html
            """
            self._values = {
                "execution_role_arn": execution_role_arn,
                "image": image,
                "resource_configuration": resource_configuration,
            }
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def execution_role_arn(self) -> str:
            """``CfnDataset.ContainerActionProperty.ExecutionRoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-executionrolearn
            """
            return self._values.get("execution_role_arn")

        @builtins.property
        def image(self) -> str:
            """``CfnDataset.ContainerActionProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-image
            """
            return self._values.get("image")

        @builtins.property
        def resource_configuration(
            self,
        ) -> typing.Union["CfnDataset.ResourceConfigurationProperty", _IResolvable_9ceae33e]:
            """``CfnDataset.ContainerActionProperty.ResourceConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-resourceconfiguration
            """
            return self._values.get("resource_configuration")

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.VariableProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDataset.ContainerActionProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-variables
            """
            return self._values.get("variables")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.DatasetContentDeliveryRuleDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iot_events_destination_configuration": "iotEventsDestinationConfiguration",
            "s3_destination_configuration": "s3DestinationConfiguration",
        },
    )
    class DatasetContentDeliveryRuleDestinationProperty:
        def __init__(
            self,
            *,
            iot_events_destination_configuration: typing.Optional[typing.Union["CfnDataset.IotEventsDestinationConfigurationProperty", _IResolvable_9ceae33e]] = None,
            s3_destination_configuration: typing.Optional[typing.Union["CfnDataset.S3DestinationConfigurationProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param iot_events_destination_configuration: ``CfnDataset.DatasetContentDeliveryRuleDestinationProperty.IotEventsDestinationConfiguration``.
            :param s3_destination_configuration: ``CfnDataset.DatasetContentDeliveryRuleDestinationProperty.S3DestinationConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html
            """
            self._values = {}
            if iot_events_destination_configuration is not None:
                self._values["iot_events_destination_configuration"] = iot_events_destination_configuration
            if s3_destination_configuration is not None:
                self._values["s3_destination_configuration"] = s3_destination_configuration

        @builtins.property
        def iot_events_destination_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.IotEventsDestinationConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.DatasetContentDeliveryRuleDestinationProperty.IotEventsDestinationConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html#cfn-iotanalytics-dataset-datasetcontentdeliveryruledestination-ioteventsdestinationconfiguration
            """
            return self._values.get("iot_events_destination_configuration")

        @builtins.property
        def s3_destination_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.S3DestinationConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.DatasetContentDeliveryRuleDestinationProperty.S3DestinationConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryruledestination.html#cfn-iotanalytics-dataset-datasetcontentdeliveryruledestination-s3destinationconfiguration
            """
            return self._values.get("s3_destination_configuration")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentDeliveryRuleDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.DatasetContentDeliveryRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "entry_name": "entryName"},
    )
    class DatasetContentDeliveryRuleProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["CfnDataset.DatasetContentDeliveryRuleDestinationProperty", _IResolvable_9ceae33e],
            entry_name: typing.Optional[str] = None,
        ) -> None:
            """
            :param destination: ``CfnDataset.DatasetContentDeliveryRuleProperty.Destination``.
            :param entry_name: ``CfnDataset.DatasetContentDeliveryRuleProperty.EntryName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html
            """
            self._values = {
                "destination": destination,
            }
            if entry_name is not None:
                self._values["entry_name"] = entry_name

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["CfnDataset.DatasetContentDeliveryRuleDestinationProperty", _IResolvable_9ceae33e]:
            """``CfnDataset.DatasetContentDeliveryRuleProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html#cfn-iotanalytics-dataset-datasetcontentdeliveryrule-destination
            """
            return self._values.get("destination")

        @builtins.property
        def entry_name(self) -> typing.Optional[str]:
            """``CfnDataset.DatasetContentDeliveryRuleProperty.EntryName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-datasetcontentdeliveryrule.html#cfn-iotanalytics-dataset-datasetcontentdeliveryrule-entryname
            """
            return self._values.get("entry_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentDeliveryRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.DatasetContentVersionValueProperty",
        jsii_struct_bases=[],
        name_mapping={"dataset_name": "datasetName"},
    )
    class DatasetContentVersionValueProperty:
        def __init__(self, *, dataset_name: typing.Optional[str] = None) -> None:
            """
            :param dataset_name: ``CfnDataset.DatasetContentVersionValueProperty.DatasetName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-datasetcontentversionvalue.html
            """
            self._values = {}
            if dataset_name is not None:
                self._values["dataset_name"] = dataset_name

        @builtins.property
        def dataset_name(self) -> typing.Optional[str]:
            """``CfnDataset.DatasetContentVersionValueProperty.DatasetName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-datasetcontentversionvalue.html#cfn-iotanalytics-dataset-variable-datasetcontentversionvalue-datasetname
            """
            return self._values.get("dataset_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetContentVersionValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.DeltaTimeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "offset_seconds": "offsetSeconds",
            "time_expression": "timeExpression",
        },
    )
    class DeltaTimeProperty:
        def __init__(
            self, *, offset_seconds: jsii.Number, time_expression: str
        ) -> None:
            """
            :param offset_seconds: ``CfnDataset.DeltaTimeProperty.OffsetSeconds``.
            :param time_expression: ``CfnDataset.DeltaTimeProperty.TimeExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html
            """
            self._values = {
                "offset_seconds": offset_seconds,
                "time_expression": time_expression,
            }

        @builtins.property
        def offset_seconds(self) -> jsii.Number:
            """``CfnDataset.DeltaTimeProperty.OffsetSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-offsetseconds
            """
            return self._values.get("offset_seconds")

        @builtins.property
        def time_expression(self) -> str:
            """``CfnDataset.DeltaTimeProperty.TimeExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-timeexpression
            """
            return self._values.get("time_expression")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"delta_time": "deltaTime"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            delta_time: typing.Optional[typing.Union["CfnDataset.DeltaTimeProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param delta_time: ``CfnDataset.FilterProperty.DeltaTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html
            """
            self._values = {}
            if delta_time is not None:
                self._values["delta_time"] = delta_time

        @builtins.property
        def delta_time(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.DeltaTimeProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.FilterProperty.DeltaTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html#cfn-iotanalytics-dataset-filter-deltatime
            """
            return self._values.get("delta_time")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.GlueConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"database_name": "databaseName", "table_name": "tableName"},
    )
    class GlueConfigurationProperty:
        def __init__(self, *, database_name: str, table_name: str) -> None:
            """
            :param database_name: ``CfnDataset.GlueConfigurationProperty.DatabaseName``.
            :param table_name: ``CfnDataset.GlueConfigurationProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html
            """
            self._values = {
                "database_name": database_name,
                "table_name": table_name,
            }

        @builtins.property
        def database_name(self) -> str:
            """``CfnDataset.GlueConfigurationProperty.DatabaseName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html#cfn-iotanalytics-dataset-glueconfiguration-databasename
            """
            return self._values.get("database_name")

        @builtins.property
        def table_name(self) -> str:
            """``CfnDataset.GlueConfigurationProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-glueconfiguration.html#cfn-iotanalytics-dataset-glueconfiguration-tablename
            """
            return self._values.get("table_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.IotEventsDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "role_arn": "roleArn"},
    )
    class IotEventsDestinationConfigurationProperty:
        def __init__(self, *, input_name: str, role_arn: str) -> None:
            """
            :param input_name: ``CfnDataset.IotEventsDestinationConfigurationProperty.InputName``.
            :param role_arn: ``CfnDataset.IotEventsDestinationConfigurationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html
            """
            self._values = {
                "input_name": input_name,
                "role_arn": role_arn,
            }

        @builtins.property
        def input_name(self) -> str:
            """``CfnDataset.IotEventsDestinationConfigurationProperty.InputName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html#cfn-iotanalytics-dataset-ioteventsdestinationconfiguration-inputname
            """
            return self._values.get("input_name")

        @builtins.property
        def role_arn(self) -> str:
            """``CfnDataset.IotEventsDestinationConfigurationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-ioteventsdestinationconfiguration.html#cfn-iotanalytics-dataset-ioteventsdestinationconfiguration-rolearn
            """
            return self._values.get("role_arn")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.OutputFileUriValueProperty",
        jsii_struct_bases=[],
        name_mapping={"file_name": "fileName"},
    )
    class OutputFileUriValueProperty:
        def __init__(self, *, file_name: typing.Optional[str] = None) -> None:
            """
            :param file_name: ``CfnDataset.OutputFileUriValueProperty.FileName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-outputfileurivalue.html
            """
            self._values = {}
            if file_name is not None:
                self._values["file_name"] = file_name

        @builtins.property
        def file_name(self) -> typing.Optional[str]:
            """``CfnDataset.OutputFileUriValueProperty.FileName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-outputfileurivalue.html#cfn-iotanalytics-dataset-variable-outputfileurivalue-filename
            """
            return self._values.get("file_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFileUriValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.QueryActionProperty",
        jsii_struct_bases=[],
        name_mapping={"sql_query": "sqlQuery", "filters": "filters"},
    )
    class QueryActionProperty:
        def __init__(
            self,
            *,
            sql_query: str,
            filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.FilterProperty", _IResolvable_9ceae33e]]]] = None,
        ) -> None:
            """
            :param sql_query: ``CfnDataset.QueryActionProperty.SqlQuery``.
            :param filters: ``CfnDataset.QueryActionProperty.Filters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html
            """
            self._values = {
                "sql_query": sql_query,
            }
            if filters is not None:
                self._values["filters"] = filters

        @builtins.property
        def sql_query(self) -> str:
            """``CfnDataset.QueryActionProperty.SqlQuery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-sqlquery
            """
            return self._values.get("sql_query")

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.FilterProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDataset.QueryActionProperty.Filters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-filters
            """
            return self._values.get("filters")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.ResourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type": "computeType",
            "volume_size_in_gb": "volumeSizeInGb",
        },
    )
    class ResourceConfigurationProperty:
        def __init__(
            self, *, compute_type: str, volume_size_in_gb: jsii.Number
        ) -> None:
            """
            :param compute_type: ``CfnDataset.ResourceConfigurationProperty.ComputeType``.
            :param volume_size_in_gb: ``CfnDataset.ResourceConfigurationProperty.VolumeSizeInGB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html
            """
            self._values = {
                "compute_type": compute_type,
                "volume_size_in_gb": volume_size_in_gb,
            }

        @builtins.property
        def compute_type(self) -> str:
            """``CfnDataset.ResourceConfigurationProperty.ComputeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-computetype
            """
            return self._values.get("compute_type")

        @builtins.property
        def volume_size_in_gb(self) -> jsii.Number:
            """``CfnDataset.ResourceConfigurationProperty.VolumeSizeInGB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-volumesizeingb
            """
            return self._values.get("volume_size_in_gb")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: jsii.Number,
            unlimited: typing.Union[bool, _IResolvable_9ceae33e],
        ) -> None:
            """
            :param number_of_days: ``CfnDataset.RetentionPeriodProperty.NumberOfDays``.
            :param unlimited: ``CfnDataset.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html
            """
            self._values = {
                "number_of_days": number_of_days,
                "unlimited": unlimited,
            }

        @builtins.property
        def number_of_days(self) -> jsii.Number:
            """``CfnDataset.RetentionPeriodProperty.NumberOfDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-numberofdays
            """
            return self._values.get("number_of_days")

        @builtins.property
        def unlimited(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
            """``CfnDataset.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-unlimited
            """
            return self._values.get("unlimited")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "role_arn": "roleArn",
            "glue_configuration": "glueConfiguration",
        },
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: str,
            key: str,
            role_arn: str,
            glue_configuration: typing.Optional[typing.Union["CfnDataset.GlueConfigurationProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param bucket: ``CfnDataset.S3DestinationConfigurationProperty.Bucket``.
            :param key: ``CfnDataset.S3DestinationConfigurationProperty.Key``.
            :param role_arn: ``CfnDataset.S3DestinationConfigurationProperty.RoleArn``.
            :param glue_configuration: ``CfnDataset.S3DestinationConfigurationProperty.GlueConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html
            """
            self._values = {
                "bucket": bucket,
                "key": key,
                "role_arn": role_arn,
            }
            if glue_configuration is not None:
                self._values["glue_configuration"] = glue_configuration

        @builtins.property
        def bucket(self) -> str:
            """``CfnDataset.S3DestinationConfigurationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-bucket
            """
            return self._values.get("bucket")

        @builtins.property
        def key(self) -> str:
            """``CfnDataset.S3DestinationConfigurationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-key
            """
            return self._values.get("key")

        @builtins.property
        def role_arn(self) -> str:
            """``CfnDataset.S3DestinationConfigurationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def glue_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.GlueConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.S3DestinationConfigurationProperty.GlueConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-s3destinationconfiguration.html#cfn-iotanalytics-dataset-s3destinationconfiguration-glueconfiguration
            """
            return self._values.get("glue_configuration")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleProperty:
        def __init__(self, *, schedule_expression: str) -> None:
            """
            :param schedule_expression: ``CfnDataset.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger-schedule.html
            """
            self._values = {
                "schedule_expression": schedule_expression,
            }

        @builtins.property
        def schedule_expression(self) -> str:
            """``CfnDataset.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger-schedule.html#cfn-iotanalytics-dataset-trigger-schedule-scheduleexpression
            """
            return self._values.get("schedule_expression")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.TriggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule": "schedule",
            "triggering_dataset": "triggeringDataset",
        },
    )
    class TriggerProperty:
        def __init__(
            self,
            *,
            schedule: typing.Optional[typing.Union["CfnDataset.ScheduleProperty", _IResolvable_9ceae33e]] = None,
            triggering_dataset: typing.Optional[typing.Union["CfnDataset.TriggeringDatasetProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param schedule: ``CfnDataset.TriggerProperty.Schedule``.
            :param triggering_dataset: ``CfnDataset.TriggerProperty.TriggeringDataset``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html
            """
            self._values = {}
            if schedule is not None:
                self._values["schedule"] = schedule
            if triggering_dataset is not None:
                self._values["triggering_dataset"] = triggering_dataset

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.ScheduleProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.TriggerProperty.Schedule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-schedule
            """
            return self._values.get("schedule")

        @builtins.property
        def triggering_dataset(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.TriggeringDatasetProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.TriggerProperty.TriggeringDataset``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-triggeringdataset
            """
            return self._values.get("triggering_dataset")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.TriggeringDatasetProperty",
        jsii_struct_bases=[],
        name_mapping={"dataset_name": "datasetName"},
    )
    class TriggeringDatasetProperty:
        def __init__(self, *, dataset_name: str) -> None:
            """
            :param dataset_name: ``CfnDataset.TriggeringDatasetProperty.DatasetName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html
            """
            self._values = {
                "dataset_name": dataset_name,
            }

        @builtins.property
        def dataset_name(self) -> str:
            """``CfnDataset.TriggeringDatasetProperty.DatasetName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html#cfn-iotanalytics-dataset-triggeringdataset-datasetname
            """
            return self._values.get("dataset_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggeringDatasetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.VariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "variable_name": "variableName",
            "dataset_content_version_value": "datasetContentVersionValue",
            "double_value": "doubleValue",
            "output_file_uri_value": "outputFileUriValue",
            "string_value": "stringValue",
        },
    )
    class VariableProperty:
        def __init__(
            self,
            *,
            variable_name: str,
            dataset_content_version_value: typing.Optional[typing.Union["CfnDataset.DatasetContentVersionValueProperty", _IResolvable_9ceae33e]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            output_file_uri_value: typing.Optional[typing.Union["CfnDataset.OutputFileUriValueProperty", _IResolvable_9ceae33e]] = None,
            string_value: typing.Optional[str] = None,
        ) -> None:
            """
            :param variable_name: ``CfnDataset.VariableProperty.VariableName``.
            :param dataset_content_version_value: ``CfnDataset.VariableProperty.DatasetContentVersionValue``.
            :param double_value: ``CfnDataset.VariableProperty.DoubleValue``.
            :param output_file_uri_value: ``CfnDataset.VariableProperty.OutputFileUriValue``.
            :param string_value: ``CfnDataset.VariableProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html
            """
            self._values = {
                "variable_name": variable_name,
            }
            if dataset_content_version_value is not None:
                self._values["dataset_content_version_value"] = dataset_content_version_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if output_file_uri_value is not None:
                self._values["output_file_uri_value"] = output_file_uri_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def variable_name(self) -> str:
            """``CfnDataset.VariableProperty.VariableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-variablename
            """
            return self._values.get("variable_name")

        @builtins.property
        def dataset_content_version_value(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.DatasetContentVersionValueProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.VariableProperty.DatasetContentVersionValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-datasetcontentversionvalue
            """
            return self._values.get("dataset_content_version_value")

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            """``CfnDataset.VariableProperty.DoubleValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-doublevalue
            """
            return self._values.get("double_value")

        @builtins.property
        def output_file_uri_value(
            self,
        ) -> typing.Optional[typing.Union["CfnDataset.OutputFileUriValueProperty", _IResolvable_9ceae33e]]:
            """``CfnDataset.VariableProperty.OutputFileUriValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-outputfileurivalue
            """
            return self._values.get("output_file_uri_value")

        @builtins.property
        def string_value(self) -> typing.Optional[str]:
            """``CfnDataset.VariableProperty.StringValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-stringvalue
            """
            return self._values.get("string_value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDataset.VersioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_versions": "maxVersions", "unlimited": "unlimited"},
    )
    class VersioningConfigurationProperty:
        def __init__(
            self,
            *,
            max_versions: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param max_versions: ``CfnDataset.VersioningConfigurationProperty.MaxVersions``.
            :param unlimited: ``CfnDataset.VersioningConfigurationProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html
            """
            self._values = {}
            if max_versions is not None:
                self._values["max_versions"] = max_versions
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def max_versions(self) -> typing.Optional[jsii.Number]:
            """``CfnDataset.VersioningConfigurationProperty.MaxVersions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html#cfn-iotanalytics-dataset-versioningconfiguration-maxversions
            """
            return self._values.get("max_versions")

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDataset.VersioningConfigurationProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-versioningconfiguration.html#cfn-iotanalytics-dataset-versioningconfiguration-unlimited
            """
            return self._values.get("unlimited")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VersioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "content_delivery_rules": "contentDeliveryRules",
        "dataset_name": "datasetName",
        "retention_period": "retentionPeriod",
        "tags": "tags",
        "triggers": "triggers",
        "versioning_configuration": "versioningConfiguration",
    },
)
class CfnDatasetProps:
    def __init__(
        self,
        *,
        actions: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.ActionProperty", _IResolvable_9ceae33e]]],
        content_delivery_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.DatasetContentDeliveryRuleProperty", _IResolvable_9ceae33e]]]] = None,
        dataset_name: typing.Optional[str] = None,
        retention_period: typing.Optional[typing.Union["CfnDataset.RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        triggers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.TriggerProperty", _IResolvable_9ceae33e]]]] = None,
        versioning_configuration: typing.Optional[typing.Union["CfnDataset.VersioningConfigurationProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTAnalytics::Dataset``.

        :param actions: ``AWS::IoTAnalytics::Dataset.Actions``.
        :param content_delivery_rules: ``AWS::IoTAnalytics::Dataset.ContentDeliveryRules``.
        :param dataset_name: ``AWS::IoTAnalytics::Dataset.DatasetName``.
        :param retention_period: ``AWS::IoTAnalytics::Dataset.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Dataset.Tags``.
        :param triggers: ``AWS::IoTAnalytics::Dataset.Triggers``.
        :param versioning_configuration: ``AWS::IoTAnalytics::Dataset.VersioningConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
        """
        self._values = {
            "actions": actions,
        }
        if content_delivery_rules is not None:
            self._values["content_delivery_rules"] = content_delivery_rules
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers
        if versioning_configuration is not None:
            self._values["versioning_configuration"] = versioning_configuration

    @builtins.property
    def actions(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.ActionProperty", _IResolvable_9ceae33e]]]:
        """``AWS::IoTAnalytics::Dataset.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-actions
        """
        return self._values.get("actions")

    @builtins.property
    def content_delivery_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.DatasetContentDeliveryRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::IoTAnalytics::Dataset.ContentDeliveryRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-contentdeliveryrules
        """
        return self._values.get("content_delivery_rules")

    @builtins.property
    def dataset_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Dataset.DatasetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-datasetname
        """
        return self._values.get("dataset_name")

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["CfnDataset.RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Dataset.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-retentionperiod
        """
        return self._values.get("retention_period")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::IoTAnalytics::Dataset.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-tags
        """
        return self._values.get("tags")

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataset.TriggerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::IoTAnalytics::Dataset.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-triggers
        """
        return self._values.get("triggers")

    @builtins.property
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDataset.VersioningConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Dataset.VersioningConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-versioningconfiguration
        """
        return self._values.get("versioning_configuration")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDatastore(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastore",
):
    """A CloudFormation ``AWS::IoTAnalytics::Datastore``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTAnalytics::Datastore
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        datastore_name: typing.Optional[str] = None,
        datastore_storage: typing.Optional[typing.Union["DatastoreStorageProperty", _IResolvable_9ceae33e]] = None,
        retention_period: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::IoTAnalytics::Datastore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param datastore_name: ``AWS::IoTAnalytics::Datastore.DatastoreName``.
        :param datastore_storage: ``AWS::IoTAnalytics::Datastore.DatastoreStorage``.
        :param retention_period: ``AWS::IoTAnalytics::Datastore.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Datastore.Tags``.
        """
        props = CfnDatastoreProps(
            datastore_name=datastore_name,
            datastore_storage=datastore_storage,
            retention_period=retention_period,
            tags=tags,
        )

        jsii.create(CfnDatastore, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::IoTAnalytics::Datastore.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="datastoreName")
    def datastore_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Datastore.DatastoreName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorename
        """
        return jsii.get(self, "datastoreName")

    @datastore_name.setter
    def datastore_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "datastoreName", value)

    @builtins.property
    @jsii.member(jsii_name="datastoreStorage")
    def datastore_storage(
        self,
    ) -> typing.Optional[typing.Union["DatastoreStorageProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Datastore.DatastoreStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorestorage
        """
        return jsii.get(self, "datastoreStorage")

    @datastore_storage.setter
    def datastore_storage(
        self,
        value: typing.Optional[typing.Union["DatastoreStorageProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "datastoreStorage", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Datastore.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-retentionperiod
        """
        return jsii.get(self, "retentionPeriod")

    @retention_period.setter
    def retention_period(
        self,
        value: typing.Optional[typing.Union["RetentionPeriodProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "retentionPeriod", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastore.CustomerManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "role_arn": "roleArn",
            "key_prefix": "keyPrefix",
        },
    )
    class CustomerManagedS3Property:
        def __init__(
            self,
            *,
            bucket: str,
            role_arn: str,
            key_prefix: typing.Optional[str] = None,
        ) -> None:
            """
            :param bucket: ``CfnDatastore.CustomerManagedS3Property.Bucket``.
            :param role_arn: ``CfnDatastore.CustomerManagedS3Property.RoleArn``.
            :param key_prefix: ``CfnDatastore.CustomerManagedS3Property.KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html
            """
            self._values = {
                "bucket": bucket,
                "role_arn": role_arn,
            }
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix

        @builtins.property
        def bucket(self) -> str:
            """``CfnDatastore.CustomerManagedS3Property.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-bucket
            """
            return self._values.get("bucket")

        @builtins.property
        def role_arn(self) -> str:
            """``CfnDatastore.CustomerManagedS3Property.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def key_prefix(self) -> typing.Optional[str]:
            """``CfnDatastore.CustomerManagedS3Property.KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-customermanageds3.html#cfn-iotanalytics-datastore-customermanageds3-keyprefix
            """
            return self._values.get("key_prefix")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastore.DatastoreStorageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed_s3": "customerManagedS3",
            "service_managed_s3": "serviceManagedS3",
        },
    )
    class DatastoreStorageProperty:
        def __init__(
            self,
            *,
            customer_managed_s3: typing.Optional[typing.Union["CfnDatastore.CustomerManagedS3Property", _IResolvable_9ceae33e]] = None,
            service_managed_s3: typing.Optional[typing.Union["CfnDatastore.ServiceManagedS3Property", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param customer_managed_s3: ``CfnDatastore.DatastoreStorageProperty.CustomerManagedS3``.
            :param service_managed_s3: ``CfnDatastore.DatastoreStorageProperty.ServiceManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html
            """
            self._values = {}
            if customer_managed_s3 is not None:
                self._values["customer_managed_s3"] = customer_managed_s3
            if service_managed_s3 is not None:
                self._values["service_managed_s3"] = service_managed_s3

        @builtins.property
        def customer_managed_s3(
            self,
        ) -> typing.Optional[typing.Union["CfnDatastore.CustomerManagedS3Property", _IResolvable_9ceae33e]]:
            """``CfnDatastore.DatastoreStorageProperty.CustomerManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html#cfn-iotanalytics-datastore-datastorestorage-customermanageds3
            """
            return self._values.get("customer_managed_s3")

        @builtins.property
        def service_managed_s3(
            self,
        ) -> typing.Optional[typing.Union["CfnDatastore.ServiceManagedS3Property", _IResolvable_9ceae33e]]:
            """``CfnDatastore.DatastoreStorageProperty.ServiceManagedS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-datastorestorage.html#cfn-iotanalytics-datastore-datastorestorage-servicemanageds3
            """
            return self._values.get("service_managed_s3")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastoreStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastore.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"number_of_days": "numberOfDays", "unlimited": "unlimited"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            number_of_days: typing.Optional[jsii.Number] = None,
            unlimited: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param number_of_days: ``CfnDatastore.RetentionPeriodProperty.NumberOfDays``.
            :param unlimited: ``CfnDatastore.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html
            """
            self._values = {}
            if number_of_days is not None:
                self._values["number_of_days"] = number_of_days
            if unlimited is not None:
                self._values["unlimited"] = unlimited

        @builtins.property
        def number_of_days(self) -> typing.Optional[jsii.Number]:
            """``CfnDatastore.RetentionPeriodProperty.NumberOfDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-numberofdays
            """
            return self._values.get("number_of_days")

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDatastore.RetentionPeriodProperty.Unlimited``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-unlimited
            """
            return self._values.get("unlimited")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastore.ServiceManagedS3Property",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ServiceManagedS3Property:
        def __init__(self) -> None:
            """
            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-servicemanageds3.html
            """
            self._values = {}

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceManagedS3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnDatastoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "datastore_name": "datastoreName",
        "datastore_storage": "datastoreStorage",
        "retention_period": "retentionPeriod",
        "tags": "tags",
    },
)
class CfnDatastoreProps:
    def __init__(
        self,
        *,
        datastore_name: typing.Optional[str] = None,
        datastore_storage: typing.Optional[typing.Union["CfnDatastore.DatastoreStorageProperty", _IResolvable_9ceae33e]] = None,
        retention_period: typing.Optional[typing.Union["CfnDatastore.RetentionPeriodProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTAnalytics::Datastore``.

        :param datastore_name: ``AWS::IoTAnalytics::Datastore.DatastoreName``.
        :param datastore_storage: ``AWS::IoTAnalytics::Datastore.DatastoreStorage``.
        :param retention_period: ``AWS::IoTAnalytics::Datastore.RetentionPeriod``.
        :param tags: ``AWS::IoTAnalytics::Datastore.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
        """
        self._values = {}
        if datastore_name is not None:
            self._values["datastore_name"] = datastore_name
        if datastore_storage is not None:
            self._values["datastore_storage"] = datastore_storage
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datastore_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Datastore.DatastoreName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorename
        """
        return self._values.get("datastore_name")

    @builtins.property
    def datastore_storage(
        self,
    ) -> typing.Optional[typing.Union["CfnDatastore.DatastoreStorageProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Datastore.DatastoreStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorestorage
        """
        return self._values.get("datastore_storage")

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union["CfnDatastore.RetentionPeriodProperty", _IResolvable_9ceae33e]]:
        """``AWS::IoTAnalytics::Datastore.RetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-retentionperiod
        """
        return self._values.get("retention_period")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::IoTAnalytics::Datastore.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatastoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnPipeline(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline",
):
    """A CloudFormation ``AWS::IoTAnalytics::Pipeline``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
    cloudformationResource:
    :cloudformationResource:: AWS::IoTAnalytics::Pipeline
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        pipeline_activities: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActivityProperty", _IResolvable_9ceae33e]]],
        pipeline_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::IoTAnalytics::Pipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param pipeline_activities: ``AWS::IoTAnalytics::Pipeline.PipelineActivities``.
        :param pipeline_name: ``AWS::IoTAnalytics::Pipeline.PipelineName``.
        :param tags: ``AWS::IoTAnalytics::Pipeline.Tags``.
        """
        props = CfnPipelineProps(
            pipeline_activities=pipeline_activities,
            pipeline_name=pipeline_name,
            tags=tags,
        )

        jsii.create(CfnPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::IoTAnalytics::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="pipelineActivities")
    def pipeline_activities(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActivityProperty", _IResolvable_9ceae33e]]]:
        """``AWS::IoTAnalytics::Pipeline.PipelineActivities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelineactivities
        """
        return jsii.get(self, "pipelineActivities")

    @pipeline_activities.setter
    def pipeline_activities(
        self,
        value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ActivityProperty", _IResolvable_9ceae33e]]],
    ) -> None:
        jsii.set(self, "pipelineActivities", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Pipeline.PipelineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelinename
        """
        return jsii.get(self, "pipelineName")

    @pipeline_name.setter
    def pipeline_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "pipelineName", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.ActivityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_attributes": "addAttributes",
            "channel": "channel",
            "datastore": "datastore",
            "device_registry_enrich": "deviceRegistryEnrich",
            "device_shadow_enrich": "deviceShadowEnrich",
            "filter": "filter",
            "lambda_": "lambda",
            "math": "math",
            "remove_attributes": "removeAttributes",
            "select_attributes": "selectAttributes",
        },
    )
    class ActivityProperty:
        def __init__(
            self,
            *,
            add_attributes: typing.Optional[typing.Union["CfnPipeline.AddAttributesProperty", _IResolvable_9ceae33e]] = None,
            channel: typing.Optional[typing.Union["CfnPipeline.ChannelProperty", _IResolvable_9ceae33e]] = None,
            datastore: typing.Optional[typing.Union["CfnPipeline.DatastoreProperty", _IResolvable_9ceae33e]] = None,
            device_registry_enrich: typing.Optional[typing.Union["CfnPipeline.DeviceRegistryEnrichProperty", _IResolvable_9ceae33e]] = None,
            device_shadow_enrich: typing.Optional[typing.Union["CfnPipeline.DeviceShadowEnrichProperty", _IResolvable_9ceae33e]] = None,
            filter: typing.Optional[typing.Union["CfnPipeline.FilterProperty", _IResolvable_9ceae33e]] = None,
            lambda_: typing.Optional[typing.Union["CfnPipeline.LambdaProperty", _IResolvable_9ceae33e]] = None,
            math: typing.Optional[typing.Union["CfnPipeline.MathProperty", _IResolvable_9ceae33e]] = None,
            remove_attributes: typing.Optional[typing.Union["CfnPipeline.RemoveAttributesProperty", _IResolvable_9ceae33e]] = None,
            select_attributes: typing.Optional[typing.Union["CfnPipeline.SelectAttributesProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param add_attributes: ``CfnPipeline.ActivityProperty.AddAttributes``.
            :param channel: ``CfnPipeline.ActivityProperty.Channel``.
            :param datastore: ``CfnPipeline.ActivityProperty.Datastore``.
            :param device_registry_enrich: ``CfnPipeline.ActivityProperty.DeviceRegistryEnrich``.
            :param device_shadow_enrich: ``CfnPipeline.ActivityProperty.DeviceShadowEnrich``.
            :param filter: ``CfnPipeline.ActivityProperty.Filter``.
            :param lambda_: ``CfnPipeline.ActivityProperty.Lambda``.
            :param math: ``CfnPipeline.ActivityProperty.Math``.
            :param remove_attributes: ``CfnPipeline.ActivityProperty.RemoveAttributes``.
            :param select_attributes: ``CfnPipeline.ActivityProperty.SelectAttributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html
            """
            self._values = {}
            if add_attributes is not None:
                self._values["add_attributes"] = add_attributes
            if channel is not None:
                self._values["channel"] = channel
            if datastore is not None:
                self._values["datastore"] = datastore
            if device_registry_enrich is not None:
                self._values["device_registry_enrich"] = device_registry_enrich
            if device_shadow_enrich is not None:
                self._values["device_shadow_enrich"] = device_shadow_enrich
            if filter is not None:
                self._values["filter"] = filter
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if math is not None:
                self._values["math"] = math
            if remove_attributes is not None:
                self._values["remove_attributes"] = remove_attributes
            if select_attributes is not None:
                self._values["select_attributes"] = select_attributes

        @builtins.property
        def add_attributes(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.AddAttributesProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.AddAttributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-addattributes
            """
            return self._values.get("add_attributes")

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.ChannelProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.Channel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-channel
            """
            return self._values.get("channel")

        @builtins.property
        def datastore(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.DatastoreProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.Datastore``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-datastore
            """
            return self._values.get("datastore")

        @builtins.property
        def device_registry_enrich(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.DeviceRegistryEnrichProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.DeviceRegistryEnrich``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceregistryenrich
            """
            return self._values.get("device_registry_enrich")

        @builtins.property
        def device_shadow_enrich(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.DeviceShadowEnrichProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.DeviceShadowEnrich``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceshadowenrich
            """
            return self._values.get("device_shadow_enrich")

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.FilterProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-filter
            """
            return self._values.get("filter")

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.LambdaProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.Lambda``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-lambda
            """
            return self._values.get("lambda_")

        @builtins.property
        def math(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.MathProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.Math``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-math
            """
            return self._values.get("math")

        @builtins.property
        def remove_attributes(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.RemoveAttributesProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.RemoveAttributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-removeattributes
            """
            return self._values.get("remove_attributes")

        @builtins.property
        def select_attributes(
            self,
        ) -> typing.Optional[typing.Union["CfnPipeline.SelectAttributesProperty", _IResolvable_9ceae33e]]:
            """``CfnPipeline.ActivityProperty.SelectAttributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-selectattributes
            """
            return self._values.get("select_attributes")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActivityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.AddAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class AddAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param attributes: ``CfnPipeline.AddAttributesProperty.Attributes``.
            :param name: ``CfnPipeline.AddAttributesProperty.Name``.
            :param next: ``CfnPipeline.AddAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html
            """
            self._values = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(self) -> typing.Any:
            """``CfnPipeline.AddAttributesProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-attributes
            """
            return self._values.get("attributes")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.AddAttributesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.AddAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_name": "channelName", "name": "name", "next": "next"},
    )
    class ChannelProperty:
        def __init__(
            self,
            *,
            channel_name: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param channel_name: ``CfnPipeline.ChannelProperty.ChannelName``.
            :param name: ``CfnPipeline.ChannelProperty.Name``.
            :param next: ``CfnPipeline.ChannelProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html
            """
            self._values = {}
            if channel_name is not None:
                self._values["channel_name"] = channel_name
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def channel_name(self) -> typing.Optional[str]:
            """``CfnPipeline.ChannelProperty.ChannelName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-channelname
            """
            return self._values.get("channel_name")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.ChannelProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.ChannelProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.DatastoreProperty",
        jsii_struct_bases=[],
        name_mapping={"datastore_name": "datastoreName", "name": "name"},
    )
    class DatastoreProperty:
        def __init__(
            self,
            *,
            datastore_name: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
        ) -> None:
            """
            :param datastore_name: ``CfnPipeline.DatastoreProperty.DatastoreName``.
            :param name: ``CfnPipeline.DatastoreProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html
            """
            self._values = {}
            if datastore_name is not None:
                self._values["datastore_name"] = datastore_name
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def datastore_name(self) -> typing.Optional[str]:
            """``CfnPipeline.DatastoreProperty.DatastoreName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-datastorename
            """
            return self._values.get("datastore_name")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.DatastoreProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-name
            """
            return self._values.get("name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatastoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.DeviceRegistryEnrichProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "name": "name",
            "next": "next",
            "role_arn": "roleArn",
            "thing_name": "thingName",
        },
    )
    class DeviceRegistryEnrichProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
            role_arn: typing.Optional[str] = None,
            thing_name: typing.Optional[str] = None,
        ) -> None:
            """
            :param attribute: ``CfnPipeline.DeviceRegistryEnrichProperty.Attribute``.
            :param name: ``CfnPipeline.DeviceRegistryEnrichProperty.Name``.
            :param next: ``CfnPipeline.DeviceRegistryEnrichProperty.Next``.
            :param role_arn: ``CfnPipeline.DeviceRegistryEnrichProperty.RoleArn``.
            :param thing_name: ``CfnPipeline.DeviceRegistryEnrichProperty.ThingName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html
            """
            self._values = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if thing_name is not None:
                self._values["thing_name"] = thing_name

        @builtins.property
        def attribute(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceRegistryEnrichProperty.Attribute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-attribute
            """
            return self._values.get("attribute")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceRegistryEnrichProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceRegistryEnrichProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-next
            """
            return self._values.get("next")

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceRegistryEnrichProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def thing_name(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceRegistryEnrichProperty.ThingName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-thingname
            """
            return self._values.get("thing_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceRegistryEnrichProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.DeviceShadowEnrichProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "name": "name",
            "next": "next",
            "role_arn": "roleArn",
            "thing_name": "thingName",
        },
    )
    class DeviceShadowEnrichProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
            role_arn: typing.Optional[str] = None,
            thing_name: typing.Optional[str] = None,
        ) -> None:
            """
            :param attribute: ``CfnPipeline.DeviceShadowEnrichProperty.Attribute``.
            :param name: ``CfnPipeline.DeviceShadowEnrichProperty.Name``.
            :param next: ``CfnPipeline.DeviceShadowEnrichProperty.Next``.
            :param role_arn: ``CfnPipeline.DeviceShadowEnrichProperty.RoleArn``.
            :param thing_name: ``CfnPipeline.DeviceShadowEnrichProperty.ThingName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html
            """
            self._values = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if thing_name is not None:
                self._values["thing_name"] = thing_name

        @builtins.property
        def attribute(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceShadowEnrichProperty.Attribute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-attribute
            """
            return self._values.get("attribute")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceShadowEnrichProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceShadowEnrichProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-next
            """
            return self._values.get("next")

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceShadowEnrichProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def thing_name(self) -> typing.Optional[str]:
            """``CfnPipeline.DeviceShadowEnrichProperty.ThingName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-thingname
            """
            return self._values.get("thing_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceShadowEnrichProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter", "name": "name", "next": "next"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            filter: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param filter: ``CfnPipeline.FilterProperty.Filter``.
            :param name: ``CfnPipeline.FilterProperty.Name``.
            :param next: ``CfnPipeline.FilterProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html
            """
            self._values = {}
            if filter is not None:
                self._values["filter"] = filter
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def filter(self) -> typing.Optional[str]:
            """``CfnPipeline.FilterProperty.Filter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-filter
            """
            return self._values.get("filter")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.FilterProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.FilterProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "lambda_name": "lambdaName",
            "name": "name",
            "next": "next",
        },
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            lambda_name: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param batch_size: ``CfnPipeline.LambdaProperty.BatchSize``.
            :param lambda_name: ``CfnPipeline.LambdaProperty.LambdaName``.
            :param name: ``CfnPipeline.LambdaProperty.Name``.
            :param next: ``CfnPipeline.LambdaProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html
            """
            self._values = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if lambda_name is not None:
                self._values["lambda_name"] = lambda_name
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            """``CfnPipeline.LambdaProperty.BatchSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-batchsize
            """
            return self._values.get("batch_size")

        @builtins.property
        def lambda_name(self) -> typing.Optional[str]:
            """``CfnPipeline.LambdaProperty.LambdaName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-lambdaname
            """
            return self._values.get("lambda_name")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.LambdaProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.LambdaProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.MathProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "math": "math",
            "name": "name",
            "next": "next",
        },
    )
    class MathProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[str] = None,
            math: typing.Optional[str] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param attribute: ``CfnPipeline.MathProperty.Attribute``.
            :param math: ``CfnPipeline.MathProperty.Math``.
            :param name: ``CfnPipeline.MathProperty.Name``.
            :param next: ``CfnPipeline.MathProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html
            """
            self._values = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if math is not None:
                self._values["math"] = math
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attribute(self) -> typing.Optional[str]:
            """``CfnPipeline.MathProperty.Attribute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-attribute
            """
            return self._values.get("attribute")

        @builtins.property
        def math(self) -> typing.Optional[str]:
            """``CfnPipeline.MathProperty.Math``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-math
            """
            return self._values.get("math")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.MathProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.MathProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.RemoveAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class RemoveAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.List[str]] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param attributes: ``CfnPipeline.RemoveAttributesProperty.Attributes``.
            :param name: ``CfnPipeline.RemoveAttributesProperty.Name``.
            :param next: ``CfnPipeline.RemoveAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html
            """
            self._values = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(self) -> typing.Optional[typing.List[str]]:
            """``CfnPipeline.RemoveAttributesProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-attributes
            """
            return self._values.get("attributes")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.RemoveAttributesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.RemoveAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoveAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipeline.SelectAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name", "next": "next"},
    )
    class SelectAttributesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.List[str]] = None,
            name: typing.Optional[str] = None,
            next: typing.Optional[str] = None,
        ) -> None:
            """
            :param attributes: ``CfnPipeline.SelectAttributesProperty.Attributes``.
            :param name: ``CfnPipeline.SelectAttributesProperty.Name``.
            :param next: ``CfnPipeline.SelectAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html
            """
            self._values = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name
            if next is not None:
                self._values["next"] = next

        @builtins.property
        def attributes(self) -> typing.Optional[typing.List[str]]:
            """``CfnPipeline.SelectAttributesProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-attributes
            """
            return self._values.get("attributes")

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPipeline.SelectAttributesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-name
            """
            return self._values.get("name")

        @builtins.property
        def next(self) -> typing.Optional[str]:
            """``CfnPipeline.SelectAttributesProperty.Next``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-next
            """
            return self._values.get("next")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelectAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_iotanalytics.CfnPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline_activities": "pipelineActivities",
        "pipeline_name": "pipelineName",
        "tags": "tags",
    },
)
class CfnPipelineProps:
    def __init__(
        self,
        *,
        pipeline_activities: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ActivityProperty", _IResolvable_9ceae33e]]],
        pipeline_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTAnalytics::Pipeline``.

        :param pipeline_activities: ``AWS::IoTAnalytics::Pipeline.PipelineActivities``.
        :param pipeline_name: ``AWS::IoTAnalytics::Pipeline.PipelineName``.
        :param tags: ``AWS::IoTAnalytics::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
        """
        self._values = {
            "pipeline_activities": pipeline_activities,
        }
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def pipeline_activities(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnPipeline.ActivityProperty", _IResolvable_9ceae33e]]]:
        """``AWS::IoTAnalytics::Pipeline.PipelineActivities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelineactivities
        """
        return self._values.get("pipeline_activities")

    @builtins.property
    def pipeline_name(self) -> typing.Optional[str]:
        """``AWS::IoTAnalytics::Pipeline.PipelineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelinename
        """
        return self._values.get("pipeline_name")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::IoTAnalytics::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnChannel",
    "CfnChannelProps",
    "CfnDataset",
    "CfnDatasetProps",
    "CfnDatastore",
    "CfnDatastoreProps",
    "CfnPipeline",
    "CfnPipelineProps",
]

publication.publish()
