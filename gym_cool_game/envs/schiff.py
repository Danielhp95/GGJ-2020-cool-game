#!/usr/bin/env python
# -*- coding: utf-8 -*-

#         - - - - - -
# example with vector class for my pygamebook
# LICENSE: Gnu General Public License (GPL)
# includes vec2d class from www.pygame.org
# AUTHOR: (from the game, not from the vec2dclass): Horst JENS
# email: horst.jens@gmail.com
# web: http://www.spielend-programmieren.at
#        - - - - - - - 

#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



# idee Theo:
# schlachtschiff
# ölflecken, minen
# single mit mehr tasten
# peace-modus
# 4 Tasten für Schiffsteuerung, 2 Tasten für Geschützsturm-Steuerung
# Items
#  bonus wenn mehrere Items der selben ARt (Laser, Gescütz etc) aufgesammelt werden -> Upgrades
# Item in Fässern, Fässer muss man zerschiessen ( viele Hitpoints)


#FIXME: seit pygame.clock-reparatur alles zu schnell ?
#FIXME: tank.reload ist derzeit sinnlos
#FIXME: bar vom AI Schiff hinkt nach
#FIXME: rotation ordentlich machen, ohne -90° und *-1
#FIXME: self.rect.center - oldcenter in Ordnung bringen
#FIXME: Modus sinnvoll machen (derzeit nur space sinnvoll)
#FIXME: spacemove und newmoving vereinheitlichen
#FIXME: division by Zero kapieren
#FIXME: myfont eine globale Variable oder Konstante machen (im Sprite Text)


#Fixme: öltropfen spawnen zu sehr/dauernd nach Explosion... nicht-spawn-zeit einbauen ?

#TODO: AI-Schiff fährt immer in die Mitte der 4 Spieler...4 Viereck hat nicht unbedingt einen exakten Mittelpunkt
#TODO: AI-Schiff Masse (soll nicht so leicht aus der Bahn schiessbar sein)
#TODO: AI-Schiff drehen
#TODO: braunes AI Schiff ruckelt
#TODO: recalc raushaun
#TODO: tracer code entfernen oder Bugwellensystem / Blasen
#TODO: braunes Schiff: schönere Form, drehung, Antrieb, schüsse

#TODO: 4 Player / Bots / AI !
#TODO: verstehen: wird ein pos-Vektor als positionsargument übergeben wandert das ding mit (siehe victory)
#TODO: GUI oder config

#TODO: Reibung, 
#TODO: optional sich in die Kurve legen (x-schrumpfen) bei rotation-speed<>0
#TODO: Wind
#TODO: Feuer, Riffe oder gefährlicher Rand
#TODO: Segelschiffe, schiessen seitlich, eventuell Buggeschütz, schwaches Heckgeschütz(e)
#TODO: Rammen (Rammwinkel)
#TODO: mehr Segelschiff-sim
#TODO: Vektoren schöner machen, mit Pfeilspitzen oder Dreiecke

#TODO: wenn ölfleck getroffen, schneller / grösser / driften

#done: AI-Schiff hat 3 Kreise (Geschütztürme)
#done: schussweite (flytime) verringert.
#done: patrol oil rausgehaut. ölflecken nur noch dann wenn ein schiff abgeschossen wird (inkl. grosses AI schiff)
#done: patrol oil spawnt nur im eck und schrumpft nicht
#done: schwarzes AI Schiff verschwindet manchmal
#done: stossen 2 Ölflecken längere Zeit zusammen dann "kalben" Sie einen baby-Ölfleck der ins Spielfeld schwimmt und bei Kollision mit Player explodiert.
#done: AI-Schiffe kommen auch vom Zentrum. Sind selbst Feuerempfindlich-
#done: gelbe Vektoren für Feuer, schwarze Vektoren für AI Schiff
#done: schwarze statt braun, violett statt schwarz.
#done: Ölflecken patrollieren am Rand, spawnen von rand-mitte
#done: GhostTank dreht sich nicht ordentlich mit boss mit.
#done: regeneration (self.regen) von Tanks
#done: Schüsse werden kleiner, mehr damage wenn Schüsse gross sind, Tank hat flytime (für Schüsse)
#done: cooler Bug am Anfang, Schiffe schiessen am Start
#done: Spiel erkennt nicht Game-Over Situation
#done: hitratio - division by zero bug gelöst
#done: pygame <1.8 versionsabfrage, sollte jetzt auch mit pygame 1.7 laufen
#done: Tastaturkürzel sinnvoller (links/rechts), auf mac/netbook testen. Vorschlag: player1: wasd, player2: ijkl oder cursor
#done: 4 Player !
#done: feuervektorliste, gegnervektorliste
#done: Mausvecktor und Positionsvektor mit variabler Länge
#done: Vektorenkreise schön an screenrectseiten ausrichten (Blocksatz)
#done: Vektoren wachsen aus kreis raus (bei ship-coll)
#done: seltsamer zoom-fehler debugt (textsize erhöht anstatt rotozoom bei text verwendet)
#done: Text-classe die schön zoomt und davon abgeleitete hitpointtext mit hitpoint-update
#done: hitpointtext machen
#done: gelber Damagetext bei Ölflecken (danger)
#done: Vectorsprite holt sich koordinaten von bosssprite (Tank)
#done: Victory und Looser Text, vorbereitet für mehr als 2 Spieler
#done: Ölflecken "fressen" Bälle
#done: 4 Ölflecken, am Rand
#done: player2 startet rechts unten
#done: finale Explosion
#done: 2. Vektorspirte mehr nach rechts
#done: unglieche tick-zeit..kugeln fliegen unterschiedlich schnell (?)
#done: schiffe stoppen total bei zusammenstoss
#done: schüsse bremsen (gegenvektor), nicht nur verschieben der Position
#done: schwimmendes Feuer (sehr primitv)
#done:  hitpoints-balken, trefferanzeige
#done: Kugeln haben Farbe von Bosssprite
#done: keine Schmutzflecken mehr. Vorher: entstehen bei speed und schiessen.
#done: ball und schuss
#done: screen und screenrect
#done: move-vektor
#done: Forcevektor
#done: Mausvektor
#done: brems-steuerungslichter
#done: speedlimit
#done: modus umschalten mit m
#done: time-based movement
#done: 2 Tracer Linien von den Eckpunkten, wie Kondensstreifen

from __future__ import division
import operator # für vec2d
import math     # für vec2d
# für mich
import pygame   
import random
random.seed() # init random generator with time or other random value
#import vec2d

    



class vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to vec2d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'vec2d(%s, %s)' % (self.x, self.y)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
    
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        return self.x or self.y
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a vec2d"
        if isinstance(other, vec2d):
            return vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a vec2d"
        if (hasattr(other, "__getitem__")):
            return vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, vec2d):
            return vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return vec2d(self.x + other[0], self.y + other[1])
        else:
            return vec2d(self.x + other, self.y + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, vec2d):
            return vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return vec2d(self.x - other[0], self.y - other[1])
        else:
            return vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, vec2d):
            return vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, vec2d):
            return vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return vec2d(self.x*other[0], self.y*other[1])
        else:
            return vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return vec2d(-self.x, -self.y)
 
    # vectory functions
    def get_length_sqrd(self): 
        return self.x**2 + self.y**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)    
    def __setlength(self, value):
        length = self.get_length()
        if length == 0:
            pass # do nothing
        else:
            self.x *= value/length
            self.y *= value/length

    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
       
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return vec2d(x, y)
    
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))
            
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return vec2d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return vec2d(-self.y, self.x)
    
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return vec2d(-self.y/length, self.x/length)
        return vec2d(self)
        
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])
        
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
        
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2
        
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)
    
    def cross(self, other):
        return self.x*other[1] - self.y*other[0]
    
    def interpolate_to(self, other, range):
        return vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
    
    def convert_to_basis(self, x_vector, y_vector):
        return vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y]
        
    def __setstate__(self, dict):
        self.x, self.y = dict
        
# ---------------------------
# start


