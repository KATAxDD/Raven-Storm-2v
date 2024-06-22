#!/usr/bin/env python3
"""
The Raven-Storm Toolkit
------------------------
Programmed and developed by Taguar258
Published under the MIT License
Based on the CLIF-Framework by Taguar258
"""

import os
import sys
import requests
from random import choice
from time import sleep
from CLIF_Framework.framework import console, event, module, tools

try:
    import readline  # noqa: F401
except ImportError:
    pass


class Main:
    def __init__(self, console_instance):
        """
        Initialize the main console for Raven-Storm.
        """
        global var
        global self
        self = self
        var = console_instance  # noqa: VNE002

        var.modules = {}
        self._add_commands()

        # Colors
        self._init_colors()

        # Session and server configuration
        var.session = [[False, ""], [False, []]]
        var.server = [False, True, "ip", "pass", 1]

        if len(var.user_argv) != 1:
            if var.user_argv[1] == "--connect":
                var.server = [True, False, var.user_argv[2], var.user_argv[3], 1]
                self._reset_server()

    def _init_colors(self):
        """
        Initialize color codes.
        """
        var.C_None = "\x1b[0;39m"
        var.C_Bold = "\x1b[1;39m"
        var.C_Green = "\x1b[32m"
        var.C_Violet = "\x1b[0;35m"
        var.C_Dark_Blue = "\x1b[34m"
        var.C_Red = "\x1b[31m"
        var.C_Yellow = "\x1b[33m"
        var.C_Cyan = "\x1b[36m"
        var.C_Magenta = "\x1b[1;35m"

    def _reset_server(self):
        """
        Reset the server status.
        """
        status = requests.post(f"{var.server[2]}reset", data={"password": var.server[3]}).text

    def banner(self):
        """
        Display the banner.
        """
        banner_fire_color = var.C_Cyan
        banner_middle_color = var.C_Violet
        banner_bottom_color = var.C_Dark_Blue
        banner_logo = (
            """C_Bo-----------------------------------------------------------C_W
C_FIRE (
 )\\ )                                 )                C_WC_Bov.""" + var.rsversion + """C_WC_FIRE
(()/(    )   )      (              ( /(      (       )
 /(_))( /(  /((    ))\\  (      (   )\\()) (   )(     (
(C_MID_C_FIRE))  )(_))(_))\\  /((_) )\\ )   )\\ (C_MID_C_FIRE))/  )\\ (()\\    )\\  'C_MID
| _ \\C_FIRE((C_MID_C_FIRE)C_MID_ _C_FIRE)((C_MID_C_FIRE)(C_MID_C_FIRE))  C_MID_C_FIRE(C_MID_C_FIRE/(  ((C_MID_C_FIRE)C_MID| |C_FIRE  ((C_MID_C_FIRE) ((C_MID_C_FIRE) C_MID_C_FIRE((C_MID_C_FIRE))C_MID
|   // _` |\\ V / / -_)| ' \\)) (_-<|  _|/ _ \\| '_|| '  \\C_FIRE()C_BOT
|_|_\\\\__,_| \\_/  \\___||_||_|  /__/ \\__|\\___/|_|  |_|_|_|C_W

C_BoStress-Testing-Toolkit by Taguar258 (c) | MIT 2020
Based on the CLIF Framework by Taguar258 (c) | MIT 2020C_W

BY USING THIS SOFTWARE, YOU MUST AGREE TO TAKE FULL RESPONSIBILITY
FOR ANY DAMAGE CAUSED BY RAVEN-STORM.
RAVEN-STORM SHOULD NOT SUGGEST PEOPLE TO PERFORM ILLEGAL ACTIVITIES.
C_Bo-----------------------------------------------------------C_W"""
        )
        banner_logo = banner_logo.replace("C_W", var.C_None)
        banner_logo = banner_logo.replace("C_Bo", var.C_Bold)
        banner_logo = banner_logo.replace("C_FIRE", banner_fire_color)
        banner_logo = banner_logo.replace("C_MID", banner_middle_color)
        banner_logo = banner_logo.replace("C_BOT", banner_bottom_color)
        print(banner_logo)

    @event.event
    def on_ready(self):
        """
        Event triggered when the console is ready.
        """
        os.system("clear || cls")
        self.banner()
        self.help()

    @event.event
    def on_command_not_found(self, command):
        """
        Event triggered when a command is not found.
        """
        print("\nThe command you entered does not exist.\n")

    def exit_console(self):
        """
        Exit the console.
        """
        print("Have a nice day.")
        quit()

    @event.event
    def on_command(self, command):
        """
        Event triggered when a command is executed.
        """
        if var.session[0][0]:
            var.session[0][1].write(command + "\n")
        if var.server[0] and var.server[1]:
            status = requests.post(f"{var.server[2]}set/com", data={"password": var.server[3], "data": command}).text
            if status != "200":
                print("\nAn error occurred while sending commands to the server.\n")

    def _add_commands(self):
        """
        Add commands to the event handler.
        """
        event.commands(self.exit_console, ["exit", "quit", "e", "q"])
        event.commands(self.run_shell, ".")
        event.commands(self.debug, "$")
        event.commands(self.help, "help")
        event.parser(self.run_debug_arg, "$")
        event.parser(self.run_shell_arg, ".")
        self._add_help_messages()

        var.modules["Layer4"] = console()
        var.modules["Layer3"] = console()
        var.modules["Layer7"] = console()
        var.modules["BL"] = console()
        var.modules["ARP"] = console()
        var.modules["Scanner"] = console()
        var.modules["Server"] = console()
        var.modules["WIFI"] = console()

    def _add_help_messages(self):
        """
        Add help messages for commands.
        """
        event.help(["exit", "quit", "e", "q"], "Exit Raven-Storm.")
        event.help("help", "View all commands.")
        event.help("upgrade", "Upgrade Raven-Storm.")
        event.help(".", "Run a shell command.")
        event.help("clear", "Clear the screen.")
        event.help("record", "Save this session.")
        event.help("load", "Redo a session using a session file.")
        event.help("ddos", "Connect to a Raven-Storm server.")
        event.help_comment("\nModules:")
        event.help("l4", "Load the layer4 module. (UDP/TCP)")
        event.help("l3", "Load the layer3 module. (ICMP)")
        event.help("l7", "Load the layer7 module. (HTTP)")
        event.help("bl", "Load the bluetooth module. (L2CAP)")
        event.help("arp", "Load the arp spoofing module. (ARP)")
        event.help("wifi", "Load the wifi module. (IEEE)")
        event.help("server", "Load the server module for DDos attacks.")
        event.help("scanner", "Load the scanner module.")

    def run_shell(self, command):
        """
        Run a shell command.
        """
        os.system(command)

    def check_session(self):
        """
        Check if there is a session to load commands from.
        """
        if var.session[1][0] and len(var.session[1][1]) >= 1:
            if len(var.session[1][1][0]) >= 1:
                run_following = [var.session[1][1][0][0], var.session[1][1][0][0]]
                var.session[1][1][0] = var.session[1][1][0][1:]
            else:
                var.session[1][1] = var.session[1][1][1:]
                run_following = [var.session[1][1][0][0], var.session[1][1][0][0]]
                var.session[1][1][0] = var.session[1][1][0][1:]
            var.run_command = run_following

    @event.event
    def on_input(self):
        """
        Event triggered when input is received.
        """
        self.check_session()
        if var.server[0] and not var.server[1]:
            while True:
                data = requests.post(f"{var.server[2]}get/com{var.server[4]}", data={"password": var.server[3]}).text
                if data != "500":
                    var.server[4] += 1
                    var.run_command = [data, data]
                sleep(2)

    def debug(self, command):
        """
        Run a debug command.
        """
        exec(command)

    def run_shell_arg(self, command):
        """
        Parse and run a shell command.
        """
        return [command[0], "." + command[1]]

    def run_debug_arg(self, command):
        """
        Parse and run a debug command.
        """
        return [command[0], "$" + command[1]]

    def help(self):
        """
        Display help messages.
        """
        print("\n")
        event.help_title("Raven-Storm")
        event.help_print()
        print("\n")

    def upgrade(self):
        """
        Upgrade Raven-Storm.
        """
        if var.tools.confirm("Upgrade?"):
            try:
                os.system("git clone https://github.com/Taguar258/Raven-Storm.git /tmp/Raven-Storm")
                os.system("sudo cp -r /tmp/Raven-Storm/* .")
                os.system("sudo rm -r /tmp/Raven-Storm")
                print("Raven-Storm successfully upgraded.")
            except Exception as e:
                print(f"An error occurred during upgrade: {e}")

    def clear(self):
        """
        Clear the console screen.
        """
        os.system("clear || cls")

    def record(self, file):
        """
        Record the session to a file.
        """
        if var.session[0][0]:
            if var.tools.confirm("End recording?"):
                var.session[0][0] = False
                var.session[0][1].close()
        else:
            var.session[0][0] = True
            var.session[0][1] = open(file, "a")

    def load(self, file):
        """
        Load a session from a file.
        """
        try:
            with open(file) as f:
                content = f.read().split("\n")
            var.session[1][0] = True
            var.session[1][1].append(content)
        except Exception as e:
            print(f"An error occurred while loading the session: {e}")

    def ddos(self, ip, passwd):
        """
        Connect to a Raven-Storm server.
        """
        var.server = [True, False, ip, passwd, 1]
        self._reset_server()

    def l4(self):
        """
        Load the Layer4 module.
        """
        var.modules["Layer4"].run("main")

    def l3(self):
        """
        Load the Layer3 module.
        """
        var.modules["Layer3"].run("main")

    def l7(self):
        """
        Load the Layer7 module.
        """
        var.modules["Layer7"].run("main")

    def bl(self):
        """
        Load the Bluetooth module.
        """
        var.modules["BL"].run("main")

    def arp(self):
        """
        Load the ARP spoofing module.
        """
        var.modules["ARP"].run("main")

    def wifi(self):
        """
        Load the WiFi module.
        """
        var.modules["WIFI"].run("main")

    def server(self):
        """
        Load the server module for DDoS attacks.
        """
        var.modules["Server"].run("main")

    def scanner(self):
        """
        Load the scanner module.
        """
        var.modules["Scanner"].run("main")
