m4_include(stdlib.m4)  m4_dnl
m4_define(_mbrace, `<font color=blue>{</font> $1 <font color=blue>}</font>')
_HEADER(Gee Parser)

<blockquote><pre>
_b(Due): 8:00 AM, Thurs, Oct 3</font>
_b(Submit Project): parser
_b(Source File): _SELFLINK(gee.py.txt)
_b(Grammar File): _SELFLINK(grammar.txt) <br>
_b(Test Files): _SELFLINK(t0.gee.txt) _SELFLINK(t1.gee.txt) _SELFLINK(t2.gee.txt) 
_SELFLINK(test-out.txt)
</pre></blockquote>

See Questions at the bottom.

<p>
The Gee programming language is:
<ul>
<li> A small but interesting programming language;

<li> Designed for class projects in language implementation;

<li> Intended to expose new ways of thinking about programming.

<li>  Different from typical statically-typed languages.
</ul>

</p><p>
The purpose of the project is to parse the input according to the
grammar and produce a printed representation of the
_i(abstract syntax tree).  Sample data and output are given above.
</p>


_H3(Parser)

<p>Your task is to construct the remaining recursive descent
routines to complete the parser for the <b>Expression</b> 
only portion of the Gee. Each recursive procedure should return
an <i>Abstract Syntax Tree</i> (AST) of the expression.
The AST naturally interpreted should be constructed to
correspond to the parse tree.
You are free to modify the _LINK(grammar.txt, grammar) 
provided you do not change the syntax of Gee.</p>
<p>  Specially, you must:
<ol>
	<li>Set the constant xxx to true.</li>
	
   <li> Build parse routines for the expression nonterminals:<br>
   expression, andExpr, orExpr, relationalExpr.
   Note that currently addExpr is called in 2 places:
   factor and parse; <br> 
   both must be changed to invoke expression.
   (as specified in the grammar).</li>

   <li>Build classes for ident (VarRef) and string (String)
   and add the necessary logic to factor.</li>

</ol>
</p><p>

The output of the parser is a printed representation of
the abstract syntax tree.  The abstract syntax is defined by
a collection of classes.
Each class in the abstract syntax must have an appropriate
constructor and a _c(__str__) function for displaying the
abstract syntax.
</p> 

<p>
Expressions in AST should be printed one per line; 
this can be accomplshed
by appending a "\n" to the string returned by _c(__str__) .
Expressions should print in Polish prefix
with a space separating each element from the next.
</p>

_H3(Requirements)

<ol>
    <li> Each parse function corresponding to a nonterminal _b(must)
    return an object of either _c(Expression).</li>
</ol>

_H3(To Do)

<ul>
<li> Expression subgrammar: and, or, relations. </li>

<li> A Gee program file _b(must) end with an end of line.  To check, either
execute : _c(cat filename) or in your editor, make sure you can move the cursor
to the line below the last line of text.</li>

</ul>

_H3(Questions)

<ol>
</ol>

_TRAILER(../)
