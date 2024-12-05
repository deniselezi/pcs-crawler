import sys

class CLI:
    def __init__(self):
        pass

    def _check_type(self,expected_type, args):
        return all(isinstance(item, expected_type) for item in args)
    
    def command_failed(self,msg):
        print(f"CmdError: {msg}")
        print("COMMAND: python3 pcs-crawler.py LINK [MAX_REPOS]")
        sys.exit(1)
    
    def get_args(self,args):
        self.args = args
        args.pop(0)  # remove filename
        n_args = len(args)

        if not self._check_type(str, args):
            return self.command_failed("Arguments aren't all strings.")

        if not 1 <= n_args <= 2:
            return self.command_failed("Invalid number of args, please follow the correct format")

        if not args[0].startswith("https://github.com/"):
            return self.command_failed("First arg is not a valid GitHub URL")

        if n_args == 2 and not args[1].isdigit():
            return self.command_failed("Incorrect command usage, argument 2 is not an integer")

        return args        
