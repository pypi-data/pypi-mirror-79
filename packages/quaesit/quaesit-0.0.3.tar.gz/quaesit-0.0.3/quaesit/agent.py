import inspect

from math import hypot, sin, asin, cos, radians, degrees
from abc import ABCMeta, abstractmethod
from random import randint, choice
from typing import Dict, List, Tuple, Union


class Agent(metaclass=ABCMeta):
    """
    Class to represent an agent in an agent-based model.
    """

    _id = 0
    colors = ['blue', 'brown', 'cyan', 'gray', 'green', 'magenta', 'orange',
              'pink', 'purple', 'red', 'yellow']

    def __init__(self, world, coords: Tuple = None):
        self._id = Agent._id
        Agent._id += 1

        self.world = world
        self.coords = coords or (randint(0, self.world.width - 1),
                                 randint(0, self.world.height - 1))
        self.direction = 90
        self.breed = self.__class__.__name__.lower()
        self.icon = '.'
        self.color = choice(self.colors)

        self.world.add_agent(self)

    def die(self):
        """
        Remove the agent from the world.
        """

        del self.world.agents[self._id]
        self.world.grid[self.coords]['agents'].remove(self)
        del self

    def hatch(self):
        """
        Creates an agent and initializes it with the same parameters as
        oneself.
        """

        sig = inspect.signature(self.__init__)
        filter_keys = [param.name for param in sig.parameters.values()
                       if param.kind == param.POSITIONAL_OR_KEYWORD]
        filtered_dict = {filter_key: self.__dict__[filter_key]
                         for filter_key in filter_keys}
        return self.__class__(**filtered_dict)

    def move_to(self, coords: Tuple):
        """
        Places the agent in a different cell of the world grid.
        """

        self.world.remove_from_grid(self)
        self.coords = coords
        self.world.place_on_grid(self)

    def cell_here(self, layer = None):
        """
        Returns the value of a layer in the model's grid for the cell
        where the agent is. If no layer is specified, the values of all
        layers are returned.
        """
        if layer is not None:
            return self.world.grid[self.coords][layer]
        else:
            return self.world.grid[self.coords]

    def get_distance(self, coords: Tuple) -> int:
        """
        Returns the distance (in cells) from the agent to a pair of
        coordinates.
        """

        x, y = coords
        return round(hypot((x - self.coords[0]), (y - self.coords[1])))

    def cells_in_radius(self, radius: int) -> Dict:
        """
        Returns all cells and respective attributes within a distance
        of the agent.
        """

        if self.world.torus:
            neighborhood = {self.world.to_torus((x, y)):
                            self.world.grid[self.world.to_torus((x, y))]
                            for x in range(self.coords[0] - radius,
                                           self.coords[0] + radius + 1)
                            for y in range(self.coords[1] - radius,
                                           self.coords[1] + radius + 1)
                            if self.get_distance((x, y)) <= radius}
        else:
            neighborhood = {(x, y): self.world.grid[(x, y)]
                            for x in range(self.coords[0] - radius,
                                           self.coords[0] + radius + 1)
                            for y in range(self.coords[1] - radius,
                                           self.coords[1] + radius + 1)
                            if (self.get_distance((x, y)) <= radius and
                                (x, y) in self.world.grid)}

        return neighborhood

    def empty_cells_in_radius(self, radius: int) -> Dict:
        """
        Returns all empty cells (with no agents on them) and respective
        attributes within a distance of the agent.
        """

        if self.world.torus:
            neighborhood = {self.world.to_torus((x, y)):
                            self.world.grid[self.world.to_torus((x, y))]
                            for x in range(self.coords[0] - radius,
                                           self.coords[0] + radius + 1)
                            for y in range(self.coords[1] - radius,
                                           self.coords[1] + radius + 1)
                            if (self.get_distance((x, y)) <= radius and not
                                self.world.grid[self.world.to_torus((x, y))]
                                               ['agents'])}
        else:
            neighborhood = {(x, y): self.world.grid[(x, y)]
                            for x in range(self.coords[0] - radius,
                                           self.coords[0] + radius + 1)
                            for y in range(self.coords[1] - radius,
                                           self.coords[1] + radius + 1)
                            if (self.get_distance((x, y)) <= radius and
                                (x, y) in self.world.grid and not
                                self.world.grid[(x, y)]['agents'])}

        return neighborhood

    def nearest_cell(self, cells: Union[List, Dict]) -> Tuple:
        """
        Given a list or dictionary of cells, returns the coordinates of
        the cell that is nearest to the agent.
        """

        dists = {cell: self.get_distance(cell) for cell in cells}
        return min(dists, key=dists.get)

    def agents_in_radius(self, radius: int):
        """
        Returns all agents within a distance of oneself.
        """

        neighborhood = self.cells_in_radius(radius)
        neighbors = [agent for coords in neighborhood
                     for agent in self.world.grid[coords]['agents']
                     if agent is not self]
        return neighbors

    def agents_here(self) -> List:
        """
        Returns all agents located on the same cell as oneself.
        """

        return [agent for agent in self.world.grid[self.coords]['agents']
                if agent is not self]

    def nearest_agent(self, agents: List = None):
        """
        Given a list of agents, returns the agent that is nearest to
        oneself. If no list is provided, all agents are evaluated.
        """

        if agents is None:
            agents = [self.world.agents[_id] for _id in self.world.agents]
        dists = {agent: self.get_distance(agent.coords)
                 for agent in agents if agent is not self}
        return min(dists, key=dists.get)

    def turn_right(self, angle: int = 90):
        """
        Rotates the agent's direction a number of degrees to the right.
        """

        self.direction = round((self.direction - angle) % 360)

    def turn_left(self, angle: int = 90):
        """
        Rotates the agent's direction a number of degrees to the left.
        """

        self.direction = round((self.direction + angle) % 360)

    def forward(self, n_steps: int = 1):
        """
        Moves the agent a number of cells forward in the direction it
        is currently facing.
        """

        x = round(self.coords[0] + cos(radians(self.direction)) * n_steps)
        y = round(self.coords[1] + sin(radians(self.direction)) * n_steps)

        if self.world.torus:
            self.move_to(self.world.to_torus((x, y)))
        elif (x, y) in self.world.grid:
            self.move_to((x, y))

    def face_towards(self, coords: Tuple):
        """
        Turns the agent's direction towards a given pair of coordinates.
        """

        if coords != self.coords:
            xdif = coords[0] - self.coords[0]
            ydif = coords[1] - self.coords[1]
            dist = hypot(xdif, ydif)
            angle = degrees(asin(ydif / dist))

            if xdif < 0:
                self.direction = round(180 - angle)
            else:
                self.direction = round((360 + angle) % 360)

    def random_walk(self, n_steps: int = 1):
        """
        Moves the agent one cell forward in a random direction for a
        number of times.
        """

        for i in range(n_steps):
            self.turn_right(randint(0, 360))
            self.forward()

    @abstractmethod
    def step(self):
        """
        Methods to be performed by the agent at each step of the
        simulation.
        """

        raise NotImplementedError
