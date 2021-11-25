# AWS SAM application template for Python 3.9

The purpose of this repository is to suggest a project folder structure and how
to write functions that are easy to test.
The approach used is TDD and SOLID principles following the best practices suggested by AWS.

## IMPORTANT

The application uses Python 3.9 runtime (see [template.yaml](template.yaml)).
Before go further be sure that the correct version of Python is installed and running. To check it

```
$ python3 -V
Python 3.9.6
```

If you are on macOS, you are using [Homebrew](https://brew.sh/) and you have multiple version of Python installed on your system be sure to switch to the right version.

To check which versions are installed run

```
$ brew list | grep python
python@3.8
python@3.9
```

To switch

```
$ brew unlink python@3.9
$ brew unlink python@3.8
$ brew link --force python@3.9
```

Close and reopen the terminal or run `rehash` to make the switch effective.

The reference is this [Stack Overflow post](https://stackoverflow.com/questions/64362772/switching-python-version-installed-by-homebrew).

## How to use it

The following steps assume you already [installed and configured](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) AWS SAM on your PC.

### Init

1. create the SAM application using this repository as template
   ```
   $ sam init --location https://github.com/claranet-ch/aws-sam-application-template-python.git --name my-awesome-sam-app
   ```
2. create the virtual environment and install all dependencies for local development and testing
   ```
   $ ./create_venv.sh
   ```
3. activate the virtual environment
   ```
   $ source .venv/bin/activate
   ```
4. to check that everything is ready to use, run

   ```
   $ ./run_all_tests.sh
   ```

   the output should be like

   ```
   Running all tests ...

   .
   ----------------------------------------------------------------------
   Ran 1 test in 4.318s

   OK
   ```

### Deploy

1. build the application
   ```
   $ sam build
   ```
2. deploy the application
   ```
   $ sam deploy --guided
   ```

### Cleanup

Deletes an AWS SAM application by deleting the AWS CloudFormation stack, the artifacts that were packaged and deployed to Amazon S3 and Amazon ECR, and the AWS SAM template file.

```
$ sam delete
```

## Implementation notes

### Function handler

The logic of the lambda is isolated in one file with postfix `_logic`. The handler
read the relevant data from the event and context objects, instantiates clients and pass all of them to the logic (see [Dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)).

### Layers

Layers are built by AWS SAM when you run `sam build` command.

**IMPORTANT**

> Remember to add the content `requirements.txt` located in each layer folder, in
the `requirements.txt` file inside the folder `tests/`. This will allow to write
and test your code locally.

### Testing

The test runner is [unittest](https://docs.python.org/3/library/unittest.html) build-in in Python standard library.

To write tests for AWS services we use
[botocore Stubber](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html) included in [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

### Logging

Instead of use the `print()` function, it is better to use the Python built-in
[logging library](https://docs.python.org/3/library/logging.html).

The code

```python
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
   logger.info('## ENVIRONMENT VARIABLES')
   logger.info(os.environ)
   logger.info('## EVENT')
   logger.info(event)
```

See [AWS Lambda function logging in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib).

### Tracing

By default, the X-Ray tracing mode is enabled for all functions. Keeping in mind
that

> In Lambda, you can use the X-Ray SDK to extend the Invocation subsegment with additional subsegments for downstream calls, annotations, and metadata. You can't access the function segment directly or record work done outside of the handler invocation scope. See [Using AWS Lambda with AWS X-Ray](https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html).

all functions must have a layer that contains the X-Ray SDK in order to [record metadata and trace downstream calls](https://docs.aws.amazon.com/lambda/latest/dg/python-tracing.html).

The code to add

```python
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

s3_client = boto3.client('s3')

def lambda_handler(event, context):
   ...
```

## More resources

- [License](LICENSE)
