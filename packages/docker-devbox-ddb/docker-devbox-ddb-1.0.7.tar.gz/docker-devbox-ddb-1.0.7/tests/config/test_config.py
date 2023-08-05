# -*- coding: utf-8 -*-
import os

import yaml

from ddb.config import Config


def test_defaults():
    config = Config()
    assert config.env_prefix == 'DDB'
    assert config.filenames == ('ddb', 'ddb.local')
    assert config.extensions == ('yml', 'yaml')
    assert len(config.paths) == 3


def test_load_and_clear(data_dir):
    Config.defaults = None

    ddb_home, home, project = os.path.join(data_dir, 'load', 'ddb_home'), \
                              os.path.join(data_dir, 'load', 'home'), \
                              os.path.join(data_dir, 'load', 'project')

    with open(os.path.join(data_dir, 'load', 'expect.yml'), 'rb') as stream:
        expected = yaml.load(stream, Loader=yaml.FullLoader)

    config = Config(paths=(ddb_home, home, project))
    config.load()

    assert config.data == expected

    config.clear()
    assert not config.data


def test_load_with_env_overrides(data_dir):
    Config.defaults = None

    ddb_home, home, project = os.path.join(data_dir, 'load', 'ddb_home'), \
                              os.path.join(data_dir, 'load', 'home'), \
                              os.path.join(data_dir, 'load', 'project')

    os.environ['DDB_OVERRIDE_SOME_DEEP'] = "env"
    os.environ['DDB_OVERRIDE_SOME_LIST[1]'] = "replaced"

    with open(os.path.join(data_dir, 'load', 'expect_env.yml'), 'rb') as stream:
        expected = yaml.load(stream, Loader=yaml.FullLoader)

    config = Config(paths=(ddb_home, home, project))
    config.load()

    assert config.data == expected


def test_load_env_variables(data_dir):
    env = os.path.join(data_dir, 'load', 'env')

    config = Config(paths=(env,))
    config.load()

    assert os.environ.get('FOO') == 'bar'
    assert 'env' not in config.data
    assert 'another' in config.data
