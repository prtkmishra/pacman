# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).A

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

"""
# The code has been further modified by Prateek Mishra for coursework to be 
# submitted for 6CCS3AIN Coursework at King's College London
"""
from pacman import Directions
from game import Agent
import api
import random
import game

DEBUG = False
if DEBUG:
    import time
    import logging
    log = logging.getLogger("my-logger")
else:
    pass
 
"""
Define global parameters
Static reward values for states in the env
"""
REWARD_FOOD = 10
REWARD_WALLS = -10
REWARD_CAP = 5
REWARD_GHOST = -1000
REWARD_G_NEIGH = -500
REWARD_PAC = -15
REWARD_EMPTY = 5
TERMINAL_VALUE = 500

"""
mapper() return the list of tuples valueMap[] where each entry is a state
Methods: 
    calcHeight
    calcWidth
    generateMap
"""
class mapper():
    """ Function to calculate height of the grid environment """
    def calcHeight(self, corners):
        """
        # Input:
            # @corners : coordinates of all 4 corners
            # Type: List of tuples
        # Output:
            # _height
            # Type: int
        """
        self._height = -1
        for i in range(len(corners)):
            if corners[i][1] > self._height:
                self._height = corners[i][1]
        self._height = self._height+1
        return self._height

    """ Function to calculate width of the grid environment """
    def calcWidth(self, corners):
        """
        # Input:
            # @corners : coordinates of all 4 corners
            # Type: List of tuples
        # Output:
            # _width
            # Type: int
        """
        self._width = -1
        for i in range(len(corners)):
            if corners[i][0] > self._width:
                self._width = corners[i][0]
        self._width = self._width+1
        return self._width

    """ This function creates a map of Pac-Man world """
    def generateMap(self, state):
        """
        # Input: 
            # @state: current state of the environment
        # Output:
            # overallMap
            # Type: List of tuples
        """

        """
        # Identify:
            # current PacMan location - tuple, 
            # food coorindates - list of tuples, 
            # Terminal state if any - list of tuple,
            # ghost locations - list of tuples, 
            # walls - list of tuples,  
            # corners - list of tuples, 
            # and capsules - list of tuples, 
        # using methods from api
        """
        self._currPacLoc = api.whereAmI(state)
        self._foodCoords = api.food(state)
        """ If there is any terminal state identified
            remove the state from food list to ensure it is not used 
            in Utility calculaion
        """
        if len(self._foodCoords) == 1:
            self.terminalState = [self._foodCoords[0]]
            self._foodCoords.remove(self._foodCoords[0])
        else:
            self.terminalState = []
        self._ghostLoc = api.ghosts(state)
        self._wallsCoords = api.walls(state)
        self._cornersCoords = api.corners(state)
        self._capsules = api.capsules(state)

        """# Calculate the overall Map using height and width"""
        self.calcWidth(self._cornersCoords)
        self.calcHeight(self._cornersCoords)
        """
        # Add all the coordinates falling between the corners
        # into one single array to create a map of all coordinates
        """
        self.overallMap = []
        for i in range(self._height):
            for j in range(self._width):
                _cord = (j,i)
                self.overallMap.append(_cord)
        """ If there is any terminal state identified
            remove the state from overallMap to ensure it is not used 
            in Utility calculaion
        """
        if len(self._foodCoords) == 1:
            self.overallMap.remove(self._foodCoords[0])

