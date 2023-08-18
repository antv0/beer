from typing import TypedDict, Literal

Prefix = TypedDict('Prefix', {
    'name': str,
    'dir': str,
    'runner': str,
    'enviroment': dict[str, str],
    'executable': str | None,
    'silent': bool
})

SystemRunner = Literal['system']
StandardRunner = TypedDict('StandardRunner', {
    'name': str,
    'dir': str,
    'enviroment': dict[str, str],
})
Runner = SystemRunner | StandardRunner

State = TypedDict('State', {
    'prefixes': list[Prefix],
    'runners': list[StandardRunner],
    'version': Literal[1]
})

Config = TypedDict('Config', {
    'state_file': str  # The path is absolute, the function that loads the config file should expand
                       # it
})

