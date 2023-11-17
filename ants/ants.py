"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        "有点类似于链表,不完全一样,如果左边有格子的话,左边格子的右边等于该实例"
        if self.exit:
            self.exit.entrance=self
        "others"
        if exit:
            exit.entrance=self
        # END Problem 2

    def add_insect(self, insect):
        """
        Asks the insect to add itself to the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """
        Asks the insect to remove itself from the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    is_waterproof=False
    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place  # set by Place.add_insect and Place.remove_insect

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.

         test_insect = Insect(5)
         test_insect.reduce_health(2)
         test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0 or self.place==None:
            self.death_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn.

        gamestate -- The GameState, used to access game state information.
        """

    def death_callback(self):
        # overriden by the gui
        pass

    def add_to(self, place):
        """Add this Insect to the given Place

        By default just sets the place attribute, but this should be overriden in the subclasses
            to manipulate the relevant attributes of Place
        """
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    # ADD CLASS ATTRIBUTES HERE
    flag=False
    blocks_path=True

    def __init__(self, health=1):
        """Create an Insect with a HEALTH quantity."""
        super().__init__(health)

    @classmethod
    def construct(cls, gamestate):
        """Create an Ant for a given GameState, or return None if not possible."""
        if cls.food_cost > gamestate.food:
            print('Not enough food remains to place ' + cls.__name__)
            return
        return cls()

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place): # self指的是要加进去的蚂蚁
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            """后面那句话是确定加进去的蚂蚁和原来的蚂蚁肯定有一个是容器蚂蚁,否则就会引发错误"""
            assert ((place.ant is None) 
            or self.can_contain(place.ant)
            or place.ant.can_contain(self)), 'Two ants in {0}'.format(place)
            if self.is_container and not place.ant.can_contain(self): # 说明原来在这个位置上的蚂蚁不是容器蚂蚁
                self.store_ant(place.ant)
                place.ant=self #如果特定 Place 中有两只蚂蚁,则 Place 实例的 ant 属性应引用容器蚂蚁,并且容器蚂蚁应包含非容器蚂蚁.
            elif place.ant.can_contain(self) and place.ant.is_container: # 说明原来在这个位置上面的是容器蚂蚁
                place.ant.store_ant(self)
            # else:#还有一种方法是将上面的断言取去掉,将断言放在这个位置(我也不知道为啥)
            #     assert False,'Two ants in {0}'.format(place)
            #     或者assert place.ant is None,'Two ants in {0}'.format(place)
        
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled."""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        if not self.flag:
            self.damage*=2
            self.flag=True
        # END Problem 12


class HarvesterAnt(Ant): # 向日葵(SunFlower)
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost=2
    
    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        "This is not difficult"
        gamestate.food+=1
        # END Problem 1


