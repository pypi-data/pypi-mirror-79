from json import dump
from pathlib import Path

from html_parser import HTML


def html_dump(path):
    raw = open(path).read()
    html = HTML(raw)
    for node in html.body.walk_relative():
        yield node
        if node.data and node.attrs['tag']!='script':
            yield node.data


def html_to_json(path):
    path = Path(path)

    def to_dict(node):
        items = node.attrs
        if node.data:
            items['data'] = node.data
        if node.nodes:
            items['nodes'] = [to_dict(sn) for sn in node]
        return items

    raw = open(path).read()
    html = HTML(raw)
    nodes = [to_dict(node) for node in html.body]
    with open(path.with_suffix('.json'), 'w') as out:
        dump(nodes, out)
