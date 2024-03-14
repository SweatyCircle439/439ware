import cmd2
import tkinter as tk
import git
import os
import requests

installedAntiware = False

if os.path.exists("antiware.py"):
    installedAntiware = True

def download_file_from_github(file_url, local_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        return False

class Console(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        global installedAntiware
        if installedAntiware:
            print("antiware has already been installed")
    def do_quit(self, args):
        """Quit the console."""
        os._exit(0)

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_q(self, args):
        """Alias for 'quit' command."""
        return self.do_quit(args)
    
    def do_version(self, args):
        try:
            with open("antiware.py", 'rb') as file:
                content = file.read()
                print("-------------\nantiware\n-------------\n" + content.split('\n'.encode('utf-8'))[0].split('#'.encode('utf-8'))[1] + "\n-------------\n")
        except:
            with open("antiware.py", 'rb') as file:
                content = file.read()
                content = str(content)
                start = content.find("<version>")
                end = content.find("</version>")
                print("-------------\nantiware\n-------------\n" + str(content) + "\n-------------\n")

    def do_update(self, args):
        if args == "console":
            self.stdout.write(f"\033[92m{args} has been updated\033[0m\n")
            file_url = 'https://raw.githubusercontent.com/SweatyCircle439/439ware/main/RES/console.py'
            local_path = 'console.py'

            response = download_file_from_github(file_url, local_path)

            if response:
                self.stdout.write(f"\033[92msuccessfully updated {args}\033[0m\n")
                print(f"{os.getcwd()}/console.py has been updated")
            else:
                self.stdout.write(f"\033[91mfailed to update {args}\033[0m\n")

    def do_ware(self, args):
        """run ware / obtain ware resources"""
        if (args):
            args = args.split(" ")
        if len(args) >= 1:
            if (args[0] == "antiware"):
                if (len(args) >= 2):
                    global installedAntiware
                    if (args[1] == "install"):
                        self.stdout.write(f"\033[92m installing antiware \n")
                        file_url = 'https://raw.githubusercontent.com/SweatyCircle439/439ware/main/RES/antiware.py'

                        local_path = 'antiware.py'

                        response = download_file_from_github(file_url, local_path)

                        if (response):
                            self.stdout.write(f"\033[92m\\succesfully installed antiware\033\n")
                            installedAntiware = True
                        else:
                            self.stdout.write(f"\033[91m\\failed to install antiware\033\n")
                    elif (args[1] == "uninstall" and installedAntiware):
                        self.stdout.write(f"\033[92\\uninstalling antiware\033\n")
                        os.remove("antiware.py")
                        installedAntiware = False
                    elif (args[1] == "run" and installedAntiware):
                        self.do_antiware(" ".join(args[2:]))
                    else:
                        if (installedAntiware):
                            self.stdout.write(f"\033[91mERR, invalid input for argument ware.antiware.action\033\n \possible values \n INSTALL UNINSTALL RUN \ngot {args[1]}\n")
                        else:
                            self.stdout.write(f"\033[91mERR, invalid input for argument ware.antiware.action\033\n \possible values \n INSTALL \ngot {args[1]}\n")
                else:
                    if (installedAntiware):
                        self.do_antiware("")
                    else:
                        self.stdout.write(f"\033[91mERR, invalid amount of arguments\033\n \\at least 2 arguments were expected, got {len(args)}\n")
            else:
                self.stdout.write(f"\033[91mERR, invalid input for argument ware.type\033\n \possible values \n ANTIWARE \ngot {args[0]}\n")
        else: 
            self.stdout.write(f"\033[91mERR, invalid amount of arguments\033\n \\at least 1 argument was expected, got {len(args)}\n")
        pass

    def do_antiware(self, args):
        """run antiware"""
        global installedAntiware
        if installedAntiware: 
            if (args.split(" ")[len(args.split(" ")) - 2] == "-key"):
                args = args + "\\n" + input("")
            with open(f"antiware.py", 'rb') as script_file:
                script_code = script_file.read()
            exec(script_code, {'args': args.split(" ")})
        else:
            self.stdout.write(f"\033[91mERR, antiware not installed\033\n")
        pass

    def do_edit(self, args):
        pass

    def do_run_script(self, args):
        pass

    def do_run_pyscript(self, args):
        pass

    def do_shell(self, args):
        pass

if __name__ == "__main__":
    console = Console()
    console.cmdloop()
