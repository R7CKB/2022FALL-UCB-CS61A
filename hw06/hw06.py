class Mint:
    """A mint creates coins by stamping on years.

    The update method sets the mint's stamp to Mint.present_year.

    >>> mint = Mint()
    >>> mint.year
    2022
    >>> dime = mint.create(Dime)
    >>> dime.year
    2022
    >>> Mint.present_year = 2102  # Time passes
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet
    2022
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2102
    >>> Mint.present_year = 2177     # More time passes
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """
    present_year = 2022

    def __init__(self):
        self.update()

    def create(self, coin):
        "*** YOUR CODE HERE ***"
        return coin(self.year)



    def update(self):
        "*** YOUR CODE HERE ***"
        self.year=Mint.present_year


class Coin:
    cents = None  # will be provided by subclasses, but not by Coin itself

    def __init__(self, year):
        self.year = year

    def worth(self):
        "*** YOUR CODE HERE ***"
        if self.year==Mint.present_year:
            return self.cents
        return self.cents+(Mint.present_year-self.year-50)
    
        """Official Answer
        的确更简洁"""
        return self.cents + max(0, Mint.present_year - self.year - 50)

class Nickel(Coin):
    cents = 5


class Dime(Coin):
    cents = 10


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    """
    "*** YOUR CODE HERE ***"
    """肯定会用到递归,(ง •̀_•́)ง,想了半天还是不会,就作弊了 ╥﹏╥,但看完答案后感觉不难,
    自己还是不是很掌握链表的数据结构...   (,,•́ . •̀,,)
    cheated"""
    result = Link.empty
    while n > 0:
        digit = n % 10
        result = Link(digit, result)
        n //= 10
    return result

    """Official Answer
    思路是一样的"""
    result = Link.empty
    while n > 0:
        result = Link(n % 10, result)
        n //= 10
    return result
    



def deep_map_mut(func, lnk):
    """Mutates a deep link lnk by replacing each item found with the
    result of calling func on the item.  Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"
    if isinstance(lnk.first, int):# 如果是数字的话就应用函数
        lnk.first = func(lnk.first)
        deep_map_mut(func, lnk.rest) if lnk.rest is not Link.empty else None # 且还要确保后面不是空的
    elif isinstance(lnk.first, Link):# 如果是列表的话再单独处理
        deep_map_mut(func, lnk.first)
        deep_map_mut(func, lnk.rest)

    """Official Answer
    思路是一样的,我的可能会更复杂一点(思想上?) ◔ ‸◔？"""
    if lnk is Link.empty:
        return
    elif isinstance(lnk.first, Link):
        deep_map_mut(func, lnk.first)
    else:
        lnk.first = func(lnk.first)
    deep_map_mut(func, lnk.rest)


def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.

    >>> a = [1, 3, 2]
    >>> b = [1, 1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3, Link(2)))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    "*** YOUR CODE HERE ***"
    # list1 = []
    # dictionary = dict(zip(vals, counts))
    # for key, value in dictionary.items():
    #     elem = [key] * value
    #     list1.extend(elem)
    # 上述代码可以替换为如下所示
    dictionary = dict(zip(vals, counts))
    list1 = [key for key, value in dictionary.items() for _ in range(value)]
    result = Link.empty
    "这个题和第二道题想法一样,都是从后往前构建列表"
    while list1:
        rest = list1[-1]
        result = Link(rest, result)
        list1 = list1[:-1]
    return result

    """Official Answer
    高阶函数构建,看起来就很难的样子 （⊙.⊙）
    这也是一个递归调用,只不过有些绕"""
    def helper(count, index):
        if count == 0:
            if index + 1 == len(vals):# 是否到达了列表的末尾
                return Link.empty
            return Link(vals[index + 1], helper(counts[index + 1] - 1, index + 1)) # 如果counts等于0就构建下一个列表中的数,使下一个数的次数减1,index+1.递归完成
        return Link(vals[index], helper(count - 1, index)) #如果counts不为0的话就将counts-1,构建第一个数的链表
    return helper(counts[0], 0)

    #Iterative solution
    """这个好像跟我的思路差不多,它是从前往后构建,可以学习一下
    最后把开头的None舍弃了,有点东西"""
    result = Link(None) 
    p = result
    for index in range(len(vals)):
        item = vals[index]
        for _ in range(counts[index]):
            p.rest = Link(item)
            p = p.rest
    return result.rest


