import bdb
import sys

MAX_LINES = 10000 # maximum lines run across all files

class BranchFinder(bdb.Bdb):
    def __init__(self):
        bdb.Bdb.__init__(self)
        self.branches = []
        self.prevline = None
        self.lines_left = MAX_LINES

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        # This is so awful but it works
        # Only care about lines in the string executed
        self.lines_left -= 1
        if self.lines_left <= 0:
            self.set_quit()
        if "<string>" not in str(frame.f_code):
            return
        if self.prevline and frame.f_lineno != self.prevline + 1:
            self.branches.append((self.prevline, frame.f_lineno))
        self.prevline = frame.f_lineno

    def runscript(self, script_str):
        self.set_step()
        try:
            self.run(script_str)
        except Exception, e: # catch all exceptions, and reraise them with more web-friendly message
            # Janky janky way to get exception name. Please don't break?
            name = str(type(e)).split("'")[1]
            return "%s raised on line %d: %s" % (name, self.prevline, e)
        return self.branches

# runs arbitrary code!
# (please don't break me :( )
def exec_script_str(script_str):
    runner = BranchFinder()
    return runner.runscript(script_str)

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print exec_script_str(f.read())