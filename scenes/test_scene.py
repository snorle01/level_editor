import glm, pygame, json
from engine.scene import base_scene
from models.square_model import square_frame_model, square_model
from typing import List

class test_scene(base_scene):
    def __init__(self, engine):
        super().__init__(engine)

        self.grid = (10, 3)
        square_width = 2 / self.grid[0]
        square_height = 2 / self.grid[1]
        rect_width = pygame.display.get_window_size()[0] / self.grid[0]
        rect_height = pygame.display.get_window_size()[1] / self.grid[1]
        
        self.squares: List[square_model] = []
        self.grid_values: List[int] = []

        for i in range(self.grid[0] * self.grid[1]):
            self.grid_values.append(0)

        square_y = -1
        rect_y = pygame.display.get_window_size()[1] - rect_height
        for yi in range(self.grid[1]):
            square_x = -1
            rect_x = 0
            for xi in range(self.grid[0]):
                self.squares.append(square_model(self.engine, (square_x, square_y, 0), (square_width, square_height, 1), (rect_x, rect_y), rect_width, rect_height))
                self.add_object(square_frame_model(self.engine, (square_x, square_y, 0), (square_width, square_height, 1), (rect_x, rect_y), rect_width, rect_height, glm.vec3(0.0, 0.0, 0.0)))
                square_x += square_width
                rect_x += rect_width
            
            square_y += square_height
            rect_y -= rect_height

    def event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            on_color = glm.vec3(0.0, 1.0, 0.0)
            off_color = glm.vec3(1.0, 0.0, 0.0)

            x = int(mouse_pos[0] // (pygame.display.get_window_size()[0] / self.grid[0]))
            fliped_y = int(mouse_pos[1] // (pygame.display.get_window_size()[1] / self.grid[1]))
            y = (self.grid[1] - 1) - fliped_y
            index = x + (y * self.grid[0])

            square = self.squares[index]

            if square.color == off_color:
                self.grid_values[index] = 1
                square.color = on_color
            else:
                self.grid_values[index] = 0
                square.color = off_color
            print(self.grid_values)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            dictionary = {
                "data": self.grid_values
            }

            # Serializing json
            json_object = json.dumps(dictionary, indent=4)

            # Writing to sample.json
            with open("level_data.json", "w") as outfile:
                outfile.write(json_object)

    def render(self):
        super().render()
        for square in self.squares:
            square.render()