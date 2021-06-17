import random
import operator
import os
from gui.gui import Window, Block


class Maze:
    def __init__(
        self,
        custom_height: int = None,
        custom_width: int = None,
        custom_start_from: tuple = None,
        export_to_file=False,
        visualize_creation=True,
        export_screen=True,
    ):
        self.height = custom_height or random.randint(30, 50)
        self.width = custom_width or random.randint(30, 50)
        self.start_from = custom_start_from or (
            random.randint(0, self.height - 1),
            random.randint(0, self.width - 1),
        )
        self.maze_matrix = [["#"] * self.width for _ in range(self.height)]
        self.stack = []
        self.visited = []
        self.directions = {"L": (0, -1), "R": (0, 1),
                           "U": (-1, 0), "D": (1, 0)}
        self.directions_dir2 = {
            "L": [(1, -1), (-1, -1)],
            "R": [(1, 1), (-1, 1)],
            "U": [(-1, 1), (-1, -1)],
            "D": [(1, 1), (1, -1)],
        }
        self.export = export_to_file
        self.export_screen = export_screen
        self.show = visualize_creation
        self.block_path = None
        self.block_backtrack = None
        self.wn = None
        if visualize_creation:
            os.environ["BLOCK_SIZE"] = "20"
            self.block_path = Block(height=self.height, width=self.width)
            self.block_backtrack = Block(
                color="green", backtracking=True, height=self.height, width=self.width
            )
            self.wn = Window(
                title="Generate Maze", height=self.height, width=self.width
            )

    def __repr__(self):
        """
        Make printed maze look better (when you put an object into stdout)
        :return:
        """
        maze_to_print = ""
        for maze_row in self.maze_matrix:
            temp_str: str = " ".join(maze_row) + "\n"
            maze_to_print += temp_str

        return maze_to_print

    @staticmethod
    def sum_tuples(l1, l2):
        return tuple(map(operator.add, l1, l2))

    def can_move_forward(self, current_coordinate, direction):
        next_coordinate = Maze.sum_tuples(
            current_coordinate, self.directions[direction]
        )

        if (
            next_coordinate[0] >= self.height
            or next_coordinate[0] < 0
            or next_coordinate[1] >= self.width
            or next_coordinate[1] < 0
        ):
            return False

        if next_coordinate in self.visited:
            return False

        for next_direction, shift in self.directions.items():
            next_next_coordinate = Maze.sum_tuples(next_coordinate, shift)

            if (
                next_next_coordinate in self.visited
                and next_next_coordinate != current_coordinate
            ):
                return False

        diagonal_shifts = self.directions_dir2[direction]
        for diagonal_shift in diagonal_shifts:
            diagonal_direction_shift = Maze.sum_tuples(
                next_coordinate, diagonal_shift)
            if diagonal_direction_shift in self.visited:
                return False

        return True

    def move(self, current_coordinate, direction):
        next_coordinate = Maze.sum_tuples(
            current_coordinate, self.directions[direction]
        )

        self.visited.append(next_coordinate)
        self.stack.append(next_coordinate)
        self.maze_matrix[next_coordinate[0]][next_coordinate[1]] = "$"
        if self.show:
            self.block_path.move_block(
                x_coordinate=next_coordinate[1], y_coordinate=next_coordinate[0]
            )

        return next_coordinate

    def generate_maze(self):
        coordinate = self.start_from
        self.stack.append(coordinate)
        self.visited.append(coordinate)
        self.maze_matrix[coordinate[0]][coordinate[1]] = "$"
        if self.show:
            self.block_path.move_block(
                x_coordinate=coordinate[1], y_coordinate=coordinate[0]
            )

        while len(self.stack):
            next_moves = []

            for direction in self.directions:
                if self.can_move_forward(coordinate, direction):
                    next_moves.append(direction)

            if len(next_moves):
                move_random = random.choice(next_moves)
                coordinate = self.move(coordinate, move_random)
                continue

            coordinate = self.stack.pop()
            if self.show:
                self.block_backtrack.move_block(
                    x_coordinate=coordinate[1], y_coordinate=coordinate[0]
                )

        if self.export:
            with open("maze{}".format(random.randint(1, 10 ** 5)), "+w") as file:
                for line in self.__repr__():
                    file.write(line)

        if self.show:
            self.wn.stagnate()

        if self.export and self.show:
            return self.wn

        return None

if __name__ == '__main__':
    maze = Maze()
    maze.generate_maze()
