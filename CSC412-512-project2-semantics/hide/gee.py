import re, sys, string
astdebug = False

def typeError(msg):
    sys.exit(msg)
    

#  Expression class and its subclasses
class Expression( object ):
        def __str__(self):
                return ""
            
        #def value(self, state):
        #    return IntValue(0)
        
class BinaryExpr( Expression ):
        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right
                
        def value(self, state):
            left = self.left.value(state)
            right = self.right.value(state)
            if self.op == "+":
                return left + right
            if self.op == "-":
                return left - right
            if self.op == "*":
                return left * right
            if self.op == "/":
                return left / right
        
        def __str__(self):
            return str(self.op) + " " + str(self.left) + " " + str(self.right)

class Number( Expression ):
        def __init__(self, val):
                self.val = int(val)
                
        def value(self, state):
            return self.val
        
        def __str__(self):
                return str(self.val)

class Boolean( Expression ):
        def __init__(self, val):
                self.val = val
                
        def value(self, state):
            return self.val

        def __str__(self):
                return str(self.val)

class String( Expression ):
        def __init__(self, val):
                self.val = val
                
        def value(self, state):
            return self.val
                
        def __str__(self):
                return str(self.val)
        
class VariableRef( Expression ):
        def __init__(self, ident):
                # global dict
                self.name = ident
                
        def value(self, state):
            return state.value(self.name)
                
        def __str__(self):
                return self.name

#  Statement class and its subclasses
class Statement( object ):
        def __str__(self):
                return ""
            
        #def meaning(self, state):
        #    return state
        
class Assign( Statement ):
        def __init__(self, var, expr):
            self.var = str(var)
            self.expr = expr
                
        def __str__( self ):
                return "= " + self.var + " " + str(self.expr)

        def meaning(self, state):
                state[self.var] = self.expr.value(state)
                return state
        
class Block( Statement ):
        def __init__(self, stmts):
                self.stmts = stmts
                
        def meaning(self, state):
            if astdebug: print "Block: ", str(state)
            for s in self.stmts:
                state = s.meaning(state)
            return state

        def __str__(self):
            r = ""
            for s in self.stmts:
                r += str(s) +'\n'
            return r

class WhileStmt( Statement ):
        def __init__(self, expr, block):
            self.expr = expr
            self.body = block
                
        def __str__(self):
            return "while " + str(self.expr) + "\n" + str(self.body) + "endwhile\n"

        def meaning(self, state):
                while self.expr.value(state):
                        state = self.body.meaning(state)
                return state

class IfStmt( Statement ):
        def __init__(self, expr, block, elseblock):
            self.expr = expr
            self.then = block
            self.elseblock = elseblock
                
        def __str__(self):
            return "if " + str(self.expr) + "\n" + str(self.then) + "\n" + str(self.elseblock) + "endif\n"

        def meaning(self, state):
                if self.expr.value(state):
                        state = self.then.meaning(state)
                else:
                        state = self.elseblock.meaning(state)

class Call( Statement ):
        def __init__(self, name, list):
            self.name = name
            self.exprlist = list
                
        def __str__(self):
            return "call " + self.name + list2str(self.exprlist)

class Break( Statement ):
        def __init__(self, kind):
            self.kind = kind
                
        def __str__( self ):
            return self.kind
        
class Print( Statement ):
        def __init__(self, list):
            self.list = list
                
        def __str__(self):
            return "print " + list2str(self.list)
        
class ReturnStmt( Statement ):
        def __init__(self, list):
            self.list = list
                
        def __str__(self):
            return "return " + list2str(self.list)
        
class DefStmt( Statement ):
        def __init__(self, name, args, block):
            self.name = name
            self.args = args
            self.body = block
                
        def __str__(self):
            return "Def " + str(self.name) + list2str(self.args) + "\n" + str(self.body) + "enddef\n"


debug = False

# aux routine

def list2str(list):
	r = "( "
	sep = ''
	for i in list:
		r += sep + str(i)
		sep = ", "
	return r + " )"


def error( msg ):
	#print msg
	sys.exit(msg)

def match(matchtok, tokens):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+matchtok)
	return tokens.next( )

def matchre(pat, tokens):
	tok = tokens.peek( )
	if not re.match(pat, tok): error("Not expecting "+tok)
	return tokens.next( )

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.

