m4_include(stdlib.m4)  m4_dnl
_HEADER(`Semantics')

<pre>
_b(Due): Tues, Oct 22, 8 AM 
_b(Submit Project): semantics 
_b(Test Files):  _SELFLINK(fact1.txt) _SELFLINK(if1.txt) _SELFLINK(if2.txt)
_b(Results): _SELFLINK(outfact1.txt) _SELFLINK(outif1.txt) _SELFLINK(outif2.txt)
m4_dnl _b(Grading Tests): _SELFLINK(tests.tar)
m4_dnl _b(Related Activities): _SELFLINK(sema1.py)  _SELFLINK(sema2.py)
</pre>

<p>
The basic purpose of this assignment is to 
implement a dynamically typed version of a subset of Gee.
In doing so, you should gain a deeper
understanding of dynamic typing and of an interpreter.
</p><p>

The state function described in class can be modeled using a Python
dictionary (associative array).  This dictionary, named _i(state),
should be explicitly passed as an argument to each meaning function.
</p><p>

Remember: the meaning of an _b(expression) in a state is a _b(value),
while the meaning of a _b(statement) in a state is a new state.

</p>


_H3(Your Assignment)

<ol>
  <li>  Implement the _c(meaning) function for all the relationals,
  _c(and), _c(or) for both numbers and Booleans.  Remember that the
  meaning of an expression is always a value.  No test case will contain
  the Boolean constants _c(True), _c(False).</li>

  <li>  Implement the meaning function for the following Abstract
        Syntax statements:
    <ol type=a>
      <li>  Assign.
      <li>  IfStmt (if-then-else)
      <li>  WhileStmt.
      <li>  Block.
      <li> StmtList
    </ol>
    Note that an _i(IfStmt) begins with the keyword _c(if), a
        _i(WhileStmt) with the keyword _c(while), and an _i(Assign) with
        an _i(identifier) (hint: see factor parse). </li>
</ol>

_H3(Submit)

<p>
_CODE(~noonan/bin/submit  cs312  semantics
)
</p>

_H3(Questions)

<ol>
</ol>


_TRAILER(../)
