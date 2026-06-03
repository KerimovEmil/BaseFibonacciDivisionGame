"""A lightweight confetti / sparkle system for the win celebration."""
import random
import math
import pygame

_CONFETTI_COLORS = [
    (96, 165, 250), (52, 211, 153), (250, 204, 21),
    (251, 146, 60), (167, 139, 250), (244, 114, 182),
]


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "size", "color", "life", "max_life", "spin", "angle")

    def __init__(self, x, y):
        angle = random.uniform(-math.pi, 0)
        speed = random.uniform(220, 560)
        self.x, self.y = x, y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.randint(6, 12)
        self.color = random.choice(_CONFETTI_COLORS)
        self.max_life = random.uniform(1.6, 2.8)
        self.life = self.max_life
        self.angle = random.uniform(0, math.tau)
        self.spin = random.uniform(-8, 8)

    def update(self, dt):
        self.vy += 900 * dt          # gravity
        self.vx *= 0.99
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.spin * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        s = self.size
        chip = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(chip, (*self.color, alpha), (0, 0, s, s), border_radius=2)
        chip = pygame.transform.rotate(chip, math.degrees(self.angle))
        surface.blit(chip, (self.x - chip.get_width() / 2,
                            self.y - chip.get_height() / 2))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, count=90):
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def fountain(self, width, count=40):
        """Spawn a row of confetti near the top of a `width`-wide area."""
        for _ in range(count):
            self.particles.append(Particle(random.uniform(0, width), random.uniform(-20, 60)))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    @property
    def active(self):
        return bool(self.particles)
