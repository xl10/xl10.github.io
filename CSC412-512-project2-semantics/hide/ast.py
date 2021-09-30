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
            
        def meaning(self, state):
            return state
        
class Assign( Statement ):
        def __init__(self, var, expr):
            self.var = var
            self.expr = expr
                
        def __str__( self ):
                return "= " + self.var + " " + str(self.expr)
        
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

class IfStmt( Statement ):
        def __init__(self, expr, block, elseblock):
            self.expr = expr
            self.then = block
            self.elseblock = elseblock
                
        def __str__(self):
            return "if " + str(self.expr) + "\n" + str(self.then) + "\n" + str(self.elseblock) + "endif\n"

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

