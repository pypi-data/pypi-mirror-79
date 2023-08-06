from json import dump
from pathlib import Path

from htmldump.html_parser import HTML


def html_dump(path):
    cont = open(path).read()
    html = HTML(cont)
    html.body.dump()


def html_to_json(path):
    path = Path(path)
    cont = open(path).read()
    html = HTML(cont)
    data = html.body.items
    dest = path.with_suffix('.json')
    with open(dest, 'w') as out:
        dump(data, out)


def html_tags(path):
    path = Path(path)
    cont = open(path).read()
    html = HTML(cont)
    tags = html.body.tags
    dest = path.with_suffix('.json')
    with open(dest, 'w') as out:
        dump(tags, out)


def html_dump_tags(path):
    cont = open(path).read()
    html = HTML(cont)
    html.body.dump_tags()


