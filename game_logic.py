import random

class SnakeGame:
    def __init__(self):
        self.reset()


    def reset(self):
        self.box = 20
        self.width = 600
        self.height = 600
        self.snake = [{"x": 9 * self.box, "y": 10 * self.box}]
        self.food = self.place_food()
        self.direction = "RIGHT"
        self.game_over = False

    def place_food(self):
        return {
            "x": random.randint(0, (self.width // self.box) - 1) * self.box,
            "y": random.randint(0, (self.height // self.box) - 1) * self.box
        }

    def change_direction(self, direction):
        if direction == "LEFT" and self.direction != "RIGHT":
            self.direction = direction
        elif direction == "UP" and self.direction != "DOWN":
            self.direction = direction
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = direction
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = direction

    def update(self):
        if self.game_over:
            return self.get_state()

        head = self.snake[0].copy()
        if self.direction == "LEFT":
            head["x"] -= self.box
        if self.direction == "UP":
            head["y"] -= self.box
        if self.direction == "RIGHT":
            head["x"] += self.box
        if self.direction == "DOWN":
            head["y"] += self.box

        # Check for collision with walls
        if head["x"] < 0 or head["y"] < 0 or head["x"] >= self.width or head["y"] >= self.height:
            self.game_over = True

        # Check for collision with self
        for part in self.snake:
            if head["x"] == part["x"] and head["y"] == part["y"]:
                self.game_over = True

        if self.game_over:
            return self.get_state()

        # Check for food collision
        if head["x"] == self.food["x"] and head["y"] == self.food["y"]:
            self.food = self.place_food()
        else:
            self.snake.pop()

        self.snake.insert(0, head)
        return self.get_state()

    def get_state(self):
        return {
            "snake": self.snake,
            "food": self.food,
            "game_over": self.game_over
        }
