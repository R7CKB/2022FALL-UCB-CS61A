"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact
from math import log2

GOAL = 100  # The goal of Hog is to score 100 points. 目标是100分


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.
    模拟掷骰子精确NUM_ROLLS > 0 次。返回结果，除非任何结果为 1。在这种情况下,返回 1。

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    num_rolls,将进行的掷骰子次数。
    骰子：模拟单个掷骰子结果的函数。
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    score=0
    flag=False
    for i in range(num_rolls):
        number=dice() # 要理解dice()返回每回合掷的骰子数
        if number==1:
            flag=True
        else:
            score+=number
    if flag:
        score=1
    return score
    # END PROBLEM 1


def tail_points(opponent_score):
    """Return the points scored by rolling 0 dice according to Pig Tail.
    根据猪尾巴返回掷0骰子获得的分数。
    opponent_score:   The total score of the other player.
    opponent_score:其他玩家的总分。
    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    single_digit=opponent_score%10
    ten_digit=(opponent_score//10)%10
    score=2*abs(single_digit-ten_digit)+1
    return score
    # simipify it
    return 2 * abs(opponent_score % 10 - (opponent_score // 10) % 10) + 1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    opponent has OPPONENT_SCORE points.
    返回在掷骰子回合时获得的分数NUM_ROLLS
    对手有OPPONENT_SCORE分。
    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    num_rolls:将进行的掷骰子次数。
    opponent_score:其他玩家的总分。
    骰子：模拟单个掷骰子结果的函数。
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls==0:
        return tail_points(opponent_score)
    return roll_dice(num_rolls,dice)
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Square Swine.

    
    """
    return player_score + take_turn(num_rolls, opponent_score, dice)


def square_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Square Swine.

    """
    score = player_score + take_turn(num_rolls, opponent_score, dice)
    if perfect_square(score):  # Implement perfect_square
        return next_perfect_square(score)  # Implement next_perfect_square
    else:
        return score


# BEGIN PROBLEM 4
"*** YOUR CODE HERE ***"
def perfect_square(score):
    for i in range(1,31):# 这个range无所谓，保证平方和大于100即可
        if i*i==score:
            return True
    return False
    # more simple way
    return any(i * i == score for i in range(1, 31))
def next_perfect_square(score):
    for i in range(1,31):
        if i*i==score:
            return (i+1)**2
# END PROBLEM 4


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the oppononent's score.
    始终掷出 5 个骰子的策略，无论玩家的分数如何或
    对方的分数。
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.
    模拟游戏并返回两个玩家的最终得分，使用
    玩家 0 得分第一，玩家 1 得分第二。

    E.g., play(always_roll_5, always_roll_5, square_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Square
    Swine rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.
    策略函数(例如always_roll_5)采用当前玩家的分数和对手的分数，并返回当前骰子的数量玩家选择滚动。

    An update function, such as square_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.
    更新功能(如square_update或simple_update)获取数字
    掷骰子、当前玩家的分数、对手的分数和
    用于模拟掷骰子的骰子功能。它返回更新的分数
    轮到当前玩家后。

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    while (score0<goal and score1<goal):
        if who==0:
            num_rolls=strategy0(score0,score1)
            score0=update(num_rolls,score0,score1,dice)
            who=1
        else:
            num_rolls=strategy1(score1,score0)
            score1=update(num_rolls,score1,score0,dice)
            who=0
    return score0, score1
    # END PROBLEM 5
    


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    def unsign(score0,score1):
        return n
    return unsign # 闭包函数
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether strategy always chooses the same number of dice to roll.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    '''采用自己的方法，将收集到的所有点数存进一个列表
    再将列表转化为一个集合,如集合元素大于2,则证明采取的策略不是同一个数字的'''
    list1 = []
    for score in range(goal):
        for opponent_score in range(goal):
            number = strategy(score, opponent_score)
            list1.append(number)
    length = len(set(list1))
    if length >= 2:
        return False
    return True
    # END PROBLEM 7


def make_averaged(original_function, total_samples=100):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    '''这道题就自然而然就出来了,我也不怎么明白为什么'''
    def function1(*args):
        total=0
        for _ in range(total_samples):
            total+=original_function(*args)
        return total/total_samples
    return function1
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, total_samples=100):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return positive outcomes.
    返回提供最高平均回合分数的骰子数(1 到 10)
    使用提供的 DICE 呼叫roll_dice总共 TOTAL_SAMPLES 次。
    假设骰子总是返回积极的结果。

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    '''正是因为上一道题的不怎么理解，导致这一道题也不怎么理解
    应该还是要看上一题的doctest,把上一问的注释和测试看懂就明白这道题的意思了'''
    list1 = []
    for num_rolls in range(1, 11):
        average = make_averaged(roll_dice, total_samples)(num_rolls, dice)
        list1.append(average)
    return list1.index(max(list1))+1
        # average1=total/i
        # average2=make_averaged(roll_dice)(i)
        # if average1==average2:
        #     return i
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, square_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))  # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('tail_strategy win rate:', average_win_rate(tail_strategy))
    print('square_strategy win rate:', average_win_rate(square_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def tail_strategy(score, opponent_score, threshold=12, num_rolls=6):
    """This strategy returns 0 dice if Pig Tail gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Square Swine.
    如果猪尾巴至少给出阈值，则此策略返回 0 个骰子点,否则返回NUM_ROLLS。忽略分数和方形猪。
    
    """
    # BEGIN PROBLEM 10
    if tail_points(opponent_score)>=threshold:
        return 0
    return num_rolls
    # END PROBLEM 10


def square_strategy(score, opponent_score, threshold=12, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    # BEGIN PROBLEM 11
    get_score=tail_points(opponent_score)
    final_score=get_score+score
    if get_score>=threshold or perfect_square(final_score):
        score=square_update(0,final_score,opponent_score)
        return 0
    else:
        return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