class ThrowerAnt(Ant): #豌豆射手类
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost=3
    lower_bound=0
    upper_bound=float('inf')

    def nearest_bee(self,beehive=0):# beehive这里指的是距离
        """Return the nearest Bee in a Place that is not the HIVE, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN Problem 3 and 4
        """我写的这个不是很简单,第三问的话还行,
        用循环来实现逐步检查前面的格子是否有蜜蜂,如果有就进行攻击,直到蜂巢
        Example:
        attack_place=self.place #它的攻击格子
        while attack_place.is_hive!=True:
            if attack_place.bees:
                return random_bee(attack_place.bees)
            attack_place=attack_place.entrance
        retur None # 记住如果没有要返回None
        """
        """第四问就开始上难度了,要设计两种不同射程的蚂蚁,最主要的是要读明白题干
        Make sure to give these lower_bound and upper_bound attributes appropriate 
        values in the ThrowerAnt class so that the behavior of ThrowerAnt is unchanged.
        翻译成中文可能不是很能理解,大致就是要在该类中添加这两个属性lower_bound和upper_bound
        且不影响第三问的作答,我一开始没明白一直在子类中添加这两个属性,导致一直通不过,
        后来看了网上的才知道是这个意思,就很离谱,还有
        You should not need to repeat any code between ThrowerAnt, ShortThrower, and LongThrower.
        这句话的意思是只需要更改ThrowerAnt类,而他继承的子类中只需要添加对应的范围即可,不能重写方法,
        这我一开始也没搞明白,在这道题上面花费了很多时间,搞明白题干,就很容易做出来了
        """
        self.range=beehive # 蜜蜂离它的距离
        attack_place=self.place #它的攻击格子
        while attack_place.is_hive!=True:# 攻击格子不是蜂巢的话
            if attack_place.bees and self.lower_bound<=self.range<=self.upper_bound: #存在蜜蜂且在攻击范围内才可以攻击得到
                return random_bee(attack_place.bees)
            attack_place=attack_place.entrance
            self.range+=1
        return None
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt): #小喷菇
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    upper_bound=3 # 添加的属性
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    # END Problem 4

"""说实话,这个第四个问题我感到很疑惑,为什么不用继承就直接可以通过测试
可能是我没有搞明白原文中
You should not need to repeat any code between ThrowerAnt, ShortThrower, and LongThrower.
这段话的含义,可能就是让我只改problem3就可以了,
亏我之前还一直耗费时间,裂开来"""
class LongThrower(ThrowerAnt):# 胆小菇
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    lower_bound=5 # 添加的属性
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    # END Problem 4


class FireAnt(Ant): #这个有点像杂合体,窝瓜升级版？
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    # END Problem 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount): # 蜜蜂对它造成几点伤害,它反击所有蜜蜂几点伤害,死亡时额外增加三点伤害
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        "如果调用self.reduce_health的话就会一直在当前函数中循环,形成死循环"
        """因为当前格子的所有蜜蜂是一个list,
        我们们可能要在迭代访问 list 的时候修改这个 list(有些蜜蜂会死亡),
        所以遍历它的拷贝即可"""

        # 它对他所在位置蜜蜂进行的攻击
        for bee in self.place.bees[:]:
            bee.reduce_health(amount)

        # 如果遭受攻击而死亡的话
        if self.health<=amount:
            for bee in self.place.bees[:]:
                bee.reduce_health(self.damage)#先造成伤害,再死亡
        super().reduce_health(amount) 
        # END Problem 5

# BEGIN Problem 6
# The WallAnt class
"没什么难度"
class WallAnt(Ant): #坚果
    name='Wall'
    damage=0
    food_cost=4
    implemented=True

    def __init__(self, health=4):
        super().__init__(health)

# END Problem 6

# BEGIN Problem 7
# The HungryAnt Class
"和射手蚂蚁的方法有些类似,可以借鉴.因为两个都是攻击随机的一只蜜蜂"
class HungryAnt(Ant):# 食人花
    """which will select a random Bee from its place and deal damage to the Bee by eating it whole.
    After eating a Bee, a HungryAnt must spend 3 turns chewing before being able to eat again."""
   
    name='Hungry'
    food_cost=4
    implemented=True
    chewing_turns=3

    def __init__(self, health=1):
        super().__init__(health)
        self.turns_to_chew=0 #刚开始是可以吃蜜蜂的,因为不需要咀嚼
        
    def action(self, gamestate):
        if self.turns_to_chew>0:
            self.turns_to_chew-=1
        elif self.turns_to_chew==0:
            chewed_bee=random_bee(self.place.bees)
            if chewed_bee:
                chewed_bee.reduce_health(chewed_bee.health)
                self.turns_to_chew=self.chewing_turns

# END Problem 7


class ContainerAnt(Ant): #南瓜罩
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # if self.ant_contained==None and not other.is_container:
        #     return True
        # return False
        "将上面的代码简化如下"
        return self.ant_contained==None and not other.is_container
        # END Problem 8a

    def store_ant(self, ant):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        self.ant_contained=ant
        # END Problem 8a

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants (this is optional)
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        if self.ant_contained:
            self.ant_contained.action(gamestate)
        # END Problem 8a


class BodyguardAnt(ContainerAnt): #南瓜罩
    """BodyguardAnt provides protection to other Ants."""

    name = 'Bodyguard'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 8c
    implemented = True   # Change to True to view in the GUI

    """这里我也不明白为什么它在ok测试中健康值是2,题目中没说啊
    仿照problem6写的,好像大家都这样写  (⊙.⊙)  """
    def __init__(self, health=2):
        return super().__init__(health)
    # END Problem 8c

# BEGIN Problem 9
# The TankAnt class
class TankAnt(ContainerAnt): #有点像近战版火炬树桩？
    name='Tank'
    food_cost=6
    implemented=True
    damage=1
    is_container=True
    def __init__(self, health=2):
        super().__init__(health)

    "这个就仿照FireAnt来写就可以"
    def action(self, gamestate):
        for bee in self.place.bees[:]:
            bee.reduce_health(self.damage)
        super().action(gamestate)
# END Problem 9


class Water(Place): #池塘
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        super().add_insect(insect) #无论是否防水,都将昆虫添加到该地方
        if not insect.is_waterproof: # 不防水就die
            insect.reduce_health(insect.health)
        # END Problem 10

# BEGIN Problem 11
# The ScubaThrower class
"很简单"
class ScubaThrower(ThrowerAnt): # 水上豌豆射手
    name='Scuba'
    food_cost=6
    implemented=True
    is_waterproof=True

# END Problem 11

# BEGIN Problem 12
"""这个就很有难度了
三个规则：
1. 蚁后一死,游戏结束(Game Over)
2.一局中只能有一个蚁后
3.蚁后不可以被铲除,一旦放好位置便无法移动
这应该算什么？没有对应的植物 (⊙.⊙)"""
class QueenAnt(ScubaThrower):  # You should change this line
# END Problem 12
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 12
    implemented = True   # Change to True to view in the GUI
    # END Problem 12

    def __init__(self, health=1):
        super().__init__(health)

    "(Rule 2)这是这个问题中最难处理的部分(我觉得,因为不了解cls,哪怕他说了我还是迷迷糊糊的.),是去网上COPY的"
    @classmethod
    def construct(cls, gamestate):
        """
        Returns a new instance of the Ant class if it is possible to construct, or
        returns None otherwise. Remember to call the construct() method of the superclass!
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        """这一块还得再Gamestate中添加实例变量"""
        if not gamestate.queen_ant: #如果不存在蚁后
            gamestate.queen_ant_created()
            return super().construct(gamestate)
        else:
            return None
        # END Problem 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        super().action(gamestate) #因为蚁后继承了水上蚂蚁,所以需要用到super关键字继承
        """接下来的就是将所有蚂蚁的伤害加倍,因为place所指的是容器蚂蚁(如果有的话),
        所以也需要把内部蚂蚁的伤害也加强"""
        behind_place=self.place.exit
        while behind_place:
            place_ant=behind_place.ant
            if place_ant:
                place_ant.double()
                if place_ant.is_container and place_ant.ant_contained:
                    place_ant.ant_contained.double()
            behind_place=behind_place.exit
        # END Problem 12

    "(Rule 1)扣除生命值和之前一样,唯一不同的是,一旦蚁后死亡,游戏就会结束"
    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        if self.health<=amount:
            super().reduce_health(amount)
            ants_lose()
        # END Problem 12

    "(Rule 3)蚁后不可以被铲除,所以返回None,或者直接pass"
    def remove_from(self, place):
        return None


