import Agent
import Jurisdiction
import numpy as np


class World:
    """A set of jurisdictions and mobile agents."""

    def __init__(self, numIssues, numAgents, numJurisdictions, institution="referendum"):
        self._institution = institution
        self._numIssues = numIssues
        self._numAgents = numAgents
        self._numJurisdictions = numJurisdictions

        self._agentList = [Agent.Agent.random(self) for _ in range(numAgents)]
        self._jurisdictionList = [Jurisdiction.Jurisdiction(self, i)
                                  for i in range(numJurisdictions)]

    # cycle method - pseudo-code
        # update and get all jurisdiction's policies (this is very involved on the jurisdiction/party level)
        # reassign agents addresses (of jurisdictions) based on preferences/policies

    def cycle(self, times=1):
        if times == 0:
            return self
        # reassign agents addresses (of jurisdictions) based on preferences/policies
        policyList = np.array([j.policy for j in self._jurisdictionList])
        for agent in self._agentList:
            agent.address = np.argmax(np.sum(policyList * agent.preferences, axis=1))

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


if __name__ == '__main__':
    myWorld = World(numIssues=2, numAgents=10, numJurisdictions=5)

    myWorldCycled = myWorld.cycle(3)
    print("placeholder")



