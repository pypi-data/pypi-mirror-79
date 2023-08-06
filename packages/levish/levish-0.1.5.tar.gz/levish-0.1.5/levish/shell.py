'''
Author: Aaron Levi (aaronlyy)
Description: levish lets you create your own shell with custom commands.
Version: 0.1.1
'''

import os
from inspect import getfullargspec

from pyfiglet import figlet_format


# TODO add system command functionality

class Shell:
    '''
    Create new Shell object
    '''
    def __init__(self, name, show_cwd=False, prefix="[>] ", figlet=False, figlet_font="standard"):
        self._name = name
        self._show_cwd = show_cwd
        self._prefix = prefix
        self._commands = {}
        self._help = ""
        self._figlet = figlet
        self._figlet_font = figlet_font
        self._looping = True

    # --- main loop function ---
    def _loop(self):
        '''
        main loop waiting for input angel du geile sau
        '''
        while self._looping:
            if self._show_cwd:
                inp = input(f"{self._name}@{os.getcwd()} {self._prefix}")
            else:
                inp = input(self._prefix)

            # test if input is longer than 0 else continue loop
            if (len(inp)) > 0:
                # split input into cmd (first words) and args (every other word as list)
                # keep in mind that the input function always returns a string, so the args also will be strings
                # use int() to convert them into an integer
                cmd, args = inp.split()[0], inp.split()[1:]
                # test if cmd is in commands dict
                if cmd in self._commands:
                    # execute function with given args
                    self._commands[cmd]["func"](args)
                else:
                    # print not found error
                    print(f"Command '{cmd}' does not exist. Try 'help'")
                print("")
            else:
                # continue loop if inp == 0
                continue
    # -------------------------

    # --- add function to object ---
    def add_command(self, cmd, function, description="no description"):
        '''
        Add a new command to the shell.\n
        Args:
            cmd (str): the commands
            function (function): the function that is executed on command call
            description (str) [opt]: command description 
        '''
        # check for naming
        # check if passed in function is really a function
        if callable(function):
            # check if function takes 1 argument called args
            if "args" in getfullargspec(function).args:
                # check if function does not already exist
                if not cmd in self._commands:
                    self._commands[cmd] = {"func": function, "desc": description}
                else:
                    raise CommandAlreadyExistError(cmd)
            else:
                raise MissingArgsInFunctionError(cmd)
        else:
            # raise function not callable error
            raise FunctionNotCallableError(cmd)
    # ------------------------------

    # --- break loop ---
    def _break_loop(self):
        '''
        break out of main loop
        '''
        self._looping = False
    # --------------------

    # --- build help function ---
    def _build_help(self):
        self._help = "------------------------\nCOMMAND: DESCRIPTION"
        for cmd in self._commands:
            self._help += f"\n{cmd}: {self._commands[cmd]['desc']}"
        self._help += "\n------------------------"
    # ---------------------------

    # --- internal commands ---
    def _cmd_help(self, args):
        if len(args) > 0:
            if args[0] in self._commands:
                print(self._commands[args[0]]["desc"])
            else:
                print(f"Command '{args[0]}' not found")
        else:
            print(self._help)


    def _cmd_cls(self, args):
        os.system("cls")
    
    def _cmd_clear(self, args):
        os.system("clear")

    def _cmd_exit(self, args):
        self._break_loop()
    

    def enable_basic_commands(self):
        '''
        This adds basic commands like 'cls/clear' & 'exit' to the shell
        '''
        self.add_command("cls", self._cmd_cls, "Clears the screen (windows)")
        self.add_command("clear", self._cmd_clear, "Clears the screen (unix)")
        self.add_command("exit", self._cmd_exit, "Exit the shell")
    # ------------------------------

    
    # --- run function ---
    def run(self):
        '''
        Start the shell
        '''
        self.add_command("help", self._cmd_help, "Shows help")
        # create help string
        self._build_help()
        # splash
        if self._figlet:
            print(figlet_format(self._name, self._figlet_font))
        # start main loop
        self._loop()
    # ------------------

# --- exception classes ---
class CommandAlreadyExistError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': This command already exists."

    def __str__(self):
        return self.message

class MissingArgsInFunctionError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': Function must take 1 argument called args."

    def __str__(self):
        return self.message

class FunctionNotCallableError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': The passed in function is not a callable object."

    def __str__(self):
        return self.message
# ------------------------


if __name__ == "__main__":

    def test(args):
        print("test function")
    
    sh = Shell("levish", show_cwd=True, figlet=True, figlet_font="slant")
    sh.enable_basic_commands()
    sh.add_command("test", test)
    sh.run()