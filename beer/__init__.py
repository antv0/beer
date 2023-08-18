import beer.argument_parser as argument_parser
import beer.utils as utils
import beer.actions as actions
from beer.types import State, Config

def main():
    args = argument_parser.parser.parse_args()
    config_filename = args.config

    config: Config = utils.load_config_from_file_or_fail(config_filename)
    state: State = utils.load_state_from_file_or_fail(config['state_file'])

    utils.dump_state(state, config['state_file'])

    if args.action == 'add':
        actions.action_add(state, config, args)
    elif args.action == 'install-runner':
        actions.action_install_runner(state, config, args)
    elif args.action == 'remove-runner':
        actions.action_remove_runner(state, config, args)
    elif args.action in ['run', 'r']:
        actions.action_run(state, config, args)
    elif args.action == 'shell':
        actions.action_shell(state, config, args)
    elif args.action == 'prefix':
        actions.action_prefix(state, config, args)
    elif args.action == 'remove':
        actions.action_remove(state, config, args)
    elif args.action in ['list', 'ls']:
        actions.action_list(state, config, args)
    elif args.action is None:
        argument_parser.parser.print_help()
    else:
        raise ValueError(f'Unexpected action: {args.action}')