def parseFactor(tokens):
	""" factor -> '(' expr ')' | ident | number | string """
	"""            | 'True' | 'False' """
	tok = tokens.peek( )
	# if debug: print "Factor: ", tok
	if tok == "True" or tok == "False":
		savval = tok == "True"
		tokens.next( )
		return Boolean(savval)
	if re.match(Lexer.number, tok):
		tokens.next( )
		return Number(tok)
	if re.match(Lexer.string, tok):
		tokens.next( )
		return String(tok)
	if re.match(Lexer.identifier, tok):
		tokens.next( )
		return VariableRef(tok)
	if tok == "(":
		tokens.next( )
		expr = parseExpr(tokens)
		tok = tokens.peek( )
		if tok != ")":
			error("Missing )");
		tokens.next( )
		return expr
	error("Invalid operand")
	return None

def parseTerm(tokens):
	""" term -> factor { ('*' | '/') factor } """
	tok = tokens.peek( )
	# if debug: print "Term: ", tok
	left = parseFactor(tokens)
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		savetok = tok
		tokens.next()
		right = parseFactor(tokens)
		left = BinaryExpr(savetok, left, right)
		tok = tokens.peek( )
	return left

def parseAddExpr(tokens):
	""" addExpr    = term { ('+' | '-') term } """
	tok = tokens.peek( )
	if debug: print "Expr: ", tok
	left = parseTerm(tokens)
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		savetok = tok
		tokens.next()
		right = parseTerm(tokens)
		left = BinaryExpr(savetok, left, right)
		tok = tokens.peek( )
	return left

def relExpr(tokens):
	""" relExpr    = addExpr { ('+' | '-') addExpr } """
	tok = tokens.peek( )
	if debug: print "Expr: ", tok
	left = parseAddExpr(tokens)
	tok = tokens.peek( )
	if tok == "<" or tok == "<=" or tok == ">" or tok == ">=" or tok == "==" or tok == "!=":
		savetok = tok
		tokens.next()
		right = parseAddExpr(tokens)
		left = BinaryExpr(savetok, left, right)
		tok = tokens.peek( )
	return left

def andExpr(tokens):
	""" andExpr    = relExpr { 'and' relExpr } """
	tok = tokens.peek( )
	if debug: print "Expr: ", tok
	left = relExpr(tokens)
	tok = tokens.peek( )
	while tok == "and":
		savetok = tok
		tokens.next()
		right = relExpr(tokens)
		left = BinaryExpr(savetok, left, right)
		tok = tokens.peek( )
	return left

def parseExpr(tokens):
	""" Expr    = andExpr { 'or' andExpr } """
	tok = tokens.peek( )
	if debug: print "Expr: ", tok
	left = andExpr(tokens)
	tok = tokens.peek( )
	while tok == "or":
		savetok = tok
		tokens.next()
		right = andExpr(tokens)
		left = BinaryExpr(savetok, left, right)
		tok = tokens.peek( )
	return left

def exprList(tokens):
	""" exprList = expr { ',' expr } """
	list = [ ]
	exp = parseExpr(tokens)
	list.append(exp)
	while tokens.peek( ) == ",":
		tokens.next( )
		exp = parseExpr(tokens)
		list.append(exp)
	return list
	
def identList(tokens):
	""" identList = [ ident { ',' ident } ] """
	list = [ ]
	id = tokens.peek()
	list.append(id)
	tok = matchre(Lexer.identifier, tokens)
	while tok == ",":
		id = tokens.next( )
		list.append(id)
		tok = matchre(Lexer.identifier, tokens)
	return list
	
def parseAssign(tokens):
	""" assignOrCall -> ident '=' expr """
	var = tokens.peek( )
	tokens.next( )
	if tokens.peek() == "=":
		match("=", tokens)
		expr = parseExpr(tokens)
		match(";", tokens)
		return Assign(var, expr)
	if tokens.peek() == "(":
		tok = match("(", tokens)
		exprlist = [ ]
		while tokens.peek( ) != ")":
			expr = parseExpr(tokens)
			exprlist.append(expr)
			if tokens.peek() == ",":
				tokens.next( )
		if debug: print "call: " + tokens.peek( )
		tokens.next( )
		match(";", tokens)
		return Call(var, exprlist)
	error("Invalid assignment or function call")
	return None
	
def parseBlock(tokens):
	tok = match("@", tokens)
	stmts = [ ]
	while tok != "~":
		if debug: print "BlocK: "+str(tok)
		stmts.append(parseStmt(tokens))
		if debug: print "Block stmt: " + tokens.peek( )
		tok = tokens.peek( ) # match(";", tokens)
	tokens.next( )
	if debug and tokens.peek() != None: print "End block: " + tokens.peek()
	return Block(stmts)

