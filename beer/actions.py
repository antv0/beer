"""
This file contains procedures for each action that can be performed by the
user. These procedures have side effects on the state dictionary, which is
dumped to the state file after each action and on the filesystem.
"""
import os
import subprocess
import shutil

from beer.utils import *
from beer.types import State, Config, Prefix, Runner

def action_add(state, config, args):
    name = args.prefix
    prefix_abs_dir = os.path.abspath(args.dir)

    # Check that the directory is valid, writable and empty or non-existent
    if not os.path.isdir(prefix_abs_dir):
        try :
            os.makedirs(prefix_abs_dir)
        except Exception as e:
            print(f'Error: could not create directory {prefix_abs_dir}')
            print(e)
            exit(1)
    if not os.access(prefix_abs_dir, os.W_OK):
        print(f'Error: {prefix_abs_dir} is not writable')
        exit(1)
    if os.listdir(prefix_abs_dir):
        print(f'Error: {prefix_abs_dir} is not empty')
        exit(1)
    if prefix_exists(state, name):
        print(f'Error: prefix {name} already exists in prefixes list')
        exit(1)

    runner_name = args.runner or 'system'

    # Check that the runner is valid and exists
    _ = get_runner_or_fail(state, runner_name)

    prefix: Prefix = Prefix(name=name,
                            dir=prefix_abs_dir,
                            runner=runner_name,
                            enviroment={},
                            executable=None,
                            silent=False)

    state['prefixes'].append(prefix)
    dump_state(state, config['state_file'])


def action_install_runner(state, config, args):
    name = args.name
    dir = os.path.abspath(args.dir)
    url = args.url

    if runner_exists(state, name):
        print(f'Error: runner {name} already exists')
        exit(1)

    try:
        os.makedirs(dir)
    except Exception as e:
        print(f'Error: could not create directory {dir}')
        print(e)
        exit(1)

    try:
        print(f'Downloading runner...')
        subprocess.run(['curl', '-L', url, '-o', os.path.join(dir, 'wine.tar.xz')])
    except Exception as e:
        print(f'Error: could not download runner from {url}')
        print(e)
        exit(1)

    try:
        print(f'Extracting runner...')
        subprocess.run(['tar', '-xf', os.path.join(dir, 'wine.tar.xz'), '-C', dir])
    except Exception as e:
        print(f'Error: could not extract runner to {dir}')
        print(e)
        exit(1)

    runner_name: Runner = {
        'name': name,
        'dir': dir,
        'enviroment': {}
    }

    state['runners'].append(runner_name)
    dump_state(state, config['state_file'])

def action_run(state, config, args):
    # Check that the prefix exists
    prefix = get_prefix_or_fail(state, args.prefix)
    runner_name = get_runner_or_fail(state, prefix['runner'])

    env = prepare_env(prefix, runner_name)

    # find the executable to run
    executable = args.executable or prefix['executable']
    if not executable:
        print('Error: no executable specified.'
              'Please specify an executable or set a default executable for this prefix.')
        exit(1)

    # run the program with wine
    p = subprocess.run(['wine', executable], env=env, capture_output=args.silent)

def action_shell(state, config, args):
    # Check that the prefix and runner exist
    prefix = get_prefix_or_fail(state, args.prefix)
    runner_name = get_runner_or_fail(state, prefix['runner'])

    env = prepare_env(prefix, runner_name)

    # run the shell
    shell_command = os.environ.get('SHELL', 'sh')
    p = subprocess.run(shell_command, env=env)

def action_prefix(state, config, args):
    name = args.prefix

    # Check that the prefix exists
    prefix = get_prefix_or_fail(state, name)

    if args.set_runner:
        runner_name = args.set_runner
        if not runner_exists(state, runner_name):
            print(f'Error: runner {runner_name} is not installed')
            exit(1)
        prefix['runner'] = runner_name

    if args.set_env:
        # TODO: change this to a more robust parser
        prefix['enviroment'] = dict([ e.split('=') for e in args.set_env.split(',') ])

    if args.set_executable:
        prefix['executable'] = os.path.abspath(args.set_executable)

    dump_state(state, config['state_file'])

def action_remove(state, config, args):
    name = args.prefix

    # Check that the prefix exists
    if not prefix_exists(state, name):
        print(f'Error: prefix {name} does not exist')
        exit(1)
    prefix = [ p for p in state['prefixes'] if p['name'] == name ][0]

    delete = args.delete

    if delete:
        try:
            shutil.rmtree(prefix['dir'])
        except Exception as e:
            print(f'Error: could not delete prefix directory {prefix["dir"]}')
            print(e)
            exit(1)

    state['prefixes'].remove(prefix)
    dump_state(state, config['state_file'])

def action_list(state, config, args):
    print('Prefixes:')
    for prefix in state['prefixes']:
        print(f' *{prefix["name"]}')
        print(f'    dir: {prefix["dir"]}')
        print(f'    runner: {prefix["runner"]}')
        print(f'    enviroment:')
        for k, v in prefix['enviroment'].items():
            print(f'        {k}={v}')

        print(f'    executable: {prefix["executable"]}')
        print()

    
    print('Runners:')
    for runner_name in state['runners']:
        print(f' *{runner_name["name"]}')
        print(f'    dir: {runner_name["dir"]}')
        print(f'    enviroment: {runner_name["enviroment"]}')


def action_remove_runner(state, config, args):
    name = args.name

    # Check that the runner exists
    runner = get_runner_or_fail(state, name)

    if runner == 'system':
        print('Error: cannot remove system runner')
        exit(1)
    
    try:
        shutil.rmtree(runner['dir'])
    except Exception as e:
        print(f'Error: could not delete runner directory {runner["dir"]}')
        print(e)
        exit(1)

    state['runners'].remove(runner)
    dump_state(state, config['state_file'])
