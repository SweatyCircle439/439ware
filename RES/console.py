import cmd2
import tkinter as tk

class Console(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.intro = "Welcome to the Python Console. Type 'quit' to exit."
        self.tk_root = tk.Tk()
        self.tk_root.title("Python Console")
        self.tk_root.geometry("800x600")
        self.text_area = tk.Text(self.tk_root)
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def do_quit(self, args):
        """Quit the console."""
        self.tk_root.quit()
        return True

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
