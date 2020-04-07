from os import path

from configparser import ConfigParser

# The path to directory this code is ran in.
CUR_PATH = path.dirname(path.abspath(__file__))

config_path = path.join(CUR_PATH, "../../config")
config_example_path = path.join(CUR_PATH, "../../config/example")

config_filename = "webserver_config.cfg"
shared_config_filename = "shared_config.cfg"

config_filepath = path.join(config_path, config_filename)
config_example_filepath = path.join(config_example_path, config_filename)

shared_config_filepath = path.join(config_path, shared_config_filename)
shared_config_example_filepath = path.join(config_example_path, shared_config_filename)

# If a person somehow included this very var, without running this script,
# they should be able to know that.
CFG = "Error"


class CFG_Exception(Exception):
    pass


def init_config():
    global CFG

    CFG = ConfigParser()
    if len(CFG.read(config_filepath)) == 0:
        raise CFG_Exception(
            "Webserver config file not supplied.\n"
            + "Please move all configs from "
            + path.realpath(config_example_path)
            + " to "
            + path.realpath(config_path)
            + "!"
        )
    if len(CFG.read(shared_config_filepath)) == 0:
        raise CFG_Exception(
            "Shared config file not supplied.\n"
            + "Please move all configs from "
            + path.realpath(config_example_path)
            + " to "
            + path.realpath(config_path)
            + "!"
        )

    if "Server" not in CFG.sections():
        raise CFG_Exception(
            "Improper Config setup: No Server section specified."
            + "Please run config.py script to generate examples if required."
        )


def generate_default():
    gen_CFG = ConfigParser()
    gen_CFG["Server"] = {
        "debug": False,
        # Use -1 to have no max count.
        "max_client_count": -1,
        "max_clients_per_ip": 1,
    }
    gen_CFG["Google_Authorization"] = {
        "google_client_id": "None",
        "google_client_secret": "None",
    }
    with open(config_example_filepath, "w") as config_file:
        gen_CFG.write(config_file)

    shared_CFG = ConfigParser()
    shared_CFG.read(shared_config_example_filepath)
    if "secret_key" not in shared_CFG["Server"].keys():
        # !!! It is very important to change this one to something !!!
        shared_CFG["Server"]["secret_key"] = "PUT_SECRET_KEY_HERE"
    if "ip" not in shared_CFG["Server"].keys():
        shared_CFG["Server"]["ip"] = "0.0.0.0"
    if "webserver_port" not in shared_CFG["Server"].keys():
        shared_CFG["Server"]["webserver_port"] = 8080

    with open(shared_config_example_filepath, "w") as shared_config_file:
        shared_CFG.write(shared_config_file)


if __name__ == "__main__":
    generate_default()

init_config()
