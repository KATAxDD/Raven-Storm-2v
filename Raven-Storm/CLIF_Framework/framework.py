"""
Raven-Storm/modules/scanner/main.py
The Raven-Storm Toolkit - Scanner Module
Programmed and developed by Taguar258
Published under the MIT License
Based on the CLIF-Framework by Taguar258
"""

import socket
from os import system
from time import sleep, time

import requests
import urllib3
from CLIF_Framework.framework import event as clif_event
from CLIF_Framework.framework import tools as clif_tools

try:
    import nmap
except ImportError:
    print("Please install the nmap module.")
    quit()

clif_event = clif_event()
clif_tools = clif_tools()

class Main:
    def __init__(self, console):
        """
        Initialize the Scanner module for Raven-Storm.
        """
        global var
        var = console

        self._add_commands()

        # Colors
        var.C_None = "\x1b[0;39m"
        var.C_Bold = "\x1b[1;39m"
        var.C_Green = "\x1b[32m"
        var.C_Violet = "\x1b[34m"
        var.C_Dark_Blue = "\x1b[35m"
        var.C_Red = "\x1b[31m"

        var.nm = None
        var.nmapinstalled = False

    def _add_commands(self):
        """
        Add commands to the event handler.
        """
        clif_event.commands(self.exit_console, ["exit", "quit", "e", "q"])
        clif_event.command(self.help)

        clif_event.commands(self.run_shell, ".")
        clif_event.commands(self.debug, "$")

        clif_event.help_comment("|\n|-- Port scanning:")
        clif_event.help("ports ip", "Get port of IP (get port i).")
        clif_event.help("ports web", "Get port of web (get port w).")
        clif_event.help_comment("|\n|-- Network scanning:")
        clif_event.help("lan scan", "Get all Ips of Wifi.")
        clif_event.help_comment("|\n|-- Domain scanning:")
        clif_event.help("domain ip", "Get the IP by host.")
        clif_event.help_comment("|\n|-- Speed testing:")
        clif_event.help("speed down", "Return the time it needs to open a website.")
        clif_event.help("speed ping", "Return the time it needs to ping an IP.")

    def banner(self):
        """
        Display the banner for the Scanner module.
        """
        system("clear || cls")
        banner_text = """
C_B----------------------------------------------------------C_W
THE CREATOR DOES NOT TAKE ANY RESPONSIBILITY FOR DAMAGE CAUSED.
THE USER ALONE IS RESPONSIBLE, BE IT: ABUSING RAVEN-STORM
TO FIT ILLEGAL PURPOSES OR ACCIDENTAL DAMAGE CAUSED BY RAVEN-STORM.
BY USING THIS SOFTWARE, YOU MUST AGREE TO TAKE FULL RESPONSIBILITY
FOR ANY DAMAGE CAUSED BY RAVEN-STORM.
EVERY ATTACK WILL CAUSE TEMPORARY DAMAGE, BUT LONG-TERM DAMAGE IS
DEFFINITIFLY POSSIBLE.
RAVEN-STORM SHOULD NOT SUGGEST PEOPLE TO PERFORM ILLEGAL ACTIVITIES.
C_B----------------------------------------------------------C_W""".replace("C_W", var.C_None).replace("C_B", var.C_Bold)
        print(banner_text)
        self.help()

    def exit_console(self):
        """
        Exit the console.
        """
        print("\033[1;32;0mHave a nice day.")
        quit()

    def run_shell(self, command):
        """
        Run a shell command.
        """
        print("")
        system(clif_tools.arg("Enter shell command: \033[1;32;0m", ". ", command))
        print("")

    def debug(self, command):
        """
        Execute a debug command.
        """
        print("")
        eval(clif_tools.arg("Enter debug command: \033[1;32;0m", "$ ", command))
        print("")

    @clif_event.command
    def clear():
        """
        Clear the console screen.
        """
        system("clear || cls")

    @clif_event.event
    def on_ready():
        """
        Event triggered when the scanner module is ready.
        """
        try:
            var.nm = nmap.PortScanner()
            var.nmapinstalled = True
        except Exception as e:
            system("clear || cls")
            print("Please install the nmap package.")
            print("Some functions will not work without it.")
            print(e)
            try:
                input("[Press enter to continue without nmap]")
            except Exception:
                quit()
        Main(var).banner()

    @clif_event.event
    def on_command_not_found(command):
        """
        Event triggered when a command is not found.
        """
        print("")
        print("The command you entered does not exist.")
        print("")

    def check_session(self):
        """
        Check the session for commands to execute.
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

    @clif_event.event
    def on_input():
        """
        Event triggered when input is received.
        """
        Main(var).check_session()
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

    @clif_event.event
    def on_interrupt():
        """
        Event triggered on interrupt.
        """
        print("")
        var.stop()

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

    def help(self):
        """
        Display help messages.
        """
        clif_event.help_title("\x1b[1;39mScanner Help:\x1b[0;39m")
        clif_tools.help("|   |-- ", " :: ", clif_event)
        print("\033[1;32;0m")

    def portscan(self, ip):
        """
        Perform a port scan on the specified IP address.
        """
        try:
            for p in range(1, 1500):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                res = sock.connect_ex((ip, p))
                if res == 0:
                    print("Port: %s" % str(p))
                sock.close()
        except Exception as e:
            print("There was an error while executing.", e)

    def lanscan(self):
        """
        Perform a local network scan.
        """
        try:
            gateways = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            gateways.connect(("8.8.8.8", 80))
            gateway = ".".join((gateways.getsockname()[0].split("."))[:len(gateways.getsockname()[0].split(".")) - 1])
            gateways.close()
            var.nm.scan(hosts=("%s.0/24" % gateway), arguments="-sP")
            lanscandev = [(x, var.nm[x]['status']['state'], var.nm[x]["hostnames"][0]["name"], var.nm[x]["hostnames"][0]["type"]) for x in var.nm.all_hosts()]
            print("Gateway: %s.0" % gateway)
            for lanscandevice in lanscandev:
                print("%s  %s  %s  %s" % (lanscandevice[0], lanscandevice[1], lanscandevice[2], lanscandevice[3]))
        except Exception as e:
            print("There was an error while executing.", e)

    def hbi(self, ip):
        """
        Get the IP address by host name.
        """
        return socket.gethostbyname(ip)

    def speedtest(self, url):
        """
        Perform speed test for download.
        """
        try:
            if "http" not in url or "://" not in url:
                url = ("https://%s" % url)
            print("Testing download speed...")
            start = time()
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = response.data  # noqa: F841
            end = time()
            result = (end - start)
            return result
        except Exception as e:
            print("There was an error while executing.", e)

    def speedping(self, ip):
        """
        Perform speed test for ping.
        """
        try:
            print("Testing ping speed... (May require sudo)")
            start = time()
            system("ping -c 1 %s > /dev/null" % ip)
            end = time()
            result = (end - start)
            return result
        except Exception as e:
            print("There was an error while executing.", e)

    @clif_event.command
    def domain_ip(command):
        """
        Command to get IP from domain.
        """
        print("")
        try:
            domain = clif_tools.arg("Domain: ", "domain ip ", command).replace("https://", "").replace("http://", "")
            print(Main(var).hbi(domain))
        except Exception as e:
            print("There was an error while executing.", e)
        print("")

    @clif_event.command
    def lan_scan(command):
        """
        Command to perform LAN scan.
        """
        print("")
        if var.nmapinstalled:
            Main(var).lanscan()
        else:
            print("Please install nmap.")
        print("")

    @clif_event.command
    def ports_ip(command):
        """
        Command to perform port scan on IP.
        """
        print("")
        try:
            ip = clif_tools.arg("IP: ", "ports ip ", command)
            Main(var).portscan(ip)
        except Exception as e:
            print("There was an error while executing.", e)
        print("")

    @clif_event.command
    def ports_web(command):
        """
        Command to perform port scan on a website.
        """
        print("")
        try:
            website = clif_tools.arg("Website: ", "ports web ", command)
            ip_address = socket.gethostbyname(website.replace("https://", "").replace("http://", ""))
            Main(var).portscan(ip_address)
        except Exception as e:
            print("There was an error while executing.", e)
        print("")

    @clif_event.command
    def speed_down(command):
        """
        Command to perform speed test for download.
        """
        print("")
        url = clif_tools.arg("Website: ", "speed down ", command)
        result = Main(var).speedtest(url)
        print("Result: %s seconds" % result)
        print("")

    @clif_event.command
    def speed_ping(command):
        """
        Command to perform speed test for ping.
        """
        print("")
        ip = clif_tools.arg("IP: ", "speed ping ", command)
        result = Main(var).speedping(ip)
        print("Result: %s seconds" % result)
        print("")

def setup(console):
    """
    Setup the Scanner module for Raven-Storm.
    """
    console.ps1 = "\033[1;32;0mScanner> "
    console.add(Main(console), clif_event)
