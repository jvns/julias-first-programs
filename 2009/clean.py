import os, sys
import pygame
import math
import random
from math import sqrt
from pygame.locals import *


DISPLAY = True

data = []
YIELD = 1
LIGHT = 2
OUT = 3
IN = 4
maxSpeed = 15

numLightCycles = 0

numLeftThisTurn = 0
numLeftRecently = []

# amount you can slow down / speed up per half second
decel = 7
accel = 3

problem = False
carLength = 4
carOffset = carLength - 1 

branchLength = 1000
circleLength = 480

inBranchLocations  = [10, 130, 250, 370]
outBranchLocations = [0, 120, 240, 360] # random.sample(range(circleLength), numOutBranches)

quiet = 0.2
busy = 0.4
inRates = [quiet, quiet,quiet, quiet]
outWeights = [1,1,1,1]
yields = [0,0,0,0]
inBranches = []
outBranches = []

cars = []
factories = []

def stoppingDistance(speed):
    return sum([speed - decel * i for i in range(speed) if (speed - decel * i) > 0])
    return 0

def findMaxTime(speed, dist):
    t = 0
    while(dist > 0):
        speed = speed - decel
        if (speed < 0): 
            return (False,False)
        dist = dist - speed
        t = t + 1
    return (t, dist)

def findMaxDist(speed, t):
    d = 0
    while(t > 0):
        d = d + speed
        speed = min(speed + accel, maxSpeed)
        t = t - 1
    return d

def findMinTime(speed, dist):
    t = 0
    speed = speed + accel
    while(dist > speed):
        dist = dist - speed
        speed = min(speed + accel, maxSpeed)
        t = t + 1
    return (t, dist)


class Tile:
    def __init__(self, track, index):
        self.tags = [] # (YIELD, inside/outside), LIGHT, OUT, IN 
        self.car = None
        self.inBranches  = []
        self.outBranches = []
        self.next = []
        self.prev = []
        self.track = track
        self.index = index
        self.yieldFrom = None
        self.yieldTo = None
        
class Track(object):
    def __init__(self, length):
        self.tiles = [Tile(self, i) for i in range(length)]
        self.length = length
        self.start = self.tiles[0]
        self.end = self.tiles[-1]
        for t in range(len(self.tiles)):
            if t < len(self.tiles)-1:
                self.tiles[t].next.append(self.tiles[t+1])
            if t > 0:
                self.tiles[t].prev.append(self.tiles[t-1])


class Circle(Track):
    def __getitem__(self,n):
        return self.tiles[n % self.length]
    def __init__(self,length):
        super(Circle,self).__init__(length)
        self.start.prev.append(self.end)
        self.end.next.append(self.start)

class InBranch(Track):
    def __getitem__(self,n):
        if n >= self.length:
            return self.branchPt
        else:
            return self.tiles[n]
    def __init__(self, length, branchPt, yieldDirection):
        super(InBranch, self).__init__(length)
        self.branchPt = branchPt
        other = self.branchPt.prev[0]
        self.branchPt.prev.append(self.end)
        if yieldDirection == 0:
            self.branchPt.yieldFrom = other
            other.yieldTo = self.branchPt
        else:
            self.branchPt.yieldFrom = self.end
            self.end.yieldTo = self.branchPt

class OutBranch(Track):
    def __getitem__(self,n):
        if (n >= self.length):
            return None
        else:
            return self.tiles[n]
    def __init__(self, length, branchPt):
        self.branchPt = branchPt
        super(OutBranch, self).__init__(length)
    

