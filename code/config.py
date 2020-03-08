from os import path

from configparser import ConfigParser

# The path to directory this code is ran in.
CUR_PATH = path.dirname(path.abspath(__file__))

config_path = path.join(CUR_PATH, "../config")
config_example_path = path.join(CUR_PATH, "../config/example")

config_filename = "config.cfg"

config_filepath = path.join(config_path, config_filename)
config_example_filepath = path.join(config_example_path, config_filename)

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
            "Config file not supplied.\n"
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
        # !!! It is very important to change this one to something !!!
        "secret_key": "PUT_SECRET_KEY_HERE",
        "ip": "0.0.0.0",
        "port": 8080,
        "debug": False,
        # Use -1 to have no max count.
        "max_client_count": -1,
        "max_clients_per_ip": 1,
    }
    with open(config_example_filepath, "w") as config_file:
        gen_CFG.write(config_file)


if __name__ == "__main__":
    generate_default()

init_config()
