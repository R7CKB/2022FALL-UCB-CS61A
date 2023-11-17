def is_prime(n):
    """Returns True if n is a prime number and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    >>> is_prime(1001)
    False
    >>> is_prime(999)
    False
    >>> is_prime(7)
    True
    """
    "*** YOUR CODE HERE ***"

    # 迭代
    # if n == 1:
    #     return False
    # else:
    #     for i in range(2, n // 2):
    #         if n % i == 0:
    #             return False
    #     return True
    def f(m, x):  # 素数只能被1和它自身整除
        if x == 1:
            return True
        elif m % x == 0:
            return False
        return f(m, x - 1)

    return f(n, n - 1) if n >= 2 else False
