import sys, string
#  Main program if called by itself

def chkIndent(line):
        ct = 0
        for ch in line:
                if ch != " ": return ct
                ct += 1
        return ct
                

def delComment(line):
        pos = line.find("#")
        if pos > -1:
                line = line[0:pos]
                line = line.rstrip()
        return line

def mklines(filename):
        inn = open(filename, "r")
        lines = [ ]
        pos = [0]
        ct = 0
        for line in inn:
                ct += 1
                line = line.rstrip( )+";"
                line = delComment(line)
                if len(line) == 0 or line == ";": continue
                indent = chkIndent(line)
                line = line.lstrip( )
                if indent > pos[-1]:
                        pos.append(indent)
                        line = '@' + line
                elif indent < pos[-1]:
                        while indent < pos[-1]:
                                del(pos[-1])
                                line = '$' + line
                print ct, "\t", line
                lines.append(line)
        return lines

def main():
        """main program for testing"""
        if len(sys.argv) < 2:
                print "Usage:  %s filename" % sys.argv[0]
                return
        mklines(sys.argv[1])
        #lines = inn.readlines()
        #parse(string.join(lines, ";"))
        # print str(ast)
        return

if __name__ == '__main__':
    main()