def parseWhile(tokens):
	""" whileStmt = 'while' expression ':' eoln block """
	tokens.next( )
	expr = parseExpr(tokens)
	match(":", tokens)
	match(";", tokens)
	stmts = parseBlock(tokens)
	return WhileStmt(expr, stmts)

def parseIf(tokens):
	""" ifStmt = 'if' expression ':' eoln block
	        { 'elseif' expression ':' eoln block }
		[ else ':' eoln block ]  """
	tokens.next( )
	expr = parseExpr(tokens)
	match(":", tokens)
	match(";", tokens)
	stmts = parseBlock(tokens)
	elsestmts = Block([ ])
	if tokens.peek( ) == "else":
		tokens.next( )
		match(":", tokens)
		match(";", tokens)
		elsestmts = parseBlock(tokens)
	return IfStmt(expr, stmts, elsestmts)

def parseDef(tokens):
	""" defStmt = 'def' ident '(' identlist ')' ':' eoln block """
	name = tokens.next( )
	re.match(Lexer.identifier, tokens.peek())
	tokens.next( )
	match("(", tokens)
	list = identList(tokens)
	# print "def=", tokens.peek()
	match(")", tokens)
	match(":", tokens)
	match(";", tokens)
	stmts = parseBlock(tokens)
	return DefStmt(name, list, stmts)

def parseReturn(tokens):
	""" returnStmt = 'return' [ expression ] ; """
	tokens.next( )
	list = [ ]
	if debug: print "Return: "+tokens.peek()
	if tokens.peek() != ";":
		exp = parseExpr(tokens)
		list.append(exp)
	match(";", tokens)
	return ReturnStmt(list)

def parseStmt(tokens):
	tok = tokens.peek( )
	if debug:
		print "Stmt: "+str(tok)
	if tok == 'break' or tok == "continue" or tok == "exit":
		tokens.next( )
		match(";", tokens)
		return Break(tok)
	if tok == "return":
		return parseReturn(tokens)
	if tok == "print":
		tokens.next( )
		list = exprList(tokens)
		match(";", tokens)
		return Print(list)
	if tok == "while":
		return parseWhile(tokens)
	if tok == "if":
		return parseIf(tokens)
	if tok == "def":
		return parseDef(tokens)
	if re.match(Lexer.identifier, tok):
		return parseAssign(tokens)
	return None

def parseScript(tokens):
	stmts = [ ]
        state = { }
	while tokens.peek( ) != None:
		s = parseStmt(tokens)
                print str(s)
                state = s.meaning(state)
                print state
		stmts.append(s)
		if tokens.peek() == ";":
			match(';', tokens)
	return Block(s)

def parse( text ) :
	tokens = Lexer( text )
	if debug: print tokens
	#while tokens.peek() != None:
	stmt = parseScript(tokens)
	return


# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o removeToken, a parameterless message that removes the next
#       token from a token sequence.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :
	
	
	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|,|:|;|@|~|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text )
		self.position = 0
		self.indent = [ 0 ]
	
	
	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def next( self ) :
		self.position = self.position + 1
		return self.peek( )
	
	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"




# The following functions form a recursive descent parser for Gee, with the start
# symbol being script.


# "makeString," a utility function that breaks a string constant into a list
# of syntax trees for its individual characters. This list can then be used as
# the elements of an array (since a Gee string is just a shorthand for an array
# of characters). Since the first and last 2 characters of the token are the
# string delimiters, and everything else is meaningful text, this just makes a
# list of "Atomtrees" for everything except those first and last characters.

#def makeString( token ) :
#	return [ AtomTree(c) for c in token[2:-2] ]


#  Main program if called by itself

#def main():
#        """main program for testing"""
#        if len(sys.argv) < 2:
#                print "Usage:  %s filename" % sys.argv[0]
#                return
#        inn = open(sys.argv[1], "r")
#        lines = inn.readlines()
#        parse(string.join(lines, ";"))
#        # print str(ast)
#        return

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
                                line = '~ ' + line
                print ct, "\t", line
                lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += " ~ "
	lines.append(undent)
	# print undent
        return lines

def main():
	"""main program for testing"""
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d":
			debug = True
	if len(sys.argv) < 2+ct:
                print "Usage:  %s filename" % sys.argv[0]
                return
        parse(string.join(mklines(sys.argv[1+ct]), ""))
        return


if __name__ == '__main__':
	main()

