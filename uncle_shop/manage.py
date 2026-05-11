#!/usr/bin/env python  # use the system Python interpreter to execute this script
"""Django's command-line utility for administrative tasks."""  # describe the purpose of this management script
import os  # import operating system utilities for environment management
import sys  # import system utilities to access command-line arguments


def main():  # define the main entry point for command execution
    """Run administrative tasks."""  # document the main function
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncle_shop.settings')  # ensure Django knows which settings to use
    try:  # attempt to import Django's command execution helper
        from django.core.management import execute_from_command_line  # import the function that runs management commands
    except ImportError as exc:  # if Django is not installed or import fails
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc  # raise an informative error chained from the original ImportError
    execute_from_command_line(sys.argv)  # execute the management command using the script arguments


if __name__ == '__main__':  # only run the main function when this file is executed directly
    main()  # call the command entry point
