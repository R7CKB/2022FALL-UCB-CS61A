from operator import add, mul

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


def ordered_digits(x):
    """Return True if the (base 10) digits of X>0 are in non-decreasing
    order, and False otherwise.

    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> result = ordered_digits(1375) # Return, don't print
    >>> result
    False

    """
    "*** YOUR CODE HERE ***"
    # 递归
    if x<10:
        return True
    single_digit=x%10
    remaining_digit=x//10
    other_digit=remaining_digit%10
    if single_digit<other_digit:
        return False
    else:
        return ordered_digits(remaining_digit)
    # 迭代
    while x!=0:
        if x<10:
            return True
        single_digit=x%10
        other_digit=(x//10)%10
        if single_digit<other_digit:
            return False
        x//=10
    return True
    



def get_k_run_starter(n, k):
    """Returns the 0th digit of the kth increasing run within n.
    返回 n 内第 k 个递增运行的第 0 位数字.
    >>> get_k_run_starter(123444345, 0) # example from description
    3
    >>> get_k_run_starter(123444345, 1)
    4
    >>> get_k_run_starter(123444345, 2)
    4
    >>> get_k_run_starter(123444345, 3)
    1
    >>> get_k_run_starter(123412341234, 1)
    1
    >>> get_k_run_starter(1234234534564567, 0)
    4
    >>> get_k_run_starter(1234234534564567, 1)
    3
    >>> get_k_run_starter(1234234534564567, 2)
    2
    """
    """这道题也有些难度,要先读题,把题读明白了,再开始动手"""
    final = None
    while k>=0:
        current=n%10
        n//=10
        while n>0 and n%10<current:
            current=n%10
            n//=10
        if  not k:
            return current
        k-=1
    return final


def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    "*** YOUR CODE HERE ***"
    def f(x):
        nonlocal n
        while n!=0:
            x=func(x)
            n-=1
        return x
    return f


def composer(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f


def apply_twice(func):
    """ Return a function that applies func twice.

    func -- a function that takes one argument

    >>> apply_twice(square)(2)
    16
    """
    "*** YOUR CODE HERE ***"
    def f(n):
        x=func(n)
        if n>1:
            x=func(x)
        return x
    return f
    # 或者
    def f(n):
        if n > 1:
            return func(func(n))
        else:
            return func(n)
    return f



def div_by_primes_under(n):
    """
    >>> div_by_primes_under(10)(11)
    False
    >>> div_by_primes_under(10)(121)
    False
    >>> div_by_primes_under(10)(12)
    True
    >>> div_by_primes_under(5)(1)
    False
    """

    """Official Answer"""
    checker = lambda x: False
    i =  2
    while i<=n:
        if not checker(i):
            checker = (lambda f,i:lambda x:x%i==0 or f(x))(checker,i)
        i = i+1
    return checker
    # 或者(自己的想法)
    def f(x):
        for i in range(2,n+1):
            if is_prime(i) and x%i==0:
                return True
        return False
    return f
def is_prime(x):
    if x == 1:
        return False
    for i in range(2, x // 2):
        if x % i == 0:
            return False
    return True



def div_by_primes_under_no_lambda(n):
    """
    >>> div_by_primes_under_no_lambda(10)(11)
    False
    >>> div_by_primes_under_no_lambda(10)(121)
    False
    >>> div_by_primes_under_no_lambda(10)(12)
    True
    >>> div_by_primes_under_no_lambda(5)(1)
    False
    """
    # 标准答案
    def checker(x):
        return False
    i = 2
    while i<=n:# 通过函数递归来更新checker函数
        if not checker(i):
            def outer(f,i):
                def inner(x):
                    return x%i==0 or f(x) #checkera函数的关键是判断i是否是素数
                return inner
            checker = outer(checker,i)
        i = i+1
    return checker
    # 自己的想法
    def f(x):
        for i in range(2,n+1):
            if is_prime(i) and x%i==0:
                return True
        return False
    return f
def is_prime(x):
    if x == 1:
        return False
    for i in range(2, x // 2):
        if x % i == 0:
            return False
    return True


def zero(f):
    return lambda x: x


def successor(n): 
    return lambda f: lambda x: f(n(f)(x))

"""one为succcessor(zero)"""
def one(f):
    """Church numeral 1: same as successor(zero)"""
    "*** YOUR CODE HERE ***"
    return lambda x:f(x)
    # 或者是 lambda x:f(zero(f)(x))
    """根据上面的zero函数,zero(f)(x)也可以转换为x,所以才有了上面的公式"""

"""two在题中的描述为succcessor(successor(zero))"""
def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    "*** YOUR CODE HERE ***"
    return lambda x:f(f(x))

"""总结以上两个公式,我们可以得出一个自然数N的函数为:
def n(f):
    return lambda x: f((n-1)(f)(x))
将其化简可以想到 为n(f)(x)
"""

three = successor(two)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    "*** YOUR CODE HERE ***"
    """观察上面的doctest以及结合前面的知识可以得知所有的自然数都可以通过不断地加一来得出
    故这里的函数应该是不断地加一"""
    return n(increment)(0)
    # 将increment这个函数执行n次,最开始传入的参数是0,最后当然就能得到int类型的n.


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    "*** YOUR CODE HERE ***"
    """如果上面的转换成整数不出问题的话,下面的这些都不难想出来"""
    return lambda f:lambda x:m(f)(x)+n(f)(x)
    # Official Answer
    return lambda f: lambda x: m(f)(n(f)(x))
    """我们来分析一下为什么官方答案可以这样写,m+n等同于m(f)(x)+n(f)(x)
	也等同于m(increment)(0)+n(increment)(0),看后半部分,n(increment)(0)
	计算后仍为一个整数,那么就可以将它作为church_to_int函数的基数(即0)
	从而得出官方答案
	"""


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    "*** YOUR CODE HERE ***"
    return lambda f:lambda x:m(f)(x)*n(f)(x)
    # Official Answer
    return lambda f: m(n(f))
    """
    这个的话就和上面的那个加法道理一样了,将m(f)(x)*n(f)(x)化简开来得
    考虑到 Church 数字的结构,我们可以将 m(f)(x) * n(f)(x) 视为 m 先应用一个函数 f,然后将结果作为参数传递给 n,再次应用函数 f.
    换句话说,我们可以将 m(f)(x) * n(f)(x) 表示为 n(m(f))(x).
    根据这个思路,我们可以将 mul_church 函数中的 return lambda f:lambda x:m(f)(x)*n(f)(x) 转化为 return lambda f: m(n(f)).
    这样做就是将 m(f)(x) * n(f)(x) 简化成了 n(m(f))(x),同时也省略了中间的参数 x,因为这个参数并没有在计算中起到实质性的作用.
	"""

def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    "*** YOUR CODE HERE ***"
    return lambda f:lambda x:pow(m(f)(x),n(f)(x))
    # Official Answer
    return n(m)
    """是对m的n次函数应用."""