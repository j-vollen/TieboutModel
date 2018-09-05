import numpy as np
import random
import World
import scipy.stats

class Jurisdiction:
    """A stationary local jurisdiction with static political institutions and parties but dynamic voters."""

    _platformList = []
    agentList = []

    # Constructor Method
    def __init__(self, world, address, numParties = 0):
        self._address = address
        self._world = world
        self._numParties = numParties
        #NOTE: I COULD ALSO ACHIEVE THIS WITH A PROPERTY GETTER/SETTER
        if numParties > 0:
            self._platformList = np.random.choice([0,1], size=(numParties,world.get_num_issues()))

    """Agent list filters the world's agent list on those mapped to this jurisdiction and puts together a 2-D array
        of their preferences, each row being an agent, and each column being an issue."""
    @property
    def agentList(self):
        return np.array(
            [agent.preferences for agent
             in self._world.get_agent_list()
             if agent.address == self._address])

    # This is where the platform adaption is called from.
    @property
    def platformList(self):

    @platformList.setter
    def platformList(self, value):
        self._platformList = value

    """Given the world's political institution, updates the jurisdiction's policy after adapting platforms."""
    @property
    def policy(self):
        institution = self.world.get_institution()
        # For referendums, we set the median voter policy, and return
        if institution == 'referendum':
            return np.where(np.median(self.agentList, axis=0) > 0, 1, 0)
        # Otherwise, the platforms will iteratively adapt, and then we'll set the policy.
        parties = self.platformList
        # Simulate poll of current party platforms to determine winner based on institution (below)
        voteCounts = self.poll(parties)
        # For Direct Competition, we just take the plurality winner, a.k.a. the platform with the most votes
        if institution == 'direct competition':
            return parties[scipy.stats.mode(voteCounts).mode,]
        # For Proportional Representation, we weight the platforms by the normalized amount of votes each received,
        # and round the final platform to the nearest whole number (i.e. if >0.5 then 1 o/w 0)
        if institution == 'proportional representation':
            # two lists: unique yielding each unique party preference, and number of agents w/ this preference
            unique, votes = np.unique(voteCounts, return_counts=True)
            # zip together into dictionary of party and number of votes, normalize vote counts so sum to 1
            proportions = dict(zip(unique, votes / len(voteCounts)))
            # multiply normalized votes by corresponding party platforms and sum for weighted population preferences
                # then round to nearest integer (0 or 1) for each issue. Result is final policy.
            return np.rint(sum(prop * parties[key,]
                               for key, prop in proportions.items()))

    @property
    def address(self):
        return self._address

    """Given the world's search heuristic, this function adapts parties' platforms iteratively."""
    def adapt_platforms(self):
        return self

    """Given the current state of the jurisdiction's agent list and party list, run a poll returning the number of
        votes each party receives as a dictionary"""
    def poll(self, platforms):
        # this gives us a matrix with rows being agents and columns being parties, values are the agents' utilities
        agentUtilities = np.matmul(self.agentList, platforms.T)
        # Yields a vector of length of jurisdiction's agentList, indicating each one's party preference
        return np.argmax(agentUtilities, axis=1)




### Biggest questions
    #1 Time to code adaptive platforms.
        # Need to decide whether to do it in the platformList property code, or to do it in a separate function
        # and to mutate the platformList attribute. More of a best practice question
