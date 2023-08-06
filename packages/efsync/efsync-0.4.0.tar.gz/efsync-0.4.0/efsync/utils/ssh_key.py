import boto3
from uuid import uuid4
import os


def write_key_to_file(file_string=None, file_path='.efsync', key_name=''):
    try:
        if os.path.isfile(f'{file_path}/{key_name}.pem'):
            os.chmod(f'{file_path}/{key_name}.pem' , 0o777)
        with open(f'{file_path}/{key_name}.pem', 'w+') as out_file:
            out_file.write(file_string)
        os.chmod(f'{file_path}/{key_name}.pem' , 0o400)
    except Exception as e:
        print(e)
        raise(e)


def create_ssh_key(bt3=None, key_name=''):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.create_key_pair(KeyName=key_name)
        write_key_to_file(
            file_string=response['KeyMaterial'], key_name=key_name)
        return True
    except Exception as e:
        print(repr(e))
        raise(e)


def delete_ssh_key(bt3=None, key_name=''):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.delete_key_pair(KeyName=key_name)
        return True
    except Exception as e:
        print(repr(e))
        raise(e)
