def insert_into_all(item, nested_list):
    """Return a new list consisting of all the lists in nested_list,
    but with item added to the front of each. You can assume that
     nested_list is a list of lists.

    >>> nl = [[], [1, 2], [3]]
    >>> insert_into_all(0, nl)
    [[0], [0, 1, 2], [0, 3]]
    """
    "*** YOUR CODE HERE ***"
    for elem in nested_list:
        elem.insert(0, item)
    return nested_list

    # Another Solution
    new_nested_list = [elem[:0] + [item] + elem[0:] for elem in nested_list]
    return new_nested_list


def subseqs(s):
    """Return a nested list (a list of lists) of all subsequences of S.
    The subsequences can appear in any order. You can assume S is a list.

    >>> seqs = subseqs([1, 2, 3])
    >>> sorted(seqs)
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    >>> subseqs([])
    [[]]
    """
    """cheated
    不知道如何将上面的那个函数与下面的这个结合起来用
    说实话,这第一道题就给我难住了,有点离谱啊 (┳◇┳)
    看完答案后,才算是理解了一点点,这道题的详细步骤可以在Python Tutor里面过一遍流程,
    或者自己拿笔画一下,就知道怎么做出来的了,有点类似于树递归,最终呈现出来的结果就像树一样"""
    if not s: # 根据上面的文档测试知道这个肯定是递归终止条件
        return [[]]
    else: # 但是下面的return语句就没那么好写了，只能说，对递归还不是太掌握  ,,Ծ‸Ծ,,
        first = s[0]
        return insert_into_all(first, subseqs(s[1:])) + subseqs(s[1:])
        

def non_decrease_subseqs(s):
    """Assuming that S is a list, return a nested list of all subsequences
    of S (a list of lists) for which the elements of the subsequence
    are strictly nondecreasing. The subsequences can appear in any order.

    >>> seqs = non_decrease_subseqs([1, 3, 2])
    >>> sorted(seqs)
    [[], [1], [1, 2], [1, 3], [2], [3]]
    >>> non_decrease_subseqs([])
    [[]]
    >>> seqs2 = non_decrease_subseqs([1, 1, 2])
    >>> sorted(seqs2)
    [[], [1], [1], [1, 1], [1, 1, 2], [1, 2], [1, 2], [2]]
    """
    """cheated
    这一题看上去好像和上面那个差不多,但实际上还是有差别的(废话文学)
    比第一题更加复杂一点,但仔细研究会发现和第一题逻辑一样,还是有难度
    """
    def subseq_helper(s, prev):  
        if not s:
            return [[]]
        elif s[0] < prev: # 如果第二个数小于第一个数,就只要第二个数的排列
            return subseq_helper(s[1:], prev)
        else:
            a = subseq_helper(s[1:], s[0])
            b = subseq_helper(s[1:], prev)
            return insert_into_all(s[0], a) + b

    return subseq_helper(s, 0) # 因为s传入的列表仅包含非负元素，所以可以用0，要不然的话应该是-float('inf')




def num_trees(n):
    """Returns the number of unique full binary trees with exactly n leaves. E.g.,
    返回具有n个叶子节点的满二叉树的数量
    
    1   2        3       3    ...
    *   *        *       *
       / \      / \     / \
      *   *    *   *   *   *
              / \         / \
             *   *       *   *

    >>> num_trees(1)
    1
    >>> num_trees(2)
    1
    >>> num_trees(3)
    2
    >>> num_trees(4)
    5
    >>> num_trees(5)
    14
    >>> num_trees(8)
    429

    """
    "*** YOUR CODE HERE ***"
    """cheated
    国内和国际定义的满二叉树的定义还不一样,
    国外是满二叉树的任意节点,要么度为0,要么度为2.
    换个说法即要么为叶子结点,要么同时具有左右孩子。
    国内是满二叉树除最后一层无任何子节点外,每一层上的所有结点都有两个子结点二叉树
    所以搜了半天并没有搜索到我满意的答案
    根据这道题提供的链接,这个数是Catalan数???
    md实在想不出来了,脑子要炸了,服了,咋还和数学扯上关系了,就很离谱
    网上也看了视频,看了帖子,没看到这种做法
    """

    if n == 1:
        return 1
    return sum(num_trees(k) * num_trees(n - k) for k in range(1, n))


