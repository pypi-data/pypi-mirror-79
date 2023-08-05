import boto3
import os
from base64 import b64decode


def DecryptEnv(env_key: str):
    """
    Helper function to decrypt environment variables in an AWS Lambda that were encrypted using AWS KMS.

    Decrypt code should run once and variables stored outside of the function handler so that these are decrypted once
    per container.

    :param env_key: The environment variable key (name of the environment variable).
    :return: The decrypted environment variable value.
    """
    encrypted = os.environ[env_key]
    decrypted = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(encrypted),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    return decrypted
