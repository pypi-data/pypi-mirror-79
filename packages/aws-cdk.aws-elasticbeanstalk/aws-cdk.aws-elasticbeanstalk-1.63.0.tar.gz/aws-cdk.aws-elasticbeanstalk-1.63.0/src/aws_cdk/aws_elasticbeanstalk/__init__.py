"""
## AWS Elastic Beanstalk Construct Library

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
class CfnApplication(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication",
):
    """A CloudFormation ``AWS::ElasticBeanstalk::Application``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticBeanstalk::Application
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        application_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        resource_lifecycle_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ApplicationResourceLifecycleConfigProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ElasticBeanstalk::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::ElasticBeanstalk::Application.ApplicationName``.
        :param description: ``AWS::ElasticBeanstalk::Application.Description``.
        :param resource_lifecycle_config: ``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.
        """
        props = CfnApplicationProps(
            application_name=application_name,
            description=description,
            resource_lifecycle_config=resource_lifecycle_config,
        )

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-name
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Application.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resourceLifecycleConfig")
    def resource_lifecycle_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ApplicationResourceLifecycleConfigProperty"]]:
        """``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
        """
        return jsii.get(self, "resourceLifecycleConfig")

    @resource_lifecycle_config.setter
    def resource_lifecycle_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ApplicationResourceLifecycleConfigProperty"]],
    ) -> None:
        jsii.set(self, "resourceLifecycleConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "service_role": "serviceRole",
            "version_lifecycle_config": "versionLifecycleConfig",
        },
    )
    class ApplicationResourceLifecycleConfigProperty:
        def __init__(
            self,
            *,
            service_role: typing.Optional[str] = None,
            version_lifecycle_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]] = None,
        ) -> None:
            """
            :param service_role: ``CfnApplication.ApplicationResourceLifecycleConfigProperty.ServiceRole``.
            :param version_lifecycle_config: ``CfnApplication.ApplicationResourceLifecycleConfigProperty.VersionLifecycleConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html
            """
            self._values = {}
            if service_role is not None:
                self._values["service_role"] = service_role
            if version_lifecycle_config is not None:
                self._values["version_lifecycle_config"] = version_lifecycle_config

        @builtins.property
        def service_role(self) -> typing.Optional[str]:
            """``CfnApplication.ApplicationResourceLifecycleConfigProperty.ServiceRole``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-servicerole
            """
            return self._values.get("service_role")

        @builtins.property
        def version_lifecycle_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]]:
            """``CfnApplication.ApplicationResourceLifecycleConfigProperty.VersionLifecycleConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-versionlifecycleconfig
            """
            return self._values.get("version_lifecycle_config")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationResourceLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_age_rule": "maxAgeRule", "max_count_rule": "maxCountRule"},
    )
    class ApplicationVersionLifecycleConfigProperty:
        def __init__(
            self,
            *,
            max_age_rule: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.MaxAgeRuleProperty"]] = None,
            max_count_rule: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.MaxCountRuleProperty"]] = None,
        ) -> None:
            """
            :param max_age_rule: ``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxAgeRule``.
            :param max_count_rule: ``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxCountRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html
            """
            self._values = {}
            if max_age_rule is not None:
                self._values["max_age_rule"] = max_age_rule
            if max_count_rule is not None:
                self._values["max_count_rule"] = max_count_rule

        @builtins.property
        def max_age_rule(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.MaxAgeRuleProperty"]]:
            """``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxAgeRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxagerule
            """
            return self._values.get("max_age_rule")

        @builtins.property
        def max_count_rule(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.MaxCountRuleProperty"]]:
            """``CfnApplication.ApplicationVersionLifecycleConfigProperty.MaxCountRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxcountrule
            """
            return self._values.get("max_count_rule")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationVersionLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxAgeRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_age_in_days": "maxAgeInDays",
        },
    )
    class MaxAgeRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
            max_age_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param delete_source_from_s3: ``CfnApplication.MaxAgeRuleProperty.DeleteSourceFromS3``.
            :param enabled: ``CfnApplication.MaxAgeRuleProperty.Enabled``.
            :param max_age_in_days: ``CfnApplication.MaxAgeRuleProperty.MaxAgeInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html
            """
            self._values = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_age_in_days is not None:
                self._values["max_age_in_days"] = max_age_in_days

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnApplication.MaxAgeRuleProperty.DeleteSourceFromS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-deletesourcefroms3
            """
            return self._values.get("delete_source_from_s3")

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnApplication.MaxAgeRuleProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-enabled
            """
            return self._values.get("enabled")

        @builtins.property
        def max_age_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnApplication.MaxAgeRuleProperty.MaxAgeInDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-maxageindays
            """
            return self._values.get("max_age_in_days")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxAgeRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxCountRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_count": "maxCount",
        },
    )
    class MaxCountRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
            max_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param delete_source_from_s3: ``CfnApplication.MaxCountRuleProperty.DeleteSourceFromS3``.
            :param enabled: ``CfnApplication.MaxCountRuleProperty.Enabled``.
            :param max_count: ``CfnApplication.MaxCountRuleProperty.MaxCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html
            """
            self._values = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_count is not None:
                self._values["max_count"] = max_count

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnApplication.MaxCountRuleProperty.DeleteSourceFromS3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-deletesourcefroms3
            """
            return self._values.get("delete_source_from_s3")

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnApplication.MaxCountRuleProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-enabled
            """
            return self._values.get("enabled")

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            """``CfnApplication.MaxCountRuleProperty.MaxCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-maxcount
            """
            return self._values.get("max_count")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxCountRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "resource_lifecycle_config": "resourceLifecycleConfig",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        resource_lifecycle_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ApplicationResourceLifecycleConfigProperty"]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticBeanstalk::Application``.

        :param application_name: ``AWS::ElasticBeanstalk::Application.ApplicationName``.
        :param description: ``AWS::ElasticBeanstalk::Application.Description``.
        :param resource_lifecycle_config: ``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html
        """
        self._values = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if description is not None:
            self._values["description"] = description
        if resource_lifecycle_config is not None:
            self._values["resource_lifecycle_config"] = resource_lifecycle_config

    @builtins.property
    def application_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-name
        """
        return self._values.get("application_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Application.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-description
        """
        return self._values.get("description")

    @builtins.property
    def resource_lifecycle_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ApplicationResourceLifecycleConfigProperty"]]:
        """``AWS::ElasticBeanstalk::Application.ResourceLifecycleConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
        """
        return self._values.get("resource_lifecycle_config")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApplicationVersion(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion",
):
    """A CloudFormation ``AWS::ElasticBeanstalk::ApplicationVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticBeanstalk::ApplicationVersion
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        application_name: str,
        source_bundle: typing.Union["SourceBundleProperty", aws_cdk.core.IResolvable],
        description: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::ElasticBeanstalk::ApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.
        :param source_bundle: ``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.
        :param description: ``AWS::ElasticBeanstalk::ApplicationVersion.Description``.
        """
        props = CfnApplicationVersionProps(
            application_name=application_name,
            source_bundle=source_bundle,
            description=description,
        )

        jsii.create(CfnApplicationVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceBundle")
    def source_bundle(
        self,
    ) -> typing.Union["SourceBundleProperty", aws_cdk.core.IResolvable]:
        """``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
        """
        return jsii.get(self, "sourceBundle")

    @source_bundle.setter
    def source_bundle(
        self, value: typing.Union["SourceBundleProperty", aws_cdk.core.IResolvable]
    ) -> None:
        jsii.set(self, "sourceBundle", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ApplicationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class SourceBundleProperty:
        def __init__(self, *, s3_bucket: str, s3_key: str) -> None:
            """
            :param s3_bucket: ``CfnApplicationVersion.SourceBundleProperty.S3Bucket``.
            :param s3_key: ``CfnApplicationVersion.SourceBundleProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html
            """
            self._values = {
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> str:
            """``CfnApplicationVersion.SourceBundleProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html#cfn-beanstalk-sourcebundle-s3bucket
            """
            return self._values.get("s3_bucket")

        @builtins.property
        def s3_key(self) -> str:
            """``CfnApplicationVersion.SourceBundleProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html#cfn-beanstalk-sourcebundle-s3key
            """
            return self._values.get("s3_key")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceBundleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "source_bundle": "sourceBundle",
        "description": "description",
    },
)
class CfnApplicationVersionProps:
    def __init__(
        self,
        *,
        application_name: str,
        source_bundle: typing.Union["CfnApplicationVersion.SourceBundleProperty", aws_cdk.core.IResolvable],
        description: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticBeanstalk::ApplicationVersion``.

        :param application_name: ``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.
        :param source_bundle: ``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.
        :param description: ``AWS::ElasticBeanstalk::ApplicationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html
        """
        self._values = {
            "application_name": application_name,
            "source_bundle": source_bundle,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::ApplicationVersion.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-applicationname
        """
        return self._values.get("application_name")

    @builtins.property
    def source_bundle(
        self,
    ) -> typing.Union["CfnApplicationVersion.SourceBundleProperty", aws_cdk.core.IResolvable]:
        """``AWS::ElasticBeanstalk::ApplicationVersion.SourceBundle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
        """
        return self._values.get("source_bundle")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ApplicationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-version.html#cfn-elasticbeanstalk-applicationversion-description
        """
        return self._values.get("description")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnConfigurationTemplate(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate",
):
    """A CloudFormation ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticBeanstalk::ConfigurationTemplate
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        application_name: str,
        description: typing.Optional[str] = None,
        environment_id: typing.Optional[str] = None,
        option_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationOptionSettingProperty"]]]] = None,
        platform_arn: typing.Optional[str] = None,
        solution_stack_name: typing.Optional[str] = None,
        source_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "SourceConfigurationProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.
        :param description: ``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.
        :param environment_id: ``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.
        :param option_settings: ``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.
        :param platform_arn: ``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.
        :param solution_stack_name: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.
        :param source_configuration: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.
        """
        props = CfnConfigurationTemplateProps(
            application_name=application_name,
            description=description,
            environment_id=environment_id,
            option_settings=option_settings,
            platform_arn=platform_arn,
            solution_stack_name=solution_stack_name,
            source_configuration=source_configuration,
        )

        jsii.create(CfnConfigurationTemplate, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
        """
        return jsii.get(self, "environmentId")

    @environment_id.setter
    def environment_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "environmentId", value)

    @builtins.property
    @jsii.member(jsii_name="optionSettings")
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationOptionSettingProperty"]]]]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
        """
        return jsii.get(self, "optionSettings")

    @option_settings.setter
    def option_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationOptionSettingProperty"]]]],
    ) -> None:
        jsii.set(self, "optionSettings", value)

    @builtins.property
    @jsii.member(jsii_name="platformArn")
    def platform_arn(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
        """
        return jsii.get(self, "platformArn")

    @platform_arn.setter
    def platform_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "platformArn", value)

    @builtins.property
    @jsii.member(jsii_name="solutionStackName")
    def solution_stack_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
        """
        return jsii.get(self, "solutionStackName")

    @solution_stack_name.setter
    def solution_stack_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "solutionStackName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "SourceConfigurationProperty"]]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
        """
        return jsii.get(self, "sourceConfiguration")

    @source_configuration.setter
    def source_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "SourceConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "sourceConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class ConfigurationOptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: str,
            option_name: str,
            resource_name: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param namespace: ``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Namespace``.
            :param option_name: ``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.OptionName``.
            :param resource_name: ``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.ResourceName``.
            :param value: ``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html
            """
            self._values = {
                "namespace": namespace,
                "option_name": option_name,
            }
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> str:
            """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-namespace
            """
            return self._values.get("namespace")

        @builtins.property
        def option_name(self) -> str:
            """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.OptionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-optionname
            """
            return self._values.get("option_name")

        @builtins.property
        def resource_name(self) -> typing.Optional[str]:
            """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.ResourceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-resourcename
            """
            return self._values.get("resource_name")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnConfigurationTemplate.ConfigurationOptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationOptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_name": "applicationName",
            "template_name": "templateName",
        },
    )
    class SourceConfigurationProperty:
        def __init__(self, *, application_name: str, template_name: str) -> None:
            """
            :param application_name: ``CfnConfigurationTemplate.SourceConfigurationProperty.ApplicationName``.
            :param template_name: ``CfnConfigurationTemplate.SourceConfigurationProperty.TemplateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html
            """
            self._values = {
                "application_name": application_name,
                "template_name": template_name,
            }

        @builtins.property
        def application_name(self) -> str:
            """``CfnConfigurationTemplate.SourceConfigurationProperty.ApplicationName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-applicationname
            """
            return self._values.get("application_name")

        @builtins.property
        def template_name(self) -> str:
            """``CfnConfigurationTemplate.SourceConfigurationProperty.TemplateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-templatename
            """
            return self._values.get("template_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "environment_id": "environmentId",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "source_configuration": "sourceConfiguration",
    },
)
class CfnConfigurationTemplateProps:
    def __init__(
        self,
        *,
        application_name: str,
        description: typing.Optional[str] = None,
        environment_id: typing.Optional[str] = None,
        option_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]] = None,
        platform_arn: typing.Optional[str] = None,
        solution_stack_name: typing.Optional[str] = None,
        source_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConfigurationTemplate.SourceConfigurationProperty"]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

        :param application_name: ``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.
        :param description: ``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.
        :param environment_id: ``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.
        :param option_settings: ``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.
        :param platform_arn: ``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.
        :param solution_stack_name: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.
        :param source_configuration: ``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
        """
        self._values = {
            "application_name": application_name,
        }
        if description is not None:
            self._values["description"] = description
        if environment_id is not None:
            self._values["environment_id"] = environment_id
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration

    @builtins.property
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
        """
        return self._values.get("application_name")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
        """
        return self._values.get("description")

    @builtins.property
    def environment_id(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.EnvironmentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
        """
        return self._values.get("environment_id")

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.OptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
        """
        return self._values.get("option_settings")

    @builtins.property
    def platform_arn(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.PlatformArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
        """
        return self._values.get("platform_arn")

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.SolutionStackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
        """
        return self._values.get("solution_stack_name")

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConfigurationTemplate.SourceConfigurationProperty"]]:
        """``AWS::ElasticBeanstalk::ConfigurationTemplate.SourceConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
        """
        return self._values.get("source_configuration")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEnvironment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment",
):
    """A CloudFormation ``AWS::ElasticBeanstalk::Environment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticBeanstalk::Environment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        application_name: str,
        cname_prefix: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        environment_name: typing.Optional[str] = None,
        option_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "OptionSettingProperty"]]]] = None,
        platform_arn: typing.Optional[str] = None,
        solution_stack_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        template_name: typing.Optional[str] = None,
        tier: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TierProperty"]] = None,
        version_label: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::ElasticBeanstalk::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::ElasticBeanstalk::Environment.ApplicationName``.
        :param cname_prefix: ``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.
        :param description: ``AWS::ElasticBeanstalk::Environment.Description``.
        :param environment_name: ``AWS::ElasticBeanstalk::Environment.EnvironmentName``.
        :param option_settings: ``AWS::ElasticBeanstalk::Environment.OptionSettings``.
        :param platform_arn: ``AWS::ElasticBeanstalk::Environment.PlatformArn``.
        :param solution_stack_name: ``AWS::ElasticBeanstalk::Environment.SolutionStackName``.
        :param tags: ``AWS::ElasticBeanstalk::Environment.Tags``.
        :param template_name: ``AWS::ElasticBeanstalk::Environment.TemplateName``.
        :param tier: ``AWS::ElasticBeanstalk::Environment.Tier``.
        :param version_label: ``AWS::ElasticBeanstalk::Environment.VersionLabel``.
        """
        props = CfnEnvironmentProps(
            application_name=application_name,
            cname_prefix=cname_prefix,
            description=description,
            environment_name=environment_name,
            option_settings=option_settings,
            platform_arn=platform_arn,
            solution_stack_name=solution_stack_name,
            tags=tags,
            template_name=template_name,
            tier=tier,
            version_label=version_label,
        )

        jsii.create(CfnEnvironment, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpointUrl")
    def attr_endpoint_url(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EndpointURL
        """
        return jsii.get(self, "attrEndpointUrl")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticBeanstalk::Environment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::Environment.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="cnamePrefix")
    def cname_prefix(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-cnameprefix
        """
        return jsii.get(self, "cnamePrefix")

    @cname_prefix.setter
    def cname_prefix(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cnamePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.EnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-name
        """
        return jsii.get(self, "environmentName")

    @environment_name.setter
    def environment_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "environmentName", value)

    @builtins.property
    @jsii.member(jsii_name="optionSettings")
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "OptionSettingProperty"]]]]:
        """``AWS::ElasticBeanstalk::Environment.OptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-optionsettings
        """
        return jsii.get(self, "optionSettings")

    @option_settings.setter
    def option_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "OptionSettingProperty"]]]],
    ) -> None:
        jsii.set(self, "optionSettings", value)

    @builtins.property
    @jsii.member(jsii_name="platformArn")
    def platform_arn(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.PlatformArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-platformarn
        """
        return jsii.get(self, "platformArn")

    @platform_arn.setter
    def platform_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "platformArn", value)

    @builtins.property
    @jsii.member(jsii_name="solutionStackName")
    def solution_stack_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.SolutionStackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-solutionstackname
        """
        return jsii.get(self, "solutionStackName")

    @solution_stack_name.setter
    def solution_stack_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "solutionStackName", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.TemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-templatename
        """
        return jsii.get(self, "templateName")

    @template_name.setter
    def template_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TierProperty"]]:
        """``AWS::ElasticBeanstalk::Environment.Tier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-tier
        """
        return jsii.get(self, "tier")

    @tier.setter
    def tier(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TierProperty"]],
    ) -> None:
        jsii.set(self, "tier", value)

    @builtins.property
    @jsii.member(jsii_name="versionLabel")
    def version_label(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.VersionLabel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-versionlabel
        """
        return jsii.get(self, "versionLabel")

    @version_label.setter
    def version_label(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "versionLabel", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.OptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class OptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: str,
            option_name: str,
            resource_name: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param namespace: ``CfnEnvironment.OptionSettingProperty.Namespace``.
            :param option_name: ``CfnEnvironment.OptionSettingProperty.OptionName``.
            :param resource_name: ``CfnEnvironment.OptionSettingProperty.ResourceName``.
            :param value: ``CfnEnvironment.OptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html
            """
            self._values = {
                "namespace": namespace,
                "option_name": option_name,
            }
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> str:
            """``CfnEnvironment.OptionSettingProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-namespace
            """
            return self._values.get("namespace")

        @builtins.property
        def option_name(self) -> str:
            """``CfnEnvironment.OptionSettingProperty.OptionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-optionname
            """
            return self._values.get("option_name")

        @builtins.property
        def resource_name(self) -> typing.Optional[str]:
            """``CfnEnvironment.OptionSettingProperty.ResourceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-elasticbeanstalk-environment-optionsetting-resourcename
            """
            return self._values.get("resource_name")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnEnvironment.OptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-option-settings.html#cfn-beanstalk-optionsettings-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.TierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type", "version": "version"},
    )
    class TierProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[str] = None,
            type: typing.Optional[str] = None,
            version: typing.Optional[str] = None,
        ) -> None:
            """
            :param name: ``CfnEnvironment.TierProperty.Name``.
            :param type: ``CfnEnvironment.TierProperty.Type``.
            :param version: ``CfnEnvironment.TierProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html
            """
            self._values = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnEnvironment.TierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-name
            """
            return self._values.get("name")

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnEnvironment.TierProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-type
            """
            return self._values.get("type")

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnEnvironment.TierProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment-tier.html#cfn-beanstalk-env-tier-version
            """
            return self._values.get("version")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "cname_prefix": "cnamePrefix",
        "description": "description",
        "environment_name": "environmentName",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "tags": "tags",
        "template_name": "templateName",
        "tier": "tier",
        "version_label": "versionLabel",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        application_name: str,
        cname_prefix: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        environment_name: typing.Optional[str] = None,
        option_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEnvironment.OptionSettingProperty"]]]] = None,
        platform_arn: typing.Optional[str] = None,
        solution_stack_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        template_name: typing.Optional[str] = None,
        tier: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEnvironment.TierProperty"]] = None,
        version_label: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticBeanstalk::Environment``.

        :param application_name: ``AWS::ElasticBeanstalk::Environment.ApplicationName``.
        :param cname_prefix: ``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.
        :param description: ``AWS::ElasticBeanstalk::Environment.Description``.
        :param environment_name: ``AWS::ElasticBeanstalk::Environment.EnvironmentName``.
        :param option_settings: ``AWS::ElasticBeanstalk::Environment.OptionSettings``.
        :param platform_arn: ``AWS::ElasticBeanstalk::Environment.PlatformArn``.
        :param solution_stack_name: ``AWS::ElasticBeanstalk::Environment.SolutionStackName``.
        :param tags: ``AWS::ElasticBeanstalk::Environment.Tags``.
        :param template_name: ``AWS::ElasticBeanstalk::Environment.TemplateName``.
        :param tier: ``AWS::ElasticBeanstalk::Environment.Tier``.
        :param version_label: ``AWS::ElasticBeanstalk::Environment.VersionLabel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html
        """
        self._values = {
            "application_name": application_name,
        }
        if cname_prefix is not None:
            self._values["cname_prefix"] = cname_prefix
        if description is not None:
            self._values["description"] = description
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if tags is not None:
            self._values["tags"] = tags
        if template_name is not None:
            self._values["template_name"] = template_name
        if tier is not None:
            self._values["tier"] = tier
        if version_label is not None:
            self._values["version_label"] = version_label

    @builtins.property
    def application_name(self) -> str:
        """``AWS::ElasticBeanstalk::Environment.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-applicationname
        """
        return self._values.get("application_name")

    @builtins.property
    def cname_prefix(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.CNAMEPrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-cnameprefix
        """
        return self._values.get("cname_prefix")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-description
        """
        return self._values.get("description")

    @builtins.property
    def environment_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.EnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-name
        """
        return self._values.get("environment_name")

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEnvironment.OptionSettingProperty"]]]]:
        """``AWS::ElasticBeanstalk::Environment.OptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-optionsettings
        """
        return self._values.get("option_settings")

    @builtins.property
    def platform_arn(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.PlatformArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-platformarn
        """
        return self._values.get("platform_arn")

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.SolutionStackName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-solutionstackname
        """
        return self._values.get("solution_stack_name")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticBeanstalk::Environment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
        """
        return self._values.get("tags")

    @builtins.property
    def template_name(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.TemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-templatename
        """
        return self._values.get("template_name")

    @builtins.property
    def tier(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEnvironment.TierProperty"]]:
        """``AWS::ElasticBeanstalk::Environment.Tier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-tier
        """
        return self._values.get("tier")

    @builtins.property
    def version_label(self) -> typing.Optional[str]:
        """``AWS::ElasticBeanstalk::Environment.VersionLabel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html#cfn-beanstalk-environment-versionlabel
        """
        return self._values.get("version_label")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnApplicationVersion",
    "CfnApplicationVersionProps",
    "CfnConfigurationTemplate",
    "CfnConfigurationTemplateProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
]

publication.publish()