class Tank(pygame.sprite.Sprite):
    def __init__(self, screenrect, id="player1", mass=100.0):
        pygame.sprite.Sprite.__init__(self)
        #, color=(0,255,0) , pos=(100.0,100.0)
        self.screenrect = screenrect
        #self.mass = mass # how heavy the ship is
        self.mass = 100
        self.geist = False # i am not a ghost
        self.friction = 0.9 # 0.9 reduce speed for 10% each second
        if id == "player1":
            self.vc = (160,200)
            self.pos = vec2d(160,200)
            self.rotating=-30.0 # heading west
            self.color = (255,64,64)
            self.color2 = (255,0,128)
            self.color3 = (255,128,0)
            self.l = pygame.K_a
            self.r = pygame.K_d
            self.u = pygame.K_w
            self.d = pygame.K_s

        elif id == "player2":
            #self.rotating = 0.0 
            self.vc = (screenrect.width - 160, 200)
            self.pos = vec2d(screenrect.width - 160, 200)
            self.rotating=-150.0 # heading west
            self.color = (64,64,255)
            self.color2 = (0,128,255)
            self.color3 = (128,0,255)
            self.l = pygame.K_LEFT
            self.r = pygame.K_RIGHT
            self.u = pygame.K_UP
            self.d = pygame.K_DOWN
        elif id=="player3":
            self.vc = (160, screenrect.height - 200)
            self.pos = vec2d(160, screenrect.height - 200)
            self.rotating= 30.0 # heading west
            self.color = (64,255,64)
            self.color2 = (0,255,128)
            self.color3 = (128,255,0)
            self.l = pygame.K_j
            self.r = pygame.K_l
            self.u = pygame.K_i
            self.d = pygame.K_k
        elif id=="player4":
            self.vc = (screenrect.width - 160, screenrect.height - 200)
            self.pos = vec2d(screenrect.width - 160, screenrect.height - 200)
            self.rotating= 150.0 # heading west
            self.color = (255,64,255) #64x3
            self.color2 = (32,64,0)
            self.color3 = (10,64,32)
            self.l = pygame.K_KP4 
            self.r = pygame.K_KP6 
            self.u = pygame.K_KP8  # or KP8
            self.d = pygame.K_KP5
            
        self.shotby = {}
        self.shotby["player1"] = 0
        self.shotby["player2"] = 0
        self.shotby["player3"] = 0
        self.shotby["player4"] = 0
        self.shotby["danger"] = 0
        self.shotbysomebody = 0
        self.wrap = True # wrap-around world
        self.force = 0
        self.regen = 1 # regenarte hitpoints per full second
        #--- reloading and ammo
        self.flytime =  2.5 #1.0 # 5.0 seconds ... how long a shot fly
        self.reloading = 0.1 # tank can not fire while relaoding -------- BUG !!!! -----
        self.reloadingtime = 0.3 # seconds needed to reload, 0.0 means automatic fire
        self.ammowrap = 1 # how many time the ammo will wrap around world edge
        self.moving = vec2d(0.0,0.0)
        self.image1 = pygame.Surface((50,50))
        self.image1.fill((255,255,255))         # fill with white
        self.image1.set_colorkey((255,255,255)) # make white transparent
        pygame.draw.rect(self.image1 , (10,10,10), (0,0,50,8))
        pygame.draw.rect(self.image1, (10,10,10), (0,42,50,50))
        self.p1 = (-25.0,-25.0) # middle is 25,25
        self.p2 = (-25.0, 25.0) # middle is 25,25
        pygame.draw.polygon(self.image1, (64,64,64), [(5,10),(5,40),(50,25)],0)
        pygame.draw.circle(self.image1, self.color,(25,25),16,0) # 0 füllt den Kreis
        self.image1.convert_alpha()
        self.image = self.image1.copy() # copy to not destroy image1
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.pos.x,0),round(self.pos.y,0)) 
        self.limit = 100 # the speed limit # --------------------- ausprobieren
        self.rotspeed = 0.0
        self.maxrotspeed =300 # maximum turnspeed
        self.rotdelta = 30   # um wieviel gedreht wird
        self.forcedelta = 5  # 
        self.oldcenter = (0,0)
        self.oldcenter2 = (0,0)
        self.oldrot = 0
        self.spacemove= vec2d(0,0)
        self.newmoving = vec2d(0,0)
        self.cm = 0.0 # angle to mouse
        self.cmd = 0.0 # distance to mouse
        self.showvector = True
        self.modus = "space"
        self.speedflag = False
        self.showtext = False
        self.drawTracer = False
        self.id= id
        self.hitpoints = 500.0  # float division ! # 500.0
        self.hitpointsfull = 500.0       # 500.0
        self.peaceful = False
        self.hitradius = 20.0
        #self.damagemax = 1 # how much damage a bullet in the center does (20)
        # damagemax can be higher by 5 because it is difficult to
        # teleport a bullet into the center
        #self.damagemin = 1  # how much damage a bullet on the edge does
        self.offset = 15 # if set to 0 tank can complete disappear behind
                        # screen edge bevor wrap-around on other site
                        # a offset > 0 spoil that, so that a bit of the tank
                        # should be always visible
        #self.shotby = None
        self.shots = 0 # how many balls this tank shoots in his lifetime
        self.hits = 0 # how many times this thank hits an enemy in his lifetime
        self.age = 0.0
        self.ageseconds = 0
        self.alive = True
        
        
    def fire(self):
        """check if firing is allowed, return True if yes and set the reloadingtime"""
        if self.peaceful:
            return False
        elif self.reloading > 0:
            return False # Tank is still reloading
        elif not self.screenrect.collidepoint(self.rect.center):
            # firing not allowed if Tank center out of screenrect
            return False
        else:
            self.reloading = self.reloadingtime # now the weapon must be reloaded for some time
            self.shots += 1
            return True
        
    def update(self, tick_seconds):
        """tick is the time passed since last frame in seconds"""
        #save old position
        self.age += tick_seconds # Tank get older
        if self.age - self.ageseconds > 1: 
            # a full second survived, time for regeneration
            self.ageseconds = int(self.age)
            self.hitpoints += self.regen # heals each full second
        self.rect = self.image.get_rect()
        self.oldcenter = self.rect.center # from the image, only for rotating
        
        # check reloading time,check if ready to fire again
        if self.reloading: # <>0..True, 0..False
            self.reloading -= tick_seconds
        if self.reloading < 0:
            self.reloading = 0
        
        # image selector / rotation / speed lights painting
        self.image = self.image1.copy()
        if self.rotspeed < 0:
            #self.image = self.image2
            pygame.draw.rect(self.image,  (255,0,0), (0,0,8,8))
            pygame.draw.rect(self.image,  (255,0,0), (42,42,50,50))
        elif self.rotspeed > 0:
            pygame.draw.rect(self.image, (255,0,0), (0,42,8,50))
            pygame.draw.rect(self.image, (255,0,0), (42,0,50,8))           
        if self.force > 0:
            pygame.draw.rect(self.image, (255,0,0), (0,10,5,30))
        elif self.force < 0:
            pygame.draw.rect(self.image, (255,0,0), (45,10,50,30))
        

        #--- rotate the sprite
        self.rot(self.image)
        
        #--- calculate new position
        self.rect.center = (round(self.pos.x,0), round(self.pos.y,0))
        #self.oldcenter2 = self.rect.center # save for drawing

        #--- render mousevector  # FIXME...ugly !
        c = vec2d(self.rect.center) # vector to center on screen
        m = vec2d(pygame.mouse.get_pos()) #vector to mousepos on screen
        cm =  m - c # vector from sprite-center to mousepos
        self.cm = cm.angle
        self.cmd = cm.length 
        cm.length = 16 # shrink length to radius of sprite circle
        #    calulate the new middle of the rotated sprite
        nm = vec2d(self.image.get_rect().width/2,self.image.get_rect().height/2)
        cm += nm  # correction because sprite is rotated, middle point moves
        pygame.draw.line(self.image, (0,0,0), (nm.x,nm.y), (int(cm.x), int(cm.y)),1)

        # more precise keyboard event handler
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.l]:
            self.rotspeed += self.rotdelta 
        if pressed_keys[self.r]:
            self.rotspeed -= self.rotdelta
        if pressed_keys[self.u]:
            self.force += self.forcedelta
        if pressed_keys[self.d]:
            self.force -= self.forcedelta
            
        # halt rotation when not-auto
        if self.modus != "auto":
            if (not pressed_keys[self.l] and 
                not pressed_keys[self.r]):
                    self.rotspeed = 0 # stop rotation
            if (not pressed_keys[self.u] and
                not pressed_keys[self.d]):
                    self.force = 0 # stop moving
            
        #limit to limit, maxrotspeed
        if self.rotspeed > self.maxrotspeed:
            self.rotspeed = self.maxrotspeed
        if self.rotspeed < -self.maxrotspeed:
            self.rotspeed = -self.maxrotspeed
        
        if self.force >= self.limit:
            self.force = self.limit
            self.speedflag = True
        elif self.force <= -self.limit:
            self.force = -self.limit
            self.speedflag = True
        else:
            self.speedflag = False
            
        #reset rotation on 360 Degree
        if self.rotating < -360:
            self.rotating += 360
        if self.rotating > 360:
            self.rotating -= 360
        
        # time-based rotation        
        self.rotating += self.rotspeed * tick_seconds 
        
        #FIXME: das geht sicher einfacher auch
        # simple forward movement
        if self.modus=="space":
            if self.force!=0:
                if self.rotating != 0:
                    dazu = vec2d(self.force, 0)
                    dazu.rotate(-self.rotating)
                    self.spacemove += dazu
                else:
                    self.spacemove += vec2d(self.force,0)
            # check speed limit
            if self.spacemove.length >= self.limit:
                self.spacemove.length = self.limit
                self.speedflag = True
            else:
                self.speedflag = False
            #self.pos += self.spacemove * tick_seconds
            self.newmoving = self.spacemove # komaptibel machen ?
            
        else:
            if self.force!= 0:
                self.newmoving = vec2d(self.force,0)
                if self.rotating != 0:
                    self.newmoving.rotate(-self.rotating)
                #self.pos += self.newmoving * tick_seconds
        self.newmoving *= self.friction ** tick_seconds # Reibung Leo
        self.pos += self.newmoving * tick_seconds 
        if self.wrap: 
            # wrap-around world
            #if self.pos.x + self.rect.width/2 < 0:
            #    #self.pos.x = self.screenrect.get_width()  + self.rect.width/2
            #    self.pos.x = self.screenrect.width  + self.rect.width/2 - self.offset
            #if self.pos.x - self.rect.width/2 > self.screenrect.width:
            #    self.pos.x = 0 - self.rect.width/2 + self.offset
            #if self.pos.y + self.rect.height/2 < 0:
            #    self.pos.y = self.screenrect.height + self.rect.height/2 - self.offset
            #if self.pos.y - self.rect.height/2 > self.screenrect.height:
            #    self.pos.y = 0 - self.rect.height/2 + self.offset
            #--------- wrap at self.rect.center, TankGhost will care about the Rest
            if self.pos.x < 0:
                self.pos.x = self.screenrect.width
            if self.pos.x > self.screenrect.width:
                self.pos.x = 0
            if self.pos.y < 0:
                self.pos.y = self.screenrect.height
            if self.pos.y > self.screenrect.height:
                self.pos.y = 0
            
            
        else:
             #no wrap-around  , stop on end of screen
            if self.pos.x < 0:
                self.pos.x = 0 
            if self.pos.x > self.screenrect.width:
                self.pos.x = self.screenrect.width
            if self.pos.y < 0:
                self.pos.y = 0
            if self.pos.y > self.screenrect.height:
                self.pos.y = self.screenrect.height
        
        #draw tracer ?
        if self.drawTracer:
            self.tracer()
        #else:
        #    self.dirtyrect=(0,0,0,0)
        
    def tracer(self):  
        #test if tracer is not too long (because world-wrap)
        nc = vec2d(self.rect.center)
        oc = vec2d(self.oldcenter2)
        if (nc - oc).length < self.rect.width:
            pygame.draw.line(background, self.color,self.oldcenter2, self.rect.center,2)
            nc1 = vec2d(self.p1)
            nc2 = vec2d(self.p2)
            oc1 = vec2d(self.p1)
            oc2 = vec2d(self.p2)
            # rotate the tracer-vectors
            vec2d.rotate(nc1,-self.rotating)
            vec2d.rotate(nc2,-self.rotating)
            vec2d.rotate(oc1,-self.rotating)
            vec2d.rotate(oc2,-self.rotating)
            #"----adding rect center----"
            nc1 += nc 
            nc2 += nc
            #"------ adding oldcenter ------"
            oc1 += oc
            oc2 += oc
            # draw the lines from old to new
            pygame.draw.line(background, self.color2, (oc1.x, oc1.y),(nc1.x,nc1.y),1)
            pygame.draw.line(background, self.color3, (oc2.x, oc2.y),(nc2.x,nc2.y),1)
            #self.dirtyrect =(int(min(nc1.x, nc2.x, oc1.x, oc2.x, oc.x, nc.x))-1,
            #                 int(min(nc1.y, nc2.y, oc1.y, oc2.y, oc.y, nc.y))-1,
            #                 int(max(nc1.x, nc2.x, oc1.x, oc2.x, oc.x, nc.x))+1,
            #                 int(max(nc1.y, nc2.y, oc1.y, oc2.y, oc.y, nc.y))+1)
        self.oldcenter2 = self.rect.center # save old tracerposition        
                                        
    def rot(self, image):
        self.image = pygame.transform.rotate(image, self.rotating)
        self.rect.center = self.oldcenter 
    def kill(self):
        self.alive = False
        pygame.sprite.Sprite.kill(self)
    
