import builtins

from pair import *


class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

################
# Environments #
################


class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        self.bindings[symbol]=value
        # END PROBLEM 1

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        if symbol in self.bindings:  #如果符号绑定在当前框架中,则返回其值
            return self.bindings.get(symbol)
        while self.parent is not None: #如果该符号未绑定在当前框架中并且该框架有父框架,则在父框架中查找该符号。
            if symbol in self.parent.bindings:  
                return self.parent.bindings.get(symbol)
            self=self.parent
        if symbol not in self.bindings: #如果在当前框架中找不到该符号并且没有父框架,则引发 SchemeError
            raise SchemeError('unknown identifier: {0}'.format(symbol))
        # END PROBLEM 1

    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals): #如果参数值的数量与形式参数的数量不匹配，则引发 SchemeError.
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        "*** YOUR CODE HERE ***"
        child_frame=Frame(self)
        for _ in range(len(formals)):# 如果循环的数与循环体无关的话,使用_
            child_frame.define(formals.first,vals.first)
            formals=formals.rest
            vals=vals.rest
        return child_frame
        # END PROBLEM 8

##############
# Procedures #
##############


class Procedure:
    """The the base class for all Procedure classes."""


class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))


class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    interesting!!!
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))

class MacroProcedure(LambdaProcedure):# 继承的是LambdaProcedure或者是Procedure都可以
    """A pocedure defined by a define-macro expression 
    
    In face,I didn't know what is macro. 
    """

    # we use 'lambda' but not use 'macro' when reprenting string
    # 因为测试里面有个样例输出的是lambda，所以要改为lambda
    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))
    
    def __repr__(self):
        return 'MacroProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))
    