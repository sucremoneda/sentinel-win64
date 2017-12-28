import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sucrd import SucreDaemon
from sucr_config import SucreConfig


def test_sucrd():
    config_text = SucreConfig.slurp_config_file(config.sucr_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000034b04ee039886ef9f2086894905a407feb53fdf89d5c6e8f6c36c8d9dd2'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000034b04ee039886ef9f2086894905a407feb53fdf89d5c6e8f6c36c8d9dd2'

    creds = SucreConfig.get_rpc_creds(config_text, network)
    sucrd = SucreDaemon(**creds)
    assert sucrd.rpc_command is not None

    assert hasattr(sucrd, 'rpc_connection')

    # Sucre testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = sucrd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sucrd.rpc_command('getblockhash', 0) == genesis_hash
