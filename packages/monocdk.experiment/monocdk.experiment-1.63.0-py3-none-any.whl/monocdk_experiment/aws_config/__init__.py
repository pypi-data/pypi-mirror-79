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
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    Resource as _Resource_884d0774,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_events import (
    EventPattern as _EventPattern_8aa7b781,
    IRuleTarget as _IRuleTarget_41800a77,
    OnEventOptions as _OnEventOptions_926fbcf9,
    Rule as _Rule_c38e0b39,
)
from ..aws_iam import IRole as _IRole_e69bbae4
from ..aws_lambda import IFunction as _IFunction_1c1de0bc
from ..aws_sns import ITopic as _ITopic_ef0ebe0e


@jsii.implements(_IInspectable_051e6ed8)
class CfnAggregationAuthorization(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnAggregationAuthorization",
):
    """A CloudFormation ``AWS::Config::AggregationAuthorization``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::AggregationAuthorization
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        authorized_account_id: str,
        authorized_aws_region: str,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::Config::AggregationAuthorization``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authorized_account_id: ``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.
        :param authorized_aws_region: ``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.
        :param tags: ``AWS::Config::AggregationAuthorization.Tags``.
        """
        props = CfnAggregationAuthorizationProps(
            authorized_account_id=authorized_account_id,
            authorized_aws_region=authorized_aws_region,
            tags=tags,
        )

        jsii.create(CfnAggregationAuthorization, self, [scope, id, props])

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
        """``AWS::Config::AggregationAuthorization.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="authorizedAccountId")
    def authorized_account_id(self) -> str:
        """``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedaccountid
        """
        return jsii.get(self, "authorizedAccountId")

    @authorized_account_id.setter
    def authorized_account_id(self, value: str) -> None:
        jsii.set(self, "authorizedAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="authorizedAwsRegion")
    def authorized_aws_region(self) -> str:
        """``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedawsregion
        """
        return jsii.get(self, "authorizedAwsRegion")

    @authorized_aws_region.setter
    def authorized_aws_region(self, value: str) -> None:
        jsii.set(self, "authorizedAwsRegion", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnAggregationAuthorizationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_account_id": "authorizedAccountId",
        "authorized_aws_region": "authorizedAwsRegion",
        "tags": "tags",
    },
)
class CfnAggregationAuthorizationProps:
    def __init__(
        self,
        *,
        authorized_account_id: str,
        authorized_aws_region: str,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::AggregationAuthorization``.

        :param authorized_account_id: ``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.
        :param authorized_aws_region: ``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.
        :param tags: ``AWS::Config::AggregationAuthorization.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
        """
        self._values = {
            "authorized_account_id": authorized_account_id,
            "authorized_aws_region": authorized_aws_region,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authorized_account_id(self) -> str:
        """``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedaccountid
        """
        return self._values.get("authorized_account_id")

    @builtins.property
    def authorized_aws_region(self) -> str:
        """``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedawsregion
        """
        return self._values.get("authorized_aws_region")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Config::AggregationAuthorization.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAggregationAuthorizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnConfigRule(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnConfigRule",
):
    """A CloudFormation ``AWS::Config::ConfigRule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope_: _Construct_f50a3f53,
        id: str,
        *,
        source: typing.Union["SourceProperty", _IResolvable_9ceae33e],
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Any = None,
        maximum_execution_frequency: typing.Optional[str] = None,
        scope: typing.Optional[typing.Union["ScopeProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::Config::ConfigRule``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source: ``AWS::Config::ConfigRule.Source``.
        :param config_rule_name: ``AWS::Config::ConfigRule.ConfigRuleName``.
        :param description: ``AWS::Config::ConfigRule.Description``.
        :param input_parameters: ``AWS::Config::ConfigRule.InputParameters``.
        :param maximum_execution_frequency: ``AWS::Config::ConfigRule.MaximumExecutionFrequency``.
        :param scope: ``AWS::Config::ConfigRule.Scope``.
        """
        props = CfnConfigRuleProps(
            source=source,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
            scope=scope,
        )

        jsii.create(CfnConfigRule, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrComplianceType")
    def attr_compliance_type(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Compliance.Type
        """
        return jsii.get(self, "attrComplianceType")

    @builtins.property
    @jsii.member(jsii_name="attrConfigRuleId")
    def attr_config_rule_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConfigRuleId
        """
        return jsii.get(self, "attrConfigRuleId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="inputParameters")
    def input_parameters(self) -> typing.Any:
        """``AWS::Config::ConfigRule.InputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-inputparameters
        """
        return jsii.get(self, "inputParameters")

    @input_parameters.setter
    def input_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "inputParameters", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Union["SourceProperty", _IResolvable_9ceae33e]:
        """``AWS::Config::ConfigRule.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-source
        """
        return jsii.get(self, "source")

    @source.setter
    def source(
        self, value: typing.Union["SourceProperty", _IResolvable_9ceae33e]
    ) -> None:
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.ConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-configrulename
        """
        return jsii.get(self, "configRuleName")

    @config_rule_name.setter
    def config_rule_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "configRuleName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="maximumExecutionFrequency")
    def maximum_execution_frequency(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.MaximumExecutionFrequency``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-maximumexecutionfrequency
        """
        return jsii.get(self, "maximumExecutionFrequency")

    @maximum_execution_frequency.setter
    def maximum_execution_frequency(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "maximumExecutionFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> typing.Optional[typing.Union["ScopeProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigRule.Scope``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-scope
        """
        return jsii.get(self, "scope")

    @scope.setter
    def scope(
        self,
        value: typing.Optional[typing.Union["ScopeProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "scope", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigRule.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compliance_resource_id": "complianceResourceId",
            "compliance_resource_types": "complianceResourceTypes",
            "tag_key": "tagKey",
            "tag_value": "tagValue",
        },
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            compliance_resource_id: typing.Optional[str] = None,
            compliance_resource_types: typing.Optional[typing.List[str]] = None,
            tag_key: typing.Optional[str] = None,
            tag_value: typing.Optional[str] = None,
        ) -> None:
            """
            :param compliance_resource_id: ``CfnConfigRule.ScopeProperty.ComplianceResourceId``.
            :param compliance_resource_types: ``CfnConfigRule.ScopeProperty.ComplianceResourceTypes``.
            :param tag_key: ``CfnConfigRule.ScopeProperty.TagKey``.
            :param tag_value: ``CfnConfigRule.ScopeProperty.TagValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html
            """
            self._values = {}
            if compliance_resource_id is not None:
                self._values["compliance_resource_id"] = compliance_resource_id
            if compliance_resource_types is not None:
                self._values["compliance_resource_types"] = compliance_resource_types
            if tag_key is not None:
                self._values["tag_key"] = tag_key
            if tag_value is not None:
                self._values["tag_value"] = tag_value

        @builtins.property
        def compliance_resource_id(self) -> typing.Optional[str]:
            """``CfnConfigRule.ScopeProperty.ComplianceResourceId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourceid
            """
            return self._values.get("compliance_resource_id")

        @builtins.property
        def compliance_resource_types(self) -> typing.Optional[typing.List[str]]:
            """``CfnConfigRule.ScopeProperty.ComplianceResourceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourcetypes
            """
            return self._values.get("compliance_resource_types")

        @builtins.property
        def tag_key(self) -> typing.Optional[str]:
            """``CfnConfigRule.ScopeProperty.TagKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagkey
            """
            return self._values.get("tag_key")

        @builtins.property
        def tag_value(self) -> typing.Optional[str]:
            """``CfnConfigRule.ScopeProperty.TagValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagvalue
            """
            return self._values.get("tag_value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigRule.SourceDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source": "eventSource",
            "message_type": "messageType",
            "maximum_execution_frequency": "maximumExecutionFrequency",
        },
    )
    class SourceDetailProperty:
        def __init__(
            self,
            *,
            event_source: str,
            message_type: str,
            maximum_execution_frequency: typing.Optional[str] = None,
        ) -> None:
            """
            :param event_source: ``CfnConfigRule.SourceDetailProperty.EventSource``.
            :param message_type: ``CfnConfigRule.SourceDetailProperty.MessageType``.
            :param maximum_execution_frequency: ``CfnConfigRule.SourceDetailProperty.MaximumExecutionFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html
            """
            self._values = {
                "event_source": event_source,
                "message_type": message_type,
            }
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency

        @builtins.property
        def event_source(self) -> str:
            """``CfnConfigRule.SourceDetailProperty.EventSource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-source-sourcedetail-eventsource
            """
            return self._values.get("event_source")

        @builtins.property
        def message_type(self) -> str:
            """``CfnConfigRule.SourceDetailProperty.MessageType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-source-sourcedetail-messagetype
            """
            return self._values.get("message_type")

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[str]:
            """``CfnConfigRule.SourceDetailProperty.MaximumExecutionFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-sourcedetail-maximumexecutionfrequency
            """
            return self._values.get("maximum_execution_frequency")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigRule.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner": "owner",
            "source_identifier": "sourceIdentifier",
            "source_details": "sourceDetails",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            owner: str,
            source_identifier: str,
            source_details: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigRule.SourceDetailProperty", _IResolvable_9ceae33e]]]] = None,
        ) -> None:
            """
            :param owner: ``CfnConfigRule.SourceProperty.Owner``.
            :param source_identifier: ``CfnConfigRule.SourceProperty.SourceIdentifier``.
            :param source_details: ``CfnConfigRule.SourceProperty.SourceDetails``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html
            """
            self._values = {
                "owner": owner,
                "source_identifier": source_identifier,
            }
            if source_details is not None:
                self._values["source_details"] = source_details

        @builtins.property
        def owner(self) -> str:
            """``CfnConfigRule.SourceProperty.Owner``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-owner
            """
            return self._values.get("owner")

        @builtins.property
        def source_identifier(self) -> str:
            """``CfnConfigRule.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourceidentifier
            """
            return self._values.get("source_identifier")

        @builtins.property
        def source_details(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigRule.SourceDetailProperty", _IResolvable_9ceae33e]]]]:
            """``CfnConfigRule.SourceProperty.SourceDetails``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourcedetails
            """
            return self._values.get("source_details")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnConfigRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "scope": "scope",
    },
)
class CfnConfigRuleProps:
    def __init__(
        self,
        *,
        source: typing.Union["CfnConfigRule.SourceProperty", _IResolvable_9ceae33e],
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Any = None,
        maximum_execution_frequency: typing.Optional[str] = None,
        scope: typing.Optional[typing.Union["CfnConfigRule.ScopeProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::ConfigRule``.

        :param source: ``AWS::Config::ConfigRule.Source``.
        :param config_rule_name: ``AWS::Config::ConfigRule.ConfigRuleName``.
        :param description: ``AWS::Config::ConfigRule.Description``.
        :param input_parameters: ``AWS::Config::ConfigRule.InputParameters``.
        :param maximum_execution_frequency: ``AWS::Config::ConfigRule.MaximumExecutionFrequency``.
        :param scope: ``AWS::Config::ConfigRule.Scope``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
        """
        self._values = {
            "source": source,
        }
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def source(
        self,
    ) -> typing.Union["CfnConfigRule.SourceProperty", _IResolvable_9ceae33e]:
        """``AWS::Config::ConfigRule.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-source
        """
        return self._values.get("source")

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.ConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-configrulename
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-description
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Any:
        """``AWS::Config::ConfigRule.InputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-inputparameters
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigRule.MaximumExecutionFrequency``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-maximumexecutionfrequency
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union["CfnConfigRule.ScopeProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigRule.Scope``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-scope
        """
        return self._values.get("scope")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnConfigurationAggregator(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnConfigurationAggregator",
):
    """A CloudFormation ``AWS::Config::ConfigurationAggregator``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::ConfigurationAggregator
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        configuration_aggregator_name: str,
        account_aggregation_sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AccountAggregationSourceProperty", _IResolvable_9ceae33e]]]] = None,
        organization_aggregation_source: typing.Optional[typing.Union["OrganizationAggregationSourceProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::Config::ConfigurationAggregator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_aggregator_name: ``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.
        :param account_aggregation_sources: ``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.
        :param organization_aggregation_source: ``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.
        :param tags: ``AWS::Config::ConfigurationAggregator.Tags``.
        """
        props = CfnConfigurationAggregatorProps(
            configuration_aggregator_name=configuration_aggregator_name,
            account_aggregation_sources=account_aggregation_sources,
            organization_aggregation_source=organization_aggregation_source,
            tags=tags,
        )

        jsii.create(CfnConfigurationAggregator, self, [scope, id, props])

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
        """``AWS::Config::ConfigurationAggregator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="configurationAggregatorName")
    def configuration_aggregator_name(self) -> str:
        """``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-configurationaggregatorname
        """
        return jsii.get(self, "configurationAggregatorName")

    @configuration_aggregator_name.setter
    def configuration_aggregator_name(self, value: str) -> None:
        jsii.set(self, "configurationAggregatorName", value)

    @builtins.property
    @jsii.member(jsii_name="accountAggregationSources")
    def account_aggregation_sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AccountAggregationSourceProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-accountaggregationsources
        """
        return jsii.get(self, "accountAggregationSources")

    @account_aggregation_sources.setter
    def account_aggregation_sources(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AccountAggregationSourceProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "accountAggregationSources", value)

    @builtins.property
    @jsii.member(jsii_name="organizationAggregationSource")
    def organization_aggregation_source(
        self,
    ) -> typing.Optional[typing.Union["OrganizationAggregationSourceProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-organizationaggregationsource
        """
        return jsii.get(self, "organizationAggregationSource")

    @organization_aggregation_source.setter
    def organization_aggregation_source(
        self,
        value: typing.Optional[typing.Union["OrganizationAggregationSourceProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "organizationAggregationSource", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigurationAggregator.AccountAggregationSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_ids": "accountIds",
            "all_aws_regions": "allAwsRegions",
            "aws_regions": "awsRegions",
        },
    )
    class AccountAggregationSourceProperty:
        def __init__(
            self,
            *,
            account_ids: typing.List[str],
            all_aws_regions: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            aws_regions: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param account_ids: ``CfnConfigurationAggregator.AccountAggregationSourceProperty.AccountIds``.
            :param all_aws_regions: ``CfnConfigurationAggregator.AccountAggregationSourceProperty.AllAwsRegions``.
            :param aws_regions: ``CfnConfigurationAggregator.AccountAggregationSourceProperty.AwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html
            """
            self._values = {
                "account_ids": account_ids,
            }
            if all_aws_regions is not None:
                self._values["all_aws_regions"] = all_aws_regions
            if aws_regions is not None:
                self._values["aws_regions"] = aws_regions

        @builtins.property
        def account_ids(self) -> typing.List[str]:
            """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AccountIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-accountids
            """
            return self._values.get("account_ids")

        @builtins.property
        def all_aws_regions(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AllAwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-allawsregions
            """
            return self._values.get("all_aws_regions")

        @builtins.property
        def aws_regions(self) -> typing.Optional[typing.List[str]]:
            """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-awsregions
            """
            return self._values.get("aws_regions")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountAggregationSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigurationAggregator.OrganizationAggregationSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "all_aws_regions": "allAwsRegions",
            "aws_regions": "awsRegions",
        },
    )
    class OrganizationAggregationSourceProperty:
        def __init__(
            self,
            *,
            role_arn: str,
            all_aws_regions: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            aws_regions: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param role_arn: ``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.RoleArn``.
            :param all_aws_regions: ``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AllAwsRegions``.
            :param aws_regions: ``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html
            """
            self._values = {
                "role_arn": role_arn,
            }
            if all_aws_regions is not None:
                self._values["all_aws_regions"] = all_aws_regions
            if aws_regions is not None:
                self._values["aws_regions"] = aws_regions

        @builtins.property
        def role_arn(self) -> str:
            """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def all_aws_regions(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AllAwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-allawsregions
            """
            return self._values.get("all_aws_regions")

        @builtins.property
        def aws_regions(self) -> typing.Optional[typing.List[str]]:
            """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AwsRegions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-awsregions
            """
            return self._values.get("aws_regions")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationAggregationSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnConfigurationAggregatorProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_aggregator_name": "configurationAggregatorName",
        "account_aggregation_sources": "accountAggregationSources",
        "organization_aggregation_source": "organizationAggregationSource",
        "tags": "tags",
    },
)
class CfnConfigurationAggregatorProps:
    def __init__(
        self,
        *,
        configuration_aggregator_name: str,
        account_aggregation_sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigurationAggregator.AccountAggregationSourceProperty", _IResolvable_9ceae33e]]]] = None,
        organization_aggregation_source: typing.Optional[typing.Union["CfnConfigurationAggregator.OrganizationAggregationSourceProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::ConfigurationAggregator``.

        :param configuration_aggregator_name: ``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.
        :param account_aggregation_sources: ``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.
        :param organization_aggregation_source: ``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.
        :param tags: ``AWS::Config::ConfigurationAggregator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
        """
        self._values = {
            "configuration_aggregator_name": configuration_aggregator_name,
        }
        if account_aggregation_sources is not None:
            self._values["account_aggregation_sources"] = account_aggregation_sources
        if organization_aggregation_source is not None:
            self._values["organization_aggregation_source"] = organization_aggregation_source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration_aggregator_name(self) -> str:
        """``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-configurationaggregatorname
        """
        return self._values.get("configuration_aggregator_name")

    @builtins.property
    def account_aggregation_sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigurationAggregator.AccountAggregationSourceProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-accountaggregationsources
        """
        return self._values.get("account_aggregation_sources")

    @builtins.property
    def organization_aggregation_source(
        self,
    ) -> typing.Optional[typing.Union["CfnConfigurationAggregator.OrganizationAggregationSourceProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-organizationaggregationsource
        """
        return self._values.get("organization_aggregation_source")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Config::ConfigurationAggregator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationAggregatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnConfigurationRecorder(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnConfigurationRecorder",
):
    """A CloudFormation ``AWS::Config::ConfigurationRecorder``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::ConfigurationRecorder
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        role_arn: str,
        name: typing.Optional[str] = None,
        recording_group: typing.Optional[typing.Union["RecordingGroupProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::Config::ConfigurationRecorder``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role_arn: ``AWS::Config::ConfigurationRecorder.RoleARN``.
        :param name: ``AWS::Config::ConfigurationRecorder.Name``.
        :param recording_group: ``AWS::Config::ConfigurationRecorder.RecordingGroup``.
        """
        props = CfnConfigurationRecorderProps(
            role_arn=role_arn, name=name, recording_group=recording_group
        )

        jsii.create(CfnConfigurationRecorder, self, [scope, id, props])

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
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::Config::ConfigurationRecorder.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigurationRecorder.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="recordingGroup")
    def recording_group(
        self,
    ) -> typing.Optional[typing.Union["RecordingGroupProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigurationRecorder.RecordingGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-recordinggroup
        """
        return jsii.get(self, "recordingGroup")

    @recording_group.setter
    def recording_group(
        self,
        value: typing.Optional[typing.Union["RecordingGroupProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "recordingGroup", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConfigurationRecorder.RecordingGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_supported": "allSupported",
            "include_global_resource_types": "includeGlobalResourceTypes",
            "resource_types": "resourceTypes",
        },
    )
    class RecordingGroupProperty:
        def __init__(
            self,
            *,
            all_supported: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            include_global_resource_types: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            resource_types: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param all_supported: ``CfnConfigurationRecorder.RecordingGroupProperty.AllSupported``.
            :param include_global_resource_types: ``CfnConfigurationRecorder.RecordingGroupProperty.IncludeGlobalResourceTypes``.
            :param resource_types: ``CfnConfigurationRecorder.RecordingGroupProperty.ResourceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html
            """
            self._values = {}
            if all_supported is not None:
                self._values["all_supported"] = all_supported
            if include_global_resource_types is not None:
                self._values["include_global_resource_types"] = include_global_resource_types
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def all_supported(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnConfigurationRecorder.RecordingGroupProperty.AllSupported``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-allsupported
            """
            return self._values.get("all_supported")

        @builtins.property
        def include_global_resource_types(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnConfigurationRecorder.RecordingGroupProperty.IncludeGlobalResourceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-includeglobalresourcetypes
            """
            return self._values.get("include_global_resource_types")

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[str]]:
            """``CfnConfigurationRecorder.RecordingGroupProperty.ResourceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-resourcetypes
            """
            return self._values.get("resource_types")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnConfigurationRecorderProps",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "name": "name",
        "recording_group": "recordingGroup",
    },
)
class CfnConfigurationRecorderProps:
    def __init__(
        self,
        *,
        role_arn: str,
        name: typing.Optional[str] = None,
        recording_group: typing.Optional[typing.Union["CfnConfigurationRecorder.RecordingGroupProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::ConfigurationRecorder``.

        :param role_arn: ``AWS::Config::ConfigurationRecorder.RoleARN``.
        :param name: ``AWS::Config::ConfigurationRecorder.Name``.
        :param recording_group: ``AWS::Config::ConfigurationRecorder.RecordingGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
        """
        self._values = {
            "role_arn": role_arn,
        }
        if name is not None:
            self._values["name"] = name
        if recording_group is not None:
            self._values["recording_group"] = recording_group

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::Config::ConfigurationRecorder.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-rolearn
        """
        return self._values.get("role_arn")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Config::ConfigurationRecorder.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-name
        """
        return self._values.get("name")

    @builtins.property
    def recording_group(
        self,
    ) -> typing.Optional[typing.Union["CfnConfigurationRecorder.RecordingGroupProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::ConfigurationRecorder.RecordingGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-recordinggroup
        """
        return self._values.get("recording_group")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationRecorderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnConformancePack(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnConformancePack",
):
    """A CloudFormation ``AWS::Config::ConformancePack``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::ConformancePack
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        conformance_pack_name: str,
        delivery_s3_bucket: str,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]] = None,
        delivery_s3_key_prefix: typing.Optional[str] = None,
        template_body: typing.Optional[str] = None,
        template_s3_uri: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::Config::ConformancePack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param conformance_pack_name: ``AWS::Config::ConformancePack.ConformancePackName``.
        :param delivery_s3_bucket: ``AWS::Config::ConformancePack.DeliveryS3Bucket``.
        :param conformance_pack_input_parameters: ``AWS::Config::ConformancePack.ConformancePackInputParameters``.
        :param delivery_s3_key_prefix: ``AWS::Config::ConformancePack.DeliveryS3KeyPrefix``.
        :param template_body: ``AWS::Config::ConformancePack.TemplateBody``.
        :param template_s3_uri: ``AWS::Config::ConformancePack.TemplateS3Uri``.
        """
        props = CfnConformancePackProps(
            conformance_pack_name=conformance_pack_name,
            delivery_s3_bucket=delivery_s3_bucket,
            conformance_pack_input_parameters=conformance_pack_input_parameters,
            delivery_s3_key_prefix=delivery_s3_key_prefix,
            template_body=template_body,
            template_s3_uri=template_s3_uri,
        )

        jsii.create(CfnConformancePack, self, [scope, id, props])

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
    @jsii.member(jsii_name="conformancePackName")
    def conformance_pack_name(self) -> str:
        """``AWS::Config::ConformancePack.ConformancePackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackname
        """
        return jsii.get(self, "conformancePackName")

    @conformance_pack_name.setter
    def conformance_pack_name(self, value: str) -> None:
        jsii.set(self, "conformancePackName", value)

    @builtins.property
    @jsii.member(jsii_name="deliveryS3Bucket")
    def delivery_s3_bucket(self) -> str:
        """``AWS::Config::ConformancePack.DeliveryS3Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3bucket
        """
        return jsii.get(self, "deliveryS3Bucket")

    @delivery_s3_bucket.setter
    def delivery_s3_bucket(self, value: str) -> None:
        jsii.set(self, "deliveryS3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="conformancePackInputParameters")
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::ConformancePack.ConformancePackInputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackinputparameters
        """
        return jsii.get(self, "conformancePackInputParameters")

    @conformance_pack_input_parameters.setter
    def conformance_pack_input_parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "conformancePackInputParameters", value)

    @builtins.property
    @jsii.member(jsii_name="deliveryS3KeyPrefix")
    def delivery_s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.DeliveryS3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3keyprefix
        """
        return jsii.get(self, "deliveryS3KeyPrefix")

    @delivery_s3_key_prefix.setter
    def delivery_s3_key_prefix(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deliveryS3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templatebody
        """
        return jsii.get(self, "templateBody")

    @template_body.setter
    def template_body(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateBody", value)

    @builtins.property
    @jsii.member(jsii_name="templateS3Uri")
    def template_s3_uri(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templates3uri
        """
        return jsii.get(self, "templateS3Uri")

    @template_s3_uri.setter
    def template_s3_uri(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateS3Uri", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnConformancePack.ConformancePackInputParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ConformancePackInputParameterProperty:
        def __init__(self, *, parameter_name: str, parameter_value: str) -> None:
            """
            :param parameter_name: ``CfnConformancePack.ConformancePackInputParameterProperty.ParameterName``.
            :param parameter_value: ``CfnConformancePack.ConformancePackInputParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html
            """
            self._values = {
                "parameter_name": parameter_name,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_name(self) -> str:
            """``CfnConformancePack.ConformancePackInputParameterProperty.ParameterName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html#cfn-config-conformancepack-conformancepackinputparameter-parametername
            """
            return self._values.get("parameter_name")

        @builtins.property
        def parameter_value(self) -> str:
            """``CfnConformancePack.ConformancePackInputParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html#cfn-config-conformancepack-conformancepackinputparameter-parametervalue
            """
            return self._values.get("parameter_value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConformancePackInputParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnConformancePackProps",
    jsii_struct_bases=[],
    name_mapping={
        "conformance_pack_name": "conformancePackName",
        "delivery_s3_bucket": "deliveryS3Bucket",
        "conformance_pack_input_parameters": "conformancePackInputParameters",
        "delivery_s3_key_prefix": "deliveryS3KeyPrefix",
        "template_body": "templateBody",
        "template_s3_uri": "templateS3Uri",
    },
)
class CfnConformancePackProps:
    def __init__(
        self,
        *,
        conformance_pack_name: str,
        delivery_s3_bucket: str,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConformancePack.ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]] = None,
        delivery_s3_key_prefix: typing.Optional[str] = None,
        template_body: typing.Optional[str] = None,
        template_s3_uri: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::ConformancePack``.

        :param conformance_pack_name: ``AWS::Config::ConformancePack.ConformancePackName``.
        :param delivery_s3_bucket: ``AWS::Config::ConformancePack.DeliveryS3Bucket``.
        :param conformance_pack_input_parameters: ``AWS::Config::ConformancePack.ConformancePackInputParameters``.
        :param delivery_s3_key_prefix: ``AWS::Config::ConformancePack.DeliveryS3KeyPrefix``.
        :param template_body: ``AWS::Config::ConformancePack.TemplateBody``.
        :param template_s3_uri: ``AWS::Config::ConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html
        """
        self._values = {
            "conformance_pack_name": conformance_pack_name,
            "delivery_s3_bucket": delivery_s3_bucket,
        }
        if conformance_pack_input_parameters is not None:
            self._values["conformance_pack_input_parameters"] = conformance_pack_input_parameters
        if delivery_s3_key_prefix is not None:
            self._values["delivery_s3_key_prefix"] = delivery_s3_key_prefix
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_s3_uri is not None:
            self._values["template_s3_uri"] = template_s3_uri

    @builtins.property
    def conformance_pack_name(self) -> str:
        """``AWS::Config::ConformancePack.ConformancePackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackname
        """
        return self._values.get("conformance_pack_name")

    @builtins.property
    def delivery_s3_bucket(self) -> str:
        """``AWS::Config::ConformancePack.DeliveryS3Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3bucket
        """
        return self._values.get("delivery_s3_bucket")

    @builtins.property
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConformancePack.ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::ConformancePack.ConformancePackInputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackinputparameters
        """
        return self._values.get("conformance_pack_input_parameters")

    @builtins.property
    def delivery_s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.DeliveryS3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3keyprefix
        """
        return self._values.get("delivery_s3_key_prefix")

    @builtins.property
    def template_body(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templatebody
        """
        return self._values.get("template_body")

    @builtins.property
    def template_s3_uri(self) -> typing.Optional[str]:
        """``AWS::Config::ConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templates3uri
        """
        return self._values.get("template_s3_uri")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConformancePackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDeliveryChannel(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnDeliveryChannel",
):
    """A CloudFormation ``AWS::Config::DeliveryChannel``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::DeliveryChannel
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        s3_bucket_name: str,
        config_snapshot_delivery_properties: typing.Optional[typing.Union["ConfigSnapshotDeliveryPropertiesProperty", _IResolvable_9ceae33e]] = None,
        name: typing.Optional[str] = None,
        s3_key_prefix: typing.Optional[str] = None,
        sns_topic_arn: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::Config::DeliveryChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param s3_bucket_name: ``AWS::Config::DeliveryChannel.S3BucketName``.
        :param config_snapshot_delivery_properties: ``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.
        :param name: ``AWS::Config::DeliveryChannel.Name``.
        :param s3_key_prefix: ``AWS::Config::DeliveryChannel.S3KeyPrefix``.
        :param sns_topic_arn: ``AWS::Config::DeliveryChannel.SnsTopicARN``.
        """
        props = CfnDeliveryChannelProps(
            s3_bucket_name=s3_bucket_name,
            config_snapshot_delivery_properties=config_snapshot_delivery_properties,
            name=name,
            s3_key_prefix=s3_key_prefix,
            sns_topic_arn=sns_topic_arn,
        )

        jsii.create(CfnDeliveryChannel, self, [scope, id, props])

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
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        """``AWS::Config::DeliveryChannel.S3BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3bucketname
        """
        return jsii.get(self, "s3BucketName")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: str) -> None:
        jsii.set(self, "s3BucketName", value)

    @builtins.property
    @jsii.member(jsii_name="configSnapshotDeliveryProperties")
    def config_snapshot_delivery_properties(
        self,
    ) -> typing.Optional[typing.Union["ConfigSnapshotDeliveryPropertiesProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties
        """
        return jsii.get(self, "configSnapshotDeliveryProperties")

    @config_snapshot_delivery_properties.setter
    def config_snapshot_delivery_properties(
        self,
        value: typing.Optional[typing.Union["ConfigSnapshotDeliveryPropertiesProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "configSnapshotDeliveryProperties", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="s3KeyPrefix")
    def s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.S3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3keyprefix
        """
        return jsii.get(self, "s3KeyPrefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "s3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.SnsTopicARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-snstopicarn
        """
        return jsii.get(self, "snsTopicArn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snsTopicArn", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_frequency": "deliveryFrequency"},
    )
    class ConfigSnapshotDeliveryPropertiesProperty:
        def __init__(self, *, delivery_frequency: typing.Optional[str] = None) -> None:
            """
            :param delivery_frequency: ``CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty.DeliveryFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html
            """
            self._values = {}
            if delivery_frequency is not None:
                self._values["delivery_frequency"] = delivery_frequency

        @builtins.property
        def delivery_frequency(self) -> typing.Optional[str]:
            """``CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty.DeliveryFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties-deliveryfrequency
            """
            return self._values.get("delivery_frequency")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigSnapshotDeliveryPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnDeliveryChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "s3_bucket_name": "s3BucketName",
        "config_snapshot_delivery_properties": "configSnapshotDeliveryProperties",
        "name": "name",
        "s3_key_prefix": "s3KeyPrefix",
        "sns_topic_arn": "snsTopicArn",
    },
)
class CfnDeliveryChannelProps:
    def __init__(
        self,
        *,
        s3_bucket_name: str,
        config_snapshot_delivery_properties: typing.Optional[typing.Union["CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty", _IResolvable_9ceae33e]] = None,
        name: typing.Optional[str] = None,
        s3_key_prefix: typing.Optional[str] = None,
        sns_topic_arn: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::DeliveryChannel``.

        :param s3_bucket_name: ``AWS::Config::DeliveryChannel.S3BucketName``.
        :param config_snapshot_delivery_properties: ``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.
        :param name: ``AWS::Config::DeliveryChannel.Name``.
        :param s3_key_prefix: ``AWS::Config::DeliveryChannel.S3KeyPrefix``.
        :param sns_topic_arn: ``AWS::Config::DeliveryChannel.SnsTopicARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
        """
        self._values = {
            "s3_bucket_name": s3_bucket_name,
        }
        if config_snapshot_delivery_properties is not None:
            self._values["config_snapshot_delivery_properties"] = config_snapshot_delivery_properties
        if name is not None:
            self._values["name"] = name
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn

    @builtins.property
    def s3_bucket_name(self) -> str:
        """``AWS::Config::DeliveryChannel.S3BucketName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3bucketname
        """
        return self._values.get("s3_bucket_name")

    @builtins.property
    def config_snapshot_delivery_properties(
        self,
    ) -> typing.Optional[typing.Union["CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties
        """
        return self._values.get("config_snapshot_delivery_properties")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-name
        """
        return self._values.get("name")

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.S3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3keyprefix
        """
        return self._values.get("s3_key_prefix")

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[str]:
        """``AWS::Config::DeliveryChannel.SnsTopicARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-snstopicarn
        """
        return self._values.get("sns_topic_arn")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnOrganizationConfigRule(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnOrganizationConfigRule",
):
    """A CloudFormation ``AWS::Config::OrganizationConfigRule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::OrganizationConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        organization_config_rule_name: str,
        excluded_accounts: typing.Optional[typing.List[str]] = None,
        organization_custom_rule_metadata: typing.Optional[typing.Union["OrganizationCustomRuleMetadataProperty", _IResolvable_9ceae33e]] = None,
        organization_managed_rule_metadata: typing.Optional[typing.Union["OrganizationManagedRuleMetadataProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::Config::OrganizationConfigRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param organization_config_rule_name: ``AWS::Config::OrganizationConfigRule.OrganizationConfigRuleName``.
        :param excluded_accounts: ``AWS::Config::OrganizationConfigRule.ExcludedAccounts``.
        :param organization_custom_rule_metadata: ``AWS::Config::OrganizationConfigRule.OrganizationCustomRuleMetadata``.
        :param organization_managed_rule_metadata: ``AWS::Config::OrganizationConfigRule.OrganizationManagedRuleMetadata``.
        """
        props = CfnOrganizationConfigRuleProps(
            organization_config_rule_name=organization_config_rule_name,
            excluded_accounts=excluded_accounts,
            organization_custom_rule_metadata=organization_custom_rule_metadata,
            organization_managed_rule_metadata=organization_managed_rule_metadata,
        )

        jsii.create(CfnOrganizationConfigRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="organizationConfigRuleName")
    def organization_config_rule_name(self) -> str:
        """``AWS::Config::OrganizationConfigRule.OrganizationConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationconfigrulename
        """
        return jsii.get(self, "organizationConfigRuleName")

    @organization_config_rule_name.setter
    def organization_config_rule_name(self, value: str) -> None:
        jsii.set(self, "organizationConfigRuleName", value)

    @builtins.property
    @jsii.member(jsii_name="excludedAccounts")
    def excluded_accounts(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Config::OrganizationConfigRule.ExcludedAccounts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-excludedaccounts
        """
        return jsii.get(self, "excludedAccounts")

    @excluded_accounts.setter
    def excluded_accounts(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "excludedAccounts", value)

    @builtins.property
    @jsii.member(jsii_name="organizationCustomRuleMetadata")
    def organization_custom_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union["OrganizationCustomRuleMetadataProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::OrganizationConfigRule.OrganizationCustomRuleMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata
        """
        return jsii.get(self, "organizationCustomRuleMetadata")

    @organization_custom_rule_metadata.setter
    def organization_custom_rule_metadata(
        self,
        value: typing.Optional[typing.Union["OrganizationCustomRuleMetadataProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "organizationCustomRuleMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="organizationManagedRuleMetadata")
    def organization_managed_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union["OrganizationManagedRuleMetadataProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::OrganizationConfigRule.OrganizationManagedRuleMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata
        """
        return jsii.get(self, "organizationManagedRuleMetadata")

    @organization_managed_rule_metadata.setter
    def organization_managed_rule_metadata(
        self,
        value: typing.Optional[typing.Union["OrganizationManagedRuleMetadataProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "organizationManagedRuleMetadata", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_arn": "lambdaFunctionArn",
            "organization_config_rule_trigger_types": "organizationConfigRuleTriggerTypes",
            "description": "description",
            "input_parameters": "inputParameters",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "resource_id_scope": "resourceIdScope",
            "resource_types_scope": "resourceTypesScope",
            "tag_key_scope": "tagKeyScope",
            "tag_value_scope": "tagValueScope",
        },
    )
    class OrganizationCustomRuleMetadataProperty:
        def __init__(
            self,
            *,
            lambda_function_arn: str,
            organization_config_rule_trigger_types: typing.List[str],
            description: typing.Optional[str] = None,
            input_parameters: typing.Optional[str] = None,
            maximum_execution_frequency: typing.Optional[str] = None,
            resource_id_scope: typing.Optional[str] = None,
            resource_types_scope: typing.Optional[typing.List[str]] = None,
            tag_key_scope: typing.Optional[str] = None,
            tag_value_scope: typing.Optional[str] = None,
        ) -> None:
            """
            :param lambda_function_arn: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.LambdaFunctionArn``.
            :param organization_config_rule_trigger_types: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.OrganizationConfigRuleTriggerTypes``.
            :param description: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.Description``.
            :param input_parameters: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.InputParameters``.
            :param maximum_execution_frequency: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.MaximumExecutionFrequency``.
            :param resource_id_scope: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.ResourceIdScope``.
            :param resource_types_scope: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.ResourceTypesScope``.
            :param tag_key_scope: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.TagKeyScope``.
            :param tag_value_scope: ``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.TagValueScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html
            """
            self._values = {
                "lambda_function_arn": lambda_function_arn,
                "organization_config_rule_trigger_types": organization_config_rule_trigger_types,
            }
            if description is not None:
                self._values["description"] = description
            if input_parameters is not None:
                self._values["input_parameters"] = input_parameters
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if resource_id_scope is not None:
                self._values["resource_id_scope"] = resource_id_scope
            if resource_types_scope is not None:
                self._values["resource_types_scope"] = resource_types_scope
            if tag_key_scope is not None:
                self._values["tag_key_scope"] = tag_key_scope
            if tag_value_scope is not None:
                self._values["tag_value_scope"] = tag_value_scope

        @builtins.property
        def lambda_function_arn(self) -> str:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.LambdaFunctionArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-lambdafunctionarn
            """
            return self._values.get("lambda_function_arn")

        @builtins.property
        def organization_config_rule_trigger_types(self) -> typing.List[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.OrganizationConfigRuleTriggerTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-organizationconfigruletriggertypes
            """
            return self._values.get("organization_config_rule_trigger_types")

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-description
            """
            return self._values.get("description")

        @builtins.property
        def input_parameters(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.InputParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-inputparameters
            """
            return self._values.get("input_parameters")

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.MaximumExecutionFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-maximumexecutionfrequency
            """
            return self._values.get("maximum_execution_frequency")

        @builtins.property
        def resource_id_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.ResourceIdScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-resourceidscope
            """
            return self._values.get("resource_id_scope")

        @builtins.property
        def resource_types_scope(self) -> typing.Optional[typing.List[str]]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.ResourceTypesScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-resourcetypesscope
            """
            return self._values.get("resource_types_scope")

        @builtins.property
        def tag_key_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.TagKeyScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-tagkeyscope
            """
            return self._values.get("tag_key_scope")

        @builtins.property
        def tag_value_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty.TagValueScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-tagvaluescope
            """
            return self._values.get("tag_value_scope")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationCustomRuleMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rule_identifier": "ruleIdentifier",
            "description": "description",
            "input_parameters": "inputParameters",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "resource_id_scope": "resourceIdScope",
            "resource_types_scope": "resourceTypesScope",
            "tag_key_scope": "tagKeyScope",
            "tag_value_scope": "tagValueScope",
        },
    )
    class OrganizationManagedRuleMetadataProperty:
        def __init__(
            self,
            *,
            rule_identifier: str,
            description: typing.Optional[str] = None,
            input_parameters: typing.Optional[str] = None,
            maximum_execution_frequency: typing.Optional[str] = None,
            resource_id_scope: typing.Optional[str] = None,
            resource_types_scope: typing.Optional[typing.List[str]] = None,
            tag_key_scope: typing.Optional[str] = None,
            tag_value_scope: typing.Optional[str] = None,
        ) -> None:
            """
            :param rule_identifier: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.RuleIdentifier``.
            :param description: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.Description``.
            :param input_parameters: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.InputParameters``.
            :param maximum_execution_frequency: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.MaximumExecutionFrequency``.
            :param resource_id_scope: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.ResourceIdScope``.
            :param resource_types_scope: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.ResourceTypesScope``.
            :param tag_key_scope: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.TagKeyScope``.
            :param tag_value_scope: ``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.TagValueScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html
            """
            self._values = {
                "rule_identifier": rule_identifier,
            }
            if description is not None:
                self._values["description"] = description
            if input_parameters is not None:
                self._values["input_parameters"] = input_parameters
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if resource_id_scope is not None:
                self._values["resource_id_scope"] = resource_id_scope
            if resource_types_scope is not None:
                self._values["resource_types_scope"] = resource_types_scope
            if tag_key_scope is not None:
                self._values["tag_key_scope"] = tag_key_scope
            if tag_value_scope is not None:
                self._values["tag_value_scope"] = tag_value_scope

        @builtins.property
        def rule_identifier(self) -> str:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.RuleIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-ruleidentifier
            """
            return self._values.get("rule_identifier")

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-description
            """
            return self._values.get("description")

        @builtins.property
        def input_parameters(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.InputParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-inputparameters
            """
            return self._values.get("input_parameters")

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.MaximumExecutionFrequency``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-maximumexecutionfrequency
            """
            return self._values.get("maximum_execution_frequency")

        @builtins.property
        def resource_id_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.ResourceIdScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-resourceidscope
            """
            return self._values.get("resource_id_scope")

        @builtins.property
        def resource_types_scope(self) -> typing.Optional[typing.List[str]]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.ResourceTypesScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-resourcetypesscope
            """
            return self._values.get("resource_types_scope")

        @builtins.property
        def tag_key_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.TagKeyScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-tagkeyscope
            """
            return self._values.get("tag_key_scope")

        @builtins.property
        def tag_value_scope(self) -> typing.Optional[str]:
            """``CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty.TagValueScope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-tagvaluescope
            """
            return self._values.get("tag_value_scope")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationManagedRuleMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnOrganizationConfigRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "organization_config_rule_name": "organizationConfigRuleName",
        "excluded_accounts": "excludedAccounts",
        "organization_custom_rule_metadata": "organizationCustomRuleMetadata",
        "organization_managed_rule_metadata": "organizationManagedRuleMetadata",
    },
)
class CfnOrganizationConfigRuleProps:
    def __init__(
        self,
        *,
        organization_config_rule_name: str,
        excluded_accounts: typing.Optional[typing.List[str]] = None,
        organization_custom_rule_metadata: typing.Optional[typing.Union["CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty", _IResolvable_9ceae33e]] = None,
        organization_managed_rule_metadata: typing.Optional[typing.Union["CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::OrganizationConfigRule``.

        :param organization_config_rule_name: ``AWS::Config::OrganizationConfigRule.OrganizationConfigRuleName``.
        :param excluded_accounts: ``AWS::Config::OrganizationConfigRule.ExcludedAccounts``.
        :param organization_custom_rule_metadata: ``AWS::Config::OrganizationConfigRule.OrganizationCustomRuleMetadata``.
        :param organization_managed_rule_metadata: ``AWS::Config::OrganizationConfigRule.OrganizationManagedRuleMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html
        """
        self._values = {
            "organization_config_rule_name": organization_config_rule_name,
        }
        if excluded_accounts is not None:
            self._values["excluded_accounts"] = excluded_accounts
        if organization_custom_rule_metadata is not None:
            self._values["organization_custom_rule_metadata"] = organization_custom_rule_metadata
        if organization_managed_rule_metadata is not None:
            self._values["organization_managed_rule_metadata"] = organization_managed_rule_metadata

    @builtins.property
    def organization_config_rule_name(self) -> str:
        """``AWS::Config::OrganizationConfigRule.OrganizationConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationconfigrulename
        """
        return self._values.get("organization_config_rule_name")

    @builtins.property
    def excluded_accounts(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Config::OrganizationConfigRule.ExcludedAccounts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-excludedaccounts
        """
        return self._values.get("excluded_accounts")

    @builtins.property
    def organization_custom_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union["CfnOrganizationConfigRule.OrganizationCustomRuleMetadataProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::OrganizationConfigRule.OrganizationCustomRuleMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata
        """
        return self._values.get("organization_custom_rule_metadata")

    @builtins.property
    def organization_managed_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union["CfnOrganizationConfigRule.OrganizationManagedRuleMetadataProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::OrganizationConfigRule.OrganizationManagedRuleMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata
        """
        return self._values.get("organization_managed_rule_metadata")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationConfigRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnOrganizationConformancePack(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnOrganizationConformancePack",
):
    """A CloudFormation ``AWS::Config::OrganizationConformancePack``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::OrganizationConformancePack
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        delivery_s3_bucket: str,
        organization_conformance_pack_name: str,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]] = None,
        delivery_s3_key_prefix: typing.Optional[str] = None,
        excluded_accounts: typing.Optional[typing.List[str]] = None,
        template_body: typing.Optional[str] = None,
        template_s3_uri: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::Config::OrganizationConformancePack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param delivery_s3_bucket: ``AWS::Config::OrganizationConformancePack.DeliveryS3Bucket``.
        :param organization_conformance_pack_name: ``AWS::Config::OrganizationConformancePack.OrganizationConformancePackName``.
        :param conformance_pack_input_parameters: ``AWS::Config::OrganizationConformancePack.ConformancePackInputParameters``.
        :param delivery_s3_key_prefix: ``AWS::Config::OrganizationConformancePack.DeliveryS3KeyPrefix``.
        :param excluded_accounts: ``AWS::Config::OrganizationConformancePack.ExcludedAccounts``.
        :param template_body: ``AWS::Config::OrganizationConformancePack.TemplateBody``.
        :param template_s3_uri: ``AWS::Config::OrganizationConformancePack.TemplateS3Uri``.
        """
        props = CfnOrganizationConformancePackProps(
            delivery_s3_bucket=delivery_s3_bucket,
            organization_conformance_pack_name=organization_conformance_pack_name,
            conformance_pack_input_parameters=conformance_pack_input_parameters,
            delivery_s3_key_prefix=delivery_s3_key_prefix,
            excluded_accounts=excluded_accounts,
            template_body=template_body,
            template_s3_uri=template_s3_uri,
        )

        jsii.create(CfnOrganizationConformancePack, self, [scope, id, props])

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
    @jsii.member(jsii_name="deliveryS3Bucket")
    def delivery_s3_bucket(self) -> str:
        """``AWS::Config::OrganizationConformancePack.DeliveryS3Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3bucket
        """
        return jsii.get(self, "deliveryS3Bucket")

    @delivery_s3_bucket.setter
    def delivery_s3_bucket(self, value: str) -> None:
        jsii.set(self, "deliveryS3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="organizationConformancePackName")
    def organization_conformance_pack_name(self) -> str:
        """``AWS::Config::OrganizationConformancePack.OrganizationConformancePackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-organizationconformancepackname
        """
        return jsii.get(self, "organizationConformancePackName")

    @organization_conformance_pack_name.setter
    def organization_conformance_pack_name(self, value: str) -> None:
        jsii.set(self, "organizationConformancePackName", value)

    @builtins.property
    @jsii.member(jsii_name="conformancePackInputParameters")
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::OrganizationConformancePack.ConformancePackInputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-conformancepackinputparameters
        """
        return jsii.get(self, "conformancePackInputParameters")

    @conformance_pack_input_parameters.setter
    def conformance_pack_input_parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "conformancePackInputParameters", value)

    @builtins.property
    @jsii.member(jsii_name="deliveryS3KeyPrefix")
    def delivery_s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.DeliveryS3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3keyprefix
        """
        return jsii.get(self, "deliveryS3KeyPrefix")

    @delivery_s3_key_prefix.setter
    def delivery_s3_key_prefix(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deliveryS3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="excludedAccounts")
    def excluded_accounts(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Config::OrganizationConformancePack.ExcludedAccounts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-excludedaccounts
        """
        return jsii.get(self, "excludedAccounts")

    @excluded_accounts.setter
    def excluded_accounts(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "excludedAccounts", value)

    @builtins.property
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templatebody
        """
        return jsii.get(self, "templateBody")

    @template_body.setter
    def template_body(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateBody", value)

    @builtins.property
    @jsii.member(jsii_name="templateS3Uri")
    def template_s3_uri(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templates3uri
        """
        return jsii.get(self, "templateS3Uri")

    @template_s3_uri.setter
    def template_s3_uri(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateS3Uri", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnOrganizationConformancePack.ConformancePackInputParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ConformancePackInputParameterProperty:
        def __init__(self, *, parameter_name: str, parameter_value: str) -> None:
            """
            :param parameter_name: ``CfnOrganizationConformancePack.ConformancePackInputParameterProperty.ParameterName``.
            :param parameter_value: ``CfnOrganizationConformancePack.ConformancePackInputParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html
            """
            self._values = {
                "parameter_name": parameter_name,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_name(self) -> str:
            """``CfnOrganizationConformancePack.ConformancePackInputParameterProperty.ParameterName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html#cfn-config-organizationconformancepack-conformancepackinputparameter-parametername
            """
            return self._values.get("parameter_name")

        @builtins.property
        def parameter_value(self) -> str:
            """``CfnOrganizationConformancePack.ConformancePackInputParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html#cfn-config-organizationconformancepack-conformancepackinputparameter-parametervalue
            """
            return self._values.get("parameter_value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConformancePackInputParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnOrganizationConformancePackProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_s3_bucket": "deliveryS3Bucket",
        "organization_conformance_pack_name": "organizationConformancePackName",
        "conformance_pack_input_parameters": "conformancePackInputParameters",
        "delivery_s3_key_prefix": "deliveryS3KeyPrefix",
        "excluded_accounts": "excludedAccounts",
        "template_body": "templateBody",
        "template_s3_uri": "templateS3Uri",
    },
)
class CfnOrganizationConformancePackProps:
    def __init__(
        self,
        *,
        delivery_s3_bucket: str,
        organization_conformance_pack_name: str,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOrganizationConformancePack.ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]] = None,
        delivery_s3_key_prefix: typing.Optional[str] = None,
        excluded_accounts: typing.Optional[typing.List[str]] = None,
        template_body: typing.Optional[str] = None,
        template_s3_uri: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::OrganizationConformancePack``.

        :param delivery_s3_bucket: ``AWS::Config::OrganizationConformancePack.DeliveryS3Bucket``.
        :param organization_conformance_pack_name: ``AWS::Config::OrganizationConformancePack.OrganizationConformancePackName``.
        :param conformance_pack_input_parameters: ``AWS::Config::OrganizationConformancePack.ConformancePackInputParameters``.
        :param delivery_s3_key_prefix: ``AWS::Config::OrganizationConformancePack.DeliveryS3KeyPrefix``.
        :param excluded_accounts: ``AWS::Config::OrganizationConformancePack.ExcludedAccounts``.
        :param template_body: ``AWS::Config::OrganizationConformancePack.TemplateBody``.
        :param template_s3_uri: ``AWS::Config::OrganizationConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html
        """
        self._values = {
            "delivery_s3_bucket": delivery_s3_bucket,
            "organization_conformance_pack_name": organization_conformance_pack_name,
        }
        if conformance_pack_input_parameters is not None:
            self._values["conformance_pack_input_parameters"] = conformance_pack_input_parameters
        if delivery_s3_key_prefix is not None:
            self._values["delivery_s3_key_prefix"] = delivery_s3_key_prefix
        if excluded_accounts is not None:
            self._values["excluded_accounts"] = excluded_accounts
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_s3_uri is not None:
            self._values["template_s3_uri"] = template_s3_uri

    @builtins.property
    def delivery_s3_bucket(self) -> str:
        """``AWS::Config::OrganizationConformancePack.DeliveryS3Bucket``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3bucket
        """
        return self._values.get("delivery_s3_bucket")

    @builtins.property
    def organization_conformance_pack_name(self) -> str:
        """``AWS::Config::OrganizationConformancePack.OrganizationConformancePackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-organizationconformancepackname
        """
        return self._values.get("organization_conformance_pack_name")

    @builtins.property
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOrganizationConformancePack.ConformancePackInputParameterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Config::OrganizationConformancePack.ConformancePackInputParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-conformancepackinputparameters
        """
        return self._values.get("conformance_pack_input_parameters")

    @builtins.property
    def delivery_s3_key_prefix(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.DeliveryS3KeyPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3keyprefix
        """
        return self._values.get("delivery_s3_key_prefix")

    @builtins.property
    def excluded_accounts(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Config::OrganizationConformancePack.ExcludedAccounts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-excludedaccounts
        """
        return self._values.get("excluded_accounts")

    @builtins.property
    def template_body(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.TemplateBody``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templatebody
        """
        return self._values.get("template_body")

    @builtins.property
    def template_s3_uri(self) -> typing.Optional[str]:
        """``AWS::Config::OrganizationConformancePack.TemplateS3Uri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templates3uri
        """
        return self._values.get("template_s3_uri")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationConformancePackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnRemediationConfiguration(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration",
):
    """A CloudFormation ``AWS::Config::RemediationConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::Config::RemediationConfiguration
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        config_rule_name: str,
        target_id: str,
        target_type: str,
        automatic: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        execution_controls: typing.Optional[typing.Union["ExecutionControlsProperty", _IResolvable_9ceae33e]] = None,
        maximum_automatic_attempts: typing.Optional[jsii.Number] = None,
        parameters: typing.Any = None,
        resource_type: typing.Optional[str] = None,
        retry_attempt_seconds: typing.Optional[jsii.Number] = None,
        target_version: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::Config::RemediationConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config_rule_name: ``AWS::Config::RemediationConfiguration.ConfigRuleName``.
        :param target_id: ``AWS::Config::RemediationConfiguration.TargetId``.
        :param target_type: ``AWS::Config::RemediationConfiguration.TargetType``.
        :param automatic: ``AWS::Config::RemediationConfiguration.Automatic``.
        :param execution_controls: ``AWS::Config::RemediationConfiguration.ExecutionControls``.
        :param maximum_automatic_attempts: ``AWS::Config::RemediationConfiguration.MaximumAutomaticAttempts``.
        :param parameters: ``AWS::Config::RemediationConfiguration.Parameters``.
        :param resource_type: ``AWS::Config::RemediationConfiguration.ResourceType``.
        :param retry_attempt_seconds: ``AWS::Config::RemediationConfiguration.RetryAttemptSeconds``.
        :param target_version: ``AWS::Config::RemediationConfiguration.TargetVersion``.
        """
        props = CfnRemediationConfigurationProps(
            config_rule_name=config_rule_name,
            target_id=target_id,
            target_type=target_type,
            automatic=automatic,
            execution_controls=execution_controls,
            maximum_automatic_attempts=maximum_automatic_attempts,
            parameters=parameters,
            resource_type=resource_type,
            retry_attempt_seconds=retry_attempt_seconds,
            target_version=target_version,
        )

        jsii.create(CfnRemediationConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        """``AWS::Config::RemediationConfiguration.ConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-configrulename
        """
        return jsii.get(self, "configRuleName")

    @config_rule_name.setter
    def config_rule_name(self, value: str) -> None:
        jsii.set(self, "configRuleName", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::Config::RemediationConfiguration.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> str:
        """``AWS::Config::RemediationConfiguration.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetid
        """
        return jsii.get(self, "targetId")

    @target_id.setter
    def target_id(self, value: str) -> None:
        jsii.set(self, "targetId", value)

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> str:
        """``AWS::Config::RemediationConfiguration.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter
    def target_type(self, value: str) -> None:
        jsii.set(self, "targetType", value)

    @builtins.property
    @jsii.member(jsii_name="automatic")
    def automatic(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Config::RemediationConfiguration.Automatic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-automatic
        """
        return jsii.get(self, "automatic")

    @automatic.setter
    def automatic(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "automatic", value)

    @builtins.property
    @jsii.member(jsii_name="executionControls")
    def execution_controls(
        self,
    ) -> typing.Optional[typing.Union["ExecutionControlsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::RemediationConfiguration.ExecutionControls``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-executioncontrols
        """
        return jsii.get(self, "executionControls")

    @execution_controls.setter
    def execution_controls(
        self,
        value: typing.Optional[typing.Union["ExecutionControlsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "executionControls", value)

    @builtins.property
    @jsii.member(jsii_name="maximumAutomaticAttempts")
    def maximum_automatic_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Config::RemediationConfiguration.MaximumAutomaticAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-maximumautomaticattempts
        """
        return jsii.get(self, "maximumAutomaticAttempts")

    @maximum_automatic_attempts.setter
    def maximum_automatic_attempts(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumAutomaticAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> typing.Optional[str]:
        """``AWS::Config::RemediationConfiguration.ResourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-resourcetype
        """
        return jsii.get(self, "resourceType")

    @resource_type.setter
    def resource_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="retryAttemptSeconds")
    def retry_attempt_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Config::RemediationConfiguration.RetryAttemptSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-retryattemptseconds
        """
        return jsii.get(self, "retryAttemptSeconds")

    @retry_attempt_seconds.setter
    def retry_attempt_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retryAttemptSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="targetVersion")
    def target_version(self) -> typing.Optional[str]:
        """``AWS::Config::RemediationConfiguration.TargetVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetversion
        """
        return jsii.get(self, "targetVersion")

    @target_version.setter
    def target_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "targetVersion", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration.ExecutionControlsProperty",
        jsii_struct_bases=[],
        name_mapping={"ssm_controls": "ssmControls"},
    )
    class ExecutionControlsProperty:
        def __init__(
            self,
            *,
            ssm_controls: typing.Optional[typing.Union["CfnRemediationConfiguration.SsmControlsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param ssm_controls: ``CfnRemediationConfiguration.ExecutionControlsProperty.SsmControls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-executioncontrols.html
            """
            self._values = {}
            if ssm_controls is not None:
                self._values["ssm_controls"] = ssm_controls

        @builtins.property
        def ssm_controls(
            self,
        ) -> typing.Optional[typing.Union["CfnRemediationConfiguration.SsmControlsProperty", _IResolvable_9ceae33e]]:
            """``CfnRemediationConfiguration.ExecutionControlsProperty.SsmControls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-executioncontrols.html#cfn-config-remediationconfiguration-executioncontrols-ssmcontrols
            """
            return self._values.get("ssm_controls")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration.RemediationParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_value": "resourceValue",
            "static_value": "staticValue",
        },
    )
    class RemediationParameterValueProperty:
        def __init__(
            self,
            *,
            resource_value: typing.Optional[typing.Union["CfnRemediationConfiguration.ResourceValueProperty", _IResolvable_9ceae33e]] = None,
            static_value: typing.Optional[typing.Union["CfnRemediationConfiguration.StaticValueProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param resource_value: ``CfnRemediationConfiguration.RemediationParameterValueProperty.ResourceValue``.
            :param static_value: ``CfnRemediationConfiguration.RemediationParameterValueProperty.StaticValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html
            """
            self._values = {}
            if resource_value is not None:
                self._values["resource_value"] = resource_value
            if static_value is not None:
                self._values["static_value"] = static_value

        @builtins.property
        def resource_value(
            self,
        ) -> typing.Optional[typing.Union["CfnRemediationConfiguration.ResourceValueProperty", _IResolvable_9ceae33e]]:
            """``CfnRemediationConfiguration.RemediationParameterValueProperty.ResourceValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html#cfn-config-remediationconfiguration-remediationparametervalue-resourcevalue
            """
            return self._values.get("resource_value")

        @builtins.property
        def static_value(
            self,
        ) -> typing.Optional[typing.Union["CfnRemediationConfiguration.StaticValueProperty", _IResolvable_9ceae33e]]:
            """``CfnRemediationConfiguration.RemediationParameterValueProperty.StaticValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html#cfn-config-remediationconfiguration-remediationparametervalue-staticvalue
            """
            return self._values.get("static_value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemediationParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration.ResourceValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class ResourceValueProperty:
        def __init__(self, *, value: typing.Optional[str] = None) -> None:
            """
            :param value: ``CfnRemediationConfiguration.ResourceValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-resourcevalue.html
            """
            self._values = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnRemediationConfiguration.ResourceValueProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-resourcevalue.html#cfn-config-remediationconfiguration-resourcevalue-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration.SsmControlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "concurrent_execution_rate_percentage": "concurrentExecutionRatePercentage",
            "error_percentage": "errorPercentage",
        },
    )
    class SsmControlsProperty:
        def __init__(
            self,
            *,
            concurrent_execution_rate_percentage: typing.Optional[jsii.Number] = None,
            error_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param concurrent_execution_rate_percentage: ``CfnRemediationConfiguration.SsmControlsProperty.ConcurrentExecutionRatePercentage``.
            :param error_percentage: ``CfnRemediationConfiguration.SsmControlsProperty.ErrorPercentage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html
            """
            self._values = {}
            if concurrent_execution_rate_percentage is not None:
                self._values["concurrent_execution_rate_percentage"] = concurrent_execution_rate_percentage
            if error_percentage is not None:
                self._values["error_percentage"] = error_percentage

        @builtins.property
        def concurrent_execution_rate_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnRemediationConfiguration.SsmControlsProperty.ConcurrentExecutionRatePercentage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html#cfn-config-remediationconfiguration-ssmcontrols-concurrentexecutionratepercentage
            """
            return self._values.get("concurrent_execution_rate_percentage")

        @builtins.property
        def error_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnRemediationConfiguration.SsmControlsProperty.ErrorPercentage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html#cfn-config-remediationconfiguration-ssmcontrols-errorpercentage
            """
            return self._values.get("error_percentage")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_config.CfnRemediationConfiguration.StaticValueProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class StaticValueProperty:
        def __init__(self, *, values: typing.Optional[typing.List[str]] = None) -> None:
            """
            :param values: ``CfnRemediationConfiguration.StaticValueProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-staticvalue.html
            """
            self._values = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[str]]:
            """``CfnRemediationConfiguration.StaticValueProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-staticvalue.html#cfn-config-remediationconfiguration-staticvalue-values
            """
            return self._values.get("values")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StaticValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CfnRemediationConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "config_rule_name": "configRuleName",
        "target_id": "targetId",
        "target_type": "targetType",
        "automatic": "automatic",
        "execution_controls": "executionControls",
        "maximum_automatic_attempts": "maximumAutomaticAttempts",
        "parameters": "parameters",
        "resource_type": "resourceType",
        "retry_attempt_seconds": "retryAttemptSeconds",
        "target_version": "targetVersion",
    },
)
class CfnRemediationConfigurationProps:
    def __init__(
        self,
        *,
        config_rule_name: str,
        target_id: str,
        target_type: str,
        automatic: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        execution_controls: typing.Optional[typing.Union["CfnRemediationConfiguration.ExecutionControlsProperty", _IResolvable_9ceae33e]] = None,
        maximum_automatic_attempts: typing.Optional[jsii.Number] = None,
        parameters: typing.Any = None,
        resource_type: typing.Optional[str] = None,
        retry_attempt_seconds: typing.Optional[jsii.Number] = None,
        target_version: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Config::RemediationConfiguration``.

        :param config_rule_name: ``AWS::Config::RemediationConfiguration.ConfigRuleName``.
        :param target_id: ``AWS::Config::RemediationConfiguration.TargetId``.
        :param target_type: ``AWS::Config::RemediationConfiguration.TargetType``.
        :param automatic: ``AWS::Config::RemediationConfiguration.Automatic``.
        :param execution_controls: ``AWS::Config::RemediationConfiguration.ExecutionControls``.
        :param maximum_automatic_attempts: ``AWS::Config::RemediationConfiguration.MaximumAutomaticAttempts``.
        :param parameters: ``AWS::Config::RemediationConfiguration.Parameters``.
        :param resource_type: ``AWS::Config::RemediationConfiguration.ResourceType``.
        :param retry_attempt_seconds: ``AWS::Config::RemediationConfiguration.RetryAttemptSeconds``.
        :param target_version: ``AWS::Config::RemediationConfiguration.TargetVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html
        """
        self._values = {
            "config_rule_name": config_rule_name,
            "target_id": target_id,
            "target_type": target_type,
        }
        if automatic is not None:
            self._values["automatic"] = automatic
        if execution_controls is not None:
            self._values["execution_controls"] = execution_controls
        if maximum_automatic_attempts is not None:
            self._values["maximum_automatic_attempts"] = maximum_automatic_attempts
        if parameters is not None:
            self._values["parameters"] = parameters
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if retry_attempt_seconds is not None:
            self._values["retry_attempt_seconds"] = retry_attempt_seconds
        if target_version is not None:
            self._values["target_version"] = target_version

    @builtins.property
    def config_rule_name(self) -> str:
        """``AWS::Config::RemediationConfiguration.ConfigRuleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-configrulename
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def target_id(self) -> str:
        """``AWS::Config::RemediationConfiguration.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetid
        """
        return self._values.get("target_id")

    @builtins.property
    def target_type(self) -> str:
        """``AWS::Config::RemediationConfiguration.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targettype
        """
        return self._values.get("target_type")

    @builtins.property
    def automatic(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Config::RemediationConfiguration.Automatic``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-automatic
        """
        return self._values.get("automatic")

    @builtins.property
    def execution_controls(
        self,
    ) -> typing.Optional[typing.Union["CfnRemediationConfiguration.ExecutionControlsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Config::RemediationConfiguration.ExecutionControls``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-executioncontrols
        """
        return self._values.get("execution_controls")

    @builtins.property
    def maximum_automatic_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Config::RemediationConfiguration.MaximumAutomaticAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-maximumautomaticattempts
        """
        return self._values.get("maximum_automatic_attempts")

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::Config::RemediationConfiguration.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-parameters
        """
        return self._values.get("parameters")

    @builtins.property
    def resource_type(self) -> typing.Optional[str]:
        """``AWS::Config::RemediationConfiguration.ResourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-resourcetype
        """
        return self._values.get("resource_type")

    @builtins.property
    def retry_attempt_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Config::RemediationConfiguration.RetryAttemptSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-retryattemptseconds
        """
        return self._values.get("retry_attempt_seconds")

    @builtins.property
    def target_version(self) -> typing.Optional[str]:
        """``AWS::Config::RemediationConfiguration.TargetVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetversion
        """
        return self._values.get("target_version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRemediationConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_config.IRule")
class IRule(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A config rule.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRuleProxy

    @builtins.property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        """The name of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="onComplianceChange")
    def on_compliance_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule compliance events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onReEvaluationStatus")
    def on_re_evaluation_status(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule re-evaluation status events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...


class _IRuleProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A config rule.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_config.IRule"

    @builtins.property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        """The name of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleName")

    @jsii.member(jsii_name="onComplianceChange")
    def on_compliance_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule compliance events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onComplianceChange", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onReEvaluationStatus")
    def on_re_evaluation_status(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule re-evaluation status events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onReEvaluationStatus", [id, options])


@jsii.implements(IRule)
class ManagedRule(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.ManagedRule",
):
    """A new managed rule.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        identifier: str,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param identifier: The identifier of the AWS managed rule.
        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        props = ManagedRuleProps(
            identifier=identifier,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
        )

        jsii.create(ManagedRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromConfigRuleName")
    @builtins.classmethod
    def from_config_rule_name(
        cls, scope: _Construct_f50a3f53, id: str, config_rule_name: str
    ) -> "IRule":
        """Imports an existing rule.

        :param scope: -
        :param id: -
        :param config_rule_name: the name of the rule.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromConfigRuleName", [scope, id, config_rule_name])

    @jsii.member(jsii_name="onComplianceChange")
    def on_compliance_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule compliance events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onComplianceChange", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onReEvaluationStatus")
    def on_re_evaluation_status(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule re-evaluation status events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onReEvaluationStatus", [id, options])

    @jsii.member(jsii_name="scopeToResource")
    def scope_to_resource(
        self, type: str, identifier: typing.Optional[str] = None
    ) -> None:
        """Restrict scope of changes to a specific resource.

        :param type: the resource type.
        :param identifier: the resource identifier.

        see
        :see: https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToResource", [type, identifier])

    @jsii.member(jsii_name="scopeToResources")
    def scope_to_resources(self, *types: str) -> None:
        """Restrict scope of changes to specific resource types.

        :param types: resource types.

        see
        :see: https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToResources", [*types])

    @jsii.member(jsii_name="scopeToTag")
    def scope_to_tag(self, key: str, value: typing.Optional[str] = None) -> None:
        """Restrict scope of changes to a specific tag.

        :param key: the tag key.
        :param value: the tag value.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToTag", [key, value])

    @builtins.property
    @jsii.member(jsii_name="configRuleArn")
    def config_rule_arn(self) -> str:
        """The arn of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleArn")

    @builtins.property
    @jsii.member(jsii_name="configRuleComplianceType")
    def config_rule_compliance_type(self) -> str:
        """The compliance status of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleComplianceType")

    @builtins.property
    @jsii.member(jsii_name="configRuleId")
    def config_rule_id(self) -> str:
        """The id of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleId")

    @builtins.property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        """The name of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleName")

    @builtins.property
    @jsii.member(jsii_name="isCustomWithChanges")
    def _is_custom_with_changes(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isCustomWithChanges")

    @_is_custom_with_changes.setter
    def _is_custom_with_changes(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "isCustomWithChanges", value)

    @builtins.property
    @jsii.member(jsii_name="isManaged")
    def _is_managed(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isManaged")

    @_is_managed.setter
    def _is_managed(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "isManaged", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> typing.Optional["CfnConfigRule.ScopeProperty"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @_scope.setter
    def _scope(self, value: typing.Optional["CfnConfigRule.ScopeProperty"]) -> None:
        jsii.set(self, "scope", value)


@jsii.enum(jsii_type="monocdk-experiment.aws_config.MaximumExecutionFrequency")
class MaximumExecutionFrequency(enum.Enum):
    """The maximum frequency at which the AWS Config rule runs evaluations.

    stability
    :stability: experimental
    """

    ONE_HOUR = "ONE_HOUR"
    """1 hour.

    stability
    :stability: experimental
    """
    THREE_HOURS = "THREE_HOURS"
    """3 hours.

    stability
    :stability: experimental
    """
    SIX_HOURS = "SIX_HOURS"
    """6 hours.

    stability
    :stability: experimental
    """
    TWELVE_HOURS = "TWELVE_HOURS"
    """12 hours.

    stability
    :stability: experimental
    """
    TWENTY_FOUR_HOURS = "TWENTY_FOUR_HOURS"
    """24 hours.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.RuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
    },
)
class RuleProps:
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """Construction properties for a new rule.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        self._values = {}
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessKeysRotated(
    ManagedRule,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.AccessKeysRotated",
):
    """Checks whether the active access keys are rotated within the number of days specified in ``maxAge``.

    see
    :see: https://docs.aws.amazon.com/config/latest/developerguide/access-keys-rotated.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        max_age: typing.Optional[_Duration_5170c158] = None,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param max_age: The maximum number of days within which the access keys must be rotated. Default: Duration.days(90)
        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        props = AccessKeysRotatedProps(
            max_age=max_age,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
        )

        jsii.create(AccessKeysRotated, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.AccessKeysRotatedProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "max_age": "maxAge",
    },
)
class AccessKeysRotatedProps(RuleProps):
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
        max_age: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Construction properties for a AccessKeysRotated.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours
        :param max_age: The maximum number of days within which the access keys must be rotated. Default: Duration.days(90)

        stability
        :stability: experimental
        """
        self._values = {}
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def max_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum number of days within which the access keys must be rotated.

        default
        :default: Duration.days(90)

        stability
        :stability: experimental
        """
        return self._values.get("max_age")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessKeysRotatedProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationStackDriftDetectionCheck(
    ManagedRule,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CloudFormationStackDriftDetectionCheck",
):
    """Checks whether your CloudFormation stacks' actual configuration differs, or has drifted, from its expected configuration.

    see
    :see: https://docs.aws.amazon.com/config/latest/developerguide/cloudformation-stack-drift-detection-check.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        own_stack_only: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param own_stack_only: Whether to check only the stack where this rule is deployed. Default: false
        :param role: The IAM role to use for this rule. It must have permissions to detect drift for AWS CloudFormation stacks. Ensure to attach ``config.amazonaws.com`` trusted permissions and ``ReadOnlyAccess`` policy permissions. For specific policy permissions, refer to https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html. Default: a role will be created
        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        props = CloudFormationStackDriftDetectionCheckProps(
            own_stack_only=own_stack_only,
            role=role,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
        )

        jsii.create(CloudFormationStackDriftDetectionCheck, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CloudFormationStackDriftDetectionCheckProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "own_stack_only": "ownStackOnly",
        "role": "role",
    },
)
class CloudFormationStackDriftDetectionCheckProps(RuleProps):
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
        own_stack_only: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """Construction properties for a CloudFormationStackDriftDetectionCheck.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours
        :param own_stack_only: Whether to check only the stack where this rule is deployed. Default: false
        :param role: The IAM role to use for this rule. It must have permissions to detect drift for AWS CloudFormation stacks. Ensure to attach ``config.amazonaws.com`` trusted permissions and ``ReadOnlyAccess`` policy permissions. For specific policy permissions, refer to https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html. Default: a role will be created

        stability
        :stability: experimental
        """
        self._values = {}
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if own_stack_only is not None:
            self._values["own_stack_only"] = own_stack_only
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def own_stack_only(self) -> typing.Optional[bool]:
        """Whether to check only the stack where this rule is deployed.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("own_stack_only")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to use for this rule.

        It must have permissions to detect drift
        for AWS CloudFormation stacks. Ensure to attach ``config.amazonaws.com`` trusted
        permissions and ``ReadOnlyAccess`` policy permissions. For specific policy permissions,
        refer to https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html.

        default
        :default: a role will be created

        stability
        :stability: experimental
        """
        return self._values.get("role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationStackDriftDetectionCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationStackNotificationCheck(
    ManagedRule,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CloudFormationStackNotificationCheck",
):
    """Checks whether your CloudFormation stacks are sending event notifications to a SNS topic.

    Optionally checks whether specified SNS topics are used.

    see
    :see: https://docs.aws.amazon.com/config/latest/developerguide/cloudformation-stack-notification-check.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        topics: typing.Optional[typing.List[_ITopic_ef0ebe0e]] = None,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param topics: A list of allowed topics. At most 5 topics. Default: - No topics.
        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        props = CloudFormationStackNotificationCheckProps(
            topics=topics,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
        )

        jsii.create(CloudFormationStackNotificationCheck, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CloudFormationStackNotificationCheckProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "topics": "topics",
    },
)
class CloudFormationStackNotificationCheckProps(RuleProps):
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
        topics: typing.Optional[typing.List[_ITopic_ef0ebe0e]] = None,
    ) -> None:
        """Construction properties for a CloudFormationStackNotificationCheck.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours
        :param topics: A list of allowed topics. At most 5 topics. Default: - No topics.

        stability
        :stability: experimental
        """
        self._values = {}
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if topics is not None:
            self._values["topics"] = topics

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[_ITopic_ef0ebe0e]]:
        """A list of allowed topics.

        At most 5 topics.

        default
        :default: - No topics.

        stability
        :stability: experimental
        """
        return self._values.get("topics")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationStackNotificationCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRule)
class CustomRule(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_config.CustomRule",
):
    """A new custom rule.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Config::ConfigRule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        lambda_function: _IFunction_1c1de0bc,
        configuration_changes: typing.Optional[bool] = None,
        periodic: typing.Optional[bool] = None,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_function: The Lambda function to run.
        :param configuration_changes: Whether to run the rule on configuration changes. Default: false
        :param periodic: Whether to run the rule on a fixed frequency. Default: false
        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours

        stability
        :stability: experimental
        """
        props = CustomRuleProps(
            lambda_function=lambda_function,
            configuration_changes=configuration_changes,
            periodic=periodic,
            config_rule_name=config_rule_name,
            description=description,
            input_parameters=input_parameters,
            maximum_execution_frequency=maximum_execution_frequency,
        )

        jsii.create(CustomRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromConfigRuleName")
    @builtins.classmethod
    def from_config_rule_name(
        cls, scope: _Construct_f50a3f53, id: str, config_rule_name: str
    ) -> "IRule":
        """Imports an existing rule.

        :param scope: -
        :param id: -
        :param config_rule_name: the name of the rule.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromConfigRuleName", [scope, id, config_rule_name])

    @jsii.member(jsii_name="onComplianceChange")
    def on_compliance_change(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule compliance events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onComplianceChange", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onReEvaluationStatus")
    def on_re_evaluation_status(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for rule re-evaluation status events.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onReEvaluationStatus", [id, options])

    @jsii.member(jsii_name="scopeToResource")
    def scope_to_resource(
        self, type: str, identifier: typing.Optional[str] = None
    ) -> None:
        """Restrict scope of changes to a specific resource.

        :param type: the resource type.
        :param identifier: the resource identifier.

        see
        :see: https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToResource", [type, identifier])

    @jsii.member(jsii_name="scopeToResources")
    def scope_to_resources(self, *types: str) -> None:
        """Restrict scope of changes to specific resource types.

        :param types: resource types.

        see
        :see: https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToResources", [*types])

    @jsii.member(jsii_name="scopeToTag")
    def scope_to_tag(self, key: str, value: typing.Optional[str] = None) -> None:
        """Restrict scope of changes to a specific tag.

        :param key: the tag key.
        :param value: the tag value.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "scopeToTag", [key, value])

    @builtins.property
    @jsii.member(jsii_name="configRuleArn")
    def config_rule_arn(self) -> str:
        """The arn of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleArn")

    @builtins.property
    @jsii.member(jsii_name="configRuleComplianceType")
    def config_rule_compliance_type(self) -> str:
        """The compliance status of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleComplianceType")

    @builtins.property
    @jsii.member(jsii_name="configRuleId")
    def config_rule_id(self) -> str:
        """The id of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleId")

    @builtins.property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        """The name of the rule.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "configRuleName")

    @builtins.property
    @jsii.member(jsii_name="isCustomWithChanges")
    def _is_custom_with_changes(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isCustomWithChanges")

    @_is_custom_with_changes.setter
    def _is_custom_with_changes(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "isCustomWithChanges", value)

    @builtins.property
    @jsii.member(jsii_name="isManaged")
    def _is_managed(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "isManaged")

    @_is_managed.setter
    def _is_managed(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "isManaged", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> typing.Optional["CfnConfigRule.ScopeProperty"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @_scope.setter
    def _scope(self, value: typing.Optional["CfnConfigRule.ScopeProperty"]) -> None:
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.CustomRuleProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "lambda_function": "lambdaFunction",
        "configuration_changes": "configurationChanges",
        "periodic": "periodic",
    },
)
class CustomRuleProps(RuleProps):
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
        lambda_function: _IFunction_1c1de0bc,
        configuration_changes: typing.Optional[bool] = None,
        periodic: typing.Optional[bool] = None,
    ) -> None:
        """Consruction properties for a CustomRule.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours
        :param lambda_function: The Lambda function to run.
        :param configuration_changes: Whether to run the rule on configuration changes. Default: false
        :param periodic: Whether to run the rule on a fixed frequency. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            "lambda_function": lambda_function,
        }
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if configuration_changes is not None:
            self._values["configuration_changes"] = configuration_changes
        if periodic is not None:
            self._values["periodic"] = periodic

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def lambda_function(self) -> _IFunction_1c1de0bc:
        """The Lambda function to run.

        stability
        :stability: experimental
        """
        return self._values.get("lambda_function")

    @builtins.property
    def configuration_changes(self) -> typing.Optional[bool]:
        """Whether to run the rule on configuration changes.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("configuration_changes")

    @builtins.property
    def periodic(self) -> typing.Optional[bool]:
        """Whether to run the rule on a fixed frequency.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("periodic")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_config.ManagedRuleProps",
    jsii_struct_bases=[RuleProps],
    name_mapping={
        "config_rule_name": "configRuleName",
        "description": "description",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "identifier": "identifier",
    },
)
class ManagedRuleProps(RuleProps):
    def __init__(
        self,
        *,
        config_rule_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        input_parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        maximum_execution_frequency: typing.Optional["MaximumExecutionFrequency"] = None,
        identifier: str,
    ) -> None:
        """Construction properties for a ManagedRule.

        :param config_rule_name: A name for the AWS Config rule. Default: a CloudFormation generated name
        :param description: A description about this AWS Config rule. Default: no description
        :param input_parameters: Input parameter values that are passed to the AWS Config rule. Default: no input parameters
        :param maximum_execution_frequency: The maximum frequency at which the AWS Config rule runs evaluations. Default: 24 hours
        :param identifier: The identifier of the AWS managed rule.

        stability
        :stability: experimental
        """
        self._values = {
            "identifier": identifier,
        }
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency

    @builtins.property
    def config_rule_name(self) -> typing.Optional[str]:
        """A name for the AWS Config rule.

        default
        :default: a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("config_rule_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description about this AWS Config rule.

        default
        :default: no description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def input_parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Input parameter values that are passed to the AWS Config rule.

        default
        :default: no input parameters

        stability
        :stability: experimental
        """
        return self._values.get("input_parameters")

    @builtins.property
    def maximum_execution_frequency(
        self,
    ) -> typing.Optional["MaximumExecutionFrequency"]:
        """The maximum frequency at which the AWS Config rule runs evaluations.

        default
        :default: 24 hours

        stability
        :stability: experimental
        """
        return self._values.get("maximum_execution_frequency")

    @builtins.property
    def identifier(self) -> str:
        """The identifier of the AWS managed rule.

        see
        :see: https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html
        stability
        :stability: experimental
        """
        return self._values.get("identifier")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessKeysRotated",
    "AccessKeysRotatedProps",
    "CfnAggregationAuthorization",
    "CfnAggregationAuthorizationProps",
    "CfnConfigRule",
    "CfnConfigRuleProps",
    "CfnConfigurationAggregator",
    "CfnConfigurationAggregatorProps",
    "CfnConfigurationRecorder",
    "CfnConfigurationRecorderProps",
    "CfnConformancePack",
    "CfnConformancePackProps",
    "CfnDeliveryChannel",
    "CfnDeliveryChannelProps",
    "CfnOrganizationConfigRule",
    "CfnOrganizationConfigRuleProps",
    "CfnOrganizationConformancePack",
    "CfnOrganizationConformancePackProps",
    "CfnRemediationConfiguration",
    "CfnRemediationConfigurationProps",
    "CloudFormationStackDriftDetectionCheck",
    "CloudFormationStackDriftDetectionCheckProps",
    "CloudFormationStackNotificationCheck",
    "CloudFormationStackNotificationCheckProps",
    "CustomRule",
    "CustomRuleProps",
    "IRule",
    "ManagedRule",
    "ManagedRuleProps",
    "MaximumExecutionFrequency",
    "RuleProps",
]

publication.publish()