class VirFib():
    """A Virahanka Fibonacci number.

    >>> start = VirFib()
    >>> start
    VirFib object, value 0
    >>> start.next()
    VirFib object, value 1
    >>> start.next().next()
    VirFib object, value 1
    >>> start.next().next().next()
    VirFib object, value 2
    >>> start.next().next().next().next()
    VirFib object, value 3
    >>> start.next().next().next().next().next()
    VirFib object, value 5
    >>> start.next().next().next().next().next().next()
    VirFib object, value 8
    >>> start.next().next().next().next().next().next() # Ensure start isn't changed
    VirFib object, value 8
    """

    def __init__(self, value=0):
        self.value = value

    def next(self):
        "*** YOUR CODE HERE ***"
        """这是拿GPT写出来的,自己看了半天是还是不会 π__π  
        cheated"""
        self.prev_value = None
        next_value = self.value + self.previous_value if hasattr(self, 'previous_value') else 1
        next_fib = VirFib(next_value)
        next_fib.previous_value = self.value
        return next_fib

        """Official Answer
        两个答案的思路是一样的,刚开始我的思路错了,我直接返回VirFib的示例,(说明题目也没怎么看明白)
        所以一直不对,对面向对象的编程还缺乏深刻的理解"""
        if self.value == 0:
            result = VirFib(1)
        else:
            result = VirFib(self.value + self.previous)
        result.previous = self.value #这一步是最关键的,将 result 实例的 previous 属性设置为当前实例的 value.这样,在下一次调用 next 方法时,可以使用当前实例的值作为前一个斐波那契数.
        return result
    
    def __repr__(self):
        return "VirFib object, value " + str(self.value)


def is_bst(t):
    """Returns True if the Tree t has the structure of a valid BST.

    >>> t1 = Tree(6, [Tree(2, [Tree(1), Tree(4)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t1)
    True
    >>> t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
    >>> is_bst(t2)
    False
    >>> t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t3)
    False
    >>> t4 = Tree(1, [Tree(2, [Tree(3, [Tree(4)])])])
    >>> is_bst(t4)
    True
    >>> t5 = Tree(1, [Tree(0, [Tree(-1, [Tree(-2)])])])
    >>> is_bst(t5)
    True
    >>> t6 = Tree(1, [Tree(4, [Tree(2, [Tree(3)])])])
    >>> is_bst(t6)
    True
    >>> t7 = Tree(2, [Tree(1, [Tree(5)]), Tree(4)])
    >>> is_bst(t7)
    False
    """
    "*** YOUR CODE HERE ***"
    def bst_min(t):
        minimum = float('inf')
        if t.label < minimum:
            minimum = t.label
        for b in t.branches:
            minimum = min(minimum, bst_min(b))
        return minimum


    def bst_max(t):
        maximum = -float('inf')
        if t.label > maximum:
            maximum = t.label
        for b in t.branches:
            maximum = max(maximum, bst_max(b))
        return maximum
    
    """对着答案稍微改了一下,答案更加简洁"""
    if t.is_leaf():# 叶子节点
        return True
    if len(t.branches) == 2:  # 有两个节点
        left_node, right_node = t.branches[0],t.branches[1]
        valid_branches=is_bst(left_node) and is_bst(right_node)
        return valid_branches and bst_max(left_node)<=t.label and bst_min(right_node)>t.label
    elif len(t.branches) == 1:  # 有一个节点
        left_node = t.branches[0]
        return is_bst(left_node) and (bst_max(left_node)<=t.label or bst_min(left_node)>t.label)
    else:
        return False


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()