class Car:
    def __init__(self, tile, dest):
        self.speed = 0
        self.tile = tile
        self.problem = False
        self.destination = dest
        self.nextLocation = None
        self.colour = random.choice([(255,0,0), (200,0,0), (150,0,0), (150,0,150)])
        self.tempColour = 0
        self.stage = 0

    def solve(self, a,b,c):
        try: 
            return (-b + sqrt(b**2 - 4*a*c))/(2*a)
        except: 
            return False
    def checkBackOne(self, dist1, dist2, speed1, speed2):
        # returns -1, 0, or 1
        # yielding car is dist1 from intersection, moving at speed1
        # other car is dist2 from intersection, moving at speed2
        ## 
        if (speed1 == 0):
            return -1 # everything is fine. You can think about going faster

        t1 = math.floor(float(dist1) / speed1) # conservative
        (t2, overshootDist) = findMaxTime(speed2, dist2 + carLength)
        if (t2 == False):
            t2 = 100000
        assert(t2 > 0)
        if t2 <= t1: 
            # car 2 gets there first for sure
            deltaD = dist1 - t2 * speed1 - overshootDist
            assert(deltaD >= 0)
            if stoppingDistance(speed1) >= stoppingDistance(speed2 - decel * t2) + deltaD:
                return 0
            else: 
                return 1
        # done with first half

        t1 = math.ceil((dist1 + carLength) / float(speed1))
        (t2, undershootDist) = findMinTime(speed2, dist2)
        if (t1 <= t2):
            deltaD = dist2 - findMaxDist(speed2, t1) + t1 * speed1 - dist1 - carLength
            if stoppingDistance(speed1) + deltaD <= stoppingDistance(min(speed2 + accel * t1, maxSpeed)):
                return 0
            else: 
                return -1
        return 0
        
    def checkDanger(self, currTile, yieldTile, dist):
        nextTile = yieldTile.next[0]
        otherTile = None
        for i in nextTile.prev:
            if i is not yieldTile:
                otherTile = i
        dist2 = 1
        while True:
            if (dist2 >= otherTile.track.length):
                return False
            if (otherTile.car):
                result = self.checkBackOne(dist, dist2, currTile.car.speed, otherTile.car.speed)
                if (result == 0):
                    return True
                if (result == -1):
                    return False
            otherTile = otherTile.prev[0] 
            dist2 += 1

        
    def update(self):
        global numLeftThisTurn
        assert(self.tile.car)
        assert(self.destination)
        track = self.tile.track
        trackLength = track.length
        nextCar = None
        doDecel = False
        doAccel = False
        currDist = 0
        assert(self.tile)
        for dist in range(0, stoppingDistance(min(self.speed + accel, maxSpeed)) + carLength):
            j = (dist + self.tile.index)
            if (track[j] == None):
                if (dist < max(self.speed, 5)):
                    self.nextLocation = None
                    return
                break
            if (track[j].car and (not nextCar) and (track[j].car != self.tile.car)):
                nextCar = track[j].car
                currDist = dist - carOffset
            if (track[j].yieldTo != None):
                if self.checkDanger(self.tile, track[j], dist + 1):
                    doDecel = True
                    #decelerating because of danger
            if track[j] == self.destination.branchPt:
                if (dist < self.speed):
                    self.nextLocation = self.destination[0]
                    numLeftThisTurn +=1
                    return

        if nextCar == None:
            if self.speed < maxSpeed:
                doAccel = True
        else:
            if (currDist < 1): 
                self.tile.car.tempColour = (0,255,0)
                nextCar.tempColour = (128,128,255)

            if stoppingDistance(self.speed) >= stoppingDistance(nextCar.speed - decel) + currDist:
                doDecel = True
            elif stoppingDistance(self.speed + accel) < stoppingDistance(nextCar.speed - decel) + currDist:
                doAccel = True
            # else same speed
        if (doDecel):
            self.speed = max(self.speed - decel, 0)
        elif (random.random() < 0.1):
            self.speed = max(self.speed - 1, 0)
        elif (doAccel):
            oldspeed = self.speed
            self.speed = min(self.speed + accel, maxSpeed)
            for dist in range(0, stoppingDistance(self.speed)+ carLength):
                j = (dist + self.tile.index)
                if (track[j] == None):
                    continue
                if (track[j].yieldTo != None):
                    if self.checkDanger(self.tile, track[j], dist + 1):
                        self.speed = oldspeed
                    break


                

        self.nextLocation = self.tile.track[(self.tile.index + self.speed)]



