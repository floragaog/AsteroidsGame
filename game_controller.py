from laserbeam import LaserBeam
from asteroid import Asteroid
from spaceship import Spaceship
import math


class GameController:
    """
    Maintains the state of the game
    and manages interactions of game elements.
    """

    def __init__(self, SPACE, fadeout):
        """Initialize the game controller"""
        self.SPACE = SPACE
        self.fadeout = fadeout

        self.spaceship_hit = False
        self.asteroid_destroyed = False
        self.asteroids = [Asteroid(self.SPACE)]
        self.laser_beams = []
        self.spaceship = Spaceship(self.SPACE)

    def update(self):
        """Updates game state on every frame"""
        self.do_intersections()

        for asteroid in self.asteroids:
            asteroid.display()

        # The code will replace (or augment) the next several
        # lines. Laser beam objects should remain in the scene
        # as many frames as their lifespan allows.
        for l in range(len(self.laser_beams)):
            if self.laser_beams[l].lifespan > 0:
                self.laser_beams[l].display()

        self.spaceship.display()

        # Carries out necessary actions if game over
        if self.spaceship_hit:
            if self.fadeout <= 0:
                fill(1)
                textSize(30)
                text("YOU HIT AN ASTEROID",
                     self.SPACE['w']/2 - 165, self.SPACE['h']/2)
            else:
                self.fadeout -= 1

        if self.asteroid_destroyed:
            fill(1)
            textSize(30)
            text("YOU DESTROYED THE ASTEROIDS!!!",
                 self.SPACE['w']/2 - 250, self.SPACE['h']/2)

    def fire_laser(self, x, y, rot):
        """Add a laser beam to the game"""
        x_vel = sin(radians(rot))
        y_vel = -cos(radians(rot))
        self.laser_beams.append(
            LaserBeam(self.SPACE, x, y, x_vel, y_vel)
        )

    def handle_keypress(self, key, keycode=None):
        if (key == ' '):
            if self.spaceship.intact:
                self.spaceship.control(' ', self)
        if (keycode):
            if self.spaceship.intact:
                self.spaceship.control(keycode)

    def handle_keyup(self):
        if self.spaceship.intact:
            self.spaceship.control('keyup')

    def do_intersections(self):
        # Check for intersections
        # between asteroids and laser beams. Laser beams should be removed
        # from the scene if they hit an asteroid, and the asteroid should
        # blow up

        for i in range(len(self.asteroids)):
            for j in range(len(self.laser_beams)):
                if (
                    abs(self.laser_beams[j].x - self.asteroids[i].x)
                    < max(self.asteroids[i].radius, self.laser_beams[j].radius)
                    and
                    abs(self.laser_beams[j].y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius, self.laser_beams[j].radius)):
                    self.blow_up_asteroid(i, j)
                    self.laser_beams.remove(self.laser_beams[j])

        # If the space ship still hasn't been blown up
        if self.spaceship.intact:
            # Check each asteroid for intersection
            for i in range(len(self.asteroids)):
                if (
                    abs(self.spaceship.x - self.asteroids[i].x)
                    < max(self.asteroids[i].radius, self.spaceship.radius)
                    and
                    abs(self.spaceship.y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius, self.spaceship.radius)):
                    # We've intersected an asteroid
                    self.spaceship.blow_up(self.fadeout)
                    self.spaceship_hit = True

    def blow_up_asteroid(self, i, j):
        # The code to blow up an asteroid.
        # The parameters represent the indexes for the list of
        # asteroids and the list of laser beams, indicating
        # which asteroid is hit by which laser beam.

        # Specifically. If the large asteroid is hit, it should
        # break into two medium asteroids, which should fly off
        # perpendicularly to the direction of the laser beam.

        # If a medium asteroid is hit, it should break into three
        # small asteroids, two of which should fly off perpendicularly
        # to the direction of the laser beam, and the third
        # should fly off in the same direction that the laser
        # beam had been traveling.

        # If a small asteroid is hit, it disappears.

        if self.asteroids[i].asize == 'Large':
            self.asteroids.append(
                Asteroid(self.SPACE, 'Med',
                         self.asteroids[i].x, self.asteroids[i].x, math.radians(
                             self.laser_beams[j].rotation+90),
                         -math.radians(self.laser_beams[j].rotation+90),
                         self.laser_beams[j].rotation, 1.0)
            )
            self.asteroids.append(
                Asteroid(self.SPACE, 'Med',
                         self.asteroids[i].x, self.asteroids[i].x, math.radians(
                             self.laser_beams[j].rotation-90),
                         - math.radians(self.laser_beams[j].rotation-90),
                         self.laser_beams[j].rotation, 1.0)
            )
        if self.asteroids[i].asize == 'Med':
            self.asteroids.append(
                Asteroid(self.SPACE, 'Small',
                         self.asteroids[i].x, self.asteroids[i].x, math.radians(
                             self.laser_beams[j].rotation+90),
                         -math.radians(self.laser_beams[j].rotation+90),
                         self.laser_beams[j].rotation, 1.0)
            )
            self.asteroids.append(
                Asteroid(self.SPACE, 'Small',
                         self.asteroids[i].x, self.asteroids[i].x, math.radians(
                             self.laser_beams[j].rotation-90),
                         - math.radians(self.laser_beams[j].rotation-90),
                         self.laser_beams[j].rotation, 1.0)
            )
            self.asteroids.append(
                Asteroid(self.SPACE, 'Small',
                         self.asteroids[i].x, self.asteroids[i].x, math.radians(
                             self.laser_beams[j].rotation-180)/2,
                         math.radians(self.laser_beams[j].rotation-180)/2,
                         self.laser_beams[j].rotation, 1.0)
            )
        if self.asteroids[i].asize == 'Small':
            self.asteroids.remove(self.asteroids[i])
        self.asteroids.remove(self.asteroids[i])
