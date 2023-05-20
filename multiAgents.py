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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        def calculate_min_food_distance(newPos, newFoodList):
            min_food_distance = float('inf')
            for food in newFoodList:
                distance = manhattanDistance(newPos, food)
                min_food_distance = min(min_food_distance, distance)
            return min_food_distance

        def calculate_ghost_metrics(newPos, ghostPositions):
            distances_to_ghosts = float('inf')
            proximity_to_ghosts = 0
            for ghost_pos in ghostPositions:
                distance = manhattanDistance(newPos, ghost_pos)
                distances_to_ghosts += distance
                if distance <= 1:
                    proximity_to_ghosts += 1
            return distances_to_ghosts, proximity_to_ghosts
        newFoodList = newFood.asList()
        # Calculate distance to the nearest food pellet
        min_food_distance = calculate_min_food_distance(newPos, newFoodList)
        # Calculate distances from Pacman to the ghosts and their proximity
        distances_to_ghosts, proximity_to_ghosts = calculate_ghost_metrics(newPos, successorGameState.getGhostPositions())
        # Combine the calculated metrics to create the evaluation function
        evaluation = successorGameState.getScore() + (1 / min_food_distance) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts
        return evaluation
    
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
        def max_(state, depth):            
            if depth==self.depth or state.isWin() or state.isLose():                
                return self.evaluationFunction(state)            
            value = float("-inf")            
            legalMoves = state.getLegalActions()            
            for action in legalMoves:                
                value = max(value, min_(state.generateSuccessor(0, action), depth, 1))            
            return value        
            
        def min_(state, depth, agentIndex):            
            if depth==self.depth or state.isWin() or state.isLose():                
                return self.evaluationFunction(state)            
            value = float("inf")            
            legalMoves = state.getLegalActions(agentIndex)            
            if agentIndex==state.getNumAgents()-1:                
                for action in legalMoves:                    
                    value = min(value, max_(state.generateSuccessor(agentIndex, action), depth+1))
            else:                
                for action in legalMoves:                    
                    value = min(value, min_(state.generateSuccessor(agentIndex, action), depth, agentIndex+1))            
            return value        

        legalMoves = gameState.getLegalActions()        
        move = Directions.STOP        
        value = float("-inf")        
        for action in legalMoves:            
            temp = min_(gameState.generateSuccessor(0, action), 0, 1)            
            if temp > value:                
                value = temp                
                move = action        
        return move
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def max_(state, depth, alpha, beta):
            # Base case: if the maximum depth is reached or the game is over, return the evaluation score
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float("-inf")
            legalMoves = state.getLegalActions()

            for action in legalMoves:
                value = max(value, min_(state.generateSuccessor(0, action), depth, 1, alpha, beta))
                if value > beta:
                    return value
                alpha = max(alpha, value)

            return value

        def min_(state, depth, agentIndex, alpha, beta):
            # Base case: if the maximum depth is reached or the game is over, return the evaluation score
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            value = float("inf")
            legalMoves = state.getLegalActions(agentIndex)

            if agentIndex == state.getNumAgents() - 1:
                for action in legalMoves:
                    value = min(value, max_(state.generateSuccessor(agentIndex, action), depth+1, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
            else:
                for action in legalMoves:
                    value = min(value, min_(state.generateSuccessor(agentIndex, action), depth, agentIndex+1, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)

            return value

        legalMoves = gameState.getLegalActions()
        move = Directions.STOP
        value = float("-inf")
        alpha = float("-inf")  # Initialize alpha to negative infinity
        beta = float("inf")    # Initialize beta to positive infinity

        for action in legalMoves:
            temp = min_(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if temp > value:
                value = temp
                move = action
            alpha = max(alpha, value)

        return move
        # util.raiseNotDefined()

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
        def max_(state, depth):
            if depth==self.depth or state.isWin() or state.isLose():                
                return self.evaluationFunction(state)            
            value = float("-inf")            
            legalMoves = state.getLegalActions()            
            for action in legalMoves:                
                value = max(value, expect_(state.generateSuccessor(0, action), depth, 1))
            return value        
        def expect_(state, depth, agentIndex):
            if depth==self.depth or state.isWin() or state.isLose():                
                return self.evaluationFunction(state)            
            value = 0            
            legalMoves = state.getLegalActions(agentIndex)            
            if agentIndex==state.getNumAgents()-1:                
                for action in legalMoves:                    
                    value +=  max_(state.generateSuccessor(agentIndex, action), depth+1)
            else:                
                for action in legalMoves:                    
                    value += expect_(state.generateSuccessor(agentIndex, action), depth, agentIndex+1)
            return value/len(legalMoves)        

        legalMoves = gameState.getLegalActions()        
        move = Directions.STOP        
        value = float("-inf")        
        for action in legalMoves:            
            temp = expect_(gameState.generateSuccessor(0, action), 0, 1)
            if temp > value:                
                value = temp                
                move = action        
        return move
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    capsulePos = currentGameState.getCapsules()    
    layout = currentGameState.getWalls()
    maxlength = layout.height - 2 + layout.width - 2    
    fooddistance = []
    capsuledistance = []
    for food in currentFood.asList():        
        fooddistance.append(manhattanDistance(currentPos, food))
    for capsule in capsulePos:        
        capsuledistance.append(manhattanDistance(currentPos, capsule))
    score = 0    
    x = currentPos[0]    
    y = currentPos[1]    
    for ghostState in currentGameState.getGhostStates():        
        gd = manhattanDistance(currentPos, ghostState.configuration.getPosition())        
        if gd < 2:            
            if ghostState.scaredTimer != 0:                
                score += 1000.0/(gd+1)            
            else :                
                score -= 1000.0/(gd+1)
    if min(capsuledistance+[float(100)])<5:        
        score += 500.0/(min(capsuledistance))    
    for capsule in capsulePos:        
        if (capsule[0]==x)&(capsule[1]==y):            
            score += 600.0    
    minfooddistance = min(fooddistance+[float(100)])    
    return score + 1.0/minfooddistance - len(fooddistance)*10.0
    
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