class TankGhost(Tank):
    def __init__(self, boss, id):
        """ id = N, S , W, E"""
        Tank.__init__(self, boss.screenrect, boss.id, mass=100.0)
        self.boss = boss
        self.id = id
        self.color = boss.color
        self.peaceful = True # Ghost does not fire
        self.geist = True # i am a ghost
            
    def update(self, tick_seconds):
        # is boss dead ?
        if self.boss.alive == False:
            pygame.sprite.Sprite.kill(self)
            #TankGhost.kill(self)
            
        self.image = self.boss.image
        self.rect = self.image.get_rect()
        if self.id == "N":
            self.rect.center = (self.boss.rect.centerx, self.boss.rect.centery - self.boss.screenrect.height)
        elif self.id == "S":
            self.rect.center = (self.boss.rect.centerx, self.boss.rect.centery + self.boss.screenrect.height)
        elif self.id == "W":
            self.rect.center = (self.boss.rect.centerx - self.boss.screenrect.width , self.boss.rect.centery)
        elif self.id =="E":
            self.rect.center = (self.boss.rect.centerx + self.boss.screenrect.width , self.boss.rect.centery)
        
 
         
    
            
            
            
class Bar(pygame.sprite.Sprite):
        """ a health-bar floating above each player"""
        
        def __init__(self, boss, vectorbar=False, color=(0,255,0)):
            pygame.sprite.Sprite.__init__(self)
            self.vectorbar = vectorbar
            self.boss = boss
            if self.vectorbar:
                self.long = 300 # vectorsprite circle radius * 2
            else:
                self.long = boss.rect.width
            self.longold = self.long
            self.percent = 1.0
            self.percentold = 0.0
            self.color = color
            self.image = pygame.Surface((self.long,5))
            
        def update(self, tick):
            """tick is the time passed since last frame in seconds"""
            if self.boss.hitpoints <= 0:
                self.kill()
            self.percent = (self.boss.hitpoints /
                            self.boss.hitpointsfull)
            if not self.vectorbar:
                self.long = self.boss.rect.width
            if self.percent != self.percentold or self.longold != self.long:
                self.image = pygame.Surface((self.long,5))
                self.rect = self.image.get_rect()
                self.image.fill((255,255,255))        # white
                pygame.draw.rect(self.image,(0,255,0),(0,0,
                                 int(self.long*self.percent), 5))
                #black rectangle
                pygame.draw.rect(self.image,(0,0,0),(0,0,self.long,5), 1) 
                self.image.set_colorkey((255,255,255))
                self.image.convert_alpha()
            if self.vectorbar:
                self.rect.centerx = self.boss.vc[0]
                self.rect.centery = self.boss.vc[1] - 160 # vectorbar above vectorcircle
            else:
                self.rect.centerx = self.boss.rect.centerx
                self.rect.centery = self.boss.rect.y - 10
            self.percentold = self.percent
            self.longold = self.long

