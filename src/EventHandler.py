from panda3d.core import AmbientLight, PointLight, VBase4, TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import WindowProperties
import sys

class EventHandler(DirectObject):
    """
    Diese Klasse ist fuer das Verwalten der Events zustaendig. Sobald eine bestimmte Taste gedrueckt beziehungsweise
    der Mauszeiger bewegt wurde, wird ein bestimmtes Event ausgefuehrt.

    :ivar RuntimeHandler runtime: beinhaltet alle Himmelskoerper
    :ivar Camera camera: ermoeglicht den Umgang mit einer Kamera
    :ivar Luminary middle: stellt die Sonne dar
    :ivar boolean pointlightOn: Punktlichtquelle wird im Konstruktor auf "true" gesetzt
    :ivar boolean textureOn: Textur wird im Konstruktor auf "true" gesetzt
    :ivar boolean lightOn: dient zum Togglen des Lichts
    """
    def __init__(self, runtime, camera, middle):
        """
        Hier werden alle Attribute, welche zum Verwalten der Events benoetigt werden, initialisiert. Als Parameter
        werden Objekte vom RuntimeHandler, Camera und Luminary uebergeben. Ebenfalls werden die Methoden "setEvents"
        und "setLegend" aufgerufen.

        :param runtime: beinhaltet alle Himmelskoerper
        :param camera: ermoeglicht den Umgang mit einer Kamera
        :param middle: stellt die Sonne dar
        """
        self.runtime = runtime
        self.camera = camera
        self.middle = middle
        self.pointlightOn = True
        self.textureOn = True
        self.initializeLight()
        self.lightOn = True

        self.setEvents()
        self.setLegend()

    def initializeLight(self):
        """
        In dieser Methode werden 3 Lichtarten initialisiert. Es wird ein AmbientLight auf die Sonne gesetzt und ebenfalls
        ein AmbientLight und ein PointLight auf das gesamte System. Mittels "Vase4" wird hier eingestellt, wie stark
        das Licht das jeweilige Objekt beleuchten soll (je hoeher die Zahl, desto staerker wird beleuchtet).
        """
        self.sunLight = AmbientLight('slight')
        self.sunLight.setColor(VBase4(1, 1, 1, 1))
        sun = self.middle
        slnp = sun.model.attachNewNode(self.sunLight)
        sun.model.setLight(slnp)

        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(alight)

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        self.plnp = render.attachNewNode(plight)
        self.plnp.setPos(0, 0, 0)
        render.setLight(self.plnp)

    def setEvents(self):
        """
        In dieser Methode wird explizit beschrieben, welche Funktion aufgerufen werden soll nachdem eine bestimmte
        Taste gedrueckt wurde (z.B.: "sys.exit" soll nach Druecken von "escape" ausgefuehrt werden, um das Programm
        zu beenden).
        """
        self.accept("escape", sys.exit)
        self.accept("space", self.toggleSimulation)
        self.accept("t", self.toggleTexture)
        self.accept("l", self.toggleLight)
        self.accept("+", self.fasterSimulation)
        self.accept("-", self.slowerSimulation)
        self.accept("r", self.restartSimulation)
        self.accept("b", self.camera.birdPerspective)

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
        self.accept("wheel_up", self.camera.setMouseBtn, [4, 1])

        self.accept("j", self.camera.setMouseBtn, [5, 1])
        self.accept("j-up", self.camera.setMouseBtn, [5, 0])
        self.accept("wheel_down", self.camera.setMouseBtn, [5, 1])

    def genLabelText(self, text, i):
        """
        Mittels dieser Methode wird eine Legendenbeschreibung beim Programm generiert. Dazu muss man als Parameter
        uebergeben, welcher Text dargestellt wird und an welcher Position sich dieser befinden soll.

        :param text: Text, der dargestellt werden soll
        :param i: Position, an dem sich der Text befinden soll
        :return: stellt die Beschreibung am Programm dar
        """
        return OnscreenText(text=text, pos=(-1.3, .95 - .05 * i), fg=(1, 1, 1, 1),
                            align=TextNode.ALeft, scale=.05, mayChange=1)

    def setLegend(self):
        """
        Hier werden die jeweiligen Hilfestellungen zum Verwalten der Events beschrieben und an einer bestimmten Position
        gesetzt (in diesem Fall handelt es sich lediglich um eine fortlaufende Nummer). Fuer jede einzelne
        Textbeschreibung muss die Methode "genLabelText" aufgerufen werden.
        """
        self.escEventText = self.genLabelText(
            "ESC: Quit program", 0)
        self.spaceEventText = self.genLabelText(
            "Space: Toggle entire Solar System", 1)
        self.tEventText = self.genLabelText(
            "T: Toggle the Texture", 2)
        self.lEventText = self.genLabelText(
            "L: Toggle the Point-Light Source", 3)
        self.nEventText = self.genLabelText(
            "+: Make the simulation faster", 4)
        self.mEventText = self.genLabelText(
            "-: Make the simulation slower", 5)
        self.lEventText = self.genLabelText(
            "W|Arrow-up: Go forward", 6)
        self.bEventText = self.genLabelText(
            "B: Bird's-eye view", 7)
        self.lEventText = self.genLabelText(
            "S|Arrow-down: Go backward", 8)
        self.lEventText = self.genLabelText(
            "A|Arrow-left: Go left", 9)
        self.lEventText = self.genLabelText(
            "D|Arrow-right: Go right", 10)
        self.lEventText = self.genLabelText(
            "U: Go upward", 11)
        self.lEventText = self.genLabelText(
            "J: Go downward", 12)

    def toggleLight(self):
        """
        Diese Methode dient zum Verwalten der Punktlichtquelle. Je nachdem, ob das Attribut "lightOn" true oder false
        ist, wird entweder das AmbientLight von der Sonne staerker oder schwaecher gesetzt. Ebenfalls wird entweder
        ein AmbientLight oder ein PointLight auf das gesamte System gesetzt.
        """
        if self.lightOn == True:
            self.sunLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
            render.setLightOff()
            render.setLight(self.alnp)
            self.lightOn = False
        else:
            self.sunLight.setColor(VBase4(1, 1, 1, 1))
            render.setLightOff()
            render.setLight(self.plnp)
            self.lightOn = True

    def toggleTexture(self):
        """
        Diese Methode dient zum Verwalten der Textur. Je nachdem, ob das Attribut "textureOn" true oder false ist,
        wird die Textur entweder ein- oder ausgeschaltet. Davor werden alle Himmelskoerper geholt, damit die
        Aenderungen fuer jeden Himmelskoerper aktiv werden.
        """
        luminaries = self.runtime.getAllLuminaries()
        if self.textureOn == True:
            for luminary in luminaries:
                if luminaries[luminary].textureToggle==True:
                    luminaries[luminary].model.clearTexture()
            self.textureOn = False
        else:
            for luminary in luminaries:
                if luminaries[luminary].textureToggle==True:
                    luminaries[luminary].model.setTexture(loader.loadTexture(luminaries[luminary].texturePath), 1)
            self.textureOn = True

    def restartSimulation(self):
        """
        Moechte man die Simulation neustarten (mittels der Taste "R"), wird diese Funktion aufgerufen.
        """
        self.runtime.restartSimulation()

    def toggleSimulation(self):
        """
        Moechte man die Simulation stoppen bzw. weiter ausfuehren (mittels der Taste "space"), wird diese Funktion
        aufgerufen.
        """
        self.runtime.togglePlaying()

    def fasterSimulation(self):
        """
        Moechte man die Simulation verschnellern (mittels der Taste "+"), wird diese Funktion aufgerufen.
        """
        self.runtime.fasterPlaying()

    def slowerSimulation(self):
        """
        Moechte man die Simulation verlangsamen (mittels der Taste "-"), wird diese Funktion aufgerufen.
        """
        self.runtime.slowerPlaying()

