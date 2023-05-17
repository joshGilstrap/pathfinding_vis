from random import randint
import arcade

'''WINDOW SETTINGS'''
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_PADDING_X = WINDOW_WIDTH * 0.05
WINDOW_PADDING_Y = WINDOW_HEIGHT * 0.05

'''NODE SETTINGS'''
NODE_WIDTH = 20
NODE_HEIGHT = 20
DEFAULT_NUM_NODES = 25
MARGIN = 2
HOVER_MARGIN = 3

'''SCALING'''
MOUSE_SPRITE_SCALING = 0.5

'''TEXTURES'''
BLUE_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                                arcade.color.BLUE,
                                                255, 255, 'blue')
WHITE_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                                arcade.color.WHITE,
                                                255, 255, 'white')
GREEN_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                                arcade.color.GREEN,
                                                255, 255, 'green')
RED_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                              arcade.color.RED,
                                              255, 255, 'red')
YELLOW_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                                 arcade.color.YELLOW,
                                                 255, 255, 'yellow')
ORANGE_TEXTURE = arcade.make_soft_square_texture(NODE_WIDTH,
                                                 arcade.color.ORANGE,
                                                 255, 255, 'orange')
TEXTURE_LIST = [
    BLUE_TEXTURE,
    WHITE_TEXTURE,
    GREEN_TEXTURE,
    RED_TEXTURE,
    YELLOW_TEXTURE,
    ORANGE_TEXTURE
]

class Visualizer(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, 'Visualizer', resizable=True)
        self.scene = None
        self.mouse_sprite = None
        self.mouse_sprite_list = []
        self.grid_nodes = []
        self.grid_list = None
        self.active_node = None
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.setup()

    def setup(self):
        self.scene = arcade.Scene()
        self.mouse_sprite = arcade.SpriteSolidColor(int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    arcade.color.ORANGE)
        self.mouse_sprite_list = arcade.SpriteList()
        self.mouse_sprite_list.append(self.mouse_sprite)
        self.grid_list = arcade.SpriteList()
        self.active_node = arcade.SpriteList()
        for i in range(DEFAULT_NUM_NODES):
            self.grid_nodes.append([])
            for j in range(DEFAULT_NUM_NODES):
                new_sprite = Node(NODE_WIDTH, NODE_HEIGHT, arcade.color.BLUE)
                new_sprite.center_x = j * (NODE_WIDTH + MARGIN) + (NODE_WIDTH // 2 + MARGIN) + WINDOW_PADDING_X
                new_sprite.center_y = i * (NODE_HEIGHT + MARGIN) + (NODE_HEIGHT // 2 + MARGIN) + WINDOW_PADDING_Y
                new_sprite.default_width = new_sprite.center_x
                new_sprite.default_height = new_sprite.center_y
                for texture in TEXTURE_LIST:
                    new_sprite.append_texture(texture)
                new_sprite.set_texture(0)
                self.grid_nodes[i].append(new_sprite)
                self.grid_list.append(new_sprite)

    def on_draw(self):
        self.clear()
        self.grid_list.draw()
        self.mouse_sprite_list.draw()
        self.active_node.draw()

    def on_update(self, delta_time):
        node_hovered = arcade.check_for_collision_with_list(self.mouse_sprite, self.grid_list)
        if node_hovered:
            temp_node = Node(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
            temp_node.set_position(node_hovered[0].center_x, node_hovered[0].center_y)
            self.active_node = temp_node
        for node in node_hovered:
            node.width = NODE_WIDTH
            node.height = NODE_HEIGHT
            node.set_texture(0)
            node.color = arcade.color.BLUE
            if self.active_node is node_hovered[0]:
                self.active_node.remove_from_sprite_lists()
        self.grid_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_mouse_motion(self, x, y):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_mouse_enter(self, x: int, y: int):
        if not self.mouse_sprite_list:
            self.mouse_sprite_list.append(self.mouse_sprite)

    def on_mouse_leave(self, x: int, y: int):
        if self.mouse_sprite_list:
            self.mouse_sprite_list.pop()

    def is_on_node(self, x: int, y: int):
        for i in range(DEFAULT_NUM_NODES):
            for j in range(DEFAULT_NUM_NODES):
                node_l = self.grid_nodes[i][j].center_x - NODE_WIDTH // 2
                node_r = self.grid_nodes[i][j].center_x + NODE_WIDTH // 2
                node_b = self.grid_nodes[i][j].center_y - NODE_HEIGHT // 2
                node_t = self.grid_nodes[i][j].center_y + NODE_HEIGHT // 2
                if (x >= node_l and x <= node_r) and (y >= node_b and y <= node_t):
                    return True
        return False
                    

class Node(arcade.SpriteSolidColor):
    def __init__(self, width, height, color):
        super().__init__(width, height, color)
        self.default_width = width
        self.default_height = height

        self.up_neighbor = None
        self.down_neighbor= None
        self.left_neighbor= None
        self.right_neighbor= None

        self.is_start = False
        self.is_target = False
        self.is_wall = False
        
        self.is_hovered = False

    def on_draw(self):
        pass

def main():
    Visualizer(WINDOW_WIDTH, WINDOW_HEIGHT).run()

if __name__ == '__main__':
    main()
