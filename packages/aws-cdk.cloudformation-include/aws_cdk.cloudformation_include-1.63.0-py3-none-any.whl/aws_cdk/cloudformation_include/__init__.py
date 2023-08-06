"""
# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.CfnInclude.html).

## Basic usage

Assume we have a file with an existing template.
It could be in JSON format, in a file `my-template.json`:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

Or it could by in YAML format, in a file `my-template.yaml`:

```yaml
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: some-bucket-name
```

It can be included in a CDK application with the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.cloudformation_include as cfn_inc

cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

Or, if your template uses YAML:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.yaml"
)
```

**Note**: different YAML parsers sometimes don't agree on what exactly constitutes valid YAML.
If you get a YAML exception when including your template,
try converting it to JSON, and including that file instead.
If you're downloading your template from the CloudFormation AWS Console,
you can easily get it in JSON format by clicking the 'View in Designer'
button on the 'Template' tab -
once in Designer, select JSON in the "Choose template language"
radio buttons on the bottom pane.

This will add all resources from `my-template.json` / `my-template.yaml` into the CDK application,
preserving their original logical IDs from the template file.

Note that this including process will *not* execute any
[CloudFormation transforms](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html) -
including the [Serverless transform](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html).

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3

cfn_bucket = cfn_template.get_resource("Bucket")
```

Note that any resources not present in the latest version of the CloudFormation schema
at the time of publishing the version of this module that you depend on,
including [Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html),
will be returned as instances of the class `CfnResource`,
and so cannot be cast to a different resource type.

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

If you need, you can also convert the CloudFormation resource to a higher-level
resource by importing it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)
```

## Non-resource template elements

In addition to resources,
you can also retrieve and mutate all other template elements:

* [Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  param = cfn_template.get_parameter("MyParameter")

  # mutating the parameter
  param.default = "MyDefault"
  ```
* [Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  condition = cfn_template.get_condition("MyCondition")

  # mutating the condition
  condition.expression = core.Fn.condition_equals(1, 2)
  ```
* [Mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  mapping = cfn_template.get_mapping("MyMapping")

  # mutating the mapping
  mapping.set_value("my-region", "AMI", "ami-04681a1dbd79675a5")
  ```
* [Service Catalog template Rules](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  rule = cfn_template.get_rule("MyRule")

  # mutating the rule
  rule.add_assertion(core.Fn.condition_contains(["m1.small"], my_parameter.value), "MyParameter has to be m1.small")
  ```
* [Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  output = cfn_template.get_output("MyOutput")

  # mutating the output
  output.value = cfn_bucket.attr_arn
  ```
* [Hooks for blue-green deployments](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  hook = cfn_template.get_hook("MyOutput")

  # mutating the hook
  code_deploy_hook = hook
  code_deploy_hook.service_role = my_role.role_arn
  ```

## Parameter replacement

If your existing template uses CloudFormation Parameters,
you may want to remove them in favor of build-time values.
You can do that using the `parameters` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
inc.CfnInclude(self, "includeTemplate",
    template_file="path/to/my/template",
    parameters={
        "MyParam": "my-value"
    }
)
```

This will replace all references to `MyParam` with the string `'my-value'`,
and `MyParam` will be removed from the 'Parameters' section of the template.

## Nested Stacks

This module also supports templates that use [nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html).

For example, if you have the following parent template:

```json
{
  "Resources": {
    "ChildStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": "https://my-s3-template-source.s3.amazonaws.com/child-stack.json"
      }
    }
  }
}
```

where the child template pointed to by `https://my-s3-template-source.s3.amazonaws.com/child-stack.json` is:

```json
{
  "Resources": {
    "MyBucket": {
      "Type": "AWS::S3::Bucket"
    }
  }
}
```

You can include both the parent stack,
and the nested stack in your CDK application as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
parent_template = inc.CfnInclude(self, "ParentStack",
    template_file="path/to/my-parent-template.json",
    nested_stacks={
        "ChildStack": {
            "template_file": "path/to/my-nested-template.json"
        }
    }
)
```

Here, `path/to/my-nested-template.json`
represents the path on disk to the downloaded template file from the original template URL of the nested stack
(`https://my-s3-template-source.s3.amazonaws.com/child-stack.json`).
In the CDK application,
this file will be turned into an [Asset](https://docs.aws.amazon.com/cdk/latest/guide/assets.html),
and the `TemplateURL` property of the nested stack resource
will be modified to point to that asset.

The included nested stack can be accessed with the `getNestedStack` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
included_child_stack = parent_template.get_nested_stack("ChildStack")
child_stack = included_child_stack.stack
child_template = included_child_stack.included_template
```

Now you can reference resources from `ChildStack`,
and modify them like any other included template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket = child_template.get_resource("MyBucket")
cfn_bucket.bucket_name = "my-new-bucket-name"

role = iam.Role(child_stack, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)

role.add_to_policy(iam.PolicyStatement(
    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"
    ],
    resources=[cfn_bucket.attr_arn]
))
```

## Vending CloudFormation templates as Constructs

In many cases, there are existing CloudFormation templates that are not entire applications,
but more like specialized fragments, implementing a particular pattern or best practice.
If you have templates like that,
you can use the `CfnInclude` class to vend them as CDK Constructs:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import path as path

class MyConstruct(Construct):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # include a template inside the Construct
        cfn_inc.CfnInclude(self, "MyConstruct",
            template_file=path.join(__dirname, "my-template.json"),
            preserve_logical_ids=False
        )
```

Notice the `preserveLogicalIds` parameter -
it makes sure the logical IDs of all the included template elements are re-named using CDK's algorithm,
guaranteeing they are unique within your application.
Without that parameter passed,
instantiating `MyConstruct` twice in the same Stack would result in duplicated logical IDs.
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


class CfnInclude(
    aws_cdk.core.CfnElement,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/cloudformation-include.CfnInclude",
):
    """Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        template_file: str,
        nested_stacks: typing.Optional[typing.Mapping[str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from {@link CfnInclude.getNestedStack}. If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        stability
        :stability: experimental
        """
        props = CfnIncludeProps(
            template_file=template_file,
            nested_stacks=nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(self, condition_name: str) -> aws_cdk.core.CfnCondition:
        """Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getCondition", [condition_name])

    @jsii.member(jsii_name="getHook")
    def get_hook(self, hook_logical_id: str) -> aws_cdk.core.CfnHook:
        """Returns the CfnHook object from the 'Hooks' section of the included CloudFormation template with the given logical ID.

        Any modifications performed on the returned object will be reflected in the resulting CDK template.

        If a Hook with the given logical ID is not present in the template,
        an exception will be thrown.

        :param hook_logical_id: the logical ID of the Hook in the included CloudFormation template's 'Hooks' section.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getHook", [hook_logical_id])

    @jsii.member(jsii_name="getMapping")
    def get_mapping(self, mapping_name: str) -> aws_cdk.core.CfnMapping:
        """Returns the CfnMapping object from the 'Mappings' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Mapping with the given name is not present in the template,
        an exception will be thrown.

        :param mapping_name: the name of the Mapping in the template to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getMapping", [mapping_name])

    @jsii.member(jsii_name="getNestedStack")
    def get_nested_stack(self, logical_id: str) -> "IncludedNestedStack":
        """Returns the NestedStack with name logicalId.

        For a nested stack to be returned by this method, it must be specified in the {@link CfnIncludeProps.nestedStacks}
        property.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNestedStack", [logical_id])

    @jsii.member(jsii_name="getOutput")
    def get_output(self, logical_id: str) -> aws_cdk.core.CfnOutput:
        """Returns the CfnOutput object from the 'Outputs' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If an Output with the given name is not present in the template,
        throws an exception.

        :param logical_id: the name of the output to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getOutput", [logical_id])

    @jsii.member(jsii_name="getParameter")
    def get_parameter(self, parameter_name: str) -> aws_cdk.core.CfnParameter:
        """Returns the CfnParameter object from the 'Parameters' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getParameter", [parameter_name])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: str) -> aws_cdk.core.CfnResource:
        """Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResource", [logical_id])

    @jsii.member(jsii_name="getRule")
    def get_rule(self, rule_name: str) -> aws_cdk.core.CfnRule:
        """Returns the CfnRule object from the 'Rules' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Rule with the given name is not present in the template,
        an exception will be thrown.

        :param rule_name: the name of the Rule in the CloudFormation template.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getRule", [rule_name])


@jsii.data_type(
    jsii_type="@aws-cdk/cloudformation-include.CfnIncludeProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "nested_stacks": "nestedStacks",
        "parameters": "parameters",
        "preserve_logical_ids": "preserveLogicalIds",
    },
)
class CfnIncludeProps:
    def __init__(
        self,
        *,
        template_file: str,
        nested_stacks: typing.Optional[typing.Mapping[str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[bool] = None,
    ) -> None:
        """Construction properties of {@link CfnInclude}.

        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from {@link CfnInclude.getNestedStack}. If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        stability
        :stability: experimental
        """
        self._values = {
            "template_file": template_file,
        }
        if nested_stacks is not None:
            self._values["nested_stacks"] = nested_stacks
        if parameters is not None:
            self._values["parameters"] = parameters
        if preserve_logical_ids is not None:
            self._values["preserve_logical_ids"] = preserve_logical_ids

    @builtins.property
    def template_file(self) -> str:
        """Path to the template file.

        Both JSON and YAML template formats are supported.

        stability
        :stability: experimental
        """
        return self._values.get("template_file")

    @builtins.property
    def nested_stacks(self) -> typing.Optional[typing.Mapping[str, "CfnIncludeProps"]]:
        """Specifies the template files that define nested stacks that should be included.

        If your template specifies a stack that isn't included here, it won't be created as a NestedStack
        resource, and it won't be accessible from {@link CfnInclude.getNestedStack}.

        If you include a stack here with an ID that isn't in the template,
        or is in the template but is not a nested stack,
        template creation will fail and an error will be thrown.

        default
        :default: - no nested stacks will be included

        stability
        :stability: experimental
        """
        return self._values.get("nested_stacks")

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Specifies parameters to be replaced by the values in this mapping.

        Any parameters in the template that aren't specified here will be left unmodified.
        If you include a parameter here with an ID that isn't in the template,
        template creation will fail and an error will be thrown.

        default
        :default: - no parameters will be replaced

        stability
        :stability: experimental
        """
        return self._values.get("parameters")

    @builtins.property
    def preserve_logical_ids(self) -> typing.Optional[bool]:
        """Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file.

        If you're vending a Construct using an existing CloudFormation template,
        make sure to pass this as ``false``.

        **Note**: regardless of whether this option is true or false,
        the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element,
        as specified in the template file.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("preserve_logical_ids")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloudformation-include.IncludedNestedStack",
    jsii_struct_bases=[],
    name_mapping={"included_template": "includedTemplate", "stack": "stack"},
)
class IncludedNestedStack:
    def __init__(
        self, *, included_template: "CfnInclude", stack: aws_cdk.core.NestedStack
    ) -> None:
        """The type returned from {@link CfnInclude.getNestedStack}. Contains both the NestedStack object and CfnInclude representations of the child stack.

        :param included_template: The CfnInclude that represents the template, which can be used to access Resources and other template elements.
        :param stack: The NestedStack object which represents the scope of the template.

        stability
        :stability: experimental
        """
        self._values = {
            "included_template": included_template,
            "stack": stack,
        }

    @builtins.property
    def included_template(self) -> "CfnInclude":
        """The CfnInclude that represents the template, which can be used to access Resources and other template elements.

        stability
        :stability: experimental
        """
        return self._values.get("included_template")

    @builtins.property
    def stack(self) -> aws_cdk.core.NestedStack:
        """The NestedStack object which represents the scope of the template.

        stability
        :stability: experimental
        """
        return self._values.get("stack")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludedNestedStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
    "IncludedNestedStack",
]

publication.publish()
