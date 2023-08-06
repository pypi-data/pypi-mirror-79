"""
Logging CLI
"""
import click
from ocrd_utils import initLogging, getLogger, getLevelName

initLogging()

class LogCtx():

    def __init__(self, name):
        self.logger = getLogger(name)

    def log(self, lvl, *args, **kwargs):
        self.logger.log(getLevelName(lvl), *args, **kwargs)

pass_log = click.make_pass_decorator(LogCtx)

@click.group("log")
@click.option('-n', '--name', envvar='OCRD_TOOL_NAME', default='', metavar='LOGGER_NAME', help='Name of the logger', show_default=True)
@click.pass_context
def log_cli(ctx, name, *args, **kwargs):
    """
    Logging
    """
    ctx.obj = LogCtx(name)

def _bind_log_command(lvl):
    @click.argument('msgs', nargs=-1)
    @pass_log
    def _log_wrapper(ctx, msgs):
        if not msgs:
            ctx.log(lvl.upper(), '')
        else:
            msg = list(msgs) if '%s' in msgs[0] else ' '.join([x.replace('%', '%%') for x in msgs])
            ctx.log(lvl.upper(), msg)
    return _log_wrapper

for lvl in ['trace', 'debug', 'info', 'warning', 'error', 'critical']:
    log_cli.command(lvl, help="Log a %s message" % lvl.upper())(_bind_log_command(lvl))