def destFactory():
    while 1:
        choiceLst = []
        for i in range(min(len(outBranches), len(outWeights))):
            for j in range(outWeights[i]):
                choiceLst.append(outBranches[i])
        yield random.choice(choiceLst)



def newCar(location, dest):
    car = Car(location, dest)
    cars.append(car)
    location.car = car


def carFactory(rate, start, destGen):
    while 1:
        if random.random() < rate and start.car == None:
            newcar = newCar(start, destGen.next())
            yield newcar
        else:
            yield None


def carFactory2(rate, start, destGen):
    global numLightCycles
    global data
    counter = 0
    go = False
    while 1:
        counter += 1
        if (counter % 60) == 0:
            numLightCycles += 1
            data.append(sum(numLeftRecently))
            go = not go
        if random.random() < rate and start.car == None and go:
            newcar = newCar(start, destGen.next())
            yield newcar
        else:
            yield None


def createInBranches(inBranchLocations):
    for i in range(len(inBranchLocations)):
        loc = inBranchLocations[i]
        track = InBranch(branchLength, loc, yields[i])
        inBranches.append(track)
        factory = carFactory2(inRates[i], track.start, destFactory())
        factories.append(factory)
        track.end.next.append(loc)
        loc.inBranches.append(track)


def createOutBranches(outBranchLocations):
    for loc in outBranchLocations:
        track = OutBranch(branchLength, loc)
        outBranches.append(track)
        loc.outBranches.append(track)

        
circle = Circle(circleLength)
createInBranches(map(lambda x: circle[x], inBranchLocations))
createOutBranches(map(lambda x: circle[x], outBranchLocations))

def update():
    for car in cars:
        car.tile.car = car 
        car.update()
        if (not car.nextLocation):
            car.tile = None
            cars.remove(car)
    for car in cars:
        assert(car.tile)
        car.tile.car = None
    for car in cars:
        car.tile = car.nextLocation
        car.tile.car = car
    for factory in factories:
        factory.next()
    

def drawTrack(track, horiz, startPoint, screen):
    (x0,y0) = startPoint
    if (track in inBranches):
        perm = lambda x, y: (x0 + (track.length - (x - x0)) , y)
    elif (horiz):
        perm = lambda x, y: (x, y)
    else:
        perm = lambda x, y: (y, x)
    for i in range(track.length):
        if (track[i].car):
            if (track[i].car.tempColour):
                pygame.draw.line(screen, track[i].car.tempColour, perm(x0 + i, y0), perm(x0 + i+carOffset, y0))
                track[i].car.tempColour = None
            else:
                pygame.draw.line(screen, track[i].car.colour, perm(x0 + i, y0), perm(x0 + i+carOffset, y0))



def draw(screen):
    global numLeftThisTurn
    global numLeftRecently
    if not DISPLAY:
        return
    drawTrack(circle, False, (8,9), screen)
    for i in range(circleLength):
        for branch in circle[i].inBranches:
            drawTrack(branch, True, (11, i+8), screen)
        for branch in circle[i].outBranches:
            drawTrack(branch, True, (11, i+8), screen)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((468, 800))
    pygame.display.set_caption('Traffic Jam')
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    while 1:
        clock.tick(1000)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        global numLeftRecently
        global numLeftThisTurn
        global numLightCycles
        global data
        numLeftRecently.append(numLeftThisTurn)
        numLeftRecently = numLeftRecently[-60:]
        if (numLightCycles == 40):
            data = data[12:]
            print float(sum(data)) / len(data)
            break
        numLeftThisTurn = 0

    #Draw Everything
        screen.blit(background, (0, 0))
        d = dict()
        update()
        draw(screen)

main()
