# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        # methods to use
        def getMoves(state):
            return self.mdp.getPossibleActions(state)
        def isTerminal(state):
            return self.mdp.isTerminal(state)
        
        count = self.iterations

        #for each iteration
        while count != 0:
            qVals = util.Counter()
            for s in states:
                qList = util.Counter()
                legalMoves = getMoves(s)
                if isTerminal(s):
                    continue
                for m in legalMoves:
                    qList[m] = self.computeQValueFromValues(s, m)
                qVals[s] = max(qList.values())
            
            self.values = qVals
            count -= 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        def getTSandProbs(state, move):
            return self.mdp.getTransitionStatesAndProbs(state, move)
        def getReward(state, move, nextState):
            return self.mdp.getReward(state, move, nextState)

        #compute q-value
        sum = 0
        for ts, p in getTSandProbs(state, action):
            r = getReward(state, action, ts)
            sum += (self.values[ts] * self.discount + r) * p
        
        return sum


        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        def getMoves(state):
            return self.mdp.getPossibleActions(state)
        def isTerminal(state):
            return self.mdp.isTerminal(state)

        legalMoves = getMoves(state)
        #return none if no legal actions exist
        if len(legalMoves) == 0 | isTerminal(state):
            return None

        #get move with highest q-val
        bestMove = None
        bestQVal = -9999999
        for m in legalMoves:
            qNew = self.computeQValueFromValues(state, m)
            if qNew > bestQVal:
                bestMove = m
                bestQVal = qNew
        return bestMove

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
