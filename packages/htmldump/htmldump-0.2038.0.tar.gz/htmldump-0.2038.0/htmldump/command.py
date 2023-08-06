from sys import argv

from .html_utils import dump, to_json


html_dump_usage = f'''Usage:
    htmll_dump {{path}}

    Dumps HTML file
'''
def html_dump():
    try:
        path = argv[1]
        dump(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(htmldump_usage)


html_json_usage = f'''Usage:
    html_json {{path}}

    Convert HTML to JSON
'''
def html_json():
    try:
        path = argv[1]
        to_json(path)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(html_json_usage)