class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        super().__init__(0)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    is_waterproof=True
    blocks_path=False

    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN Problem Optional 1
        return self.place.ant is not None and self.place.ant.blocks_path
        # END Problem Optional 1

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit

        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        Insect.add_to(self, place)

    def remove_from(self, place):
        place.bees.remove(self)
        Insect.remove_from(self, place)


############
# Optional #
############

class NinjaAnt(Ant): # 地刺
    """NinjaAnt does not block the path and damages all bees in its place.
    This class is optional.
    """

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    blocks_path=False
    # BEGIN Problem Optional 1
    implemented = True   # Change to True to view in the GUI
    # END Problem Optional 1

    "这个也不难,会写FireAnt就都差不多了"
    def action(self, gamestate):
        # BEGIN Problem Optional 1
        "*** YOUR CODE HERE ***"
        if self.place.bees:
            for bee in self.place.bees[:]:
                bee.reduce_health(self.damage)
        else:
            return None
        # END Problem Optional 1

############
# Statuses #
############

"这个我感觉难度也挺大的,没有那么简单"
class SlowThrower(ThrowerAnt): #寒冰射手
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC
    implemented = False   # Change to True to view in the GUI
    damage=0
    slow_turninng=5 #减速的回合
    # END Problem EC

    def throw_at(self, target):
        
        # BEGIN Problem EC
        "*** YOUR CODE HERE ***"
        "这是网上copy的,看的明白,写不出来 (╥╯^╰╥)"
        def target_action(gamestate):
            self.slow_turninng-=1
            if gamestate.time%2==0 or self.slow_turninng<0:
                Bee.action(target,gamestate)
        if target is not None:
            self.slow_turninng=5
            target.action=target_action
        # END Problem EC


