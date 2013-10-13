import bdb
import sys
import time

MAX_LINES = 10000 # maximum lines run across all files

# Credit to Online Python Tutor for these bans
# blacklist of builtins
BANNED_BUILTINS = ['reload', 'open',
                   'file', 'eval', 'exec', 'execfile',
                   'exit', 'quit', 'help',
                   'raw_input', 'input']

class BranchFinder(bdb.Bdb):
    def __init__(self):
        bdb.Bdb.__init__(self)
        self.branches = []
        self.prevline = None
        self.lines_left = MAX_LINES
        self.lines_in_file = 0
        self.run_info = dict()

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        self.lines_left -= 1
        if self.lines_left <= 0:
            self.set_quit()
            self.run_info['early_stop'] = True
        # This is so awful but it works
        # Only care about lines in the string executed
        if "<string>" not in str(frame.f_code):
            return
        self.lines_in_file += 1
        if self.prevline and frame.f_lineno != self.prevline + 1:
            self.branches.append((self.prevline, frame.f_lineno))
        self.prevline = frame.f_lineno

    def runscript(self, script_str):
        self.set_step()
        for func in BANNED_BUILTINS:
            if func + '(' in script_str:
                return "Using %s() is not allowed." % func
        # Special case for exec
        if 'exec ' in script_str:
            return "Using exec is not allowed."
        try:
            start = time.time()
            self.run(script_str)
            run_time = time.time() - start
        except Exception, e: # catch all exceptions, and reraise them with more web-friendly message
            # Janky janky way to get exception name. Please don't break?
            name = str(type(e)).split("'")[1]
            name = name.split(".")[-1]
            return "%s raised on line %d: %s" % (name, self.prevline or 0, e)
        self.run_info['lines'] = self.lines_in_file
        # Hacky solution to make things work fast
        self.run_info['run_time'] = run_time if 'early_stop' not in self.run_info else -1
        return self.branches, self.run_info

# Although this no longer runs arbitrary code, it is still partly sketchy
# (please don't break me :( )
def exec_script_str(script_str):
    runner = BranchFinder()
    return runner.runscript(script_str)

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print exec_script_str(f.read())
