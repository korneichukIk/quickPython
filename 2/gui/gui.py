import time
import turtle
import os


class Window:
    def __init__(self, color="Black", title="Untitled Window", height=None, width=None):
        try:
            block_size = int(os.getenv("BLOCK_SIZE"))
        except KeyError:
            print("Environment variable BLOCK_SIZE not found. Set to 20 (default).")
        if height:
            self.height = height * block_size + 50
        else:
            self.height = 1.0

        if width:
            self.width = width * block_size + 50
        else:
            self.width = 1.0
        self.wn = turtle.Screen()
        self.wn.bgcolor(color)
        self.wn.title(title)
        self.wn.setup(width=self.width, height=self.height)

    def stagnate(self, secs=5):
        start = time.time()
        now = 0

        while now - start < secs:
            self.wn.update()

            now = time.time()


class Block(turtle.Turtle):
    def __init__(
        self,
        color="white",
        visualization_speed=10000,
        backtracking=False,
        width=None,
        height=None,
    ):
        super(Block, self).__init__()
        self.hideturtle()
        try:
            self.block_size = int(os.getenv("BLOCK_SIZE"))
        except KeyError:
            print("Environment variable BLOCK_SIZE not found. Set to 20 (default).")
        self.shape("square")
        self.color(color)
        self.penup()
        self.speed(0)
        self.height = height
        self.width = width
        self.vis_speed = visualization_speed
        self.backtracking = backtracking

    def move_block(self, x_coordinate, y_coordinate):
        self.goto(
            x=(x_coordinate - self.width // 2) * self.block_size,
            y=(y_coordinate - self.height // 2) * self.block_size,
        )

        self.showturtle()

        if self.vis_speed > 0:
            time.sleep(1 / self.vis_speed)

        if not self.backtracking:
            self.stamp()
        else:
            self.hideturtle()
