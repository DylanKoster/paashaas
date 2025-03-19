#!/usr/bin/env python
"""
Main PaaS-HaaS python file. Builds and Deploys the PaaS-HaaS API to AWS using AWS configuration and custom configuration
using the --path (-p) parameter.

Usage: python3 paas-haas.py [-p/--path PATH] template_directory
"""

import os
import yaml
from dataclasses import dataclass
import subprocess
import argparse
import tomllib
import tomli_w

# Dataclasses for automatic conversion from dictionary.
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
    aws_region: str = 'eu-central-1'

# Helper functions
def translate_config_key_to_template(name: str) -> str:
    """
    Translate a key from the configuration file to a key usable in an AWS SAM template file.

    This does the following: 
        - Capitalizes the first letter.
        - Capilatizes letters directly after underscores.
        - Removes all underscores (_)

    Examples:
        - mail_dest_address -> MailDestAddress
        - empty_item_mail_template -> EmptyItemMailTemplate
    """
    return ''.join(map(lambda v: v.capitalize(), name.split("_")))  

def translate_config_value_to_template(value: str) -> str:
    """
    Translate a value from the configuration file to a value usable in an AWS SAM template file.

    This turns all URL unusable symbols to URL encoded symbols.
    """
    return value.replace(" ", "\ ")

def create_args() -> argparse.Namespace:
    """
    Creates the ArgumentParser used for executing PaaS-HaaS.
    """
    parser = argparse.ArgumentParser(
                        prog='PaaS-HaaS',
                        description='Build and deploy a custom PaaS-HaaS instance using your configuration.')
    parser.add_argument('template', help="The path to the template file.")
    parser.add_argument('-p', '--path', help="The path of the PaaS-HaaS folder.", default="./paas-haas")
    parser.add_argument('-c', '--config', help="The path to the default samconfig.toml", default="./config/sam/samconfig.toml")

    return parser.parse_args()

# Main functionality
def load_template(file_path: str="template.yml") -> PaashaasConfig:
    """
    Initialize PyYAML custom constructors and parse the file stored at file_path into an PaashaasConfig object.
    """
    try:
        with open(file_path, "r") as file:
            template_raw = yaml.load(file, Loader=yaml.FullLoader)

        config: PaashaasConfig = PaashaasConfig(**template_raw)
        return config
    except:
        print("Failed parsing yaml file, is it the correct format?")
        exit(1)

def build(path: str):
    """
    Executes the sam build command in the path directory. Captures stdout and stderr. Stdout is printed in real time and
    stderr is printed iff the return code is not 0.
    """
    print("Starting SAM build...", end="\n\n")
    
    with subprocess.Popen(f"cd {path} && sam build", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line) 
        
        _, stderr = process.communicate()


    return_code = process.wait()
    if return_code != 0:
        print("Something went wrong while building the template file! Error message:")
        print("\n  " + stderr)
        exit(1)

    print("\nBuild succesful!", end="\n\n")

def deploy(template: PaashaasConfig, path: str) -> None:
    """
    Executes the sam deploy command in the path directory. Captures stdout and stderr. Stdout is printed in real time and
    stderr is printed iff the return code is not 0.

    All parameters in template are first translated to valid --parameters-override values.
    """
    print("\nStarting SAM deployment...", end="\n\n")

    cmd: str = "sam deploy --parameter-overrides "
    parameters = []
    for key, value in vars(template).items():
        if value == None: continue

        trans_key: str = translate_config_key_to_template(key)
        
        # If current item is mail template, first traverse that object.
        if key == "empty_item_mail_template":
            for key_sub, value_sub in value.items():
                trans_key_sub = translate_config_key_to_template(key_sub)
                trans_value: str = translate_config_value_to_template(value_sub)

                parameters.append(f"{trans_key}{trans_key_sub}=\"{trans_value}\"")

        else: 
            parameters.append(f"{trans_key}={value}")

    
    cmd += " ".join(parameters)

    with subprocess.Popen(f"cd {path} && {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line, end="")

        _, stderr = process.communicate()

    return_code = process.wait()
    if return_code != 0:
        print("Something went wrong while deploying the template file! Error message:")
        print("\n  " + stderr)
        exit(1)

    print("\nDeployment succesful!", end="\n\n")

def create_samconfig(template: str, config: PaashaasConfig, path: str) -> None:
    """
    Create a new samconfig.toml based on the given config.
    """
    with open(template, 'rb') as f:
        toml: dict[str, any] = tomllib.load(f)

        if (config.stack_name): 
            toml['default']['global']['parameters']['stack_name'] = config.stack_name
            toml['default']['deploy']['parameters']['s3_prefix'] = config.stack_name
        if (config.version): toml['version'] = config.version
        if (config.aws_region): toml['default']['deploy']['parameters']['region'] = config.aws_region
        
        with open(f"{path}/samconfig.toml", "wb+") as f:
            tomli_w.dump(toml, f)

if __name__ == "__main__":
    args: argparse.Namespace = create_args()

    template: PaashaasConfig = load_template(args.template)
    create_samconfig(args.config, template, args.path)

    build(args.path)
    deploy(template, args.path)