def num_eights(pos):
    if pos == 0:
        return 0
    if (pos % 10) == 8:
        return 1 + num_eights(pos // 10)
    return num_eights(pos // 10)


def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(8)
    8
    >>> pingpong(10)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    -2
    >>> pingpong(30)
    -2
    >>> pingpong(68)
    0
    >>> pingpong(69)
    -1
    >>> pingpong(80)
    0
    >>> pingpong(81)
    1
    >>> pingpong(82)
    0
    >>> pingpong(100)
    -6
    """
    "*** YOUR CODE HERE ***"

    # 递归
    def f(x):  # 向上加
        if x == n:
            return 0
        if num_eights(x) >= 1 or x % 8 == 0:
            return g(x + 1) - 1
        return 1 + f(x + 1)

    def g(x):  # 向下减
        if x == n:
            return 0
        if num_eights(x) >= 1 or x % 8 == 0:
            return f(x + 1) + 1
        return g(x + 1) - 1

    return 1 + f(1)