def partition_gen(n):
    """
    >>> for partition in partition_gen(4): # note: order doesn't matter
    ...     print(partition)
    [4]
    [3, 1]
    [2, 2]
    [2, 1, 1]
    [1, 1, 1, 1]
    """
    """cheated
    这道题就和上楼梯的那道题很相似了,还是递归,我这辈子和递归有仇
    但在if判断和yield语句上不是怎么会
    """
    def yield_helper(j, k):
        if j == 0:
            yield []
        elif k > 0 and j > 0:
            for small_part in yield_helper(j - k, k):
                yield [k] + small_part
            yield from yield_helper(j, k - 1)

    yield from yield_helper(n, n)


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please update your balance with $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please update your balance with $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    "*** YOUR CODE HERE ***"
    """总算有一个能自己写出来的了,我哭死 呜呜呜呜  ╥﹏╥"""
    def __init__(self, goods, price) -> None:
        self.goods = goods
        self.price = price
        self.inventory = 0
        self.balance = 0

    def vend(self): # 答案和我的有些不也一样,不过问题不大
        if self.inventory == 0:
            return 'Nothing left to vend. Please restock.'
        if self.balance < self.price:
            return f'Please update your balance with ${10 - self.balance} more funds.'
        elif self.balance > self.price:
            self.inventory -= 1
            print(f'\'Here is your {self.goods} and ${self.balance - 10} change.\'')
            self.balance = 0
        else:
            self.inventory -= 1
            return f'Here is your {self.goods}.'

    def restock(self, amount):
        self.inventory += amount
        return f'Current {self.goods} stock: {self.inventory}'

    def add_funds(self, money):
        if self.inventory == 0:
            return self.vend() + f' Here is your ${money}.'
        self.balance += money
        return f'Current balance: ${self.balance}'



def trade(first, second):
    """Exchange the smallest prefixes of first and second that have equal sum.

    >>> a = [1, 1, 3, 2, 1, 1, 4]
    >>> b = [4, 3, 2, 7]
    >>> trade(a, b) # Trades 1+1+3+2=7 for 4+3=7
    'Deal!'
    >>> a
    [4, 3, 1, 1, 4]
    >>> b
    [1, 1, 3, 2, 2, 7]
    >>> c = [3, 3, 2, 4, 1]
    >>> trade(b, c)
    'No deal!'
    >>> b
    [1, 1, 3, 2, 2, 7]
    >>> c
    [3, 3, 2, 4, 1]
    >>> trade(a, c)
    'Deal!'
    >>> a
    [3, 3, 2, 1, 4]
    >>> b
    [1, 1, 3, 2, 2, 7]
    >>> c
    [4, 3, 1, 4, 1]
    >>> d = [1, 1]
    >>> e = [2]
    >>> trade(d, e)
    'Deal!'
    >>> d
    [2]
    >>> e
    [1, 1]
    """
    """这道题和之前的递归比起来难度就差很多了,不难想出答案
    Perfect Answer 和答案一模一样"""
    m, n = 1, 1

    equal_prefix = lambda: sum(first[:m]) == sum(second[:n])
    while not equal_prefix() and m <= len(first) and n <= len(second):
        if sum(first[:m]) < sum(second[:n]):
            m += 1
        else:
            n += 1

    if equal_prefix():
        first[:m], second[:n] = second[:n], first[:m]
        return 'Deal!'
    else:
        return 'No deal!'


def card(n):
    """Return the playing card numeral as a string for a positive n <= 13."""
    assert type(n) == int and n > 0 and n <= 13, "Bad card n"
    specials = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    return specials.get(n, str(n))


