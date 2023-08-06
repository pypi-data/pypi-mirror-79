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
    RemovalPolicy as _RemovalPolicy_5986e9f3,
    Resource as _Resource_884d0774,
    SecretValue as _SecretValue_99478b8b,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_ec2 import (
    IConnectable as _IConnectable_a587039f,
    ISecurityGroup as _ISecurityGroup_d72ab8e8,
    IVpc as _IVpc_3795853f,
    SubnetSelection as _SubnetSelection_36a13cd6,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_d2a345d1,
    Grant as _Grant_96af6d2d,
    IGrantable as _IGrantable_0fcfc53a,
    PolicyDocument as _PolicyDocument_1d1bca11,
    PolicyStatement as _PolicyStatement_f75dc775,
)
from ..aws_kms import IKey as _IKey_3336c79d
from ..aws_lambda import IFunction as _IFunction_1c1de0bc


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.AttachedSecretOptions",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class AttachedSecretOptions:
    def __init__(self, *, target: "ISecretAttachmentTarget") -> None:
        """Options to add a secret attachment to a secret.

        :param target: The target to attach the secret to.

        deprecated
        :deprecated: use ``secret.attach()`` instead

        stability
        :stability: deprecated
        """
        self._values = {
            "target": target,
        }

    @builtins.property
    def target(self) -> "ISecretAttachmentTarget":
        """The target to attach the secret to.

        stability
        :stability: deprecated
        """
        return self._values.get("target")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachedSecretOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    """The type of service or database that's being associated with the secret.

    stability
    :stability: experimental
    """

    INSTANCE = "INSTANCE"
    """A database instance.

    deprecated
    :deprecated: use RDS_DB_INSTANCE instead

    stability
    :stability: deprecated
    """
    CLUSTER = "CLUSTER"
    """A database cluster.

    deprecated
    :deprecated: use RDS_DB_CLUSTER instead

    stability
    :stability: deprecated
    """
    RDS_DB_PROXY = "RDS_DB_PROXY"
    """AWS::RDS::DBProxy.

    stability
    :stability: experimental
    """
    REDSHIFT_CLUSTER = "REDSHIFT_CLUSTER"
    """AWS::Redshift::Cluster.

    stability
    :stability: experimental
    """
    DOCDB_DB_INSTANCE = "DOCDB_DB_INSTANCE"
    """AWS::DocDB::DBInstance.

    stability
    :stability: experimental
    """
    DOCDB_DB_CLUSTER = "DOCDB_DB_CLUSTER"
    """AWS::DocDB::DBCluster.

    stability
    :stability: experimental
    """


