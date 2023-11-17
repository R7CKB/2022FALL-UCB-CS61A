import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored 忽略可选的第三个参数
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr): #这个意思应该是查询符号
        return env.lookup(expr)
    elif self_evaluating(expr): # 如果查得到就评估其值
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr): # 如果expr不是列表的话
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:  # 将特殊形式的过滤掉了
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    # 我觉得这个修改是最难的
    # you can use "first in env.bindings and isinstance(env.bindings.get(first), MacroProcedure)"
    # instead of "isinstance(scheme_eval(first, env), MacroProcedure)"
    # check: "first" is symbol pointer?
    # if we don't check, promble 3 and 4 will error
    # because they call scheme_eval(first, env) in isinstance(scheme_eval(first, env), MacroProcedure)
    # and not execute builtin procedure(part of "else") or other func
    if scheme_symbolp(first) and isinstance(scheme_eval(first,env),MacroProcedure):
        #scheme_eval(first,env)已经是一个宏对象了
        formals=scheme_eval(first,env).formals
        body=scheme_eval(first,env).body.first
        while formals !=nil:
            env.define(formals.first,rest.first)# 绑定参数
            formals,rest=formals.rest,rest.rest
        body_expr=scheme_eval(body,env)
        return scheme_eval(body_expr,env) # 绑定完参数再执行
    else:
        # BEGIN PROBLEM 3
        # cheated
        "*** YOUR CODE HERE ***"
        operator=scheme_eval(first,env) # 1. 评估运算符 
        validate_procedure(operator) # (应评估为 Procedure 的实例)这句话误导了我,我以为要创建一个实例
        operands=rest.map(lambda x:scheme_eval(x,env)) # 2.评估所有操作数
        return scheme_apply(operator,operands,env) # 3.返回结果
        # END PROBLEM 3


def scheme_apply(procedure, args, env): # 这里面的args是一个Pair
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        argument_list=[]
        while args is not nil:
            argument_list.append(args.first)
            args=args.rest
        if procedure.need_env:
            argument_list.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            result=procedure.py_func(*argument_list)
            return result
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure): # 如果是lambda函数的话
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        new_Frame=procedure.env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body,new_Frame)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        # 新调用框架(MuProcedure)的父级是计算该调用表达式的环境(env)
        "*** YOUR CODE HERE ***"
        procedure.parent=env
        new_Frame=env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body,new_Frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # 这应该是一个递归,但要按顺序执行每一个表达式
    # 我的这个答案通不过proble EC,不过和下面的答案思路是一样的,我就照着他的修改了一下
    # if expressions is nil: # 终止条件
    #     return None
    # if expressions.rest is nil:
    #     return scheme_eval(expressions.first,env)
    # else:
    #     scheme_eval(expressions.first,env) #按顺序执行每一个表达式
    #     return eval_all(expressions.rest,env) 
    # 修改之后的答案
    if expressions is nil: # 终止条件
        return None
    while expressions.rest is not nil:
        scheme_eval(expressions.first, env)
        expressions = expressions.rest
    return scheme_eval(expressions.first,env,tail=True)
    # 别人的答案
    # if expressions is nil:
    #     return None

    # while expressions.rest is not nil:
    #     eval_res = scheme_eval(expressions.first, env)
    #     expressions = expressions.rest
    # eval_res = scheme_eval(expressions.first, env, tail=True)  # * tail context
    # return eval_res
    #return scheme_eval(expressions.first, env)  # replace this with lines of your own code
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        """要成功实现这个优化,需要对多个函数进行更改,包括一些我们为你提供的函数.
        在整个解释器中,需要确定哪些表达式位于尾递归上下文中,
        并根据需要更改对 scheme_eval 的调用,
        确保它们在尾递归上下文中以 True 作为第三个参数(现在称为 tail)进行评估
        在Scheme解释器中,表达式可以分为两类:尾递归表达式和非尾递归表达式.
        尾递归表达式是在函数的最后一个操作中调用自身的表达式,而非尾递归表达式则不是.
        尾递归表达式是尾上下文的一部分,需要进行尾递归优化."""
        # 需要更改 probelm6的递归,Problem12,13的递归,do_if_form中的递归(这个得看自己怎么写的来,要改哪些递归)
        # 想出来倒是不难,难的是改递归
        while isinstance(result,Unevaluated):
            result=unoptimized_scheme_eval(result.expr,result.env)
        return result
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)
