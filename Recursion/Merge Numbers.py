def merge(n1, n2):
    """ Merges two numbers by digit in decreasing order

    >>> merge(31, 42)
    4321
    >>> merge(21, 0)
    21
    >>> merge (21, 31)
    3211
    """
    "*** YOUR CODE HERE ***"
    # if n1 == 0:
    #     return n2
    # elif n2 == 0:
    #     return n1
    # elif n1 % 10 < n2 % 10:
    #     return merge(n1 // 10, n2) * 10 + n1 % 10
    # else:
    #     return merge(n1, n2 // 10) * 10 + n2 % 10
    if n1 > 0 and n2 > 0:
        if n1 % 10 < n2 % 10:
            return n1 % 10 + 10 * (n2 % 10) + 100 * merge(n1 // 10, n2 // 10)
        else:
            return n2 % 10 + 10 * (n1 % 10) + 100 * merge(n1 // 10, n2 // 10)
    if n1 == 0 and n2 == 0:
        return 0
    elif n1 == 0:
        return n2
    elif n2 == 0:
        return n1


print(merge(13, 24))
