# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sso_cfn_helper']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.60,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['aws-sso-cfn-helper = aws_sso_cfn_helper.template:main',
                     'aws-sso-lookup = aws_sso_cfn_helper.lookup:main']}

setup_kwargs = {
    'name': 'aws-sso-cfn-helper',
    'version': '0.1.0',
    'description': 'Work around current capabilities of AWS SSO CloudFormation resources',
    'long_description': "# aws-sso-cfn-helper\n## Work around current capabilities of AWS SSO CloudFormation resources\n\nAWS SSO's CloudFormation support currently only includes [`AWS::SSO::Assignment`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html), which means for every combination of principal (group or user), permission set, and target (AWS account), you need a separate CloudFormation resource. Additionally, AWS SSO does not support OUs as targets, so you need to specify every account separately.\n\nObviously, this gets verbose. `aws-sso-cfn-helper` will generate the assignment combinations according to your specifications.\n\nI am against client-side generation of CloudFormation templates, and look forward to discarding this tool once there are two prerequisites:\n1. OUs as targets for assignments\n2. An `AWS::SSO::AssignmentSet` resource that allows specifications of multiple principals, permission sets, and targets, and performs the combinatorics directly.\n\n## Install\n\nI recommend you install `aws-sso-cfn-helper` with [`pipx`](https://pipxproject.github.io/pipx/), which installs the tool in an isolated virtualenv while linking the script you need.\n\n```bash\n# with pipx\npipx install aws-sso-cfn-helper\n\n# without pipx\npython -m pip install --user aws-sso-cfn-helper\n```\n\n## Usage\nAll of the identifiers required below can be looked up using the included `aws-sso-lookup` utility, documented below. On both utilities the credentials used can be controlled with the `--profile` paramater.\n\n### AWS SSO instance id\nYou can provide the AWS SSO instance id directly using the `--instance` or `-i` parameter, or you can omit it and `aws-sso-cfn-helper` will query your account for the instance id. The instance id will be used to fill out permission set ARNs, if that information is missing.\n\n### Principals\nYou can specify principal ids using either or both of `--groups` and `--users`, abbreviated `-g` and `-u`, respectively.\n\n### Permission sets\nPermission sets can be provided either as ARNs (which include the SSO instance id), as the ARN suffix (`$INSTANCE_ID/$PERMISSION_SET_ID`) or simply as the permission set id, in which case the ARN will be constructed using the instance id as obtained above.\n\n### Targets\nYou can specify targets using either or both of `--ous` and `--accounts`, abbreviated `-o` and `-a`, respectively. Because AWS SSO does not support OUs as targets currently, specifying an OU will cause a lookup through the Organizations API to find all the accounts in that OU (and any child OUs). Note that this only happens once, so you would need to run this again after adding another account to the OU.\n\n### Output template\nBy default, `aws-sso-cfn-helper` will produce a template file called `template.yaml`. This can be changed with the `--template-file` parameter. If your inputs cause more assignment resources to be generated than can be held in one template, multiple files will be generated, with numbers inserted before the file suffix (e.g., `template01.yaml`, `template02.yaml`, etc.). You can adjust the number of resources per template (for example, if you plan to add additional resources to each template yourself) with `--max-resources-per-template`.\n\n### CloudFormation references\n\nCloudFormation resources can reference other resources or template parameters. To enable this when generating a template, use the syntax `!Ref=ReferenceName`, without spaces, for any of the inputs, and the generated resources will have the appropriate references (note that whatever they are referencing will not be present in the template, that is on you to add).\n\n### Input file\nAs all of this is in service of infrastructure as code, you may want to define the inputs as a file checked into source control. This file can be specified with the `--input-file` parameter, and takes the form of an INI file with the following section headers (corresponding to the command line parameters):\n* `instance`\n* `groups`\n* `users`\n* `permission-sets`\n* `ous`\n* `accounts`\n\nYou can use the same `!Ref=ReferenceName` syntax in the file, though you can include spaces around the equals.\n\n[Check out the example file.](example.ini)\n\n## `aws-sso-lookup`\nThe AWS SSO APIs and CloudFormation resources require the use of identifiers that are not displayed in the console, and that the APIs do not make easy to look up by name. `aws-sso-lookup` is provided to make this a little easier.\n\n| Item                    | Syntax                                             |\n| ----------------------- | -------------------------------------------------- |\n| AWS SSO instance        | `aws-sso-lookup instance`                          |\n| AWS SSO identity store  | `aws-sso-lookup identity-store`                    |\n| Groups                  | `aws-sso-lookup groups GROUP_NAME [GROUP_NAME...]` |\n| Users                   | `aws-sso-lookup users USER_NAME [USER_NAME...]`    |\n| Permission sets         | `aws-sso-lookup permission-sets NAME [NAME...]`    |\n\nFor instance and identity store, it just prints out the id. For the others, it displays the instance/identity store id being used, and then a CSV with columns for the name and identifier. By default, any names not found will have `NOT_FOUND` as their identifier, but with `--error-if-not-found`/`-e` it will exit with an error at the first name not found.\n\nFor group/user/permission set lookups, the instance/identity store will be automatically retrieved if you do not provide `--instance-arn` (for permission sets) or `--instance-store-id` (for groups and users).\n",
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-sso-cfn-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
