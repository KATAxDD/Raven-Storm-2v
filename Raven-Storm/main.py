#!/usr/bin/env python3
"""
The Raven-Storm Toolkit
------------------------
Programmed and developed by Taguar258
Published under the MIT License
Based on the CLIF-Framework by Taguar258
"""

import sys
from CLIF_Framework.framework import console, module

def run():
    """
    Initialize and run the main console for Raven-Storm.
    """
    try:
        main_console = console()
        main_console.rsversion = "4.1 (Pre)"
        main_console.user_argv = sys.argv

        module("modules.main", main_console)

        main_console.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