class Text(pygame.sprite.Sprite):
        """a changable text"""
        def __init__(self, pos, msg="Hello World",color=(5,5,5), maxlifetime=-1.0, textsize=25, vec=vec2d(0,0),msgchange=False, zoom=False):
            """ negative maxlifetime means stay until Game Over
                msgchange means the message may change over time
                pos in format(x,y), will be changed into vec2d in Text__init__"""
            pygame.sprite.Sprite.__init__(self)
            #self.static = static #static means text does not disappear
            self.zoom = zoom
            self.zoomfactor = 4.0
            self.textsize = int(textsize)
            self.textsize0 = self.textsize
            self.msgchange = msgchange
            self.vec = vec
            self.pos = vec2d(pos)
            self.msg = msg
            self.color = color
            self.recalcimage()
            self.rect.center = pos
            self.lifetime = 0
            self.maxlifetime = maxlifetime #seconds
            self.tick = 0.0 # seconds since last frame
            #self.recalc(self.msg)

        
        def update(self, tick):
            """tick is passed seconds"""
            self.tick = tick
            self.lifetime += tick
            if self.zoom:
                self.textsize = int(self.textsize0 + self.lifetime * self.zoomfactor) # int instead of round becaouse round makes float and float upset pygame.font
                self.msgchange = True
            if self.msgchange:
                self.recalcimage()
            if self.vec != vec2d(0,0):
                self.pos += self.vec * self.tick # self.pos is a vec2d object
                self.rect.center  = (round(self.pos.x,0), round(self.pos.y,0))
            if self.maxlifetime > 0 and self.lifetime > self.maxlifetime:
                self.kill()
        
        #def kill(self):
        #    pygame.sprite.Sprite.kill(self)
            
        def recalcimage(self):
            """renders the text to self.image"""
            self.font = pygame.font.SysFont("None",self.textsize)
            self.textsurface1 = self.font.render(self.msg, True, self.color) #antialias = False
            self.image = pygame.Surface((self.textsurface1.get_size()))
            self.image.fill((255,255,255))         # fill with white
            self.image.set_colorkey((255,255,255)) # make white transparent
            #self.image = self.image1.copy() # to save image1
            self.image.blit(self.textsurface1,(0,0))
            self.rect = self.image.get_rect()
            self.rect.center  = (round(self.pos.x,0), round(self.pos.y,0))
     


class HitpointText(Text):
    """ this class inherit from Text class and updated the hitpoints of a given player"""
    def __init__(self, boss):
        Text.__init__(self, boss.vc , "dummytext", (0,0,0),-1,20, vec2d(0,0), True, False)
        self.boss = boss
        self.pos += vec2d(0,-170) # self.pos is a vec2d object from Text ?
    def update(self, tick):
        self.msg = "Hitpoints:"+str(self.boss.hitpoints)
        Text.update(self, tick)




        
        
class VectorSprite(pygame.sprite.Sprite):
    """draws a drawing of the tank in a fixed position
       including vectors for relative speed, enemy etc."""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        #self.startx = startx
        self.image0 = pygame.Surface((300,300)) # 200,200
        self.image0.fill((255,255,255))         # fill with white
        self.image0.set_colorkey((255,255,255)) # make white transparent
        self.image0.convert_alpha()
        self.vc = (int(self.boss.vc[0]),int(self.boss.vc[1])) # Vectorcenter from boss_sprite
        self.color = self.boss.color # get color from boss
        # draw polygon, same as Tank, but without colors
        self.image1 = pygame.Surface((50,50))
        self.image1.fill((255,255,255))         # fill with white
        self.image1.set_colorkey((255,255,255)) # make white transparent
        pygame.draw.rect(self.image1 , self.color, (0,0,50,8),1)
        pygame.draw.rect(self.image1 , self.color, (0,42,50,8),1) # small bug
        pygame.draw.polygon(self.image1, self.color, [(0,10),(0,40),(50,25)],1)
        pygame.draw.circle(self.image1, self.color,(25,25),16,1) # 0 füllt den Kreis
        pygame.draw.line(self.image1, self.color,(25,25),(50,25),1) # strich schaut nach rechts
        self.image1.convert_alpha()
        self.image = self.image0.copy() # to save image1
        self.rect = self.image.get_rect()
        self.size = 5
        self.dangerlist = []
        self.enemylist = []

    def learn(self, enemy, danger=True):
        """ learn about one enemy at a time, but not about self"""
        if danger:
            self.dangerlist.append(enemy)
        else:
            if enemy.color != self.boss.color:
                self.enemylist.append(enemy)
           
    
    def update(self, tick_seconds):
        """ update the vectors and rotation of the tank.
            tick_seconds is only here to get accepted, but i do nothing with it"""
        #self.dangerlist = []
        #self.enemylist = []
        if self.boss.showvector:
            #--- draw vectorsprite with correct rotation
            self.image = self.image0.copy()
            self.image2 = self.image1.copy()
            self.image2 = pygame.transform.rotate(self.image2 , self.boss.rotating)
            rect = self.image2.get_rect()
            center2 = rect.center
            #self.image.blit(self.image2, (100-rect.width/2, 100-rect.height/2))
            self.image.blit(self.image2, (150-rect.width/2, 150-rect.height/2))
            self.rect.center = self.vc
            
            #--- draw big mousevector
            #cm = vec2d(0,min(150, self.boss.cmd)) # cmd is sprite-mousedistance
            #cm.rotate(self.boss.cm-90) # self.boss.cm contains the angle from tank to mouse
            #cm += vec2d(self.vc)
            #pygame.draw.line(screen, (0,255,255),(self.vc), (cm.x, cm.y),1) # cyan
            
            #--- draw force vector
            f = 1.0 * self.boss.force / self.boss.limit # 1.5 is around the vectorcircle 
            cm = vec2d(0, f*150.0)
            cm.rotate(-self.boss.rotating-90)
            cm += vec2d(self.vc)
            pygame.draw.line(screen, self.boss.color, (self.vc), (round(cm.x,0), round(cm.y,0)),20)
            
            
            #--- draw space vector
            if self.boss.modus =="space":
                speed = 1.0 * self.boss.spacemove.length / self.boss.limit
                s = min(1, speed)
                if speed > 1:
                    self.size +=1
                else:
                    self.size = 5
                cm = vec2d(0, s*150.0)
                cm.rotate(self.boss.spacemove.angle-90)
                cm += vec2d(self.vc)
                pygame.draw.line(screen, (255,0,255), (self.vc), (int(cm.x), int(cm.y)),self.size) # pink
            
            #--- draw sprite vector
            cm =  vec2d(self.boss.rect.center) - vec2d(self.vc)  
            #diagonal = vec2d(self.vc) - vec2d(self.boss.screenrect.width, self.boss.screenrect.height)
            #dia = diagonal.length * 1.0 # to get float
            #cm.length = (cm.length / dia)*100
            cm.length = min(cm.length, 150.0)  #100
            cm+=vec2d(self.vc)
            pygame.draw.line(screen, (0,0,0), (self.vc), (int(cm.x), int(cm.y)),1)
                        
            #--- draw dangervector
            for dang in self.dangerlist:
                size = 1
                cd = dang.pos - self.boss.pos
                cd.length = min(cd.length, 150.0)
                if cd.length < 150:
                    size = int(150 - cd.length)
                cd+=vec2d(self.vc)
                if dang.type == "oil":
                    col = (255,255,0)
                else:
                    col = (0,0,0)
                pygame.draw.line(screen, col, (self.vc), (int(cd.x), int(cd.y)),size)
            self.dangerlist = []
            
            #--- draw enemyvector
            for enemy in self.enemylist:
                size = 1
                cd = enemy.pos - self.boss.pos
                cd.length = min(cd.length, 150.0)
                if cd.length < 150:
                    size = int(150 - cd.length)
                cd+=vec2d(self.vc)
                pygame.draw.line(screen, enemy.color, (self.vc), (int(cd.x), int(cd.y)),size)
            self.enemylist = []
            
        else:
            self.rect.center = (-400,-400) # hide vectorsprite out of screenrect


        
