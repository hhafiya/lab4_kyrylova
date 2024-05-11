"""
NFA for the ROUTINE day in the game
"""
import random
from collections import deque
import time
class States:
    """
    States of the NFA
    """
    def __init__(self):
        """
        Initialize the states
        """
        self.wake_up = 'wake_up'
        self.eat = 'eat'
        self.fight = 'fight'
        self.gather = 'gather'
        self.build = 'build'
        self.sleep = 'sleep'
        self.explore = 'explore'
        self.death = 'death'
        self.dead = 'dead'
        self.wait_for_morning = 'wait_for_morning'

class Transitions:
    """
    Transitions of the NFA
    """
    def __init__(self):
        """
        Initialize the transitions
        """
        self.time_830am = 8.5
        self.time_1230pm = 12.5
        self.time_14pm = 14
        self.time_1430pm = 14.5
        self.time_18pm = 18
        self.time_20pm = 20
        self.time_22pm = 22
        self.health_0 = 0
        self.life_count_0 = 0
        self.life_count_gt0 = 0

class NFA:
    """
    NFA
    """
    def __init__(self):
        """
        Initialize the NFA
        """
        self.states = States()
        self.transitions = Transitions()
        self.state = self.states.wake_up
        self.end_states = [self.states.sleep, self.states.dead]
        self.health = 30
        self.life_count = 3
        self.mob_attack = False
        self.house = False
        self.time_queue = None
        self.wait_for_morning_done = False

    def health_manage(self):
        """
        Manage the health
        """
        if self.state == self.states.eat:
            self.health += 10
            if self.health > 30:
                self.health = 30
        elif self.state == self.states.fight:
            self.health -= 30
            if self.health < 0:
                self.health = 0
        elif self.state == self.states.wake_up:
            self.health += 30
            if self.health > 30:
                self.health = 30
        return self.health

    def life_count_manage(self):
        """
        Manage the life count
        """
        if self.state == self.states.death:
            self.life_count -= 1
        elif self.state == self.states.dead:
            self.life_count = 0
        if self.life_count < 0:
            self.life_count = 0
        return self.life_count

    def random_mob_attack(self):
        """
        Mob attack
        """
        self.mob_attack = random.choice([True, False])
        return self.mob_attack

    def manage_house(self):
        """
        Manage the house
        """
        if self.state == self.states.build:
            self.house = True
        return self.house

    def transition(self, cur_time):
        """
        Transition to the next state
        """
        change = False
        if self.state == self.states.wake_up:
            if cur_time == self.transitions.time_830am:
                self.state = random.choice([self.states.eat, self.states.gather])
                change = True
            elif cur_time == self.transitions.time_14pm:
                self.state = self.states.eat
                change = True

        elif self.state == self.states.eat:
            if cur_time == self.transitions.time_22pm:
                self.state = self.states.sleep
                change = True
            elif cur_time == self.transitions.time_1430pm:
                self.state = self.states.build
                change = True

        elif self.state == self.states.build:
            if cur_time == self.transitions.time_18pm:
                self.state = random.choice([self.states.eat, self.states.explore])
                change = True
            elif cur_time == self.transitions.time_22pm:
                self.state = self.states.sleep
                change = True

        elif self.state == self.states.explore:
            if cur_time == self.transitions.time_20pm and self.mob_attack:
                self.state = self.states.fight
                change = True
            elif cur_time == self.transitions.time_20pm:
                self.state = random.choice([self.states.build, self.states.eat])
                change = True
            elif cur_time == self.transitions.time_22pm:
                self.state = self.states.sleep
                change = True

        elif self.state == self.states.fight:
            if self.health == self.transitions.health_0:
                self.state = self.states.death
                change = True
            elif self.health > self.transitions.health_0:
                self.state = self.states.gather
                change = True

        elif self.state == self.states.gather:
            if cur_time == self.transitions.time_1230pm:
                self.state = random.choice([self.states.eat, self.states.fight])
                change = True
            elif cur_time == self.transitions.time_1230pm and not self.house:
                self.state = self.states.build
                change = True
            elif cur_time == self.transitions.time_22pm:
                self.state = self.states.sleep
                change = True

        elif self.state == self.states.death:
            if self.life_count == self.transitions.life_count_0:
                self.state = self.states.dead
                change = True
            elif self.life_count > self.transitions.life_count_0:
                self.state = self.states.wake_up
                change = True

        return change

    def run(self):
        """
        Run the NFA
        """
        time_range = [(i / 2) % 24 for i in range(16, 64)]
        prev_state = None
        while self.state not in self.end_states:
            if not self.time_queue: 
                self.time_queue = deque(time_range)
            cur_time = self.time_queue.popleft()
            # time.sleep(1)
            change = self.transition(cur_time)
            self.health_manage()
            self.life_count_manage()
            self.random_mob_attack()
            self.manage_house()
            if change or self.state != prev_state:
                print(f'Current state: {self.state}, time: {cur_time}{"am" if cur_time < 12 else "pm"}, health: {self.health}, life count: {self.life_count}')
            else:
                print(f'... {cur_time}{"am" if cur_time < 12 else "pm"} ...')
            prev_state = self.state
        if self.state == self.states.dead:
            return "Routine day is over. You are dead"
        return "Routine day is over. You are asleep."

if __name__ == '__main__':
    nfa = NFA()
    print(nfa.run())