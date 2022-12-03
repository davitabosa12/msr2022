from dataclasses import dataclass


@dataclass(frozen=True)
class Label():
    id: str
    node_id: str
    url: str
    name: str
    color: str
    default: bool
    description: str


[{'id': 256180708, 'node_id': 'MDU6TGFiZWwyNTYxODA3MDg=', 'url': 'https://api.github.com/repos/TeamNewPipe/NewPipe/labels/feature%20request',
    'name': 'feature request', 'color': '84b6eb', 'default': False, 'description': 'Issue is related to a feature in the app.'}]
