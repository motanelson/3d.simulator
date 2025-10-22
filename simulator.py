import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class CarSimulator:
    def __init__(self):
        self.car_position = [0.0, 0.0, 0.0]
        self.car_speed = 0.0
        self.road_width = 8.0
        self.road_length = 100.0
        self.camera_distance = 10.0
        self.camera_height = 3.0
        self.steering_angle = 0.0
        
    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Configuração da luz
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 0, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        
        glClearColor(0.53, 0.81, 0.98, 1.0)
        
    def draw_cube(self):
        # Desenhar um cubo manualmente (substitui glutSolidCube)
        vertices = [
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
        ]
        
        faces = [
            [0, 1, 2, 3], [3, 2, 6, 7], [7, 6, 5, 4],
            [4, 5, 1, 0], [1, 5, 6, 2], [4, 0, 3, 7]
        ]
        
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
    
    def draw_torus(self, inner_radius, outer_radius, sides, rings):
        # Desenhar um torus manualmente (substitui glutSolidTorus)
        for i in range(rings):
            glBegin(GL_QUAD_STRIP)
            for j in range(sides + 1):
                for k in range(2):
                    s = (i + k) % rings + 0.5
                    t = j % sides
                    
                    x = (outer_radius + inner_radius * np.cos(s * 2 * np.pi / rings)) * np.cos(t * 2 * np.pi / sides)
                    y = (outer_radius + inner_radius * np.cos(s * 2 * np.pi / rings)) * np.sin(t * 2 * np.pi / sides)
                    z = inner_radius * np.sin(s * 2 * np.pi / rings)
                    
                    glVertex3f(x, y, z)
            glEnd()
        
    def draw_road(self):
        # Desenhar a estrada amarela
        glColor3f(1.0, 0.84, 0.0)
        
        glBegin(GL_QUADS)
        glVertex3f(-self.road_width/2, 0.0, -self.road_length/2)
        glVertex3f(self.road_width/2, 0.0, -self.road_length/2)
        glVertex3f(self.road_width/2, 0.0, self.road_length/2)
        glVertex3f(-self.road_width/2, 0.0, self.road_length/2)
        glEnd()
        
        # Marcas da estrada
        glColor3f(1.0, 1.0, 1.0)
        stripe_width = 0.2
        stripe_length = 2.0
        gap_length = 4.0
        
        z = -self.road_length/2
        while z < self.road_length/2:
            glBegin(GL_QUADS)
            glVertex3f(-stripe_width/2, 0.01, z)
            glVertex3f(stripe_width/2, 0.01, z)
            glVertex3f(stripe_width/2, 0.01, z + stripe_length)
            glVertex3f(-stripe_width/2, 0.01, z + stripe_length)
            glEnd()
            z += stripe_length + gap_length
    
    def draw_car(self):
        glPushMatrix()
        glTranslatef(self.car_position[0], self.car_position[1] + 0.5, self.car_position[2])
        glRotatef(self.steering_angle, 0, 1, 0)
        
        # Corpo do carro (vermelho)
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glScalef(1.5, 0.5, 3.0)
        self.draw_cube()
        glPopMatrix()
        
        # Teto do carro
        glColor3f(0.8, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glScalef(1.0, 0.3, 2.0)
        self.draw_cube()
        glPopMatrix()
        
        # Rodas
        glColor3f(0.1, 0.1, 0.1)
        
        # Roda dianteira esquerda
        glPushMatrix()
        glTranslatef(-1.0, -0.3, 1.0)
        self.draw_torus(0.1, 0.3, 10, 10)
        glPopMatrix()
        
        # Roda dianteira direita
        glPushMatrix()
        glTranslatef(1.0, -0.3, 1.0)
        self.draw_torus(0.1, 0.3, 10, 10)
        glPopMatrix()
        
        # Roda traseira esquerda
        glPushMatrix()
        glTranslatef(-1.0, -0.3, -1.0)
        self.draw_torus(0.1, 0.3, 10, 10)
        glPopMatrix()
        
        # Roda traseira direita
        glPushMatrix()
        glTranslatef(1.0, -0.3, -1.0)
        self.draw_torus(0.1, 0.3, 10, 10)
        glPopMatrix()
        
        glPopMatrix()
    
    def draw_environment(self):
        # Grama ao lado da estrada
        glColor3f(0.0, 0.6, 0.0)
        glBegin(GL_QUADS)
        # Lado esquerdo
        glVertex3f(-20.0, 0.0, -self.road_length/2)
        glVertex3f(-self.road_width/2, 0.0, -self.road_length/2)
        glVertex3f(-self.road_width/2, 0.0, self.road_length/2)
        glVertex3f(-20.0, 0.0, self.road_length/2)
        
        # Lado direito
        glVertex3f(self.road_width/2, 0.0, -self.road_length/2)
        glVertex3f(20.0, 0.0, -self.road_length/2)
        glVertex3f(20.0, 0.0, self.road_length/2)
        glVertex3f(self.road_width/2, 0.0, self.road_length/2)
        glEnd()
    
    def setup_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800/600), 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Câmera seguindo o carro
        camera_x = self.car_position[0] - np.sin(np.radians(self.steering_angle)) * self.camera_distance
        camera_z = self.car_position[2] - np.cos(np.radians(self.steering_angle)) * self.camera_distance
        camera_y = self.car_position[1] + self.camera_height
        
        gluLookAt(
            camera_x, camera_y, camera_z,
            self.car_position[0], self.car_position[1] + 1.0, self.car_position[2],
            0, 1, 0
        )
    
    def update(self, keys, dt):
        acceleration = 0.0
        steering = 0.0
        
        if keys[K_UP] or keys[K_w]:
            acceleration = 20.0
        if keys[K_DOWN] or keys[K_s]:
            acceleration = -15.0
        if keys[K_LEFT] or keys[K_a]:
            steering = 2.0
        if keys[K_RIGHT] or keys[K_d]:
            steering = -2.0
        
        self.car_speed += acceleration * dt
        self.car_speed *= 0.95
        
        self.steering_angle += steering * self.car_speed * dt
        
        self.car_position[0] += np.sin(np.radians(self.steering_angle)) * self.car_speed * dt
        self.car_position[2] += np.cos(np.radians(self.steering_angle)) * self.car_speed * dt
        
        self.car_position[0] = max(-self.road_width/2 + 0.5, min(self.road_width/2 - 0.5, self.car_position[0]))
        
        if self.car_position[2] > self.road_length/2:
            self.car_position[2] = -self.road_length/2
        elif self.car_position[2] < -self.road_length/2:
            self.car_position[2] = self.road_length/2
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.setup_camera()
        self.draw_environment()
        self.draw_road()
        self.draw_car()
        
        pygame.display.flip()

def main():
    # Inicializar GLUT
    glutInit()
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulador de Condução 3D - Estrada Amarela")
    
    simulator = CarSimulator()
    simulator.init_gl()
    
    clock = pygame.time.Clock()
    
    print("Controles:")
    print("Setas/WASD: Controlar o carro")
    print("ESC: Sair")
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        keys = pygame.key.get_pressed()
        simulator.update(keys, dt)
        simulator.draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()