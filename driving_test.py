import os
import pygame
from math import tan, radians, degrees, copysign
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=90.0, length=4, max_steering=300, max_acceleration=5.0):
        self.pos = pygame.Rect(x, y, 32, 16)
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        self.pos.x = self.position.x * 32
        self.pos.y = self.position.y * 32

class Wall:
    def __init__(self, x, y, a, b, r = 0):
        self.pos = pygame.Rect(x, y, a, b)
        self.rotation = r

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.walls = []

        self.walls.append(Wall(100 , 10, 10, 720))
        self.walls.append(Wall(200 , 110, 10, 500))

        self.walls.append(Wall(1200 , 10, 10, 720))
        self.walls.append(Wall(1100 , 110, 10, 500))

        self.walls.append(Wall(100 , 10, 1100, 10))
        self.walls.append(Wall(200 , 110, 900, 10))
    
        self.walls.append(Wall(100 , 710, 1100, 10))
        self.walls.append(Wall(200 , 610, 900, 10))
    
    
    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(5, 5)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User inpu
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)
        
            for w in self.walls:
                if car.pos.colliderect(w.pos):
                    print('a')

            # Drawing
            self.screen.fill((0, 0, 0))
            for w in self.walls:
                pygame.draw.rect(self.screen, (0,255,0), w.pos, 0)
            
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()

            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()