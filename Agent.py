import numpy as np
import random
import World


class Agent:
    """A voting citizen with free ability to move communities."""

    # Constructor Method
    def __init__(self, world, address, preferences):
        self._world = world
        self._address = address
        self.preferences = preferences

    @classmethod
    def random(cls, world):
        numIssues = world.get_num_issues()
        return cls(world,
                   address=random.randint(0, world.get_num_jurisdictions() - 1),
                   preferences=np.random.uniform(-400/numIssues, 400/numIssues, size=numIssues))

    # Given a binary vector representing a set of policies,
    # compute agent's utility as dot product with their preferences
    def compute_utility(self, policy):
        # return sum([i * j for i, j in zip(self._preferences, policy)])
        return np.dot(self._preferences, policy)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value


if __name__ == '__main__':
    myPreferences = [-10, 2, 3]
    myLocation = 11
    myPolicy = [1, 1, 1]
    myWorld = World.World(3, 1, 3)

    myAgent = Agent.random(myWorld)
    print("Agent lives in town {}.".format(myAgent.get_address()))
    print("Given policy, agent's utility is {}.".format(myAgent.compute_utility(myPolicy)))
