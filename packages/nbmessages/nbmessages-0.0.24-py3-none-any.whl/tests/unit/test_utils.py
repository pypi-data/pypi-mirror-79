from nbmessages.utils import *
from nbmessages import CONFIG_DIR

import unittest, os

class TestUtils(unittest.TestCase):
    def test_load_yaml(self):
        yaml = load_yaml(os.path.join(CONFIG_DIR, 'nbmessages-config.yaml'))
        assert isinstance(yaml, dict)
        assert bool(yaml)
        
    def test_parse_body(self):
        teststr = 'publishMode=Staging&tabTitle=adfsdfas&messageOperation=None'
        parsed_body = parse_body(teststr)
        
        keys = ['publishMode', 'tabTitle', 'messageOperation']
        values = ['Staging', 'adfsdfas', 'None']
        for k, v in parsed_body.items():
            assert k in keys
            keys.remove(k)
            
            assert v in values
            values.remove(v)
        
        assert len(values) == 0
        assert len(keys) == 0
