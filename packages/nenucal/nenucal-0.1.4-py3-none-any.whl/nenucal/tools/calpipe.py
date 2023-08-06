#!/usr/bin/env python

import os
import sys

import click

from nenucal import tasks
from nenucal import __version__
from nenucal.settings import Settings

t_file = click.Path(exists=True, dir_okay=False)
t_dir = click.Path(exists=True, file_okay=False)

tasks_help = '\n'.join([f'  {name.ljust(17)}{desc}' for name, desc in tasks.get_all_tasks_descriptions().items()])


@click.command(epilog='\b\nAvailable tasks:\n' + tasks_help)
@click.version_option(__version__)
@click.argument('tasks_str', metavar='TASKS')
@click.argument('ms_ins', nargs=-1, type=str, required=False)
@click.option('--config', '-c', type=str, help='Configuration file', default=tasks.default_calpipe_filename,
              show_default=True)
def main(tasks_str, config, ms_ins):
    ''' End-to-end power spectra generation pipeline

        \b
        TASKS: Tasks to execute, comma separated
        CONFIG: Configuration file
        MS_INS: Measurement Sets to process
    '''
    if tasks_str == 'init':
        tasks.Init(None).run([])
        sys.exit(0)

    if config is tasks.default_calpipe_filename and not os.path.exists(config):
        print('Error: no config file given and default calpipe.toml not found. Did you try calpipe init ?')
        sys.exit(1)
    elif not os.path.exists(config):
        print(f"Error: Invalid value for '--config' / '-c': File '{config}' does not exist.")
        sys.exit(1)

    s = Settings.load_with_defaults(config)

    all_tasks = tasks.get_all_tasks()

    for task_name in tasks_str.split(','):
        if task_name not in all_tasks:
            print(f'Error: task {task_name} does not exist.')
            sys.exit(1)

    for task_name in tasks_str.split(','):
        ms_ins = all_tasks[task_name](s).run(ms_ins)
        if not ms_ins:
            print('\nError: no MS to process.')
            sys.exit(1)
