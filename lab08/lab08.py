def convert_link(link):
    """Takes a linked list and returns a Python list with the same elements.

    >>> link = Link(1, Link(2, Link(3, Link(4))))
    >>> convert_link(link)
    [1, 2, 3, 4]
    >>> convert_link(Link.empty)
    []
    """
    "*** YOUR CODE HERE ***"
    "迭代方案"
    list1 = []
    while link is not Link.empty:
        list1.append(link.first)
        link = link.rest
    return list1
    "递归方案"
    if link==Link.empty:
        return []
    else:
        return [link.first]+convert_link(link.rest)
    """这个challenged的意思是链表嵌套链表,也没什么难度"""
    if link==Link.empty:
        return []
    if type(link.first)==Link:
        return [convert_link(link.first)]+convert_link(lik.rest)
    return [link.first]+convert_link(link.rest)
    "Official Answer 的递归和迭代方案都和我的一样"


def duplicate_link(link, val):
    """Mutates link such that if there is a linked list
    node that has a first equal to value, that node will
    be duplicated. Note that you should be mutating the
    original link list.

    >>> x = Link(5, Link(4, Link(3)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(3))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, (Link(2, Link(3)))))
    >>> duplicate_link(z, 2) #ensures that back to back links with val are both duplicated
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    "*** YOUR CODE HERE ***"
    "这道题的思路就是插入数据,可以借鉴之前那个在有序链表中插入值的方法"
    while link is not Link.empty:
        if link.first == val:
            link.rest = Link(val, link.rest)
            link = link.rest.rest # 跳过当前值和添加的值
        else:
            link = link.rest
    "Official Answer"
    """答案用到了递归,我是迭代处理,不过无所谓,它也就是将我的两句话改为原函数,道理是一样的
    link = link.rest.rest 替换为duplicate_link(remaining val)
    link = link.rest 替换为duplicate_link(link.rest, val)
    """
    if link is Link.empty:
        return
    elif link.first == val:
        remaining = link.rest
        link.rest = Link(val, remaining)
        duplicate_link(remaining, val)
    else:
        duplicate_link(link.rest, val)



def cumulative_mul(t):
    """Mutates t so that each node's label becomes the product of all labels in
    the corresponding subtree rooted at t.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> cumulative_mul(t)
    >>> t
    Tree(105, [Tree(15, [Tree(5)]), Tree(7)])
    >>> otherTree = Tree(2, [Tree(1, [Tree(3), Tree(4), Tree(5)]), Tree(6, [Tree(7)])])
    >>> cumulative_mul(otherTree)
    >>> otherTree
    Tree(5040, [Tree(60, [Tree(3), Tree(4), Tree(5)]), Tree(42, [Tree(7)])])
    """
    "*** YOUR CODE HERE ***"
    """肯定会用到递归  (ง •̀_•́)ง  我觉得应该倒着来
    即在处理子树之后对树进行变异"""
    for b in t.branches:
        if b.branches:
            for bb in b.branches:
                b.label *= bb.label
        t.label *= b.label
    """我的这个做法完全是为了应付测试,对以上代码总结,观察即可得出递归形式
    将上面的代码优化一下,可得如下代码"""            
    if not t.branches: # 这两行代码在doctest不重要,甚至也可以删除掉(答案中没有),但为了严谨一点,很有必要
        return
    for b in t.branches:
        cumulative_mul(b)
        t.label *= b.label
    "Official Answer 和上面的代码一样"
    "还有一种如下(这种是正常遍历树中的所有节点,需要循环次数较多)"
    for b in t.branches:
        cumulative_mul(b)
    total = t.label
    for b in t.branches:
        total *= b.label
    t.label = total


def every_other(s):
    """Mutates a linked list so that all the odd-indiced elements are removed
    (using 0-based indexing).

    >>> s = Link(1, Link(2, Link(3, Link(4))))
    >>> every_other(s)
    >>> s
    Link(1, Link(3))
    >>> odd_length = Link(5, Link(3, Link(1)))
    >>> every_other(odd_length)
    >>> odd_length
    Link(5, Link(1))
    >>> singleton = Link(4)
    >>> every_other(singleton)
    >>> singleton
    Link(4)
    """
    "*** YOUR CODE HERE ***"
    "这一道题可以作为链表的移除值例题"
    "我觉得还是会用到递归 (..•˘_˘•..) (好像是废话)"
    if s.rest == Link.empty or s == Link.empty:
        return
    else:
        s.rest = s.rest.rest
        s.rest.rest = Link.empty
    "Official Answer 就是将上面的代码的最后一行改为every_other(s.rest)"

    """以上代码也仅仅是为应付测试用的,优化一下以上代码,仔细想想,
    即可得出递归形式,如下所示(这个很妙啊!!!)"""
    if s is not Link.empty and s.rest is not Link.empty:
        s.rest = s.rest.rest
        every_other(s.rest)



def prune_small(t, n):
    """Prune the tree mutatively, keeping only the n branches
    of each node with the smallest labels.

    >>> t1 = Tree(6)
    >>> prune_small(t1, 2)
    >>> t1
    Tree(6)
    >>> t2 = Tree(6, [Tree(3), Tree(4)])
    >>> prune_small(t2, 1)
    >>> t2
    Tree(6, [Tree(3)])
    >>> t3 = Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2), Tree(3)]), Tree(5, [Tree(3), Tree(4)])])
    >>> prune_small(t3, 2)
    >>> t3
    Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])
    """
    "这一道题可以作为树的移除分支例题"
    "Perfect Answer 和答案一模一样"
    while len(t.branches) > n:
        largest = max(t.branches, key=lambda x: x.label)# 这个key的启发是在网上搜关于max函数的key的用法时看到的,很妙!
        t.branches = [b for b in t.branches if b != largest] # 这个也很关键,用这么巧妙的办法将树的一个分支删除掉
    for b in t.branches:
        prune_small(b, n)


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
