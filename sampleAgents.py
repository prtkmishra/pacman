# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
from game import Actions
import api
import random
import game
import util
import math
import operator
# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class PrateekAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Move west when possible
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        else:
            pick = random.choice(legal)
            return api.makeMove(pick, legal)


class HungryAgent(Agent):
    def __init__(self):
         self.last = ""

    def getAction(self, state):
        # 1. Get the list of foods items on the grid.
        # 2. Get the PacMan current location.
        # 3. Calculate distance between PacMan and all the food items.
        # 4. Sort it in ascending order to get the nearest food item.
        # 5. Move the PacMan to the direction.
        # 6. If legal move, proceed.
        # 7. If not legal move, get the second nearest item and move. Repeat this till move is legal.

        #(x, y) co ordinates for food items.
        foodList = api.food(state)
        # print "length of foodlist: ",len(foodList),"\nfoodList: ",foodList
        #Current Position of PacMan (x, y)
        currentPacPosition = api.whereAmI(state)
        distances = {}

        #PacMan (7, 4)
        #FoodItem (3, 2)
        #loop over the co ordinates of food items and calculate the distances 
        for i in range(len(foodList)):
            # print "index: ",i
            # d = math.sqrt(((currentPacPosition[0] - foodList[i][0]) ** 2)+((currentPacPosition[1] - foodList[i][1]) ** 2))
            d = util.manhattanDistance(currentPacPosition,foodList[i])
            distances[foodList[i]] = d
            # print "Distance Key: ", foodList[i], "Food value: ", d
        
        # print "Dictionary for distance and coords pair",distances,"\n","lenght of Dictionary: ",len(distances)
        #sort the dict based of keys. 
        sortedDistance = sorted(distances.items(), key=operator.itemgetter(1))
        # print "sorted distance Dictionary",sortedDistance
        """ get direction to nearest food """
        legal = api.legalActions(state)
        directionFood = ""
        for i in sortedDistance:
            foodId = i[0]
            print "targeting food coords:",foodId
            if foodId[0]-currentPacPosition[0] > 0:
                directionFood = Directions.EAST
            elif foodId[0]-currentPacPosition[0] < 0:
                directionFood = Directions.WEST
            elif foodId[1]-currentPacPosition[1] > 0:
                directionFood = Directions.NORTH   
            elif foodId[1]-currentPacPosition[1] < 0:
                directionFood = Directions.SOUTH

            """ Steps to eat nearest food"""                    
            if directionFood in legal:
                print "------"+"nearestFood = "+ str(foodId)
                print "------"+"currentPacPosition = "+ str(currentPacPosition)
                print "Going ",directionFood,"\n"
                self.last = directionFood
                return api.makeMove(directionFood, legal)
            else:
                print "skip to next food"
                if self.last in legal:
                    return api.makeMove(self.last, legal)
                pass

class SurvivalAgent(Agent):
    def __init__(self):
         self.last = ""

    def getAction(self, state):
        """ A function to enable survival of pacman by avoiding ghosts and still behave as hungry agent
            for a survival agent below steps are considered:
                1. Identify the distance between PacMan and ghosts
                2. If any ghost is less than 3 unit distance away from PacMan
                    a. Identify direction of the ghost
                    b. move away from that direction towards a legal direction
                3. Else: Act as a hungry agent
        """
        print "***************************START of NEW STATE***************************"
        """ Get all the available Food"""
        foodList = api.food(state)

        """ Get current location of Ghosts"""
        ghostLoc = api.ghosts(state)
        print "Ghost Location: ",ghostLoc
        """ Get Pacman's current location"""
        currentPacPosition = api.whereAmI(state)
        print "Pacman Location: ", currentPacPosition

        distanceList = []
        for i in range(len(ghostLoc)):
            distanceList.append(util.manhattanDistance(currentPacPosition,ghostLoc[i]))

        print "distanceList to Ghost:", distanceList,"\n"
        print "Closest Ghost is:",ghostLoc[distanceList.index(min(distanceList))]
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        """ Code for Survival Agent in the IF condition. Pacman acts as Hungry agent in else condition"""
        if min(distanceList) < 3:
            print "Closest Ghost distance is: ",min(distanceList)
            ghostCoord = ghostLoc[distanceList.index(min(distanceList))]

            """Identify Directions to move"""
            if ghostCoord[0]-currentPacPosition[0] > 0:
                directionMove = Directions.WEST
            elif ghostCoord[0]-currentPacPosition[0] < 0:
                directionMove = Directions.EAST
            elif ghostCoord[1]-currentPacPosition[1] > 0:
                directionMove = Directions.SOUTH   
            elif ghostCoord[1]-currentPacPosition[1] < 0:
                directionMove = Directions.NORTH
            
            """Perform move"""
            if directionMove in legal:
                print "------"+"nearest Ghost = "+ str(ghostCoord)
                print "------"+"currentPacPosition = "+ str(currentPacPosition)
                print "Going ",directionMove,"\n"
                self.last = directionMove
                return api.makeMove(directionMove, legal)
            else:
                print "Continue the Last Step"
                if self.last in legal:
                    return api.makeMove(self.last, legal)
                else:
                    print "Last thing to do is leave it to chance"
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        else:
            print "Act as HUNGRY AGENT"
            distances = {}
            for i in range(len(foodList)):
                d = util.manhattanDistance(currentPacPosition,foodList[i])
                distances[foodList[i]] = d
            
            #sort the dict based of keys. 
            sortedDistance = sorted(distances.items(), key=operator.itemgetter(1))
            """ get direction to nearest food """
            directionFood = ""
            for i in sortedDistance:
                foodId = i[0]
                print "targeting food coords:",foodId
                if foodId[0]-currentPacPosition[0] > 0:
                    directionFood = Directions.EAST
                elif foodId[0]-currentPacPosition[0] < 0:
                    directionFood = Directions.WEST
                elif foodId[1]-currentPacPosition[1] > 0:
                    directionFood = Directions.NORTH   
                elif foodId[1]-currentPacPosition[1] < 0:
                    directionFood = Directions.SOUTH

                """ Steps to eat nearest food"""                    
                if directionFood in legal:
                    print "------"+"nearestFood = "+ str(foodId)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going ",directionFood,"\n"
                    self.last = directionFood
                    return api.makeMove(directionFood, legal)
                else:
                    print "skip to next food"
                    if self.last in legal:
                        return api.makeMove(self.last, legal)
                    pass
        





            

