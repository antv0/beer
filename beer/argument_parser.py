import argparse
import os

parser = argparse.ArgumentParser(description='Easily manage wine prefixes for games')

parser.add_argument('--config',
                    '-c',
                    type=str,
                    help='The config file to use (default: ~/.config/beer.json)',
                    default=os.path.join(os.environ['HOME'], '.config', 'beer.json')
                    )
subparser = parser.add_subparsers(title='Actions', dest='action')

### Add
add_parser = subparser.add_parser('add', help='Add a new prefix')
add_parser.add_argument('prefix', type=str, help='The name of the prefix')
add_parser.add_argument('dir', type=str, help='The directory where the prefix will be created')
add_parser.add_argument(
    '--runner',
    type=str,
    help='The runner (version of wine) to use for this prefix. Defaults to system wine'
)

### Run
run_parser = subparser.add_parser(
    'run',
    aliases=['r'],
    help='Run an executable in a prefix'
)
run_parser.add_argument('prefix', type=str, help='The name of the prefix')
run_parser.add_argument(
    'executable',
    type=str,
    help='The executable to run',
    nargs='?',
    default=None
)
run_parser.add_argument(
    '--silent', '-s',
    action='store_true',
    help='Do not print the output of the program'
)

### Shell
shell_parser = subparser.add_parser('shell', help='Run a shell in a prefix')
shell_parser.add_argument('prefix', type=str, help='The name of the prefix')
shell_parser.add_argument('args', type=str, help='The arguments to pass to the shell', nargs='*')

### Remove
remove_parser = subparser.add_parser('remove', help='Remove a prefix')
remove_parser.add_argument('prefix', type=str, help='The name of the prefix')
remove_parser.add_argument(
    '--delete',
    '-d',
    action='store_true',
    help='Delete the prefix directory'
)

### Prefix
prefix_parser = subparser.add_parser('prefix', help='Configure a prefix')
prefix_parser.add_argument('prefix', type=str, help='The name of the prefix')
prefix_parser.add_argument(
    '--set-runner',
    type=str,
    help='Set the runner (version of wine) to use for this prefix.'
)
prefix_parser.add_argument(
    '--set-env',
    type=str,
    help='Set the enviroment variables for this prefix. Format: KEY1=VALUE1,KEY2=VALUE2,...'
)
prefix_parser.add_argument(
    '--set-executable',
    type=str,
    help='Set the default executable for this prefix'
)
prefix_parser.add_argument(
    '--silent',
    type=bool,
    help='Set if the output of the program should be printed by default'
)

### Install Runner
install_runner_parser = subparser.add_parser('install-runner', help='Install a new runner')
install_runner_parser.add_argument('name', type=str, help='The name of the runner')
install_runner_parser.add_argument('dir', type=str, help='The directory where the runner is installed')
install_runner_parser.add_argument('url', type=str, help='The url to download the runner from')

### Remove Runner
remove_runner_parser = subparser.add_parser('remove-runner', help='Remove a runner')
remove_runner_parser.add_argument('name', type=str, help='The name of the runner')


### List
list_parser = subparser.add_parser(
    'list',
    aliases=['ls'],
    help='List all prefixes'
)
