"""Configuration"""

import yaml, os, sys

from .utils import load_yaml
STATIC_DIR = os.path.join(sys.prefix, 'nbmessages')

default_config = os.path.join(STATIC_DIR, 'nbmessages-config.yaml')

CONFIG_FILE = '/etc/jupyter/nbmessages-config.yaml'
CONFIG_FILE = CONFIG_FILE if os.path.isfile(CONFIG_FILE) else default_config

class Config:
    """Representation of the config file"""
    def __init__(self):
        self._configs = load_yaml(CONFIG_FILE)
        self.path = CONFIG_FILE
    
    def _save(self) -> None:
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(self._configs, f, default_flow_style=False)

    @property
    def config(self) -> dict:
        """Get the config file as a dict

        Returns:
            dict -- config file fields + values
        """
        return self._configs
    
    def update_config(self, kv: dict):
        """Overwrite what's in the config file

        Arguments:
            kv {dict} -- The new config file object representation
        """
        self._configs.update(kv)
        self._save()