def shuffle(cards):
    """Return a shuffled list that interleaves the two halves of cards.

    >>> shuffle(range(6))
    [0, 3, 1, 4, 2, 5]
    >>> suits = ['H', 'D', 'S', 'C']
    >>> cards = [card(n) + suit for n in range(1,14) for suit in suits]
    >>> cards[:12]
    ['AH', 'AD', 'AS', 'AC', '2H', '2D', '2S', '2C', '3H', '3D', '3S', '3C']
    >>> cards[26:30]
    ['7S', '7C', '8H', '8D']
    >>> shuffle(cards)[:12]
    ['AH', '7S', 'AD', '7C', 'AS', '8H', 'AC', '8D', '2H', '8S', '2D', '8C']
    >>> shuffle(shuffle(cards))[:12]
    ['AH', '4D', '7S', '10C', 'AD', '4S', '7C', 'JH', 'AS', '4C', '8H', 'JD']
    >>> cards[:12]  # Should not be changed
    ['AH', 'AD', 'AS', 'AC', '2H', '2D', '2S', '2C', '3H', '3D', '3S', '3C']
    """
    """轻松解决,哈哈哈哈哈  (●′ϖ`●)  
    答案和我思路一样,只不过答案没有将half转化为列表"""
    assert len(cards) % 2 == 0, 'len(cards) must be even'
    half = list(cards)[:len(list(cards))//2]
    shuffled = []
    for i in half:
        shuffled.append(i)
        shuffled.append(cards[cards.index(i) + len(half)])
    return shuffled


def insert(link, value, index):
    """Insert a value into a Link at the given index.

    >>> link = Link(1, Link(2, Link(3)))
    >>> print(link)
    <1 2 3>
    >>> other_link = link
    >>> insert(link, 9001, 0)
    >>> print(link)
    <9001 1 2 3>
    >>> link is other_link # Make sure you are using mutation! Don't create a new linked list.
    True
    >>> insert(link, 100, 2)
    >>> print(link)
    <9001 1 100 2 3>
    >>> insert(link, 4, 5)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds!
    """
    "*** YOUR CODE HERE ***"
    """这道题也不难,仔细思考就可以得出结果"""
    "先计算链表的长度"
    def length_link(s):
        length = 0
        while s is not Link.empty:
            length += 1
            s = s.rest
        return length

    length = length_link(link)
    if index >= length:
        raise IndexError('Out of bounds!')
    for i in range(length):
        if i == index:
            link.first, link.rest = value, Link(link.first, link.rest)
            break
        link = link.rest # 因为链表特殊的数据结构,所以可以这样操作
    # 或者是下列方法,不用计算长度,更简单
    length = 0
    while link is not Link.empty:
        if length == index:
            link.first, link.rest = value, Link(link.first, link.rest)
            return
        link = link.rest
        length += 1
    raise IndexError('Out of bounds!')

    """Official Answer 答案又用到了递归,但也不难理解"""
    if index == 0:
        link.rest = Link(link.first, link.rest)
        link.first = value
    elif link.rest is Link.empty:
        raise IndexError("Out of bounds!")
    else:
        insert(link.rest, value, index - 1)

    """还有一种迭代方式"""
    while index > 0 and link.rest is not Link.empty:
        link = link.rest
        index -= 1
    if index == 0:
        link.rest = Link(link.first, link.rest)
        link.first = value
    else:
        raise IndexError("Out of bounds!")



def deep_len(lnk):
    """ Returns the deep length of a possibly deep linked list.

    >>> deep_len(Link(1, Link(2, Link(3))))
    3
    >>> deep_len(Link(Link(1, Link(2)), Link(3, Link(4))))
    4
    >>> levels = Link(Link(Link(1, Link(2)), \
            Link(3)), Link(Link(4), Link(5)))
    >>> print(levels)
    <<<1 2> 3> <4> 5>
    >>> deep_len(levels)
    5
    """
    """这道题应该也是递归,和那个分割数的代码形式好像
    这道题仔细想想也就出来了,不是很难"""
    if lnk is Link.empty:
        return 0
    elif isinstance(lnk, int): # 答案是 elif not isinstance(lnk, Link):(一个意思)
        return 1
    else:
        return deep_len(lnk.first) + deep_len(lnk.rest)


def make_to_string(front, mid, back, empty_repr):
    """ Returns a function that turns linked lists to strings.

    >>> kevins_to_string = make_to_string("[", "|-]-->", "", "[]")
    >>> jerrys_to_string = make_to_string("(", " . ", ")", "()")
    >>> lst = Link(1, Link(2, Link(3, Link(4))))
    >>> kevins_to_string(lst)
    '[1|-]-->[2|-]-->[3|-]-->[4|-]-->[]'
    >>> kevins_to_string(Link.empty)
    '[]'
    >>> jerrys_to_string(lst)
    '(1 . (2 . (3 . (4 . ()))))'
    >>> jerrys_to_string(Link.empty)
    '()'
    """
    """这也算是一个小递归,但是这个递归就比前面的难度小了好多,不会让人一点思路都没有"""
    def printer(lnk):
        if lnk is Link.empty:
            return empty_repr
        else:
            return front+str(lnk.first)+mid+printer(lnk.rest)+back

    return printer


def long_paths(t, n):
    """Return a list of all paths in t with length at least n.

    >>> long_paths(Tree(1), 0)
    [[1]]
    >>> long_paths(Tree(1), 1)
    []
    >>> t = Tree(3, [Tree(4), Tree(4), Tree(5)])
    >>> left = Tree(1, [Tree(2), t])
    >>> mid = Tree(6, [Tree(7, [Tree(8)]), Tree(9)])
    >>> right = Tree(11, [Tree(12, [Tree(13, [Tree(14)])])])
    >>> whole = Tree(0, [left, Tree(13), mid, right])
    >>> print(whole)
    0
      1
        2
        3
          4
          4
          5
      13
      6
        7
          8
        9
      11
        12
          13
            14
    >>> for path in long_paths(whole, 2):
    ...     print(path)
    ...
    [0, 1, 2]
    [0, 1, 3, 4]
    [0, 1, 3, 4]
    [0, 1, 3, 5]
    [0, 6, 7, 8]
    [0, 6, 9]
    [0, 11, 12, 13, 14]
    >>> for path in long_paths(whole, 3):
    ...     print(path)
    ...
    [0, 1, 3, 4]
    [0, 1, 3, 4]
    [0, 1, 3, 5]
    [0, 6, 7, 8]
    [0, 11, 12, 13, 14]
    >>> long_paths(whole, 4)
    [[0, 11, 12, 13, 14]]
    """
    "*** YOUR CODE HERE ***"
    """cheated
    想法:
    
    """
    if n <= 0 and t.is_leaf(): #递归终止条件,满足条件的话就将其作为路径的末尾
      return [[t.label]]
    paths = []
    for b in t.branches:
      for path in long_paths(b, n - 1):
          paths.append([t.label] + path) #将当前节点t的标签添加到每条找到的路径的前面，形成一条完整的路径。
    return paths


def reverse_other(t):
    """Mutates the tree such that nodes on every other (odd-depth)
    level have the labels of their branches all reversed.

    >>> t = Tree(1, [Tree(2), Tree(3), Tree(4)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(4), Tree(3), Tree(2)])
    >>> t = Tree(1, [Tree(2, [Tree(3, [Tree(4), Tree(5)]), Tree(6, [Tree(7)])]), Tree(8)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(8, [Tree(3, [Tree(5), Tree(4)]), Tree(6, [Tree(7)])]), Tree(2)])
    """
    "*** YOUR CODE HERE ***"
    """cheated 
    整体看上去也不难能理解,但自己就是写不出来......
    """
    def reverse_helper(t, need_reverse):
        if t.is_leaf():
            return
        new_labs = [child.label for child in t.branches][::-1] # 将所有子树的标签倒序存储在一个列表中
        for i in range(len(t.branches)):
            child = t.branches[i]
            reverse_helper(child, not need_reverse) # 这个not need——reverse就是奇偶翻转的关键,奇数标签为真,偶数标签为假
            if need_reverse:
                child.label = new_labs[i]
    reverse_helper(t, True)



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
