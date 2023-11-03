# Eddie Castro
# Map Model used to create the Map with Block objects
from Block import Block


class MapModel:

    height = None
    width = None
    size = []

    # Dictionary used for Block objects
    map = {}

    player_pos = None
    enemy_pos = None

    # Manually defined Dictionary used to store all Obstacle positions for the map
    # Contains (x, y) coordinates as key
    obstacle_map = {}

    def __init__(self, height, width, enemy_pos, player_pos, obstacle_map):
        self.height = height
        self.width = width
        self.size = height, width
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.obstacle_map = obstacle_map

    def get_map(self):
        return self.map

    def get_type_at(self, position):
        block = self.map[position]
        return block.get_type()

    def get_size(self):
        return self.size

    def generate_map(self):
        p = Block.BlockType

        for y in range(0, self.height):
            for x in range(0, self.width):

                if self.player_pos == (x, y):
                    block = Block(p.PLAYER)
                    self.map[(x, y)] = block

                elif self.enemy_pos == (x, y):
                    block = Block(p.ENEMY)
                    self.map[(x, y)] = block

                # If the key exists in the obstacle map, the obstacle is added to the map
                elif (x, y) in self.obstacle_map:
                    block = Block(p.OBSTACLE)
                    self.map[(x, y)] = block

                else:
                    block = Block(p.GROUND)
                    self.map[(x, y)] = block

    def is_within_bounds(self, pos_tuple):
        x = pos_tuple[0]
        y = pos_tuple[1]
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    # get adjacent grid positions in a tuple
    def get_neighbors(self, current_pos):

        adjacent_positions = []

        x = current_pos[0]
        y = current_pos[1]

        positions = [(x - 1, y),  # left
                     (x + 1, y),  # right
                     (x, y - 1),  # up
                     (x, y + 1)]  # down

        for position in positions:
            if self.is_within_bounds(position):
                adjacent_positions.append(position)

        return adjacent_positions
