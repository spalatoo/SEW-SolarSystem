# Author: Shao Zhang and Phil Saltzman
# Last Updated: 4/20/2005
#
# This tutorial will cover events and how they can be used in Panda
# Specifically, this lesson will use events to capture keyboard presses and
# mouse clicks to trigger actions in the world. It will also use events
# to count the number of orbits the Earth makes around the sun. This
# tutorial uses the same base code from the solar system tutorial.

import direct.directbase.DirectStart
from direct.showbase import DirectObject
from panda3d.core import TextNode, Vec3, Vec4
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
import sys
from RuntimeHandler import *
from Planet import *
from Camera import *
from EventHandler import *



# We start this tutorial with the standard class. However, the class is a
# subclass of an object called DirectObject. This gives the class the ability
# to listen for and respond to events. From now on the main class in every
# tutorial will be a subclass of DirectObject

class World(DirectObject):
    # Macro-like function used to reduce the amount to code needed to create the
    # on screen instructions
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(-1.3, .95 - .05 * i), fg=(1, 1, 1, 1),
                            align=TextNode.ALeft, scale=.05, mayChange=1)

    def __init__(self):

        self.runtime = RuntimeHandler()
        self.eventHandler = EventHandler(self.runtime)
        self.camera = Camera(render, 40)
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        # base.disableMouse()
        # camera.setPos(0, 0, 45)
        # camera.setHpr(0, -90, 0)

        # The global variables we used to control the speed and size of objects
        self.yearscale = 60
        self.dayscale = self.yearscale / 365.0 * 5
        self.orbitscale = 10
        self.sizescale = 0.6

        self.loadPlanets()  # Load, texture, and position the planets
        self.runtime.rotatePlanets()  # Set up the motion to start them moving

        # The standard title text that's in every tutorial
        # Things to note:
        # -fg represents the forground color of the text in (r,g,b,a) format
        # -pos  represents the position of the text on the screen.
        #      The coordinate system is a x-y based wih 0,0 as the center of the
        #      screen
        # -align sets the alingment of the text relative to the pos argument.
        #      Default is center align.
        # -scale set the scale of the text
        # -mayChange argument lets us change the text later in the program.
        #       By default mayChange is set to 0. Trying to change text when
        #       mayChange is set to 0 will cause the program to crash.
        self.title = OnscreenText(text="Solarsystem",
                                  style=1, fg=(1, 1, 1, 1),
                                  pos=(0.9, -0.95), scale=.07)

        self.escEventText = self.genLabelText(
            "ESC: Quit program", 0)

        self.spaceEventText = self.genLabelText(
            "Space: Toggle entire Solar System", 1)

        self.tEventText = self.genLabelText(
            "T: Toggle the Texture", 2)

        self.lEventText = self.genLabelText(
            "L: Toggle the Point-Light Source", 3)

        self.nEventText = self.genLabelText(
            "N: Make the simulation faster", 4)

        self.mEventText = self.genLabelText(
            "M: Make the sumulation slower", 5)

        self.lEventText = self.genLabelText(
            "W|Arrow-up: Go forward", 6)
        self.lEventText = self.genLabelText(
            "S|Arrow-down: Go backward", 7)
        self.lEventText = self.genLabelText(
            "A|Arrow-left: Go left", 8)
        self.lEventText = self.genLabelText(
            "D|Arrow-right: Go right", 9)
        self.lEventText = self.genLabelText(
            "U: Go upward", 10)
        self.lEventText = self.genLabelText(
            "J: Go downward", 11)

        # Events
        # Each self.accept statement creates an event handler object that will call
        # the specified function when that event occurs.
        # Certain events like "mouse1", "a", "b", "c" ... "z", "1", "2", "3"..."0"
        # are references to keyboard keys and mouse buttons. You can also define
        # your own events to be used within your program. In this tutorial, the
        # event "newYear" is not tied to a physical input device, but rather
        # is sent by the function that rotates the Earth whenever a revolution
        # completes to tell the counter to update


        taskMgr.add(self.camera.controlCamera, "camera-task")
        self.accept("escape", sys.exit)  # Exit the program when escape is pressed
        self.accept("space", self.eventHandler.toggleSimulation)
        self.accept("t", self.eventHandler.toggleTexture)
        self.accept("l", self.eventHandler.toggleLight)
        self.accept("n", self.eventHandler.fasterSimulation)
        self.accept("m", self.eventHandler.slowerSimulation)
        self.accept("r", self.eventHandler.restartSimulation)

        self.accept("w", self.camera.setMouseBtn, [0, 1])
        self.accept("arrow_up", self.camera.setMouseBtn, [0, 1])
        self.accept("w-up", self.camera.setMouseBtn, [0, 0])
        self.accept("arrow_up-up", self.camera.setMouseBtn, [0, 0])

        self.accept("s", self.camera.setMouseBtn, [1, 1])
        self.accept("arrow_down", self.camera.setMouseBtn, [1, 1])
        self.accept("s-up", self.camera.setMouseBtn, [1, 0])
        self.accept("arrow_down-up", self.camera.setMouseBtn, [1, 0])

        self.accept("a", self.camera.setMouseBtn, [2, 1])
        self.accept("arrow_left", self.camera.setMouseBtn, [2, 1])
        self.accept("a-up", self.camera.setMouseBtn, [2, 0])
        self.accept("arrow_left-up", self.camera.setMouseBtn, [2, 0])

        self.accept("d", self.camera.setMouseBtn, [3, 1])
        self.accept("arrow_right", self.camera.setMouseBtn, [3, 1])
        self.accept("d-up", self.camera.setMouseBtn, [3, 0])
        self.accept("arrow_right-up", self.camera.setMouseBtn, [3, 0])

        self.accept("u", self.camera.setMouseBtn, [4, 1])
        self.accept("u-up", self.camera.setMouseBtn, [4, 0])

        self.accept("j", self.camera.setMouseBtn, [5, 1])
        self.accept("j-up", self.camera.setMouseBtn, [5, 0])


    # end __init__

    #########################################################################
    # Except for the one commented line below, this is all as it was before #
    # Scroll down to the next comment to see an example of sending messages #
    #########################################################################

    def loadPlanets(self):
        sky = Planet("sky", "models/stars_1k_tex.jpg", "models/solar_sky_sphere", None, 40, None, None, None, False)

        mercury = Planet("mercury", "models/mercury_1k_tex.jpg", "models/planet_sphere", 0.38 * self.orbitscale, 0.385 * self.sizescale, None, 59 * self.dayscale, 0.241 * self.yearscale, True)
        venus = Planet("venus", "models/venus_1k_tex.jpg", "models/planet_sphere", 0.72 * self.orbitscale, 0.923 * self.sizescale, None, 243 * self.dayscale, 0.615 * self.yearscale, True)
        mars = Planet("mars", "models/mars_1k_tex.jpg", "models/planet_sphere", 1.52 * self.orbitscale, 0.515 * self.sizescale, None, 1.03 * self.dayscale, 1.881 * self.yearscale, True)
        moon = Planet("moon", "models/moon_1k_tex.jpg", "models/planet_sphere", 0.1 * self.orbitscale, 0.1 * self.sizescale, None, .0749 * self.yearscale, .0749 * self.yearscale, True)
        asteroid = Planet("asteroid", "models/asteroid.jpg", "models/planet_sphere", 0.3 * self.orbitscale, 0.5 * self.sizescale, None, .0749 * self.yearscale, .0749 * self.yearscale, True)
        earth = Planet("earth", "models/earth_1k_tex.jpg", "models/planet_sphere", self.orbitscale, self.sizescale, [moon], self.dayscale, self.yearscale, True)
        gas = Planet("gas", "models/gas-planet.png", "models/planet_sphere", 2 * self.orbitscale, 1.5 * self.sizescale, [asteroid], 300*self.dayscale, 3*self.yearscale, True)
        sun = Planet("sun", "models/sun_1k_tex.jpg", "models/planet_sphere", 0, 3 * self.sizescale, None, 20, None, True)

        self.runtime.addPlanet(render, mercury)
        self.runtime.addPlanet(render, venus)
        self.runtime.addPlanet(render, mars)
        self.runtime.addPlanet(render, earth)
        self.runtime.addPlanet(render, gas)
        self.runtime.addPlanet(render, sun)
        self.runtime.addPlanet(render, sky)

# end class world

w = World()

run()
