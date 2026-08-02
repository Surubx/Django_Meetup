#!/usr/bin/env python
"""Django "manage.py" entrypoint for administrative tasks.

This file is the CLI entry used during development to run the server,
create migrations, run tests, and other management commands.
"""
import os
import sys


if __name__ == "__main__":
    # Use SQLite-backed settings for local CLI runs unless explicitly overridden.
    if "test" in sys.argv and "DJANGO_SETTINGS_MODULE" not in os.environ:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meetup_site.settings_test")
    else:
        # Keep local commands on SQLite; production can override this env var.
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meetup_site.settings_sqlite")

    # Lazily import the management helper and hand off CLI args
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