class LaserAnt(ThrowerAnt): #也没有对应的植物,机关蚂蚁？
    # This class is optional. Only one test is provided for this class.

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem Optional 2
    implemented = True   # Change to True to view in the GUI
    damage=2
    # END Problem Optional 2

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    "这一问倒是不难,将所有昆虫(不论是蚂蚁还是蜜蜂)都加进字典就完事"
    def insects_in_front(self):
        # BEGIN Problem Optional 2
        distance=0
        insect_front={}
        infront_place=self.place
        while not infront_place.is_hive:
            if infront_place.bees:
                for bee in infront_place.bees:
                    insect_front[bee]=distance
            if infront_place.ant and infront_place.ant is not self:# 注意这一点,不要把它自己加进去,要不然伤害会降低
                insect_front[infront_place.ant]=distance
            distance+=1
            infront_place=infront_place.entrance
        return insect_front
        # END Problem Optional 2

    def calculate_damage(self, distance):
        # BEGIN Problem Optional 2
        "它提供一个insects_shot就很方便,不用我们再去计算经过的昆虫有多少只"
        move_down_damage=0.25
        cause_down_damage=0.0625
        total_damage=self.damage-move_down_damage*distance-cause_down_damage*self.insects_shot
        if total_damage<0:
            return 0
        else:
            return total_damage

        # END Problem Optional 2

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1



##################
# Bees Extension #
##################

class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2


class Hornet(Bee):
    """Class of bee that is capable of taking two actions per turn, although
    its overall damage output is lower. Immune to statuses.
    """
    name = 'Hornet'
    damage = 0.25

    def action(self, gamestate):
        for i in range(2):
            if self.health > 0:
                super().action(gamestate)

    def __setattr__(self, name, value):
        if name != 'action':
            object.__setattr__(self, name, value)


class NinjaBee(Bee):
    """A Bee that cannot be blocked. Is capable of moving past all defenses to
    assassinate the Queen.
    """
    name = 'NinjaBee'

    def blocked(self):
        return False


class Boss(Wasp, Hornet):
    """The leader of the bees. Combines the high damage of the Wasp along with
    status immunity of Hornets. Damage to the boss is capped up to 8
    damage by a single attack.
    """
    name = 'Boss'
    damage_cap = 8
    action = Wasp.action

    def reduce_health(self, amount):
        super().reduce_health(self.damage_modifier(amount))

    def damage_modifier(self, amount):
        return amount * self.damage_cap / (self.damage_cap + amount)


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)


class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        self.queen_ant=False # 是否存在蚁后
        # END Problem 12

    def queen_ant_exists(self):# 蚁后存在
        return self.queen_ant
    
    def queen_ant_created(self): #创造蚁后
        self.queen_ant=True

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place, self.dimensions[0], self.dimensions[1])

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self)         # Bees invade
                self.strategy(self)                 # Ants deploy
                for ant in self.ants:               # Ants take actions
                    if ant.health > 0:
                        ant.action(self)
                for bee in self.active_bees[:]:     # Bees take actions
                    if bee.health > 0:
                        bee.action(self)
                    if bee.health <= 0:
                        num_bees -= 1
                        self.active_bees.remove(bee)
                if num_bees == 0:
                    raise AntsWinException()
                self.time += 1
        except AntsWinException:
            print('All bees are vanquished. You win!')
            return True
        except AntsLoseException:
            print('The ant queen has perished. Please try again.')
            return False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        ant = ant_type.construct(self)
        if ant:
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


def interactive_strategy(gamestate):
    """A strategy that starts an interactive session and lets the user make
    changes to the gamestate.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    gamestate.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('gamestate: ' + str(gamestate))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

     AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]