class Ball(pygame.sprite.Sprite):
    def __init__(self, bossSprite, smoke=False, mass=1):
        pygame.sprite.Sprite.__init__(self)
        self.boss = bossSprite
        self.radius = 5  #5
        Ball.paintme(self, self.radius)
        self.pos = vec2d(self.boss.rect.center)
        self.rect.center = (round(self.pos.x,0), round(self.pos.y,0))
        self.moving=vec2d(self.boss.limit * 1.1,0) # speeed of bullet = 110% of max speed of player 
        #self.moving.rotate(self.boss.cm) # shoot to mousepointer
        self.moving.rotate(-self.boss.rotating) # shoot to direction of Tank/Ship
        self.moving += self.boss.spacemove # add tank velocity to ball velocity
        self.massfactor = 0.2 # reduces the impact in relation to a players mass. #.91 a bissl gross
        self.ammowrap = self.boss.ammowrap # how many times bullet can wrap around screen edge
        self.age = 0.0 # lifetime of ball since start in seconds
        self.maxage = self.boss.flytime # ball is killed if he gets older than this time (in seconds)
        
        
    def update(self, tick_seconds):
        '''tick is time passed in seconds'''
        self.age += tick_seconds # ball get older
        if self.age > self.maxage:
            self.kill()
        else:
            factor = self.age / self.maxage # % of oldness of Ball
            Ball.paintme(self, 1 + self.radius - int(self.radius * factor))
        self.pos += self.moving * tick_seconds
        self.rect.center = (round(self.pos.x,0), round(self.pos.y,0))
        if not self.boss.screenrect.collidepoint(self.rect.center):
            if self.ammowrap > 0:
                self.ammowrap -=1 # one less time allowed to wrap world
                if self.pos.x > self.boss.screenrect.width:
                    self.pos.x = 0
                if self.pos.x < 0:
                    self.pos.x = self.boss.screenrect.width
                if self.pos.y > self.boss.screenrect.height:
                    self.pos.y = 0
                if self.pos.y < 0:
                    self.pos.y= self.boss.screenrect.height
            else:
                self.kill()

            
        
    def paintme(self, radius):
        self.tempradius = radius
        self.image = pygame.Surface((radius*2,radius*2))
        self.image.fill((255,255,255))         # fill with white
        self.image.set_colorkey((255,255,255)) # make white transparent
        pygame.draw.circle( self.image,self.boss.color, (radius,radius), radius , 0)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()   

