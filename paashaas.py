#!/usr/bin/env python
"""
Parses a SAM template.yaml, searches for any DynamoDB table specifications and creates local DynamoDB tables based on
these specifications. 
"""

import os
import yaml
from dataclasses import dataclass
import subprocess
import argparse

@dataclass
class EmptyItemNotification:        
    subject: str
    html: str
    text: str

@dataclass
class PaashaasConfig:
    name: str
    version: str 
    mail_source_address: str
    mail_dest_address: str

    empty_item_mail_template: EmptyItemNotification = None

    stack_name: str = None

def translate_config_key_to_template(name: str) -> str:
    return ''.join(map(lambda v: v.capitalize(), name.split("_")))  

def translate_config_value_to_template(value: str) -> str:
    return value.replace(" ", "\ ").replace('\n', '\t\n')

def create_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                        prog='PaaS-HaaS',
                        description='Build and deploy a custom PaaS-HaaS instance using your configuration.')
    parser.add_argument('template', help="The path to the template file.")
    parser.add_argument('-p', '--path', help="The path of the PaaS-HaaS folder.", default="./paas-haas")
    return parser.parse_args()

def load_template(file_path: str="template.yml") -> PaashaasConfig:
    """
    Initialize PyYAML custom constructors and parse the file stored at file_path.
    """
    try:
        with open(file_path, "r") as file:
            template_raw = yaml.load(file, Loader=yaml.FullLoader)

        config: PaashaasConfig = PaashaasConfig(**template_raw)
        return config
    except:
        print("Failed parsing yaml file, is it the correct format?")
        exit(1)

def clean(path: str) -> None:
    os.remove(f"{path}/.aws-sam")

def build(path: str):
    print("Starting SAM build...")
    
    with subprocess.Popen(f"cd {path} && sam build", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line) 
        
        stdout, stderr = process.communicate()


    return_code = process.wait()
    if return_code != 0:
        print("Something went wrong while building the template file! Error message:")
        print("\n  " + stderr)
        exit(1)

    print("Build succesful!")

def deploy(template: PaashaasConfig, path: str) -> None:
    print("Starting SAM deployment...")

    cmd: str = "sam deploy --parameter-overrides "
    parameters = []
    for key, value in vars(template).items():
        if value == None: continue

        trans_key: str = translate_config_key_to_template(key)
        
        if key == "empty_item_mail_template":
            for key_sub, value_sub in value.items():
                trans_key_sub = translate_config_key_to_template(key_sub)
                trans_value: str = translate_config_value_to_template(value_sub)

                print(f"debug: {value_sub}")

                parameters.append(f"{trans_key}{trans_key_sub}=\"{trans_value}\"")

        else: 
            parameters.append(f"{trans_key}={value}")

    
    cmd += " ".join(parameters)
    print(cmd)
    process = subprocess.Popen(f"cd {path} && {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    return_code = process.wait()
    if return_code != 0:
        print("Something went wrong while deploying the template file! Error message:")
        print("\n  " + stderr)
        exit(1)

    print("Deployment succesful!")

if __name__ == "__main__":
    args: argparse.Namespace = create_args()

    template: PaashaasConfig = load_template(args.template)

    # clean(args.path)
    # build(args.path)
    deploy(template, args.path)