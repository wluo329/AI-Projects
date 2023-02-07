# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # %..              G...   %
            # %..             ..  ... %
            # %..                 ... %
            # %..                     %
            # %..                  .. %
            # %..   ^              .. %
            # %..                    o%
            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # Score: 395
        successorGameState = currentGameState.generatePacmanSuccessor(action)



        #pacman position after moving
        # (6, 2)
        newPos = successorGameState.getPacmanPosition()


        #remaining food
        #FFFFFFFFFFFFFFFFFFFFFFFFF
        # FTTFFFFFFFFFFFFFFTTTTFFFF
        # FTTFFFFFFFFFFFFFTTFFTTTFF
        # FTTFFFFFFFFFFFFFFFFFTTTFF
        # FTTFFFFFFFFFFFFFFFFFFFFFF
        # FTTFFFFFFFFFFFFFFFFFFTTFF
        # FTTFFFFFFFFFFFFFFFFFFTTFF
        # FTTFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        newFood = successorGameState.getFood()

        #[<game.AgentState object at 0x7ff2777bc760>]
        newGhostStates = successorGameState.getGhostStates()

        #number of moves each ghost will remain scared b/c of power pellet
        #[0]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        newFoodPos = newFood.asList()
        #print('WHY HELLO THERE')
        #coords of remaining food dots
        #print(newFoodPos)
        #[(5, 5), (5, 6), (6, 2), (6, 5), (6, 6), (7, 4)

        #returns ghost positions
        #[(12.0, 1.0)]
        ghostPos = successorGameState.getGhostPositions()
        #print(ghostPos)

        #Returns a list of positions (x,y) of the remaining capsules.
        #<bound method GameState.getCapsules of <pacman.GameState object at 0x7ff0e1c7e58
        capsulePos = currentGameState.getCapsules()
        #print(capsulePos)

        #print(successorGameState.getScore())

        score = successorGameState.getScore()
        
        food_array = []
        if newFoodPos:
            for food in newFoodPos:
                food_array.append(manhattanDistance(newPos, food))
            bestFoodDist = min(food_array)

            score += 1/bestFoodDist

        return score


        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, 1)[1]


    def getMax(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        #get total agents in game
        numAgents = gameState.getNumAgents()
        #get possible moves of pacman
        legalMoves = gameState.getLegalActions(0)
        #get successor game state after agent takes an action
        successor_arr = []
        for move in legalMoves:
            successor_arr.append(gameState.generateSuccessor(0, move))
        sMinVals = []
        for s in successor_arr:
            sMinVals.append(self.getMin(s, 1, depth)[0])

        sMax = max(sMinVals)
        maxIndex = sMinVals.index(sMax)
        bestMove = legalMoves[maxIndex]
        return (sMax, bestMove)


    def getMin(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        #get total agents in game
        numAgents = gameState.getNumAgents()
        #get possible moves of pacman
        legalMoves = gameState.getLegalActions(agentIndex)
        #get successor game state after agent takes an action
        successor_arr = []
        for move in legalMoves:
            successor_arr.append(gameState.generateSuccessor(agentIndex, move))

        sVals = []
        if agentIndex == numAgents-1:
            if depth != self.depth:
                for s in successor_arr:
                    sVals.append(self.getMax(s, depth+1)[0])
            else:
                for s in successor_arr:
                    sVals.append(self.evaluationFunction(s))
        else:
            for s in successor_arr:
                    sVals.append(self.getMin(s, agentIndex+1, depth)[0])
        
        sMin = min(sVals)
        minIndex = sVals.index(sMin)
        bestMove = legalMoves[minIndex]
        
        return (sMin, bestMove)


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")
        beta = float("inf")
        return self.getMax(gameState, 1, alpha, beta)[1]
        util.raiseNotDefined()

    def getMax(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)

        numAgents = gameState.getNumAgents()
        legalMoves = gameState.getLegalActions(0)
        sMax = -float("inf")
        bestMove = None
        for move in legalMoves:
            s = gameState.generateSuccessor(0, move)
            sVal = self.getMin(s, depth, 1, alpha, beta)[0]
            if sVal > sMax:
                bestMove = move
            sMax = max(sMax, sVal)
            if sMax > beta:
                return (sMax, bestMove)
            alpha = max(alpha, sMax)

        return (sMax, bestMove)

    def getMin(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)

        numAgents = gameState.getNumAgents()
        legalMoves = gameState.getLegalActions(agentIndex)
        sMin = float('inf')
        bestMove = None
        
        for move in legalMoves:
            s = gameState.generateSuccessor(agentIndex, move)
            if agentIndex == numAgents-1:
                if depth != self.depth:
                    sVal = self.getMax(s, depth+1, alpha, beta)[0]
                else:
                    sVal = self.evaluationFunction(s)
            else:
                sVal = self.getMin(s, depth, agentIndex+1, alpha, beta)[0]
            
            sMin = min(sMin, sVal)
            bestMove = move
            if sMin < alpha:
                return (sMin, bestMove)
            beta = min(beta, sMin)

        return (sMin, bestMove)
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getMax(gameState, 1)[1]

    def getMax(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        legalMoves = gameState.getLegalActions(0)
        sMax = None
        bestMove = None
        successor_arr = []
        for move in legalMoves:
            successor_arr.append(gameState.generateSuccessor(0, move))
        sMaxVals = []
        for s in successor_arr:
            sMaxVals.append(self.getEV(s, depth, 1)[0])
        sMax = max(sMaxVals)
        bestMove = legalMoves[sMaxVals.index(sMax)]
        return (sMax, bestMove)

    def getEV(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        numAgents = gameState.getNumAgents()
        legalMoves = gameState.getLegalActions(agentIndex)
        successor_arr = []
        for move in legalMoves:
             successor_arr.append(gameState.generateSuccessor(agentIndex, move))

        sMin = None  #placeholder
        bestMove = None
        sVals = []
        if agentIndex == numAgents - 1:
            if depth != self.depth:
                for s in successor_arr:
                    sVals.append(self.getMax(s, depth + 1)[0])
            else:
                for s in successor_arr:
                    sVals.append(self.evaluationFunction(s))
        else:
            for s in successor_arr:
                    sVals.append(self.getEV(s, depth, agentIndex + 1)[0])
        
        sMin = sum(sVals)/len(legalMoves)

        return (sMin, bestMove)

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Find the closest food dot to pac-man using manhattan distance. 
    Reward more for the closer the dot by using the reciprocal of the distance.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    #[<game.AgentState object at 0x7ff2777bc760>]
    newGhostStates = currentGameState.getGhostStates()

    #number of moves each ghost will remain scared b/c of power pellet
    #[0]
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    newFoodPos = newFood.asList()
    #print('WHY HELLO THERE')
    #coords of remaining food dots
    #print(newFoodPos)
    #[(5, 5), (5, 6), (6, 2), (6, 5), (6, 6), (7, 4)

    #returns ghost positions
    #[(12.0, 1.0)]
    ghostPos = currentGameState.getGhostPositions()
    #print(ghostPos)

    #Returns a list of positions (x,y) of the remaining capsules.
    #<bound method GameState.getCapsules of <pacman.GameState object at 0x7ff0e1c7e58
    capsulePos = currentGameState.getCapsules()

    score = currentGameState.getScore()
        
    food_array = []
    if newFoodPos:
        for food in newFoodPos:
            food_array.append(manhattanDistance(newPos, food))
        bestFoodDist = min(food_array)

        score += 1/bestFoodDist

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
