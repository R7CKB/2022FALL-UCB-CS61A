def next_larger_coin(coin):
    """Returns the next larger coin in order.
    >>> next_larger_coin(1)
    5
    >>> next_larger_coin(5)
    10
    >>> next_larger_coin(10)
    25
    >>> next_larger_coin(2) # Other values return None
    """
    if coin == 1:
        return 5
    elif coin == 5:
        return 10
    elif coin == 10:
        return 25


def next_smaller_coin(coin):
    """Returns the next smaller coin in order.
    >>> next_smaller_coin(25)
    10
    >>> next_smaller_coin(10)
    5
    >>> next_smaller_coin(5)
    1
    >>> next_smaller_coin(2) # Other values return None
    """
    if coin == 25:
        return 10
    elif coin == 10:
        return 5
    elif coin == 5:
        return 1


def count_coins(change):
    """Return the number of ways to make change using coins of value of 1, 5, 10, 25.
    >>> count_coins(15)
    6
    >>> count_coins(10)
    4
    >>> count_coins(20)
    9
    >>> count_coins(100) # How many ways to make change for a dollar?
    242
    >>> count_coins(200)
    1463
    """
    "*** YOUR CODE HERE ***"

    def f(amount, coin):
        if amount == 0:
            return 1
        if amount < 0 or coin is None:
            return 0
        return f(amount - coin, coin) + f(amount, next_smaller_coin(coin))

    return f(change, 25)
    # def f(amount, coin):
    #     if amount == 0:
    #         return 1
    #     if amount < 0 or coin is None:
    #         return 0
    #     return f(amount - coin, coin) + f(amount, next_larger_coin(coin))
    # return f(change, 1)


count_coins(10)
