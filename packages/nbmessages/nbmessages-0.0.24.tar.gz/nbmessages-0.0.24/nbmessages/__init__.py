import sys, os, pkg_resources
from .etc import Config, STATIC_DIR

version = pkg_resources.require("nbmessages")[0].version

config = Config()
_config = config.config
CONFIG_DIR = os.path.dirname(config.path)
DATA_DIR_IGNORE_DIRS = _config['application_data_dir']['data_dirs_to_ignore']
APPLICATION_DATA_DIR = _config['application_data_dir']['location']

def _jupyter_nbextension_paths():
    paths = [
        dict(
            section="tree",
            src=os.path.join('nbextensions', 'message'),
            dest="message",
            require="message/main"
        ),
        dict(
            section="tree",
            src=os.path.join('nbextensions', 'admin'),
            dest="admin",
            require="admin/main"
        )
    ]

    return paths

def _jupyter_server_extension_paths():
    paths = [
        dict(module="nbmessages.extensions.message"),
        dict(module="nbmessages.extensions.admin")
    ]

    return paths