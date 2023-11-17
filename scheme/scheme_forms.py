from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.


def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2)  # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2)  # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        # 我感觉我写的应该是没毛病的,搞了半天 少加了一个.first
        value=scheme_eval(expressions.rest.first,env)
        env.define(signature,value) # 根据OK测试提供的问题得出
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        # 它提供了两种方法,我选用的是第二种方法(直接实现)
        "*** YOUR CODE HERE ***"
        name=signature.first
        formals=expressions.first.rest
        validate_formals(formals) # 检查参数是否有效,有可能就是数字,所以需要这个函数
        body=expressions.rest
        env.define(name,LambdaProcedure(formals,body,env))
        return name
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))


def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil))) # 这是最后一个OK测试的答案,观察之前的测试可以找到规律,就是只返回expressions.first
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    return expressions.first
    # END PROBLEM 5


def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)


def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    # 最后一个OK测试卡我卡半天,服了,还得空格一一对齐。。。 想骂人了
    # 说的是和begin一样，顺序计算*主体*的所有表达式
    # 函数的参数又该如何处理?
    # 想了半天,一看doctest测试。。 发现自己想多了 两行就可以解决
    "*** YOUR CODE HERE ***"
    body=expressions.rest
    return LambdaProcedure(formals,body,env)
    # END PROBLEM 7


def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env,tail=True) # 尾递归
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env,tail=True)# 尾递归


def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    if expressions is nil:
        return True
    while expressions.rest is not nil:
        if is_scheme_false(scheme_eval(expressions.first,env)):
            return scheme_eval(expressions.first, env)
        expressions=expressions.rest 
    result=scheme_eval(expressions.first,env,tail=True) # 尾递归
    return result
    # END PROBLEM 12


def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    if expressions is nil:
        return False
    while expressions.rest is not nil:
        if is_scheme_true(scheme_eval(expressions.first,env)):
            return scheme_eval(expressions.first,env)
        expressions=expressions.rest
    result=scheme_eval(expressions.first,env,tail=True)# 尾递归
    return result
    # END PROBLEM 12


def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    # 这是一个无限循环
    while expressions is not nil:
        clause = expressions.first # 条件
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            "*** YOUR CODE HERE ***"
            if clause.rest is nil: #当true谓词没有对应的结果子表达式时，返回谓词值
                return test
            if len(clause.rest)>1: #当cond情况的结果子表达式有多个表达式时，将对所有表达式求值并返回最后一个表达式的值
                return eval_all(clause.rest,env)
            return scheme_eval(clause.rest.first,env,tail=True) # 尾递归,如果为真,则返回其后的值
            # END PROBLEM 13
        expressions = expressions.rest


def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)


def make_let_frame(bindings, env): # 将符号绑定在本地值,不改变它原来的值,但还有一点很奇怪
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    # cheated
    "*** YOUR CODE HERE ***"
    while bindings is not nil: 
        validate_form(bindings.first,2,2) # 每个binings.first都是一个(<name> <expression>)
        names=Pair(bindings.first.first,names) # 这里我想到了Pair,但没有用,感觉自己呆呆的,这也是一种递归啊.
        vals=Pair(scheme_eval(bindings.first.rest.first,env),vals) #看了别人的才知道的,应该想到的
        bindings=bindings.rest
    validate_formals(names)
    # END PROBLEM 14
    return env.make_child_frame(names, vals)


def do_define_macro(expressions, env): # 感觉有点像自定义函数? 
    """Evaluate a define-macro form.

    >>> env = create_global_frame()
    >>> do_define_macro(read_line("((f x) (car x))"), env)
    'f'
    >>> scheme_eval(read_line("(f (1 2))"), env)
    1
    """
    # BEGIN PROBLEM OPTIONAL_1
    "*** YOUR CODE HERE ***"
    # 没写出来 不过我觉得我的思路应该是对的 主要是不会更改scheme_eval里面的内容
    # 宏实际上也是lambda函数的一张特殊实现
    # cheated
    validate_form(expressions,2)
    expr=expressions.first
    # 这整个下面都是模仿do_define_form写的
    if isinstance(expr,Pair) and scheme_symbolp(expr.first):
        signature=expr.first
        formals=expr.rest 
        validate_formals(formals)
        body=expressions.rest
        env.define(signature,MacroProcedure(formals,body,env))
        return signature
    else: # 确保正确使用macro
        raise SchemeError('Invalid use of macro')
    # END PROBLEM OPTIONAL_1


def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)


def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    "*** YOUR CODE HERE ***"
    body=expressions.rest
    return MuProcedure(formals,body)
    # END PROBLEM 11


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
    'define-macro':do_define_macro,
}
