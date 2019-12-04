from mesa import Agent
from RandomWalk import RandomWalker
from random import *


class Deer(RandomWalker):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell
                           if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.sheep_reproduce:
            # Create a new sheep:
            if self.model.grass:
                self.energy /= 2
            lamb = Deer(self.model.next_id(), self.pos, self.model,
                        self.moore, self.energy)
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)


class Wolf(RandomWalker):
    '''
    A wolf that walks around, reproduces (asexually) and eats sheep.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Deer)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    '''

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1

class Hunter(RandomWalker):
    '''
    Hunter That randomly moves, and hunts deer that cross his/her path. Gains Welfare per kill. Will always kill deer
    over a certain energy level. Will kill deer under a certain energy level by chance.
    '''

    wealth = 0 #starting wealths are 0

    def __init__(self, unique_id, pos, model, moore, wealth=0):
        super().__init__(unique_id, pos, model, moore=moore)
        self.wealth = wealth


    def Kill_Payoff(self):
        wealth_from_kill = 5
        self.wealth += wealth_from_kill

    def Kill_Prob(self):
        return self.random.random()

    def step(self):
        self.random_move()

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        deer = [obj for obj in this_cell if isinstance(obj, Deer)]
        if len(deer) > 0:
            deer_to_kill = self.random.choice(deer)
            if deer_to_kill.energy <= 2:
                if randomunif[0, 1] <= PROBCHEAT  # have the code for this
                    self.model.grid._remove_agent(self.pos, deer_to_kill)
                    self.model.schedule.remove(deer_to_kill)
                    cheat = 1  # Have to define this previously
                else:
                    nothing
            else:
                self.model.grid._remove_agent(self.pos, deer_to_kill)
                self.model.schedule.remove(deer_to_kill)

#positions rangers can see
#add baby deer counter
