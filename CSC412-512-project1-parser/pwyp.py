class Declaration:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return "declaration"

class Variable:
    def __init__(self, ident):
        if not re.match(TokenSequence.identifier, ident):
            raise palError("not a valid identifier: " + ident)
        self.ident = ident

    def __str__(self):
        return self.ident

def parseStmt(tokens):
    tok = tokens.peek()
    if tok == "declare":
        tokens.removeToken()
        id = tokens.peek()
        tokens.removeToken()
        expr = parseExpr(tokens)
        return Declaration(Variable(id), expr)
    else:
        return parseExpr(tokens)
