"""
Fetch and load user configuration.
"""
import os
import yaml
from getpass import getpass


def _prompt_credentials() -> dict:
    user_config = dict()
    username = input("Username:")
    password = getpass()
    user_config["username"] = username
    user_config["password"] = password
    return user_config


def save_config(config_path, user_data: dict):
    """Save `user_data` to `config_path`."""
    with open(config_path, "rw+") as dest:
        yaml.dump(user_data, dest)


def fetch_path() -> str:
    """"""
    home = os.path.expanduser("~")
    home_config = "{}/.config".format(home)
    if os.path.isdir(home_config):
        return "{}/shout.yml".format(home_config)
    return "{}/.shout.yml".format(home)
