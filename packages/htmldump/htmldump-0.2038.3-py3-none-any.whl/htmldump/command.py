from sys import argv

from htmldump import (
    html_dump,
    html_to_json,
    html_tags,
    html_dump_tags,
)


html_dump_usage = f'''Usage:
    html_dump {{path}}

    Dumps HTML file
'''
def do_html_dump():
    try:
        path = argv[1]
        html_dump(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_dump_usage)


html_json_usage = f'''Usage:
    html_to_json {{path}}

    Convert HTML to JSON
'''
def do_html_to_json():
    try:
        path = argv[1]
        html_to_json(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_json_usage)


html_tags_usage = f'''Usage:
    html_tags {{path}}

    Dump HTML Tags to JSON
'''
def do_html_tags():
    try:
        path = argv[1]
        html_tags(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_tags_usage)


html_dump_tags_usage = f'''Usage:
    html_dump_tags {{path}}

    Dumps HTML Tags
'''
def do_html_dump_tags():
    try:
        path = argv[1]
        html_dump_tags(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_dump_tags_usage)


