"""
This file contains utility functions that are used by the other modules.
"""
import os
import json

from beer.types import State, Config, Runner, Prefix

def empty_state() -> State:
    return {
        'prefixes': [],
        'runners': [],
        'version': 1  # version of the state file. This should be increased when the format changes
                      # so that we can migrate the state file.
    }

def default_config() -> Config:
    return {
        'state_file': '~/.beer.json',
    }

def runner_exists(state: State, runner_name: str) -> bool:
    return runner_name in [ r['name'] for r in state['runners'] ]

def get_runner_or_fail(state: State, runner_name: str) -> Runner:
    runner: Runner
    if runner_name == 'system':
        runner = 'system'
    elif runner_exists(state, runner_name):
        runner = [ r for r in state['runners'] if r['name'] == runner_name ][0]
    else:
        print(f'Error: runner {runner_name} is not installed')
        exit(1)
    return runner

def prefix_exists(state: State, prefix_name: str) -> bool:
    return prefix_name in [ p['name'] for p in state['prefixes'] ]

def get_prefix_or_fail(state: State, prefix_name: str) -> Prefix:
    if not prefix_exists(state, prefix_name):
        print(f'Error: prefix {prefix_name} does not exist')
        exit(1)
    return [ p for p in state['prefixes'] if p['name'] == prefix_name ][0]

def prefix_env(prefix: Prefix) -> dict[str, str]:
    return {
        'WINEPREFIX': prefix['dir'],
    }

def wine_env(runner: Runner) -> dict[str, str]:
    if runner == 'system':
        return {}
    else:
        return {
            'PATH': f'/opt/wine-{runner["name"]}/bin:{os.environ["PATH"]}',
            'LD_LIBRARY_PATH': f'/opt/wine-{runner["name"]}/lib:{os.environ["LD_LIBRARY_PATH"]}'
        }

def prepare_env(prefix: Prefix, runner: Runner) -> dict[str, str]:
    """
    Prepares the enviroment for a prefix and a runner and use os environ as base
    """
    env = os.environ.copy()

    env.update(wine_env(runner))
    if not runner == 'system':
        env.update(runner['enviroment'])

    env.update(prefix_env(prefix))
    env.update(prefix['enviroment'])
    return env

def dump_state(state, filename): 
    """
    Dumps the state to a file.
    Exits with an error if the file cannot be written.
    """
    try:
        json.dump(state, open(filename, 'w'), indent=2)
    except Exception as e:
        print(f'Error: could not write state file {filename}')
        print(e)
        exit(1)

def load_config_from_file_or_fail(config_filename: str) -> Config:
    try:
        with open(config_filename) as f:
            config_ = json.load(f)
    except FileNotFoundError:
        config_ = default_config()
    except json.decoder.JSONDecodeError:
        print('Error: invalid config file')
        exit(1)

    config = default_config()
    config.update(config_)

    # Special case for the state file
    config['state_file'] = os.path.expanduser(config_['state_file'])

    return config

def load_state_from_file_or_fail(state_filename: str) -> State:
    try:
        with open(state_filename) as f:
            state = json.load(f)
    except FileNotFoundError:
        state = empty_state()
    except json.decoder.JSONDecodeError:
        print('Error: invalid state file')
        exit(1)
    except Exception as e:
        print('Error: unexpected error')
        print(e)
        exit(1)

    if state['version'] != 1:
        print('Error: invalid state file version')
        exit(1)

    return state
