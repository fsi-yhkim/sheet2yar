# coding: utf-8
import os
import sys
import argparse
import jinja2
from jinja2 import Environment, FileSystemLoader
from importers.base import ImporterBase
from importers import IMPORTER_CLASSES


def load_sheet(importer_class: ImporterBase, parsed_arguments, *args, **kwargs):
    importer_object = importer_class(parsed_arguments)
    entries = importer_object.load(*args, **kwargs)

    return entries


def main():
    argument_parser = argparse.ArgumentParser()

    argument_group_base = argument_parser.add_argument_group('Base Options')
    argument_group_base.add_argument(
        '--rule-name'
        , help='name of rule'
        , action='store'
        , default='untitled'
    )
    argument_group_base.add_argument(
        '--template-root'
        , help='path of template root directory (default: ./templates/)'
        , default='./templates/'
    )
    argument_group_base.add_argument(
        '--template-name'
        , help='name of template file'
    )

    subparsers = argument_parser.add_subparsers(
        title='Available importers', dest='selected_importer'
    )

    for name, klass in IMPORTER_CLASSES.items():
        klass.add_subparser(subparsers)
    
    parsed_arguments = argument_parser.parse_args()

    if not parsed_arguments.selected_importer:
        argument_parser.print_help()
        exit(-1)

    context = dict()
    context['rows'] = load_sheet(
        IMPORTER_CLASSES[parsed_arguments.selected_importer]
        , parsed_arguments
    )
    context['rule_name'] = parsed_arguments.rule_name

    path_template_root = os.path.abspath(
        parsed_arguments.template_root
    )

    filesystem_template_loader = FileSystemLoader(path_template_root)
    template_environment = Environment(loader=filesystem_template_loader)

    template = template_environment.get_template(
        parsed_arguments.template_name
    )

    rendered_result = template.render(**context)
    print(rendered_result)


if '__main__' == __name__:
    main()