"""
Main class called by pacman to return the intended action to 
move from one state to another.

Methods:
    __init__
    registerInitialState
    neighbStates
    final
    valueMapping
    valueIteration
    getAction
"""
class MDPAgent(Agent):

    """Constructor: this gets run when we first invoke pacman.py"""
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"
        """
        # Initialise below values :
            # @Gamma(discount factor)
            # @action probability 
            # @utility dictionary for relevant states and 
            # @utilRecord dictionary for keeping a record of last util for calculating convergence
        # for the Bellman's update in value iteration
        """
        self.gamma = 0.9
        self.actionProb = api.directionProb
        self.utilRecord = {}
        self.utility = {}
        self.valueMap = {}

    """
    Gets run after an MDPAgent object is created and once there is
    game state to access.
    """
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
    
    """
    # This is what gets run in between multiple games
    # reset the values for utilities between each action
    """
    def final(self, state):
        print "Looks like the game just ended!"
        self.utilRecord = {}
        self.utility = {}
        self.valueMap = {}
    
    """ This function returns a list of neighbouring states of Ghosts """
    def neighbStates(self,location):
        """
        # Input:
            # @location
            # Type: List of tuples
        # Output: 
            # neigh[]
            # Type: List of tuples
        """
        self.neigh = []
        for g in location:
            n = [
                (g[0]-1,g[1]),
                (g[0]+1,g[1]),
                (g[0],g[1]-1),
                (g[0],g[1]+1)
                ]
            for i in n:
                self.neigh.append(i)
        return self.neigh

    """
    This function returns 
        Rewards as valueMap of all states
        Initial U(s) as utilityMap of all states
    """
    def valueMapping(self, state):
        """
        # Input:
            # @state
            # Type: 
        # Output: 
            # valueMap{}
            # Type: Dict{}
            # utility{}
            # Type: Dict{}
        """
        """
        Approach: 
            # Assign rewards for the bellmans update
                # Create a value map for respective states to assign rewards for each state.
                # For food coordinate, assign a high value
                # and a similar value for the capsules (in case of MediumClassic Grid)
                # Assign walls lower value as we want to discourage PacMan to prefer attempting running into the wall
                # Any empty coordinates will have a low reward to discourage PacMan to wander in empty zones
                # Ghosts will have the least reward to discourage PacMan to be around ghosts
                # Neighbouring states of ghosts will have a low reward to discourage PacMan from going near ghosts
            # Assign Utilities for each state
                # Initialise each state with Utility U(s) = 0, except terminal state (when identified)
                # Create a utility map utility{} and initialise it with value '0'
                # Utility map will be used by PacMan to navigate through the environment
        """
        _map = mapper()
        _map.generateMap(state)
        for i in range(len(_map.overallMap)):
            """ 
            Check if the state has food
            Check if the state is a wall
            Check if the state is a capsule
            Check if the state is current state
            Check if the state is a Ghost location
            Check if the state is a neighbour of ghost
            Any remaining state i.e. empty states 
            """
            if _map.overallMap[i] in _map._foodCoords:
                self.valueMap[_map.overallMap[i]] = REWARD_FOOD
                self.utility[_map.overallMap[i]] = 0
            
            elif _map.overallMap[i] in _map._wallsCoords:
                self.valueMap[_map.overallMap[i]] = REWARD_WALLS
                
            elif _map.overallMap[i] in _map._capsules:
                self.valueMap[_map.overallMap[i]] = REWARD_CAP
                self.utility[_map.overallMap[i]] = 0
            
            elif _map.overallMap[i] in _map._currPacLoc:
                self.valueMap[_map.overallMap[i]] = REWARD_PAC
                self.utility[_map.overallMap[i]] = 0
            
            elif _map.overallMap[i] in _map._ghostLoc:
                self.valueMap[_map.overallMap[i]] = REWARD_GHOST
                self.utility[_map.overallMap[i]] = 0
            
            elif _map.overallMap[i] in self.neighbStates(_map._ghostLoc):
                self.valueMap[_map.overallMap[i]] = REWARD_G_NEIGH
                self.utility[_map.overallMap[i]] = 0

            else:
                self.valueMap[_map.overallMap[i]] = REWARD_EMPTY
                self.utility[_map.overallMap[i]] = 0

    """ 
    This function returns the the updated maximum expected utility of every state
    as per Bellman Update
    """
    def valueIteration(self, state):
        """
        # Input:
            # @state
            # Type: 
        # Output: 
            # utility{}
            # Type: Dict{} 
        """
        """
        # Approach:
            # For the PacMan to use Markov Decision Process to win this game, Value Iteration has been used
            # For all states:
                # Identify 4 neghbours for each state by +/- in the X and Y directions for coordinates.
                # For each of the 4 neighbours, map them with Initialised Uitlity
                # For each of the 4 neighbours, calculate Expected Utility of the of the action towards them 
                # (If NORTH is 80% then EAST and WEST are 10% each)
                    # If any direction is a wall, then use the currect state utility
                # Calculate the maximum expected utility among all the neighbours
                # Then calculate the utility of that state adding reward and gamma in Bellman's Update with MEU
            # Repeat above step untill Utilities for every state converge with a tolerance of 0.005 using while loop
        """
        _map = mapper()
        _map.generateMap(state)
        self.valueMapping(state)
        """ Get the actions we can try, and remove "STOP" if that is one of them. """
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        """ Create a local list to store converged states """
        _convergedList = []        
        """ DEBUG MODE """
        if DEBUG:
            """ Iteration counter for debugging """
            _iteration = 0
        
        """ State loop to update utilities for every state except terminal state and stop when utilities for each state converge """
        while not len(_convergedList) == len(self.utility.keys()):
            """ DEBUG MODE """
            if DEBUG:
                print "*"*100
                print "START of Iteration"
                print "Overall Map: ",_map.overallMap,"\n"
                print "Reward Function: ",self.valueMap,"\n"
                print "Utility Function: ",self.utility,"\n"
                _iteration = _iteration+1
            
            """ Create a copy utilRecord{} of the calculated utilities utility{}
                self.utilRecord = dict(self.utility) to ensure copy points to a different memory location
            """
            self.utilRecord = dict(self.utility)

            """ Start the Value Iteration for every state in the known environment """
            for state in self.utility.keys():
                """ DEBUG MODE """
                if DEBUG: 
                    print "START of State :",state, "for Iteration: ",_iteration
                
                """ Initialise a local list for Expected Utility """
                EU = []
                """ Define directions from the current state """
                _west = (state[0]-1, state[1]) # WEST
                _north = (state[0], state[1]+1) # NORTH
                _south = (state[0], state[1]-1) # SOUTH
                _east = (state[0]+1, state[1]) # EAST
                _dir = [_west, _east, _north, _south]
                """ Check if any direction from the state is a wall, then use the current state for Expected utility """
                for d in _dir:
                    if d in _map._wallsCoords:
                        _dir[_dir.index(d)] = state
                """ If there is any terminal state identified
                    use terminal utility in the calculation
                """
                for terminal in _dir:
                    if terminal in _map.terminalState:
                        self.utilRecord[terminal] = TERMINAL_VALUE
                """ 
                Calculate Expected Utility for all possible actions from the current state 
                utilRecord{} is used.
                """
                EU.append(self.actionProb*self.utilRecord[_dir[0]]+0.1*self.utilRecord[_dir[2]]+0.1*self.utilRecord[_dir[3]])
                EU.append(self.actionProb*self.utilRecord[_dir[2]]+0.1*self.utilRecord[_dir[0]]+0.1*self.utilRecord[_dir[1]])
                EU.append(self.actionProb*self.utilRecord[_dir[1]]+0.1*self.utilRecord[_dir[2]]+0.1*self.utilRecord[_dir[3]])
                EU.append(self.actionProb*self.utilRecord[_dir[3]]+0.1*self.utilRecord[_dir[1]]+0.1*self.utilRecord[_dir[0]])                
                """ Calculate the maximum Expected utility of that state """
                MEU = max(EU)
                
                """ Calculate Utility based on Bellman's update and Update the calculated utility in the utility Dict{} """
                self.utility[state] = self.valueMap[state] + (self.gamma*MEU)

                """ Check for convergence for every state and update the local _convergedList"""
                if self.utility[state] - self.utilRecord[state] < 0.005:
                    if state not in _convergedList:
                        _convergedList.append(state)
                
                """ DEBUG MODE """
                if DEBUG:
                    print "Iteration: ",_iteration,"; State: ",state,"; Current utility: ",self.utility[state]
                    print "Iteration: ",_iteration,"; State: ",state,"; Prev Util: ",self.utilRecord[state]
                    print "Number of states: ",len(self.utility.keys())
                    print "number of states converged: ",len(_convergedList)
                    print "converged states are: ",_convergedList
                    print "End of STATE"

    """ This Function returns the intended action for PacMan move around the environment based on MDP solution """
    def getAction(self, state):
        """
        # Input:
            # @state
            # Type: 
        # Output: 
            # api.makeMove(Action, legal)
        """
        """
        # Approach:
            # Remove STOP from list of legal actions
            # For every legal action from current state
                # select the best action based on utility update from valueIteration()
            # return api.makeMove(Action, legal)
        """
        _map = mapper()
        _map.generateMap(state)
        self.valueIteration(state)

        """ DEBUG MODE """
        if DEBUG:
            start_time = time.clock()
         
        """ Get the actions we can try, and remove "STOP" if that is one of them. """
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        """ Create a local list to store utilities of for each legal action from current state """
        _actionUtil = []
        for action in legal:
            if action == "West":
                newState = (_map._currPacLoc[0]-1, _map._currPacLoc[1])
            elif action == "East":
                newState = (_map._currPacLoc[0]+1, _map._currPacLoc[1])
            elif action == "North":
                newState = (_map._currPacLoc[0], _map._currPacLoc[1]+1)
            else: 
                action == "South"
                newState = (_map._currPacLoc[0], _map._currPacLoc[1]-1)
            _actionUtil.append(self.utility[newState])
        
        """ 
        Identify the action with max util from the value iteration. 
        As numpy is not allowed to be used for project purpose, below method is used to 
        identify the index of action with maximum utility (argmax).
        """
        _maxActionUtil = max(_actionUtil)
        self.last = legal[_actionUtil.index(_maxActionUtil)]
        
        """ DEBUG MODE """
        if DEBUG:
            print "total time taken for action: ",time.clock() - start_time, "seconds"
            print "End of Action"
            print "/"*200
        """ 
        Return the action to be made based on MDP solution and hope PacMan wins 
        Hope because the below intended action to happen has a probability of only 0.8.
        """
        return api.makeMove(self.last, legal)