class Danger(pygame.sprite.Sprite):
    """ an enemy to all players. can be a floating piece of burning oil that damage players
    but ignore shooting.
    or can be an enemy ship."""
    oilborder = [0,0,0,0] # n,w,s,o # this is a class variable
    def __init__(self, screenrect, type="oil", size=40, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.lifetime = 0.0
        self.oldsize = size
        self.screenrect = screenrect
        self.limit = 500 # absolute speed limit
        self.type = type # what kind of Danger, an oil or an boat ?
        self.bar = False # check if i have an hitpoint-bar
        self.wo = -1 # indicator of border of oil, -1 means free floating
        #self.pregnant = 0 # spawn a baby danger ?
        #self.birth = 100 # if self.pregnant reach this value, it will spawn a new baby-danger
        
        distance = 30 # distance from screenrect border to oil.rect.center
        
        if self.type == "oil":
            self.vulnerable = False # can  be shot down            
            self.damagePlayer = True # can damage player that bumb into it
            self.color = (255,random.randint(128,255),0) # between yellow and red ?
            
            if self.size==40:
                pass
                ## big oil, patrol border
                #self.hitpoints = 100
                #self.hitpointsfull = 100
                #self.size = 40
                #self.min = 50
                #self.max = 100 # oil float very slow
            
                ## where to spawn oil ?
                #for side in Danger.oilborder:
                    #if side == min(Danger.oilborder):
                        #wo = Danger.oilborder.index(min(Danger.oilborder))
                        #self.wo = wo
                        #Danger.oilborder[wo] += 1
                        #break
                #if wo == 0:
                    #self.pos = vec2d(self.screenrect.centerx, distance) 
                    #self.vec = vec2d(random.randrange(self.min,self.max) * random.choice([-1,1]), 0)
                #elif wo == 1:
                    #self.pos = vec2d(distance, self.screenrect.centery)
                    #self.vec = vec2d(0, random.randrange(self.min,self.max) * random.choice([-1,1]))
                #elif wo == 2:
                    #self.pos = vec2d(self.screenrect.centerx, self.screenrect.height - distance)
                    #self.vec = vec2d(random.randrange(self.min,self.max) * random.choice([-1,1]), 0)
                #elif wo == 3:
                    #self.pos = vec2d(self.screenrect.width - distance, self.screenrect.centery)
                    #self.vec = vec2d(0, random.randrange(self.min,self.max) * random.choice([-1,1]))
                
            else:
                # small oil. self.wo = -1
                self.hitpoints = 10
                self.hitpointsfull = 10
                self.min = 100
                self.max = 200
                self.pos = vec2d(pos)
                self.vec = vec2d(random.randrange(self.min, self.max) * random.choice([-1,1]),
                                 random.randrange(self.min, self.max) * random.choice([-1,1]))
            
            #for all oil:
            self.image = pygame.Surface((self.size,self.size))
            self.damage = 1 # hitpoint loss for player
            pygame.draw.rect( self.image,self.color, (0,0,self.size,self.size), 0)    
          
        elif self.type == "boat":
            self.vulnerable = True
            self.hitpoints = 100
            self.hitpointsfull = 100
            self.size = 50
            self.damagePlayer = True
            self.min = 5 # minimal speed
            self.max = 100 # maximal speed
            self.pos = vec2d(self.screenrect.centerx, self.screenrect.centery) 
            self.vec = vec2d(random.randrange(self.min,self.max) * random.choice([-1,1]), random.randrange(self.min,self.max) * random.choice([-1,1]))
            #self.damageBall = True
            self.heading = self.vec.angle
            self.vulnerable = True
            self.color = (100,100,100) # grey
            #-------
            self.damage = 10 # damage to player ?
            self.image = pygame.Surface((200,200))
            self.image.fill((255,255,255)) # fill white
            self.image.set_colorkey((255,255,255)) # make white transparent
            pygame.draw.polygon(self.image, self.color, [(0,100), (20,70), (190,70), (200,100), (190,130), (20,130) ] , 0)
            pygame.draw.circle(self.image, (40,100,40), (50,100), 20, 0)
            pygame.draw.circle(self.image, (40,100,40), (100,100), 20, 0)
            pygame.draw.rect(self.image, (40,40,100), [120,72,30,58])
            pygame.draw.circle(self.image, (40,100,40), (170,100), 20, 0)
            self.image.convert_alpha()
            #pygame.transform.flip(self.image, True, False)
            self.image0 = self.image.copy()
            
        # start in screenrect
        
        #complete random direction
        
        #self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center=  (round(self.pos.x,0), round(self.pos.y,0))
        
        

    
    def update(self, tick_seconds):
        '''tick is time passed in seconds'''
        self.lifetime+= tick_seconds
        if self.hitpoints < 0:
            self.kill()
        if self.type == "oil":
            if self.size != self.oldsize:
                 self.image = pygame.Surface((self.size,self.size))
                 self.rect = self.image.get_rect()
            self.color = (255,random.randint(128,255),0) # between yellow and red ?
            pygame.draw.rect( self.image,self.color, (0,0,self.size,self.size), 0)
        elif self.type == "boat":
            #heading is actual mouse position
            #self.vec = vec2d(pygame.mouse.get_pos) - vec2d(self.rect.center)
            c = vec2d(self.rect.center) # vector to center on screen
            m = vec2d(pygame.mouse.get_pos()) #vector to mousepos on screen
            cm =  m - c # vector from sprite-center to mousepos
            #self.cm = cm.angle
            #self.cmd = cm.length 
            cm.length = min(self.max, cm.length) # not faster than self.max
            self.vec = cm
            #rotate boat toward heading
            #self.oldpos = self.rect.center
            self.image = pygame.transform.rotate( self.image0, self.vec.angle)
            #self.rect.center = self.oldpos
        if self.vec.length > self.limit:
            self.vec.length = self.limit
        self.pos += self.vec * tick_seconds
        
        
        
        grow = False
        #no wrap-around  , stop on end of screen
        if self.pos.x < 0:
            #grow = True
            self.pos.x = 0  # stuck on the left side
            #if self.wo == 0 or self.wo == 2:
                #self.vec = vec2d(random.randrange(self.min,self.max), 0)
            #else:
            self.vec = vec2d(random.randrange(self.min,self.max), random.randrange(self.min,self.max) * random.choice([-1,1]))
        if self.pos.x > self.screenrect.width:
            #grow = True
            self.pos.x = self.screenrect.width # stuck on the right side
            #if self.wo == 0 or self.wo == 2:
                #self.vec = vec2d(random.randrange(self.min,self.max)*-1, 0)
            #else:
            self.vec = vec2d(random.randrange(self.min,self.max)*-1, random.randrange(self.min,self.max) * random.choice([-1,1]))
        if self.pos.y < 0:
            #grow = True
            self.pos.y = 0 # stuck on top border
            #if self.wo == 1 or self.wo == 3:
                #self.vec = vec2d(0,random.randrange(self.min, self.max))
            #else:
            self.vec = vec2d(random.randrange(self.min,self.max) * random.choice([-1,1]), random.randrange(self.min,self.max) )
        if self.pos.y > self.screenrect.height:
            #grow = True
            self.pos.y = self.screenrect.height #stuck on bottom
            #if self.wo == 1 or self.wo == 3:
                #self.vec = vec2d(0,random.randrange(self.min, self.max)*-1)
            #else:
            self.vec = vec2d(random.randrange(self.min,self.max) * random.choice([-1,1]), random.randrange(self.min,self.max) * -1)
        self.rect.center = (round(self.pos.x,0), round(self.pos.y,0))
        #self.oldsize = self.size       
        #if grow and self.wo > -1:
            #self.size +=1
        
class Wound(pygame.sprite.Sprite):
        """ a little explosion marking the 'wound' of a hit"""
        def __init__(self, pos, size, maxlifetime=0.5, boss_sprite=None):
            pygame.sprite.Sprite.__init__(self)
            self.size = int(size) # sometimes, wound comes as float (from tux?)
            #if self.size < medium:
            #    self.size *=2
            
            self.pos = pos
            self.maxlifetime = maxlifetime # in seconds
            self.boss_sprite = boss_sprite
            self.age = 0 # age in decimal seconds
            self.frames = 0 #frames in integer
            self.image = pygame.Surface((size*2, size*2))
            self.surface_center = (self.size, self.size) 
            self.rect = self.image.get_rect()
            self.rect.center = (round(self.pos.x,0),round(self.pos.y,0))
            #if self.boss_sprite:
            #    self.dx = self.pos[0] - self.boss_sprite.rect.centerx 
            #    self.dy = self.pos[1] - self.boss_sprite.rect.centery
            self.update(0) # update need the argument tick
            
        def update(self, tick_seconds):
            """ tick_seconds is decimalseconds passed since last frame"""
            self.age += tick_seconds
            self.frames +=1
            if self.age > self.maxlifetime: #one second at 30 fps
                self.kill()
            else:
                self.rect.center = (round(self.pos.x, 0), round(self.pos.y,0))
                pygame.draw.circle(self.image, (255,random.randint(0,255),0),
                     self.surface_center,min(self.size,self.frames), 0)
                self.image.set_colorkey((0,0,0))
                self.image.convert_alpha()
                #if self.boss_sprite:
                #    self.rect.centerx = self.boss_sprite.rect.centerx + self.dx
                #    self.rect.centery = self.boss_sprite.rect.centery + self.dy
                #else:
                #    self.rect.center = self.pos
                



def paint(x, y,  color):
    pygame.draw.circle(background, color, (x,y), 150, 1)
    pygame.draw.line(background, color, (x-160, y) , (x+160,y), 1)
    pygame.draw.line(background, color, (x,y-160), (x,y+160),1)
    textsurface = myFont.render(u"0° = 360°", True, color)
    background.blit(textsurface, (x+50,y-20))
    textsurface = myFont.render(u"90°", True, color)
    background.blit(textsurface, (x-10,y-150))
    textsurface = myFont.render(u"180°", True, color)
    background.blit(textsurface, (x-140,y-20))
    textsurface = myFont.render(u"270°", True, color)
    background.blit(textsurface, (x-10,y+125))
    
#--- main start  --
pygame.init()
try:
    screen=pygame.display.set_mode((0,0)) # (0,0) uses the full screensize
except:
    x = raw_input("enter x resolution of screen:", 800)
    y = raw_input("enter y resolution of screen:", 600)
    if int(x) <= 0 or int(y) <= 0:
        x = 800
        y = 600
    screen=pygame.display.set_mode((x,y))
screenrect = screen.get_rect()
pygame.display.set_caption("press Esc to exit")
#--- background
background = pygame.Surface(screen.get_size())
#background = background.convert()
background.fill((255,255,255))     #fill the background white
#a bit of text
myFont = pygame.font.SysFont("None",25)
#textsurface = myFont.render("Player1: F1=modus, w,as,d,cursor=move, space=shoot", True, (0,0,255))
textsurface0 = myFont.render("pres ESC to Quit", True, (0,0,0))
textsurface1 = myFont.render("Player1: w,a,s,d", True, (0,0,0))
#textsurface2 = myFont.render("Player2: F12=modus, j,i,l,k, Numpad=move, RCTRl,NUM_Enter=shoot", True, (0,0,255))
textsurface2 = myFont.render("Player2: j,i,l,k", True, (0,0,0))
textsurface3 = myFont.render("Player3: cursor-keys", True, (0,0,0))
textsurface4 = myFont.render("Player4: Numpad 4,8,5,6", True, (0,0,0))
#background.blit(textsurface, (20,410)) # blit the textsurface on the backgroundsurface
#background.blit(textsurface2, (20, 430))
#background.blit(textsurface3, (20, 450))
# red circle with crosshair

paint(160, 200, (255,32,32)) # player1, red, left upper corner
paint(screenrect.width - 160, 200, (32,32,255)) # player2, blue right upper corner
paint(160, screenrect.height - 200 , (32,255,32)) # player3, green, lower left corner
paint(screenrect.width - 160, screenrect.height - 200 , (32,32,32)) # player4, black, lower right corner

background.blit(textsurface1, (screenrect.width/2-40,50))
background.blit(textsurface2, (screenrect.width/2-40,70))
background.blit(textsurface3, (screenrect.width/2-40,90))
background.blit(textsurface4, (screenrect.width/2-40,110))
background.blit(textsurface0, (screenrect.width/2-40,130))

backgroundnew = background.copy()
screen.blit(background, (0,0)) # blit the  backgroundsurface on the screen

#--- sprite groups
vectorgroup = pygame.sprite.Group()
ballgroup = pygame.sprite.Group()
tankgroup = pygame.sprite.Group()
bargroup = pygame.sprite.Group()
dangergroup = pygame.sprite.Group()
woundgroup = pygame.sprite.Group()
textgroup = pygame.sprite.Group()
newgroup = pygame.sprite.Group()
# create some sprites
#--- player1 
player1 = Tank(screenrect,"player1") #red
player1vector = VectorSprite(player1)
textgroup.add( HitpointText(player1)  )
#--- player2
player2 = Tank(screenrect,"player2") # blue
player2vector = VectorSprite(player2)
textgroup.add( HitpointText(player2)  )
#-- player3
player3 = Tank(screenrect, "player3") # green
player3vector = VectorSprite(player3)
textgroup.add( HitpointText(player3))
#-- player4
player4 = Tank(screenrect, "player4") # black
player4vector = VectorSprite(player4)
textgroup.add( HitpointText(player4))



# put the sprites in the correct group
bargroup.add(Bar(player1), Bar(player1, True),
             Bar(player2), Bar(player2, True),
             Bar(player3), Bar(player3, True),
             Bar(player4), Bar(player4, True) )

tankgroup.add(player1, TankGhost(player1, "N"), TankGhost(player1, "S"), TankGhost(player1, "W"), TankGhost(player1, "E"),  
              player2, TankGhost(player2, "N"), TankGhost(player2, "S"), TankGhost(player2, "W"), TankGhost(player2, "E"),  
              player3, TankGhost(player3, "N"), TankGhost(player3, "S"), TankGhost(player3, "W"), TankGhost(player3, "E"),  
              player4, TankGhost(player4, "N"), TankGhost(player4, "S"), TankGhost(player4, "W"), TankGhost(player4, "E"))
#stuffgroup.add(player1text, player1speedtext, player1vector,  player2text, player2speedtext, player2vector)
vectorgroup.add(player1vector, player2vector, player3vector, player4vector)
#dangergroup.add( Danger(screenrect, "oil"),
#                 Danger(screenrect, "oil"),
#                 Danger(screenrect, "oil"),
#                 Danger(screenrect, "oil"),
#                 Danger(screenrect, "boat"))
dangergroup.add( Danger(screenrect, "boat") )
# hitpoints for boat
for dang in dangergroup:
    #if dang.vulnerable and not dang.bar:
    if (dang.bar == False)  and (dang.type != "oil"):
        bargroup.add(Bar(dang))
        dang.bar = True

#allgroup = pygame.sprite.LayeredUpdates(playervector, playertext, speedtext, player, ballgroup)
if pygame.ver < "1.8.1":
    allgroup = pygame.sprite.LayeredUpdates(vectorgroup,  dangergroup, woundgroup, textgroup, bargroup, ballgroup, tankgroup)
else:
    allgroup = pygame.sprite.Group(vectorgroup,  dangergroup, woundgroup, textgroup, bargroup, ballgroup, tankgroup)
    



#--- loop prepare ---
mainloop = True
#clock = pygame.time.Clock()
fps = 30 #frames per second
seconds_played = 0.0
recalc = False # recalculate the sprite groups reset to False
finale = False # draw the game-over scene (final explosion etc.)
startGameOverMsg = False
rank = 4 # decrease at each playerkill. 4 because 4 players at maximum
clock = pygame.time.Clock() # create Clock object
#--- mainloop ------
while mainloop:
    tick_time = clock.tick(fps) # milliseconds since last frame
    tick_seconds = tick_time / 1000.0 # decimal-seconds since last frame
    seconds_played += tick_seconds # counter, will not be resetted    
    #clock.tick(30)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # Toggle keys better with keydown than with pressed_keys
            #--- Esc quit -------------
            if event.key == pygame.K_ESCAPE:
                mainloop = False
   
               
            #--- clean F5 -------------
            if event.key == pygame.K_F5:    
                background = backgroundnew.copy()
                screen.blit(background, (0,0)) # redraw the background
            #---tracer F6 -----------------    
            if event.key == pygame.K_F6:
                for tank in tankgroup:
                    tank.drawTracer = not tank.drawTracer          

    #--- fire 
    for tank in tankgroup:
        if tank.fire():
            ballgroup.add(Ball(tank))
            recalc = True        
        
    #--- mainloop core -----------                  
    #--- clear the sprites
    allgroup.clear(screen, background)
     
    if recalc:
        # it is very important that this lines comes AFTER allgroup.clear!
        # else there will be ugly uncleaned sprites all around
        # allgroup = pygame.sprite.LayeredUpdates(stuffgroup,  woundgroup, textgroup, dangergroup, bargroup, tankgroup, ballgroup)
        #allgroup = pygame.sprite.LayeredUpdates(vectorgroup,  dangergroup, woundgroup, textgroup, bargroup, ballgroup, tankgroup)
        if newgroup:
            # any new dangersprites in this group ?
            for dang in newgroup:
                dangergroup.add(dang)
            #newgroup = [] # will be empty at beginning of danger-danger-collision-detection
            for dang in dangergroup:
                # add hitbar if missing
                if (dang.bar == False)  and (dang.type != "oil"):
                    bargroup.add(Bar(dang))
                    dang.bar = True
            newgroup.empty() # remove all sprites from this group
                        
        
        if pygame.ver < "1.8.1":
            allgroup = pygame.sprite.LayeredUpdates(vectorgroup,  dangergroup, woundgroup, textgroup, bargroup, ballgroup, tankgroup)
        else:
            allgroup = pygame.sprite.Group(vectorgroup,  dangergroup, woundgroup, textgroup, bargroup, ballgroup, tankgroup)
    
        
        
    recalc = False # reset recalc
    #--- update all sprites
    allgroup.update(tick_seconds)
    #--- feed sprite-position to vectorgroup
    for vsprite in vectorgroup:
        for dang in dangergroup:
            vsprite.learn(dang, True)
        for tank in tankgroup:
            vsprite.learn(tank, False)
       
    #--- collision detection
    
    
    # ball kills ball:--- removed, because too slow
    #for ball in ballgroup:
    #    ballgroup2 = ballgroup.copy()
    #    crashgroup = pygame.sprite.spritecollide(ball, ballgroup2, False)
    #    killme = False
    #    for ball2 in crashgroup:
    #        if ball2.boss == ball.boss:
    #            #friendly fire
    #            pass # survive
    #        else:
    #            ball2.kill()
    #            killme = True
    #    if killme:
    #        ball.kill()
    
    # --- collision with tank and ball ?
    for tank in tankgroup:
        # ball is always inside screenrect.
        crashgroup = pygame.sprite.spritecollide(tank, ballgroup, False)
        for ball in crashgroup:
            if ball.boss != tank: # no friendly fire
               distance1 = vec2d(tank.pos) #calculate distance to tank center
               distance2 = vec2d(ball.pos)
               distance = distance1 - distance2
               if distance.length > tank.hitradius:
                    pass # nothing happened, bullet missed tank
               else:
                   tank.shotby[ball.boss.id] += 1 
                   tank.shotbysomebody += 1
                   ball.boss.hits += 1 # one point for the shooter                   
                   # ----- more damage depending on  impact speed 
                   impact = tank.spacemove - ball.moving
                   damage = int(impact.length/100)
                   # ----- additional damage if radius of Ball > 1 (point blank shot)
                   damage += ball.tempradius - 1 # tempradius is minimum 1
                   textgroup.add(Text(vec2d(tank.pos), str(damage), ball.boss.color, 1.5, 25, 
                                      vec2d(random.randint(-90,90),random.randint(-250,-120)),
                                      False, True )) # vc = vectorcenter
                   if tank.id[0] == "p":
                       # is it the Tank or a TankGhost ? Tank name begins with player
                       tank.hitpoints -= damage 
                       tank.spacemove += ball.moving * ball.massfactor
                   else:
                       tank.boss.hitpoints -= damage
                       tank.boss.spacemove += ball.moving * ball.massfactor
                   woundgroup.add(Wound(ball.pos, 5))
                   recalc = True
                   ball.kill()
    
    # -- collision tank  with danger ?
    for tank in tankgroup:
        crashgroup = pygame.sprite.spritecollide(tank, dangergroup, False)
        for dang in crashgroup:
            if dang.damagePlayer:
                damage = dang.damage
                textgroup.add(Text(vec2d(tank.pos), str(damage), dang.color, 1.5, 25, 
                              vec2d(random.randint(-90,90),random.randint(-250,-120)),
                              False, True )) # vc = vectorcenter
                if tank.id[0] == "p":
                    # is it the Tank or a TankGhost ?                  
                    tank.hitpoints -= damage
                    tank.shotby["danger"] += 1
                else:
                    tank.boss.hitpoints -= damage
                    tank.boss.shotby["danger"] +=1
                tank.shotbysomebody += 1
                if dang.type == "oil":
                    dang.size -=1
                    #dang.size +=1
                    pass
                else:
                    dang.hitpoints -= 1
            
    #-- collision between ball and danger, explosion, :
    for dang in dangergroup:
        if dang.vulnerable:
            # ---------dang is an AI boat
            crashgroup = pygame.sprite.spritecollide(dang, ballgroup, True) #kill shot
            for ball in crashgroup:
                dang.vec += ball.moving * ball.massfactor
                woundgroup.add(Wound(ball.pos, 5))
                dang.hitpoints -= 1
                
                # dang dead ? explosion, drop goodie, respawn at center 
                
    # -- collision danger with danger ? 
    for dang in dangergroup:
         dangergroup2 = dangergroup.copy()
         dangergroup2.remove(dang) # remove myself from the clone group
         crashgroup = pygame.sprite.spritecollide(dang, dangergroup2, False) # dang survives
         for dang2 in crashgroup:
             if dang.type == "oil" and dang2.type == "oil" and dang.wo == -1 and dang2.wo == -1:
                 #  border patrols spawn only at corner
                 #the bigger oil eats the smaller oil
                 if dang.size > dang2.size and dang2.lifetime > 2.0:
                     dang.size += 1
                     dang2.size = max(5, dang2.size-1)
             if dang.type == "boat" and dang2.type == "oil":
                 dang.hitpoints -= 1
                 dang2.size -=1
                 textgroup.add(Text(vec2d(dang.pos), str(1), (255,255,0), 1.5, 25, 
                    vec2d(random.randint(-90,90),random.randint(120,240)),
                    False, True ))
    
    # -- collision tank with other player ?
    for tank in tankgroup:
        if tank.id[0] == "p":
            # is it the Tank or a TankGhost ?
            tankgroup2 = tankgroup.copy() # copy of tankgroup, include self
            tankgroup2.remove(tank) # remove self of group
            crashgroup = pygame.sprite.spritecollide(tank, tankgroup2, False)
            for tank2 in crashgroup:
                #FIXME --- bis mir was bessers einfällt
                tank.hitpoints -= 1
                textgroup.add(Text(vec2d(tank.pos), str(1), tank2.color, 1.5, 25, 
                  vec2d(random.randint(-90,90),random.randint(120,240)),
                  False, True )) # tank-collision: damage text floats DOWN instead up
        else:
            pass # no collision damage for TankGhost (yet)
            
    #-- danger hitpoint check and oilspawn check
    for dang in dangergroup:
        if dang.type == "oil":
            if dang.wo != -1:
                # immortal oil,  patrol the border
                dang.size = max(40, dang.size) # size can not be less than 10
            else:
                if dang.size < 1:
                    woundgroup.add(Wound(dang.pos, 50, .5)) # small explosion
                    dang.kill()
            if dang.size > 40:
                     dang.size = 40 #  reduce size and spawn child
                     newgroup.add(Danger(screenrect, "oil", 10, dang.pos))
        else:
            #dang is a boat
            if dang.hitpoints < 1:
                woundgroup.add(Wound(dang.pos, 75, .5)) # final explosion
                #rebirth of ship in the middel of the screen
                #spawn 5 mini-oils
                newgroup.add(Danger(screenrect, "oil", 10, dang.pos),
                         Danger(screenrect, "oil", 10, dang.pos),
                         Danger(screenrect, "oil", 10, dang.pos),
                         Danger(screenrect, "oil", 10, dang.pos),
                         Danger(screenrect, "oil", 10, dang.pos))
                dang.pos = vec2d(screenrect.centerx, screenrect.centery)
                dang.hitpoints = dang.hitpointsfull                
    
    
    #--- calculate middle position of polygon made by surviving players
    calclist = []
    for tank in tankgroup:
        if not tank.geist:
            calclist.append(tank.rect.center)
    
    
    #--- tank hitpoint check, game over ?  
    for tank in tankgroup:
        if tank.hitpoints < 0:
            woundgroup.add(Wound(tank.pos, 100, .75)) # final explosion
            tank.peaceful = True # dead Tank cannot shoot
            #spawn oil
            newgroup.add(Danger(screenrect, "oil", 10, tank.pos),
                         Danger(screenrect, "oil", 10, tank.pos),
                         Danger(screenrect, "oil", 10, tank.pos),
                         Danger(screenrect, "oil", 10, tank.pos),
                         Danger(screenrect, "oil", 10, tank.pos))
            if len(tankgroup) > 5:
                textgroup.add(Text(tank.pos, "Loser", tank.color, 5.0, 72, vec2d(0,0), False, True))
                textgroup.add(Text(tank.vc+ vec2d(0,-50), "Loser", (0,0,0), -1, 48, vec2d(0,0), False, False))
                textgroup.add(Text(tank.vc+ vec2d(0,-25), "Rank: %i " % rank, (0,0,0), -1, 48, vec2d(0,0), False, False))
                rank -= 1
                textgroup.add(Text(tank.vc+ vec2d(0,35), "shot by:", (0,0,0), -1, 24, vec2d(0,0), False, False))
                if tank.shotbysomebody == 0:
                    tank.shotbysomebody = 1 # to avoid division by zero
                dy = 75
                if tank.id != "player1" and tank.shotby["player1"] > 0:
                    textgroup.add(Text(tank.vc+ vec2d(0,dy), "player1: %.2f%% " % (100*tank.shotby["player1"] / tank.shotbysomebody), (255,0,0), -1, 24, vec2d(0,0), False, False))
                    dy += 20
                if tank.id != "player2" and tank.shotby["player2"] > 0:
                    textgroup.add(Text(tank.vc+ vec2d(0,dy), "player2: %.2f%% " % (100*tank.shotby["player2"] / tank.shotbysomebody), (0,0,255), -1, 24, vec2d(0,0), False, False))
                    dy += 20
                if tank.id != "player3" and tank.shotby["player3"] > 0:
                    textgroup.add(Text(tank.vc+ vec2d(0,dy), "player3: %.2f%% " % (100*tank.shotby["player3"] / tank.shotbysomebody), (0,255,0), -1, 24, vec2d(0,0), False, False))
                    dy += 20
                if tank.id != "player4" and tank.shotby["player4"] > 0:
                    textgroup.add(Text(tank.vc+ vec2d(0,dy), "player4: %.2f%% " % (100*tank.shotby["player4"] / tank.shotbysomebody), (255,0,255), -1, 24, vec2d(0,0), False, False))
                if tank.hits == 0:
                    quota = 0.0
                else:
                    quota = tank.shots / tank.hits
                textgroup.add(Text(tank.vc+ vec2d(0,5), "hit ratio: %f" % (quota))) # future division, result in float
                tank.showvector = False
            # kill TankGhost's
            tank.kill()
    #if len(tankgroup) == 1 and not startGameOverMsg:
    if len(tankgroup) == 5 and not startGameOverMsg:
        # 1 Tank and 4 TankGhost
        startGameOverMsg = True
        for tank in tankgroup:
            textgroup.add(Text(tank.pos, "Victory", tank.color, 5.0, 72, vec2d(0,-50), False, True))
            textgroup.add(Text(tank.vc + vec2d(0,-50), "Winner", (0,0,0), -1, 48, vec2d(0,0), False, False))
            textgroup.add(Text(tank.vc + vec2d(0,-25), "Rank: %i " % rank, (0,0,0), -1, 48, vec2d(0,0), False, False))
            if tank.hits == 0:
                quota = 0.0
            else:
                quota = tank.shots / tank.hits
            textgroup.add(Text(tank.vc+ vec2d(0,5), "hit ratio: %.2f" % (quota))) # future division, result in float
        textgroup.add(Text((screenrect.width/2,screenrect.height/2), "Game Over", (1,1,1), 5.0,100, vec2d(0,-20), False, True))
        finale = True
            
                         
    if finale:
        if len(woundgroup) == 0:
            mainloop = False # leave game
                                
    #--- draw the sprites
    allgroup.draw(screen)
    #--- decorate screen
    #pygame.display.set_caption("player1 [F1]: %s player2 [F12]: %s mouse: %s balls: %i "
    #% (player.modus, p2.modus , pygame.mouse.get_pos(),len(ballgroup)))
    pygame.display.set_caption( "# text: %i, # balls: %i fps: %.2f" % (len(textgroup), len(ballgroup), 1000.0/tick_time))
    pygame.display.flip()          # flip the screen 30 times a second
#--- end of loop
