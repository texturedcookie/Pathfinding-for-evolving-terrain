# Eddie Castro
# Block class for blocks throughout the grid

class Block:
    # All possible squares
    class BlockType:
        PLAYER = 0
        ENEMY = 1
        GROUND = 2
        OBSTACLE = 3

    # VARIABLES USED FOR A* ALGORITHM
    block_type = None
    g = None  # Path score for the node
    h = None  # Heuristic score for the path
    f = None  # Path(g) and Heuristic(h) combined(f)
    parent = None
    terrain_score = None

    def __init__(self, type_value):
        self.block_type = type_value
        self.g = 0
        self.h = 0
        self.f = 0
        self.terrain_score = 1 # All blocks have the same terrain score...

    def set_type(self, type_value):
        self.block_type = type_value

    def get_type(self):
        return self.block_type

    def get_g(self):
        return self.g

    def get_h(self):
        return self.h

    def get_f(self):
        return self.f

    def get_terrain_score(self):
        return self.terrain_score

    def compare_f_score(self, score):
        temp_f = self.get_f()
        if temp_f < score:
            return -1
        elif temp_f > score:
            return 1
        else:
            return 0

    def set_parent(self, parent_position):
        self.parent = parent_position

    def set_parent_and_score(self, parent_position, parent_g, end_pos):
        self.set_parent(parent_position)

        # The cost of previous steps plus one more step
        self.g = parent_g + self.get_terrain_score()

        # Determine a guess of the remaining distance(h)
        # This is the Manhattan distance implementation
        self.h = abs(parent_position[0] - end_pos[0])
        self.h += abs(parent_position[1] - end_pos[1])

        # Set the new f score
        self.f = self.g + self.h

    def is_player(self):
        return self.block_type == self.BlockType.PLAYER

    def is_enemy(self):
        return self.block_type == self.BlockType.ENEMY

    def is_obstacle(self):
        return self.block_type == self.BlockType.OBSTACLE

    def is_ground(self):
        return self.block_type == self.BlockType.GROUND

