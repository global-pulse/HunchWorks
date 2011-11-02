#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import sys
import time
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--reload", action="store_true", dest="use_reloader",
            help="Tells Django to use the auto-reloader."),

        make_option(
            "--interval", default=10, dest="interval", type="float",
            help="Specifies the how often to poll the agent."))

    help = "Starts the given agent."
    args = "[agent name]"

    # Model validation is called explicitly each time the agent is reloaded, so
    # it doesn't need to be performed on startup
    requires_model_validation = False


    def handle(self, agent_name=None, *args, **options):
        quit_command = (sys.platform == "win32") and "CTRL-BREAK" or "CONTROL-C"
        use_reloader = options.get("use_reloader", False)
        interval = options.get("interval")

        if not agent_name:
            raise CommandError("Enter an agent name.")

        def inner_run():
            from hunchworks.utils.agents import spawn_engine
            from django.conf import settings
            import django

            print "Validating models..."
            self.validate(display_num_errors=True)

            agent = spawn_engine(
              agent_name)

            print "\nDjango version %s, using settings %r" % (django.get_version(), settings.SETTINGS_MODULE)
            print "%s %r is polling every %d seconds." % (agent.__class__.__name__, agent_name, interval)
            print "Quit the server with %s.\n" % quit_command

            try:
                while True:
                    agent.poll()
                    time.sleep(interval)

            except KeyboardInterrupt, SystemExit:
                sys.exit(0)

        if use_reloader:
            from django.utils import autoreload
            autoreload.main(inner_run)

        else:
            inner_run()
