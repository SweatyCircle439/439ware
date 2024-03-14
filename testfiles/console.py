import cmd2
import tkinter as tk
import git
import os
import requests

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

    def do_quit(self, args):
        """Quit the console."""
        os._exit(0)

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_q(self, args):
        """Alias for 'quit' command."""
        return self.do_quit(args)
    
    def do_ware(self, args):
        """run ware / obtain ware resources"""
        if (args):
            args = args.split(" ")
        if len(args) >= 1:
            if (args[0] == "antiware"):
                if (len(args) >= 2):
                    if (args[1] == "install"):
                        self.stdout.write(f"\033[92m installing antiware \n")
                        # URL of the raw file on GitHub
                        file_url = 'https://raw.githubusercontent.com/SweatyCircle439/439ware/main/RES/antiware.py'

                        # Local path where you want to save the file
                        local_path = 'antiware.py'

                        # Call the function to download the file
                        response = download_file_from_github(file_url, local_path)

                        if (response):
                            self.stdout.write(f"\033[92succesfully installed antiware\033\n")
                        else:
                            self.stdout.write(f"\033[91mfailed to install antiware\033\n")
                    else:
                        self.stdout.write(f"\033[91mERR, invalid input for argument ware.antiware.action\033\n \possible values \n INSTALL \ngot {args[0]}\n")
                else:
                    self.stdout.write(f"\033[91mERR, invalid amount of arguments\033\n \\at least 2 arguments were expected, got {len(args)}\n")
            else:
                self.stdout.write(f"\033[91mERR, invalid input for argument ware.type\033\n \possible values \n ANTIWARE \ngot {args[0]}\n")
        else: 
            self.stdout.write(f"\033[91mERR, invalid amount of arguments\033\n \\at least 1 argument was expected, got {len(args)}\n")
        pass

    def do_antiware(self, args):
        """run antiware"""
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