@jsii.implements(_IInspectable_051e6ed8)
class CfnResourcePolicy(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnResourcePolicy",
):
    """A CloudFormation ``AWS::SecretsManager::ResourcePolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::ResourcePolicy
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        resource_policy: typing.Any,
        secret_id: str,
    ) -> None:
        """Create a new ``AWS::SecretsManager::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.
        """
        props = CfnResourcePolicyProps(
            resource_policy=resource_policy, secret_id=secret_id
        )

        jsii.create(CfnResourcePolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="resourcePolicy")
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        return jsii.get(self, "resourcePolicy")

    @resource_policy.setter
    def resource_policy(self, value: typing.Any) -> None:
        jsii.set(self, "resourcePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str) -> None:
        jsii.set(self, "secretId", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"resource_policy": "resourcePolicy", "secret_id": "secretId"},
)
class CfnResourcePolicyProps:
    def __init__(self, *, resource_policy: typing.Any, secret_id: str) -> None:
        """Properties for defining a ``AWS::SecretsManager::ResourcePolicy``.

        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
        """
        self._values = {
            "resource_policy": resource_policy,
            "secret_id": secret_id,
        }

    @builtins.property
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        return self._values.get("resource_policy")

    @builtins.property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        return self._values.get("secret_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnRotationSchedule(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnRotationSchedule",
):
    """A CloudFormation ``AWS::SecretsManager::RotationSchedule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::RotationSchedule
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        secret_id: str,
        hosted_rotation_lambda: typing.Optional[typing.Union["HostedRotationLambdaProperty", _IResolvable_9ceae33e]] = None,
        rotation_lambda_arn: typing.Optional[str] = None,
        rotation_rules: typing.Optional[typing.Union["RotationRulesProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::SecretsManager::RotationSchedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param hosted_rotation_lambda: ``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.
        """
        props = CfnRotationScheduleProps(
            secret_id=secret_id,
            hosted_rotation_lambda=hosted_rotation_lambda,
            rotation_lambda_arn=rotation_lambda_arn,
            rotation_rules=rotation_rules,
        )

        jsii.create(CfnRotationSchedule, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str) -> None:
        jsii.set(self, "secretId", value)

    @builtins.property
    @jsii.member(jsii_name="hostedRotationLambda")
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union["HostedRotationLambdaProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        """
        return jsii.get(self, "hostedRotationLambda")

    @hosted_rotation_lambda.setter
    def hosted_rotation_lambda(
        self,
        value: typing.Optional[typing.Union["HostedRotationLambdaProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "hostedRotationLambda", value)

    @builtins.property
    @jsii.member(jsii_name="rotationLambdaArn")
    def rotation_lambda_arn(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        return jsii.get(self, "rotationLambdaArn")

    @rotation_lambda_arn.setter
    def rotation_lambda_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "rotationLambdaArn", value)

    @builtins.property
    @jsii.member(jsii_name="rotationRules")
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union["RotationRulesProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        return jsii.get(self, "rotationRules")

    @rotation_rules.setter
    def rotation_rules(
        self,
        value: typing.Optional[typing.Union["RotationRulesProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "rotationRules", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rotation_type": "rotationType",
            "kms_key_arn": "kmsKeyArn",
            "master_secret_arn": "masterSecretArn",
            "master_secret_kms_key_arn": "masterSecretKmsKeyArn",
            "rotation_lambda_name": "rotationLambdaName",
            "vpc_security_group_ids": "vpcSecurityGroupIds",
            "vpc_subnet_ids": "vpcSubnetIds",
        },
    )
    class HostedRotationLambdaProperty:
        def __init__(
            self,
            *,
            rotation_type: str,
            kms_key_arn: typing.Optional[str] = None,
            master_secret_arn: typing.Optional[str] = None,
            master_secret_kms_key_arn: typing.Optional[str] = None,
            rotation_lambda_name: typing.Optional[str] = None,
            vpc_security_group_ids: typing.Optional[str] = None,
            vpc_subnet_ids: typing.Optional[str] = None,
        ) -> None:
            """
            :param rotation_type: ``CfnRotationSchedule.HostedRotationLambdaProperty.RotationType``.
            :param kms_key_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.KmsKeyArn``.
            :param master_secret_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretArn``.
            :param master_secret_kms_key_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretKmsKeyArn``.
            :param rotation_lambda_name: ``CfnRotationSchedule.HostedRotationLambdaProperty.RotationLambdaName``.
            :param vpc_security_group_ids: ``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSecurityGroupIds``.
            :param vpc_subnet_ids: ``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html
            """
            self._values = {
                "rotation_type": rotation_type,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if master_secret_arn is not None:
                self._values["master_secret_arn"] = master_secret_arn
            if master_secret_kms_key_arn is not None:
                self._values["master_secret_kms_key_arn"] = master_secret_kms_key_arn
            if rotation_lambda_name is not None:
                self._values["rotation_lambda_name"] = rotation_lambda_name
            if vpc_security_group_ids is not None:
                self._values["vpc_security_group_ids"] = vpc_security_group_ids
            if vpc_subnet_ids is not None:
                self._values["vpc_subnet_ids"] = vpc_subnet_ids

        @builtins.property
        def rotation_type(self) -> str:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.RotationType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationtype
            """
            return self._values.get("rotation_type")

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-kmskeyarn
            """
            return self._values.get("kms_key_arn")

        @builtins.property
        def master_secret_arn(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretarn
            """
            return self._values.get("master_secret_arn")

        @builtins.property
        def master_secret_kms_key_arn(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretKmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretkmskeyarn
            """
            return self._values.get("master_secret_kms_key_arn")

        @builtins.property
        def rotation_lambda_name(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.RotationLambdaName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationlambdaname
            """
            return self._values.get("rotation_lambda_name")

        @builtins.property
        def vpc_security_group_ids(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsecuritygroupids
            """
            return self._values.get("vpc_security_group_ids")

        @builtins.property
        def vpc_subnet_ids(self) -> typing.Optional[str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsubnetids
            """
            return self._values.get("vpc_subnet_ids")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedRotationLambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_secretsmanager.CfnRotationSchedule.RotationRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"automatically_after_days": "automaticallyAfterDays"},
    )
    class RotationRulesProperty:
        def __init__(
            self, *, automatically_after_days: typing.Optional[jsii.Number] = None
        ) -> None:
            """
            :param automatically_after_days: ``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
            """
            self._values = {}
            if automatically_after_days is not None:
                self._values["automatically_after_days"] = automatically_after_days

        @builtins.property
        def automatically_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
            """
            return self._values.get("automatically_after_days")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RotationRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnRotationScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "hosted_rotation_lambda": "hostedRotationLambda",
        "rotation_lambda_arn": "rotationLambdaArn",
        "rotation_rules": "rotationRules",
    },
)
class CfnRotationScheduleProps:
    def __init__(
        self,
        *,
        secret_id: str,
        hosted_rotation_lambda: typing.Optional[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", _IResolvable_9ceae33e]] = None,
        rotation_lambda_arn: typing.Optional[str] = None,
        rotation_rules: typing.Optional[typing.Union["CfnRotationSchedule.RotationRulesProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::RotationSchedule``.

        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param hosted_rotation_lambda: ``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
        """
        self._values = {
            "secret_id": secret_id,
        }
        if hosted_rotation_lambda is not None:
            self._values["hosted_rotation_lambda"] = hosted_rotation_lambda
        if rotation_lambda_arn is not None:
            self._values["rotation_lambda_arn"] = rotation_lambda_arn
        if rotation_rules is not None:
            self._values["rotation_rules"] = rotation_rules

    @builtins.property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        return self._values.get("secret_id")

    @builtins.property
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union["CfnRotationSchedule.HostedRotationLambdaProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        """
        return self._values.get("hosted_rotation_lambda")

    @builtins.property
    def rotation_lambda_arn(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        return self._values.get("rotation_lambda_arn")

    @builtins.property
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union["CfnRotationSchedule.RotationRulesProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        return self._values.get("rotation_rules")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnSecret(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnSecret",
):
    """A CloudFormation ``AWS::SecretsManager::Secret``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::Secret
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        description: typing.Optional[str] = None,
        generate_secret_string: typing.Optional[typing.Union["GenerateSecretStringProperty", _IResolvable_9ceae33e]] = None,
        kms_key_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        secret_string: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::SecretsManager::Secret``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.
        """
        props = CfnSecretProps(
            description=description,
            generate_secret_string=generate_secret_string,
            kms_key_id=kms_key_id,
            name=name,
            secret_string=secret_string,
            tags=tags,
        )

        jsii.create(CfnSecret, self, [scope, id, props])

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
        """``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="generateSecretString")
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union["GenerateSecretStringProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        return jsii.get(self, "generateSecretString")

    @generate_secret_string.setter
    def generate_secret_string(
        self,
        value: typing.Optional[typing.Union["GenerateSecretStringProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "generateSecretString", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="secretString")
    def secret_string(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        return jsii.get(self, "secretString")

    @secret_string.setter
    def secret_string(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "secretString", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_secretsmanager.CfnSecret.GenerateSecretStringProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_characters": "excludeCharacters",
            "exclude_lowercase": "excludeLowercase",
            "exclude_numbers": "excludeNumbers",
            "exclude_punctuation": "excludePunctuation",
            "exclude_uppercase": "excludeUppercase",
            "generate_string_key": "generateStringKey",
            "include_space": "includeSpace",
            "password_length": "passwordLength",
            "require_each_included_type": "requireEachIncludedType",
            "secret_string_template": "secretStringTemplate",
        },
    )
    class GenerateSecretStringProperty:
        def __init__(
            self,
            *,
            exclude_characters: typing.Optional[str] = None,
            exclude_lowercase: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            exclude_numbers: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            exclude_punctuation: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            exclude_uppercase: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            generate_string_key: typing.Optional[str] = None,
            include_space: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            password_length: typing.Optional[jsii.Number] = None,
            require_each_included_type: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            secret_string_template: typing.Optional[str] = None,
        ) -> None:
            """
            :param exclude_characters: ``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.
            :param exclude_lowercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.
            :param exclude_numbers: ``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.
            :param exclude_punctuation: ``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.
            :param exclude_uppercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.
            :param generate_string_key: ``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.
            :param include_space: ``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.
            :param password_length: ``CfnSecret.GenerateSecretStringProperty.PasswordLength``.
            :param require_each_included_type: ``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.
            :param secret_string_template: ``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
            """
            self._values = {}
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if exclude_lowercase is not None:
                self._values["exclude_lowercase"] = exclude_lowercase
            if exclude_numbers is not None:
                self._values["exclude_numbers"] = exclude_numbers
            if exclude_punctuation is not None:
                self._values["exclude_punctuation"] = exclude_punctuation
            if exclude_uppercase is not None:
                self._values["exclude_uppercase"] = exclude_uppercase
            if generate_string_key is not None:
                self._values["generate_string_key"] = generate_string_key
            if include_space is not None:
                self._values["include_space"] = include_space
            if password_length is not None:
                self._values["password_length"] = password_length
            if require_each_included_type is not None:
                self._values["require_each_included_type"] = require_each_included_type
            if secret_string_template is not None:
                self._values["secret_string_template"] = secret_string_template

        @builtins.property
        def exclude_characters(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
            """
            return self._values.get("exclude_characters")

        @builtins.property
        def exclude_lowercase(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
            """
            return self._values.get("exclude_lowercase")

        @builtins.property
        def exclude_numbers(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
            """
            return self._values.get("exclude_numbers")

        @builtins.property
        def exclude_punctuation(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
            """
            return self._values.get("exclude_punctuation")

        @builtins.property
        def exclude_uppercase(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
            """
            return self._values.get("exclude_uppercase")

        @builtins.property
        def generate_string_key(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
            """
            return self._values.get("generate_string_key")

        @builtins.property
        def include_space(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
            """
            return self._values.get("include_space")

        @builtins.property
        def password_length(self) -> typing.Optional[jsii.Number]:
            """``CfnSecret.GenerateSecretStringProperty.PasswordLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
            """
            return self._values.get("password_length")

        @builtins.property
        def require_each_included_type(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
            """
            return self._values.get("require_each_included_type")

        @builtins.property
        def secret_string_template(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
            """
            return self._values.get("secret_string_template")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GenerateSecretStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "generate_secret_string": "generateSecretString",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "secret_string": "secretString",
        "tags": "tags",
    },
)
class CfnSecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[str] = None,
        generate_secret_string: typing.Optional[typing.Union["CfnSecret.GenerateSecretStringProperty", _IResolvable_9ceae33e]] = None,
        kms_key_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        secret_string: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::Secret``.

        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
        """
        self._values = {}
        if description is not None:
            self._values["description"] = description
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if secret_string is not None:
            self._values["secret_string"] = secret_string
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        return self._values.get("description")

    @builtins.property
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union["CfnSecret.GenerateSecretStringProperty", _IResolvable_9ceae33e]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        return self._values.get("generate_secret_string")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        return self._values.get("name")

    @builtins.property
    def secret_string(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        return self._values.get("secret_string")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnSecretTargetAttachment(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnSecretTargetAttachment",
):
    """A CloudFormation ``AWS::SecretsManager::SecretTargetAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::SecretTargetAttachment
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        secret_id: str,
        target_id: str,
        target_type: str,
    ) -> None:
        """Create a new ``AWS::SecretsManager::SecretTargetAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.
        """
        props = CfnSecretTargetAttachmentProps(
            secret_id=secret_id, target_id=target_id, target_type=target_type
        )

        jsii.create(CfnSecretTargetAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str) -> None:
        jsii.set(self, "secretId", value)

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        return jsii.get(self, "targetId")

    @target_id.setter
    def target_id(self, value: str) -> None:
        jsii.set(self, "targetId", value)

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter
    def target_type(self, value: str) -> None:
        jsii.set(self, "targetType", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.CfnSecretTargetAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnSecretTargetAttachmentProps:
    def __init__(self, *, secret_id: str, target_id: str, target_type: str) -> None:
        """Properties for defining a ``AWS::SecretsManager::SecretTargetAttachment``.

        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        """
        self._values = {
            "secret_id": secret_id,
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        return self._values.get("secret_id")

    @builtins.property
    def target_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        return self._values.get("target_id")

    @builtins.property
    def target_type(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        return self._values.get("target_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_secretsmanager.ISecret")
class ISecret(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A secret in AWS Secrets Manager.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretProxy

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_99478b8b:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: str,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self, statement: _PolicyStatement_f75dc775
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_0fcfc53a,
        version_stages: typing.Optional[typing.List[str]] = None,
    ) -> _Grant_96af6d2d:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: str) -> _SecretValue_99478b8b:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -

        stability
        :stability: experimental
        """
        ...


class _ISecretProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A secret in AWS Secrets Manager.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_secretsmanager.ISecret"

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretArn")

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_99478b8b:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretValue")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: str,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationScheduleOptions(
            rotation_lambda=rotation_lambda, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self, statement: _PolicyStatement_f75dc775
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_0fcfc53a,
        version_stages: typing.Optional[typing.List[str]] = None,
    ) -> _Grant_96af6d2d:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: str) -> _SecretValue_99478b8b:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "secretValueFromJson", [key])


@jsii.interface(
    jsii_type="monocdk-experiment.aws_secretsmanager.ISecretAttachmentTarget"
)
class ISecretAttachmentTarget(jsii.compat.Protocol):
    """A secret attachment target.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretAttachmentTargetProxy

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications.

        stability
        :stability: experimental
        """
        ...


class _ISecretAttachmentTargetProxy:
    """A secret attachment target.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_secretsmanager.ISecretAttachmentTarget"

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])


@jsii.interface(
    jsii_type="monocdk-experiment.aws_secretsmanager.ISecretTargetAttachment"
)
class ISecretTargetAttachment(ISecret, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretTargetAttachmentProxy

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ISecretTargetAttachmentProxy(jsii.proxy_for(ISecret)):
    """
    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_secretsmanager.ISecretTargetAttachment"

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")


class ResourcePolicy(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.ResourcePolicy",
):
    """Secret Resource Policy.

    stability
    :stability: experimental
    """

    def __init__(
        self, scope: _Construct_f50a3f53, id: str, *, secret: "ISecret"
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to attach a resource-based permissions policy.

        stability
        :stability: experimental
        """
        props = ResourcePolicyProps(secret=secret)

        jsii.create(ResourcePolicy, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_1d1bca11:
        """The IAM policy document for this policy.

        stability
        :stability: experimental
        """
        return jsii.get(self, "document")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.ResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class ResourcePolicyProps:
    def __init__(self, *, secret: "ISecret") -> None:
        """Construction properties for a ResourcePolicy.

        :param secret: The secret to attach a resource-based permissions policy.

        stability
        :stability: experimental
        """
        self._values = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> "ISecret":
        """The secret to attach a resource-based permissions policy.

        stability
        :stability: experimental
        """
        return self._values.get("secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RotationSchedule(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.RotationSchedule",
):
    """A rotation schedule.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        secret: "ISecret",
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to rotate.
        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        props = RotationScheduleProps(
            secret=secret,
            rotation_lambda=rotation_lambda,
            automatically_after=automatically_after,
        )

        jsii.create(RotationSchedule, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.RotationScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "rotation_lambda": "rotationLambda",
        "automatically_after": "automaticallyAfter",
    },
)
class RotationScheduleOptions:
    def __init__(
        self,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Options to add a rotation schedule to a secret.

        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        self._values = {
            "rotation_lambda": rotation_lambda,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after

    @builtins.property
    def rotation_lambda(self) -> _IFunction_1c1de0bc:
        """The Lambda function that can rotate the secret.

        stability
        :stability: experimental
        """
        return self._values.get("rotation_lambda")

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)

        stability
        :stability: experimental
        """
        return self._values.get("automatically_after")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.RotationScheduleProps",
    jsii_struct_bases=[RotationScheduleOptions],
    name_mapping={
        "rotation_lambda": "rotationLambda",
        "automatically_after": "automaticallyAfter",
        "secret": "secret",
    },
)
class RotationScheduleProps(RotationScheduleOptions):
    def __init__(
        self,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
        secret: "ISecret",
    ) -> None:
        """Construction properties for a RotationSchedule.

        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param secret: The secret to rotate.

        stability
        :stability: experimental
        """
        self._values = {
            "rotation_lambda": rotation_lambda,
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after

    @builtins.property
    def rotation_lambda(self) -> _IFunction_1c1de0bc:
        """The Lambda function that can rotate the secret.

        stability
        :stability: experimental
        """
        return self._values.get("rotation_lambda")

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)

        stability
        :stability: experimental
        """
        return self._values.get("automatically_after")

    @builtins.property
    def secret(self) -> "ISecret":
        """The secret to rotate.

        stability
        :stability: experimental
        """
        return self._values.get("secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecret)
class Secret(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.Secret",
):
    """Creates a new secret in AWS SecretsManager.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        generate_secret_string: typing.Optional["SecretStringGenerator"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        secret_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.

        stability
        :stability: experimental
        """
        props = SecretProps(
            description=description,
            encryption_key=encryption_key,
            generate_secret_string=generate_secret_string,
            removal_policy=removal_policy,
            secret_name=secret_name,
        )

        jsii.create(Secret, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretArn")
    @builtins.classmethod
    def from_secret_arn(
        cls, scope: _Construct_f50a3f53, id: str, secret_arn: str
    ) -> "ISecret":
        """
        :param scope: -
        :param id: -
        :param secret_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSecretArn", [scope, id, secret_arn])

    @jsii.member(jsii_name="fromSecretAttributes")
    @builtins.classmethod
    def from_secret_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        secret_arn: str,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> "ISecret":
        """Import an existing secret into the Stack.

        :param scope: the scope of the import.
        :param id: the ID of the imported Secret in the construct tree.
        :param secret_arn: The ARN of the secret in SecretsManager.
        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.

        stability
        :stability: experimental
        """
        attrs = SecretAttributes(secret_arn=secret_arn, encryption_key=encryption_key)

        return jsii.sinvoke(cls, "fromSecretAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: str,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationScheduleOptions(
            rotation_lambda=rotation_lambda, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(
        self, id: str, *, target: "ISecretAttachmentTarget"
    ) -> "SecretTargetAttachment":
        """Adds a target attachment to the secret.

        :param id: -
        :param target: The target to attach the secret to.

        return
        :return: an AttachedSecret

        deprecated
        :deprecated: use ``attach()`` instead

        stability
        :stability: deprecated
        """
        options = AttachedSecretOptions(target=target)

        return jsii.invoke(self, "addTargetAttachment", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self, statement: _PolicyStatement_f75dc775
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="attach")
    def attach(self, target: "ISecretAttachmentTarget") -> "ISecret":
        """Attach a target to this secret.

        :param target: The target to attach.

        return
        :return: An attached secret

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attach", [target])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_0fcfc53a,
        version_stages: typing.Optional[typing.List[str]] = None,
    ) -> _Grant_96af6d2d:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants writing and updating the secret value to some role.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: str) -> _SecretValue_99478b8b:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretArn")

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_99478b8b:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretValue")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretAttachmentTargetProps",
    jsii_struct_bases=[],
    name_mapping={"target_id": "targetId", "target_type": "targetType"},
)
class SecretAttachmentTargetProps:
    def __init__(self, *, target_id: str, target_type: "AttachmentTargetType") -> None:
        """Attachment target specifications.

        :param target_id: The id of the target to attach the secret to.
        :param target_type: The type of the target to attach the secret to.

        stability
        :stability: experimental
        """
        self._values = {
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def target_id(self) -> str:
        """The id of the target to attach the secret to.

        stability
        :stability: experimental
        """
        return self._values.get("target_id")

    @builtins.property
    def target_type(self) -> "AttachmentTargetType":
        """The type of the target to attach the secret to.

        stability
        :stability: experimental
        """
        return self._values.get("target_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttachmentTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretAttributes",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "encryption_key": "encryptionKey"},
)
class SecretAttributes:
    def __init__(
        self,
        *,
        secret_arn: str,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Attributes required to import an existing secret into the Stack.

        :param secret_arn: The ARN of the secret in SecretsManager.
        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.

        stability
        :stability: experimental
        """
        self._values = {
            "secret_arn": secret_arn,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def secret_arn(self) -> str:
        """The ARN of the secret in SecretsManager.

        stability
        :stability: experimental
        """
        return self._values.get("secret_arn")

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.

        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "encryption_key": "encryptionKey",
        "generate_secret_string": "generateSecretString",
        "removal_policy": "removalPolicy",
        "secret_name": "secretName",
    },
)
class SecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        generate_secret_string: typing.Optional["SecretStringGenerator"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        secret_name: typing.Optional[str] = None,
    ) -> None:
        """The properties required to create a new secret in AWS Secrets Manager.

        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.

        stability
        :stability: experimental
        """
        if isinstance(generate_secret_string, dict):
            generate_secret_string = SecretStringGenerator(**generate_secret_string)
        self._values = {}
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """An optional, human-friendly description of the secret.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The customer-managed encryption key to use for encrypting the secret value.

        default
        :default: - A default KMS key for the account and region is used.

        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    @builtins.property
    def generate_secret_string(self) -> typing.Optional["SecretStringGenerator"]:
        """Configuration for how to generate a secret value.

        default
        :default:

        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
          category), per the default values of ``SecretStringGenerator``.

        stability
        :stability: experimental
        """
        return self._values.get("generate_secret_string")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """Policy to apply when the secret is removed from this stack.

        default
        :default: - Not set.

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def secret_name(self) -> typing.Optional[str]:
        """A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        default
        :default: - A name is generated by CloudFormation.

        stability
        :stability: experimental
        """
        return self._values.get("secret_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretRotation(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretRotation",
):
    """Secret rotation for a service or database.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        application: "SecretRotationApplication",
        secret: "ISecret",
        target: _IConnectable_a587039f,
        vpc: _IVpc_3795853f,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
        exclude_characters: typing.Optional[str] = None,
        master_secret: typing.Optional["ISecret"] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param application: The serverless application for the rotation.
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an AWS::SecretsManager::SecretTargetAttachment or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: The target service or database.
        :param vpc: The VPC where the Lambda rotation function will run.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param exclude_characters: Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        stability
        :stability: experimental
        """
        props = SecretRotationProps(
            application=application,
            secret=secret,
            target=target,
            vpc=vpc,
            automatically_after=automatically_after,
            exclude_characters=exclude_characters,
            master_secret=master_secret,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(SecretRotation, self, [scope, id, props])


class SecretRotationApplication(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretRotationApplication",
):
    """A secret rotation serverless application.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        application_id: str,
        semantic_version: str,
        *,
        is_multi_user: typing.Optional[bool] = None,
    ) -> None:
        """
        :param application_id: -
        :param semantic_version: -
        :param is_multi_user: Whether the rotation application uses the mutli user scheme. Default: false

        stability
        :stability: experimental
        """
        options = SecretRotationApplicationOptions(is_multi_user=is_multi_user)

        jsii.create(SecretRotationApplication, self, [application_id, semantic_version, options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_ROTATION_MULTI_USER")
    def MARIADB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MARIADB_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB_ROTATION_SINGLE_USER")
    def MARIADB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MARIADB_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_ROTATION_MULTI_USER")
    def MONGODB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for MongoDB using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MONGODB_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB_ROTATION_SINGLE_USER")
    def MONGODB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for MongoDB using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MONGODB_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_ROTATION_MULTI_USER")
    def MYSQL_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MySQL using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MYSQL_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL_ROTATION_SINGLE_USER")
    def MYSQL_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MySQL using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MYSQL_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_ROTATION_MULTI_USER")
    def ORACLE_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS Oracle using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ORACLE_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_ROTATION_SINGLE_USER")
    def ORACLE_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS Oracle using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ORACLE_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRES_ROTATION_MULTI_USER")
    def POSTGRES_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "POSTGRES_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRES_ROTATION_SINGLE_USER")
    def POSTGRES_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "POSTGRES_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_ROTATION_MULTI_USER")
    def REDSHIFT_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "REDSHIFT_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="REDSHIFT_ROTATION_SINGLE_USER")
    def REDSHIFT_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "REDSHIFT_ROTATION_SINGLE_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_ROTATION_MULTI_USER")
    def SQLSERVER_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the multi user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "SQLSERVER_ROTATION_MULTI_USER")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQLSERVER_ROTATION_SINGLE_USER")
    def SQLSERVER_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the single user rotation scheme.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "SQLSERVER_ROTATION_SINGLE_USER")

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        """The application identifier of the rotation application.

        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationId")

    @builtins.property
    @jsii.member(jsii_name="semanticVersion")
    def semantic_version(self) -> str:
        """The semantic version of the rotation application.

        stability
        :stability: experimental
        """
        return jsii.get(self, "semanticVersion")

    @builtins.property
    @jsii.member(jsii_name="isMultiUser")
    def is_multi_user(self) -> typing.Optional[bool]:
        """Whether the rotation application uses the mutli user scheme.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isMultiUser")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretRotationApplicationOptions",
    jsii_struct_bases=[],
    name_mapping={"is_multi_user": "isMultiUser"},
)
class SecretRotationApplicationOptions:
    def __init__(self, *, is_multi_user: typing.Optional[bool] = None) -> None:
        """Options for a SecretRotationApplication.

        :param is_multi_user: Whether the rotation application uses the mutli user scheme. Default: false

        stability
        :stability: experimental
        """
        self._values = {}
        if is_multi_user is not None:
            self._values["is_multi_user"] = is_multi_user

    @builtins.property
    def is_multi_user(self) -> typing.Optional[bool]:
        """Whether the rotation application uses the mutli user scheme.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("is_multi_user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationApplicationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretRotationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "secret": "secret",
        "target": "target",
        "vpc": "vpc",
        "automatically_after": "automaticallyAfter",
        "exclude_characters": "excludeCharacters",
        "master_secret": "masterSecret",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class SecretRotationProps:
    def __init__(
        self,
        *,
        application: "SecretRotationApplication",
        secret: "ISecret",
        target: _IConnectable_a587039f,
        vpc: _IVpc_3795853f,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
        exclude_characters: typing.Optional[str] = None,
        master_secret: typing.Optional["ISecret"] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """Construction properties for a SecretRotation.

        :param application: The serverless application for the rotation.
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an AWS::SecretsManager::SecretTargetAttachment or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: The target service or database.
        :param vpc: The VPC where the Lambda rotation function will run.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param exclude_characters: Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "application": application,
            "secret": secret,
            "target": target,
            "vpc": vpc,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if master_secret is not None:
            self._values["master_secret"] = master_secret
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def application(self) -> "SecretRotationApplication":
        """The serverless application for the rotation.

        stability
        :stability: experimental
        """
        return self._values.get("application")

    @builtins.property
    def secret(self) -> "ISecret":
        """The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>
           }

        This is typically the case for a secret referenced from an
        AWS::SecretsManager::SecretTargetAttachment or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        stability
        :stability: experimental
        """
        return self._values.get("secret")

    @builtins.property
    def target(self) -> _IConnectable_a587039f:
        """The target service or database.

        stability
        :stability: experimental
        """
        return self._values.get("target")

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC where the Lambda rotation function will run.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)

        stability
        :stability: experimental
        """
        return self._values.get("automatically_after")

    @builtins.property
    def exclude_characters(self) -> typing.Optional[str]:
        """Characters which should not appear in the generated password.

        default
        :default: - no additional characters are explicitly excluded

        stability
        :stability: experimental
        """
        return self._values.get("exclude_characters")

    @builtins.property
    def master_secret(self) -> typing.Optional["ISecret"]:
        """The master secret for a multi user rotation scheme.

        default
        :default: - single user rotation scheme

        stability
        :stability: experimental
        """
        return self._values.get("master_secret")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """The security group for the Lambda rotation function.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets in the VPC where the Lambda rotation function will run.

        default
        :default: - the Vpc default strategy if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretStringGenerator",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_characters": "excludeCharacters",
        "exclude_lowercase": "excludeLowercase",
        "exclude_numbers": "excludeNumbers",
        "exclude_punctuation": "excludePunctuation",
        "exclude_uppercase": "excludeUppercase",
        "generate_string_key": "generateStringKey",
        "include_space": "includeSpace",
        "password_length": "passwordLength",
        "require_each_included_type": "requireEachIncludedType",
        "secret_string_template": "secretStringTemplate",
    },
)
class SecretStringGenerator:
    def __init__(
        self,
        *,
        exclude_characters: typing.Optional[str] = None,
        exclude_lowercase: typing.Optional[bool] = None,
        exclude_numbers: typing.Optional[bool] = None,
        exclude_punctuation: typing.Optional[bool] = None,
        exclude_uppercase: typing.Optional[bool] = None,
        generate_string_key: typing.Optional[str] = None,
        include_space: typing.Optional[bool] = None,
        password_length: typing.Optional[jsii.Number] = None,
        require_each_included_type: typing.Optional[bool] = None,
        secret_string_template: typing.Optional[str] = None,
    ) -> None:
        """Configuration to generate secrets such as passwords automatically.

        :param exclude_characters: A string that includes characters that shouldn't be included in the generated password. The string can be a minimum of ``0`` and a maximum of ``4096`` characters long. Default: no exclusions
        :param exclude_lowercase: Specifies that the generated password shouldn't include lowercase letters. Default: false
        :param exclude_numbers: Specifies that the generated password shouldn't include digits. Default: false
        :param exclude_punctuation: Specifies that the generated password shouldn't include punctuation characters. Default: false
        :param exclude_uppercase: Specifies that the generated password shouldn't include uppercase letters. Default: false
        :param generate_string_key: The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter. If you specify ``generateStringKey`` then ``secretStringTemplate`` must be also be specified.
        :param include_space: Specifies that the generated password can include the space character. Default: false
        :param password_length: The desired length of the generated password. Default: 32
        :param require_each_included_type: Specifies whether the generated password must include at least one of every allowed character type. Default: true
        :param secret_string_template: A properly structured JSON string that the generated password can be added to. The ``generateStringKey`` is combined with the generated random string and inserted into the JSON structure that's specified by this parameter. The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate`` then ``generateStringKey`` must be also be specified.

        stability
        :stability: experimental
        """
        self._values = {}
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if exclude_lowercase is not None:
            self._values["exclude_lowercase"] = exclude_lowercase
        if exclude_numbers is not None:
            self._values["exclude_numbers"] = exclude_numbers
        if exclude_punctuation is not None:
            self._values["exclude_punctuation"] = exclude_punctuation
        if exclude_uppercase is not None:
            self._values["exclude_uppercase"] = exclude_uppercase
        if generate_string_key is not None:
            self._values["generate_string_key"] = generate_string_key
        if include_space is not None:
            self._values["include_space"] = include_space
        if password_length is not None:
            self._values["password_length"] = password_length
        if require_each_included_type is not None:
            self._values["require_each_included_type"] = require_each_included_type
        if secret_string_template is not None:
            self._values["secret_string_template"] = secret_string_template

    @builtins.property
    def exclude_characters(self) -> typing.Optional[str]:
        """A string that includes characters that shouldn't be included in the generated password.

        The string can be a minimum
        of ``0`` and a maximum of ``4096`` characters long.

        default
        :default: no exclusions

        stability
        :stability: experimental
        """
        return self._values.get("exclude_characters")

    @builtins.property
    def exclude_lowercase(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include lowercase letters.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("exclude_lowercase")

    @builtins.property
    def exclude_numbers(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include digits.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("exclude_numbers")

    @builtins.property
    def exclude_punctuation(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include punctuation characters.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("exclude_punctuation")

    @builtins.property
    def exclude_uppercase(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include uppercase letters.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("exclude_uppercase")

    @builtins.property
    def generate_string_key(self) -> typing.Optional[str]:
        """The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter.

        If you specify ``generateStringKey`` then ``secretStringTemplate``
        must be also be specified.

        stability
        :stability: experimental
        """
        return self._values.get("generate_string_key")

    @builtins.property
    def include_space(self) -> typing.Optional[bool]:
        """Specifies that the generated password can include the space character.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("include_space")

    @builtins.property
    def password_length(self) -> typing.Optional[jsii.Number]:
        """The desired length of the generated password.

        default
        :default: 32

        stability
        :stability: experimental
        """
        return self._values.get("password_length")

    @builtins.property
    def require_each_included_type(self) -> typing.Optional[bool]:
        """Specifies whether the generated password must include at least one of every allowed character type.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("require_each_included_type")

    @builtins.property
    def secret_string_template(self) -> typing.Optional[str]:
        """A properly structured JSON string that the generated password can be added to.

        The ``generateStringKey`` is
        combined with the generated random string and inserted into the JSON structure that's specified by this parameter.
        The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate``
        then ``generateStringKey`` must be also be specified.

        stability
        :stability: experimental
        """
        return self._values.get("secret_string_template")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretStringGenerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretTargetAttachment, ISecret)
class SecretTargetAttachment(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretTargetAttachment",
):
    """An attached secret.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        secret: "ISecret",
        target: "ISecretAttachmentTarget",
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to attach to the target.
        :param target: The target to attach the secret to.

        stability
        :stability: experimental
        """
        props = SecretTargetAttachmentProps(secret=secret, target=target)

        jsii.create(SecretTargetAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretTargetAttachmentSecretArn")
    @builtins.classmethod
    def from_secret_target_attachment_secret_arn(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        secret_target_attachment_secret_arn: str,
    ) -> "ISecretTargetAttachment":
        """
        :param scope: -
        :param id: -
        :param secret_target_attachment_secret_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSecretTargetAttachmentSecretArn", [scope, id, secret_target_attachment_secret_arn])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: str,
        *,
        rotation_lambda: _IFunction_1c1de0bc,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param rotation_lambda: The Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationScheduleOptions(
            rotation_lambda=rotation_lambda, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self, statement: _PolicyStatement_f75dc775
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_0fcfc53a,
        version_stages: typing.Optional[typing.List[str]] = None,
    ) -> _Grant_96af6d2d:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants writing and updating the secret value to some role.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: str) -> _SecretValue_99478b8b:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretArn")

    @builtins.property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _SecretValue_99478b8b:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretValue")

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_secretsmanager.SecretTargetAttachmentProps",
    jsii_struct_bases=[AttachedSecretOptions],
    name_mapping={"target": "target", "secret": "secret"},
)
class SecretTargetAttachmentProps(AttachedSecretOptions):
    def __init__(self, *, target: "ISecretAttachmentTarget", secret: "ISecret") -> None:
        """Construction properties for an AttachedSecret.

        :param target: The target to attach the secret to.
        :param secret: The secret to attach to the target.

        stability
        :stability: experimental
        """
        self._values = {
            "target": target,
            "secret": secret,
        }

    @builtins.property
    def target(self) -> "ISecretAttachmentTarget":
        """The target to attach the secret to.

        stability
        :stability: deprecated
        """
        return self._values.get("target")

    @builtins.property
    def secret(self) -> "ISecret":
        """The secret to attach to the target.

        stability
        :stability: experimental
        """
        return self._values.get("secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AttachedSecretOptions",
    "AttachmentTargetType",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnRotationSchedule",
    "CfnRotationScheduleProps",
    "CfnSecret",
    "CfnSecretProps",
    "CfnSecretTargetAttachment",
    "CfnSecretTargetAttachmentProps",
    "ISecret",
    "ISecretAttachmentTarget",
    "ISecretTargetAttachment",
    "ResourcePolicy",
    "ResourcePolicyProps",
    "RotationSchedule",
    "RotationScheduleOptions",
    "RotationScheduleProps",
    "Secret",
    "SecretAttachmentTargetProps",
    "SecretAttributes",
    "SecretProps",
    "SecretRotation",
    "SecretRotationApplication",
    "SecretRotationApplicationOptions",
    "SecretRotationProps",
    "SecretStringGenerator",
    "SecretTargetAttachment",
    "SecretTargetAttachmentProps",
]

publication.publish()
