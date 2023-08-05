'''
Author: Aaron Levi (aaronlyy)
Description: levish lets you create your own shell with custom commands.
Version: 0.1.1
'''

import os

class Shell:
    '''
    Create new Shell object
    '''
    def __init__(self, name, show_cwd=False, prefix="[>] "):
        self._name = name
        self._show_cwd = show_cwd
        self._prefix = prefix
        self._commands = {}
        self._help = "COMMAND: DESCRIPTION"

    # --- main loop function ---
    def _loop(self):
        '''
        main loop waiting for input angel du geile sau
        '''
        while True:
            if self._show_cwd:
                inp = input(f"{os.getcwd()} {self._prefix}")
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
                    self._msg_not_found(cmd)
                print("")
            else:
                # continue loop if inp == 0
                continue
    # -------------------------

    # --- add function to object ---
    def add_command(self, cmd, function, description=""):
        '''
        Add a new command to the shell.\n
        Args:
            cmd (str): the commands
            function (function): the function that is executed on command call
            description (str) [opt]: command description 
        '''
        # TODO check if function takes args
        # check if function does not already exist
        if not cmd in self._commands:
            self._commands[cmd] = {"func": function, "desc": description}
        else:
            raise CommandAlreadyExistError(cmd)
    # ------------------------------

    # --- build help function ---
    def _build_help(self):
        for cmd in self._commands:
            self._help += f"\n{cmd}: {self._commands[cmd]['desc']}"
    # ---------------------------

    # --- internal commands ---
    def _cmd_help(self, args):
        print(self._help)

    def _cmd_cls(self, args):
        os.system("cls")
    
    def _cmd_clear(self, args):
        os.system("clear")
    # ------------------------------
    

    # --- internal error messages ---
    def _msg_not_found(self, cmd):
        '''
        print command not found error
        '''
        print(f"Command '{cmd}' does not exist. Try '.help'")
    # ---------------------
                

    # --- run function ---
    def run(self):
        '''
        Start the shell
        '''
        # adding internal commands
        self.add_command("help", self._cmd_help, "shows help")
        self.add_command("cls", self._cmd_cls, "clears the screen (windows)")
        self.add_command("clear", self._cmd_clear, "clears the screen (unix)")
        # create help string
        self._build_help()
        # start main loop
        self._loop()
    # ------------------

# --- exception classes ---
class CommandAlreadyExistError(Exception):
    def __init__(self, cmd):
        self.message = f"'{cmd}': This command already exists."

    def __str__(self):
        return self.message
# ------------------------


if __name__ == "__main__":
    sh = Shell("hi", True,)
    sh.run()