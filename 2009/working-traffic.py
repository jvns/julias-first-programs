import os, sys
import pygame
import random
from copy import deepcopy
from pygame.locals import *

YIELD = 1
LIGHT = 2
OUT = 3
IN = 4
maxSpeed = 7
numInBranches = 10
numOutBranches = 3

branchLength = 100
trackLength = 100

inBranchLocations  = random.sample(range(trackLength), numInBranches)
outBranchLocations = random.sample(range(trackLength), numOutBranches)

inBranches = []
outBranches = []

cars = []
factories = []


class Tile:
    def __init__(self, track, index):
        self.tags = [] # (YIELD, inside/outside), LIGHT, OUT, IN 
        self.car = None
        self.inBranches  = []
        self.outBranches = []
        self.next = None
        self.prev = None
        self.track = track
        self.index = index
        
class Track(object):
    def __init__(self, length):
        self.tiles = [Tile(self, i) for i in range(trackLength)]
        self.length = length
        self.start = self.tiles[0]
        self.end = self.tiles[-1]
        for t in range(len(self.tiles)):
            if t < len(self.tiles)-1:
                self.tiles[t].next = self.tiles[t+1]
            if t > 0:
                self.tiles[t].prev = self.tiles[t-1]

class Circle(Track):
    def __getitem__(self,n):
        return self.tiles[n % self.length]

class InBranch(Track):
    def __getitem__(self,n):
        if n >= self.length:
            return self.branchPt
        else:
            return self.tiles[n]
    def __init__(self, length, branchPt):
        self.branchPt = branchPt
        super(InBranch, self).__init__(length)

class Car:
    def __init__(self, tile, dest):
        self.speed = 0
        self.tile = tile
        self.destination = dest
        self.nextLocation = None
        self.colour = random.choice([(255,0,0), (200,0,0), (150,0,0), (150,0,150)])
#        self.acceleration = 10
    def update(self):
        # set nextLocation
        track = self.tile.track
        trackLength = track.length
        nextCar = None
        for dist in range(1, self.speed * (self.speed + 1) / 2):
            j = (dist + self.tile.index) % (trackLength)
            if (track[j].car):
                print j, trackLength, self.tile.index
                nextCar = track[j].car
                break
        #if (track[j].car.location != (dist + self.location) % trackLength):
            #print "car has the wrong location!"
        #if (self.speed*(self.speed+1)/2 >= track[j].car.speed * (track[j].car.speed + 1)/2 + dist):
            #print "oh no!"
        if nextCar == None:
            if self.speed < maxSpeed:
                self.speed += 1
        else:
            if (self.speed*(self.speed+1)/2 >= nextCar.speed*(nextCar.speed - 1)/2 + dist+1):
                self.speed = self.speed - 1
                #print 1,self.speed, dist, track[j].car.speed
            elif ((self.speed + 2)*(self.speed+1)/2 < nextCar.speed*(nextCar.speed - 1)/2 + dist+1):
                self.speed = self.speed + 1
                #print 2,self.speed, dist, nextCar.speed
            #else:
                #print 3,self.speed, dist, nextCar.speed
                

        self.nextLocation = self.tile.track[(self.tile.index + self.speed)]
        print self.tile == self.nextLocation



def destFactory():
    while 1:
        print "dest"
        yield random.choice(inBranches)



def newCar(location, dest):
    car = Car(location, dest)
    cars.append(car)
    location.car = car


def carFactory(rate, start, destGen):
    while 1:
        if random.random() < rate:
            newcar = newCar(start, destGen.next())
            yield newcar
        else:
            yield None

def createInBranches(inBranchLocations):
    for loc in inBranchLocations:
        track = InBranch(branchLength, loc)
        inBranches.append(track)
        factory = carFactory(0.1, track.start, destFactory())
        factories.append(factory)
        track.end.next = loc
        loc.inBranches.append(track)


        
circle = Circle(trackLength)
createInBranches(map(lambda x: circle[x], inBranchLocations))
newCar(circle.start, None)



#for loc in inBranchLocations:
#    track = Track(branchLength)
#    for i in range(track.length):
#        if (random.random() > 0.8):
#            track[i].car = Car(track[i])
#            track[i].car.location = i
#    circle[loc].inBranches.append(track)
#for loc in outBranchLocations:
#    circle[loc].outBranches.append(Track(branchLength))


#for tile in circle:
#    if (random.random() > 0.7): 
#        tile.car = Car(tile)
#        tile.car.location = tile.location


def update():
    for car in cars:
        car.update()
    for car in cars:
        car.tile.car = None
        car.tile = car.nextLocation
        car.tile.car = car
    for factory in factories:
        factory.next()
    print "updated!"
    

def drawTrack(track, horiz, startPoint, screen):
    (x0,y0) = startPoint
    if (track in inBranches):
        perm = lambda x, y: (x0 + (5 * track.length - (x - x0)) , y)
    elif (horiz):
        perm = lambda x, y: (x, y)
    else:
        perm = lambda x, y: (y, x)
    for i in range(track.length):
        if (track[i].car):
            pygame.draw.line(screen, track[i].car.colour, perm(x0 + 5*i, y0), perm(x0 + 5*i+3, y0))
#            pygame.draw.line(screen, track[i].car.colour, perm(x0 + 5*i, y0+1), perm(x0 + 5*i+3, y0+1))


def draw(screen):
    drawTrack(circle, False, (8,9), screen)
    for i in range(trackLength):
        for branch in circle[i].inBranches:
            drawTrack(branch, True, (11, 5*i), screen)
        for branch in circle[i].outBranches:
            drawTrack(branch, True, (11, 5*i), screen)
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((468, 600))
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
        clock.tick(10)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

    #Draw Everything
        screen.blit(background, (0, 0))
        d = dict()
        update()
        draw(screen)

main()
