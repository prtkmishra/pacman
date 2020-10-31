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

    def getAction(self, state):
        """ Hungry Agent behaviour"""
        """ Get all the available Food"""
        foodList = api.food(state)

        """ Get Hungry Pacman's current location"""
        currentPacPosition = api.whereAmI(state)

        """Get the actions we can try, and remove "STOP" if that is one of them."""
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        """ Calculate distance between Food and Hungry Pacman"""
        distance = []
        for i in range(len(foodList)):
            distance.append(math.sqrt(((currentPacPosition[0]-foodList[i][0])**2)+((currentPacPosition[1]-foodList[i][1])**2)))

        """ Calculate nearest Food coordinate"""
        nearestFood = foodList[distance.index(min(distance))] # not in use right now

        sortedFoodDist = sorted(distance)
        sortedFood = []
        for i in range(len(sortedFoodDist)):
            sortedFood.append(foodList[sortedFoodDist.index(i)])
        """ get direction to nearest food """
        directionFood = ""
        # print "distance calculated: ",distance
        print "sorted food distance: ",sortedFoodDist
        # print "sorted food coords: ",sorted(sortedFood)
        for i in sortedFood:
            foodId = i
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
                return api.makeMove(directionFood, legal)
            else:
                print "skip to next food"
                # print "Random Step\n"
                # return api.makeMove(random.choice(legal), legal)  
                pass

class SurvivalAgent(Agent):

    def getAction(self, state):
        """ A function to enable survival of pacman by avoiding ghosts and still behave as hungry agent"""

        """ Get all the available Food"""
        foodList = api.food(state)

        """ Get current location of Ghosts"""
        ghostLoc = api.ghosts(state)
        for i in range(len(ghostLoc)):
            print "Ghost Location: ",ghostLoc[i]

        """ Get Pacman's current location"""
        currentPacPosition = api.whereAmI(state)
        print "Pacman Location: ", currentPacPosition

        distanceList = []
        #print "Distance to ghosts:"
        for i in range(len(ghostLoc)):
            distanceList.append(util.manhattanDistance(currentPacPosition,ghostLoc[i]))

        print "distanceList to Ghost:", distanceList,"\n"
        
        lifeSaved = 0
        if min(distanceList) < 3:
            print "min distance to Ghost:", min(distanceList)
            lifeSaved = lifeSaved+1
            print "going to DIE!!!"
            legal = api.legalActions(state)
            if Directions.STOP in legal:
                legal.remove(Directions.STOP)
            
            """closest Ghost coorindates"""
            index = distanceList.index(min(distanceList))
            ghostchacha = ghostLoc[index]
            print "closest ghost is at: ",ghostchacha, "and Pacman is at: ",currentPacPosition
            print "Life Saved: ",lifeSaved
            if ghostchacha[0]-currentPacPosition[0] < 0:
                if Directions.EAST in legal:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going East\n"
                    return api.makeMove(Directions.EAST, legal)
                else:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif ghostchacha[0]-currentPacPosition[0] > 0:
                if Directions.WEST in legal:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going West\n"
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif ghostchacha[1]-currentPacPosition[1] < 0:
                if Directions.NORTH in legal:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going North\n"
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif ghostchacha[1]-currentPacPosition[1] > 0:
                if Directions.SOUTH in legal:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going South\n"
                    return api.makeMove(Directions.SOUTH, legal)   
                else:
                    print "------"+"nearestGhost = "+ str(ghostchacha)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)  
            
        else:
            """Get the actions we can try, and remove "STOP" if that is one of them."""
            """ Hungry Agent behaviour"""
            """ Get all the available Food"""
            foodList = api.food(state)

            """ Get Hungry Pacman's current location"""
            currentPacPosition = api.whereAmI(state)

            """Get the actions we can try, and remove "STOP" if that is one of them."""
            legal = api.legalActions(state)
            if Directions.STOP in legal:
                legal.remove(Directions.STOP)
            
            """ Calculate distance between Food and Hungry Pacman"""
            distance = []
            for i in range(len(foodList)):
                distance.append(math.sqrt(((currentPacPosition[0]-foodList[i][0])**2)+((currentPacPosition[1]-foodList[i][1])**2)))

            """ Calculate nearest Food coordinate"""
            nearestFood = foodList[distance.index(min(distance))]

            """ Steps to eat nearest food"""
            if nearestFood[0]-currentPacPosition[0] > 0:
                if Directions.EAST in legal:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going East\n"
                    return api.makeMove(Directions.EAST, legal)
                else:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif nearestFood[0]-currentPacPosition[0] < 0:
                if Directions.WEST in legal:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going West\n"
                    return api.makeMove(Directions.WEST, legal)
                else:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif nearestFood[1]-currentPacPosition[1] > 0:
                if Directions.NORTH in legal:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going North\n"
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)
            elif nearestFood[1]-currentPacPosition[1] < 0:
                if Directions.SOUTH in legal:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Going South\n"
                    return api.makeMove(Directions.SOUTH, legal)   
                else:
                    print "------"+"nearestFood = "+ str(nearestFood)
                    print "------"+"currentPacPosition = "+ str(currentPacPosition)
                    print "Random Step\n"
                    return api.makeMove(random.choice(legal), legal)  

                
            
            

