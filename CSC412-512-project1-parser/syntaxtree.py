#! /usr/bin/python


import re, sys, string


# The "PALError" class.

class PALError ( Exception ) :


	# The constructor. This just saves the explanation to be reported to
	# anyone who handles the exception.
	
	def __init__( self, msg ) :
		self.msg = msg
	
	
	# A "__str__" method that ensures that when "PALError" objects print,
	# they display their explanation.
	
	def __str__( self ) :
		return self.msg



# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar. 

def parse( text ) :
	tokens = TokenSequence( text )
	while tokens.peek() != None:
                print tokens.peek()
                tokens.removeToken()
        return


# TokenSequence, a private class that represents lists of tokens from a PAL
# expression. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a PAL expression
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

class TokenSequence :
	
	
	# The constructor with some regular expressions that define PAL's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match PAL tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|{="
	char = r"'."
	string = r"\['.*?']"
	number = r"\-?\d+(?:\.\d+)?"
	idStart = r"a-zA-Z~@#$%^&*_+=\\\-<>?/."
	idChar = idStart + r"0-9"
	identifier = "[" + idStart + "][" + idChar + "]*"
	lexRules = string + "|" + special + "|" + char + "|" + number + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( TokenSequence.lexRules, text )
		self.position = 0
	
	
	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def removeToken( self ) :
		self.position = self.position + 1
	
	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<TokenSequence at " + str(self.position) + " in " + str(self.tokens) + ">"




# The following functions form a recursive descent parser for PAL, with the start
# symbol being <ExpressionList>.


# "makeString," a utility function that breaks a string constant into a list
# of syntax trees for its individual characters. This list can then be used as
# the elements of an array (since a PAL string is just a shorthand for an array
# of characters). Since the first and last 2 characters of the token are the
# string delimiters, and everything else is meaningful text, this just makes a
# list of "Atomtrees" for everything except those first and last characters.

def makeString( token ) :
	return [ AtomTree(c) for c in token[2:-2] ]


#  Main program if called by itself

def main():
        """main program for testing"""
        if len(sys.argv) < 2:
                print "Usage:  %s filename" % sys.argv[0]
                return
        inn = open(sys.argv[1], "r")
        lines = inn.readlines()
        parse(string.join(lines, ""))
        # print str(ast)
        return

if __name__ == '__main__':
    main()
