import os
import sys
from pathlib import Path
from glob import glob
from importlib import import_module
from .trace import Trace
from time import time
import click

class PyLoader(Trace):
    """
    Class that runs load modules, that is Python modules that load some data in keanu database.
    """
    def __init__(_, filename, mode, source, destination):
        Trace.__init__(_)
        _.filename = filename
        
        _.module = PyLoader.import_module(filename)

        _.options = {
            'incremental': False,
            'display': False,
            'warn': False
        }
        _.options.update(mode)

        _.source = source
        _.destination = destination

        if _.defines('TAGS'):
            if isinstance(_.module.TAGS, dict):
                _.script_tracer_tags = _.module.TAGS
            else:
                raise click.ClickException("TAGS in {} should be a dict".format(_.filename))
        else:
            _.script_tracer_tags = {}

        if _.defines('ORDER'):
            if isinstance(_.module.ORDER, int):
                _.order = _.module.ORDER
            else:
                raise click.ClickException("ORDER in {} should be a number".format(_.filename))
        else:
            _.order = 100

    @staticmethod
    def import_module(filename):
        if filename.endswith(".py"):
            mod_name = os.path.splitext(os.path.basename(filename))[0]
            dir = os.path.dirname(os.path.abspath(filename))
            sys.path.insert(0, dir)
            mod = import_module(mod_name)
            sys.path.pop(0)
            return mod
        else:
            raise click.ClickException("Cannot load non-py file {}".format(filename))

    @staticmethod
    def from_directory(sqldir, mode, source, destination):
        files = glob(os.path.join(sqldir, '**/*.py'), recursive=True)
        if len(files) == 0:
            raise click.BadParameter('No py files found in {}'.format(sqldir), param_hint='config_or_dir')
        # skip __init__.py
        files = filter(lambda x: os.path.basename(x) != "__init__.py", files)
        scripts = list(map(lambda fn: PyLoader(fn, mode, source, destination), files))
        return scripts

    def __str__(_):
        return '{} ({})'.format(_.filename, _.order)


    @Trace.trace(lambda _: 'delete.{}'.format(_.filename.replace('/', '.')))
    def delete(_):
        if not _.defines('delete'):
            return

        try:
            yield 'py.script.start.delete', { 'script': _ }
            start_time = time()

            _.module.delete(_)
            yield 'py.script.end.delete', { 'script': _, 'time': time() - start_time }

        except KeyboardInterrupt as ctrlc:
            raise ctrlc


    @Trace.trace(lambda _: 'script.{}'.format(_.filename.replace('/', '.')))
    def execute(_):
        try:
            yield 'py.script.start', { 'script': _ }
            start_time = time()

            result = _.module.execute(_)

            yield 'py.script.end', {
                'script': _,
                'time': time() - start_time,
                'result': result
            }
        except KeyboardInterrupt as ctrlc:
            raise click.Abort("aborted.")
        except (ProgrammingError, IntegrityError, MySQLError, InternalError, DataError) as e:
            transaction.rollback()
            msg = str(e.args[0])
            msg = msg.replace('\\n', "\n")
            click.echo(message=msg, err=True)
            raise click.Abort(msg)

    def defines(_, varname):
        return varname in dir(_.module)

    @staticmethod
    def path_to_module(path):
        p = Path(path)

        def strip_py(x):
            if x.endswith('.py'):
                return x[0:-3]
            else:
                return x

        m = '.'.join(map(lambda a: strip_py(a), p.parts))

        return m
