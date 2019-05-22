import Agent
import Jurisdiction
import numpy as np
import pandas as pd

#### IDEAS FOR NEXT STEPS
# build out a function which will iterate through institutions, list of numParties, and given trials and return
# pandas dataframe with resulting per capita utility in each cycle of each trial of each world
# output results from paper
# write unit tests
# allow for party entry
# incorporate quadratic voting
# create GUI for user-defined options and resulting visualizations

class World:
    """A set of jurisdictions and mobile agents."""

    def __init__(self, numIssues, numAgents, numJurisdictions, institution='referendum'):
        self.utility = []
        self._institution = institution
        self._numIssues = numIssues
        self._numAgents = numAgents
        self._numJurisdictions = numJurisdictions

        self._agentList = [Agent.Agent.random(self) for _ in range(numAgents)]
        self._jurisdictionList = [Jurisdiction.Jurisdiction(self, i)
                                  for i in range(numJurisdictions)]

    """ cycle method
            update and get all jurisdiction's policies (this is very involved on the jurisdiction/party level)
            reassign agents addresses (of jurisdictions) based on preferences/policies """
    def cycle(self, times=1):
        if times == 0:
            return
        totalUtility = 0
        # get list of policies in all jurisdictions as matrix
        policyList = np.array([j.policy for j in self._jurisdictionList])
        for agent in self._agentList:
            # product of jurisdiction's policies and agent's policy prefs yields agent's utilities in each jurisdiction
            utilities = np.sum(policyList * agent.preferences, axis=1)
            # assign agent to jurisdiction where their utility is maximized
            agent.address = np.argmax(utilities)
            # total world utility agent by agent to record state of world in each cycle
            totalUtility += np.max(utilities)
        # add each cycle's per capita utility and cycle number as tuple to list of tuples as attribute to world
        self.utility.append((len(self.utility), totalUtility/self._numAgents))
        return self.cycle(times=times-1)

    def get_num_issues(self):
        return self._numIssues

    def get_num_agents(self):
        return self._numAgents

    def get_num_jurisdictions(self):
        return self._numJurisdictions

    def get_agent_list(self):
        return self._agentList

    def get_institution(self):
        return self._institution

    def get_jurisdiction_list(self):
        return self._jurisdictionList

"""Runs Tiebout cycle specified number of times for specified number of trials for specified parameters.
    Repeats this process for each institution specified and combines all results into dataframe for output.
    NOTE: still need to add functionality of list of party counts"""
def compareTiebout(numIssues, numAgents, jurisdictionCounts,
                   numTrials, numCycles, institutionList):

    # Empty shell of output dataframe
    result = pd.DataFrame()
    # Cycle through all institutions we want to summarize
    for institution in institutionList:
        for numJurisdictions in jurisdictionCounts:
        # Need to repeat Tiebout cycling a number of times to capture distribution
            for trial in range(numTrials):
                # initiate world specified by input parameters
                myWorld = World(numIssues=numIssues, numAgents=numAgents, numJurisdictions=numJurisdictions)
                # run specified number of Tiebout cycles
                myWorld.cycle(numCycles)
                # build dataframe of utilities for this particular trial, then append to result data frame
                temp = pd.DataFrame(myWorld.utility, columns=['cycle', 'utility'])
                temp['institution'] = institution
                temp['trial'] = trial
                temp['jurisdictions'] = numJurisdictions
                result = result.append(temp)

    return result

def main():
    numTrials = 200
    numCycles = 10
    # First test referendum for 1 jurisdiction
    # for _ in range(numTrials):
    #     myWorld = World(numIssues=11, numAgents=1000, numJurisdictions=1)
    #     myWorld.cycle(numCycles)
    test = compareTiebout(numIssues=11, numAgents=1000, jurisdictionCounts=1,
                          numTrials=10, numCycles=10, institutionList=['referendum'])
    print(test)


if __name__ == '__main__':
    main()




