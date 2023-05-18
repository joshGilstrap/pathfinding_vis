from random import randint
import arcade

'''WINDOW SETTINGS'''
WINDOW_WIDTH = 610
WINDOW_HEIGHT = 600
WINDOW_PADDING_X_LEFT = WINDOW_WIDTH * 0.05
WINDOW_PADDING_Y_TOP = WINDOW_HEIGHT * 0.05
WINDOW_PADDING_X_RIGHT = WINDOW_WIDTH - WINDOW_PADDING_X_LEFT
WINDOW_PADDING_Y_BOTTOM = WINDOW_HEIGHT - WINDOW_PADDING_Y_TOP

'''NODE SETTINGS'''
NODE_WIDTH = 20
NODE_HEIGHT = 20
DEFAULT_NUM_NODES = 25
MARGIN = 2
HOVER_MARGIN = 3

'''SCALING'''
MOUSE_SPRITE_SCALING = 0.5

class Visualizer(arcade.Window):
    # Initialize the window and all self variables
    # Set background color
    def __init__(self, width, height):
        super().__init__(width, height, 'Visualizer', resizable=True)
        self.scene = None
        self.mouse_sprite = None
        self.mouse_sprite_list = []
        self.grid_nodes = []
        self.grid_list = None
        self.active_node = None
        self.wall_list = None
        self.start_node = None
        self.target_node = None
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.setup()

    # Sets up scene, assigns variables context
    # Creates grid of Nodes
    def setup(self):
        self.scene = arcade.Scene()
        
        self.mouse_sprite = arcade.SpriteSolidColor(int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    arcade.color.PURPLE)
        self.mouse_sprite_list = arcade.SpriteList()
        self.mouse_sprite_list.append(self.mouse_sprite)
        self.grid_list = arcade.SpriteList()
        self.active_node = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.start_node = arcade.SpriteList()
        self.target_node = arcade.SpriteList()
        
        for i in range(DEFAULT_NUM_NODES):
            self.grid_nodes.append([])
            for j in range(DEFAULT_NUM_NODES):
                new_sprite = Node(NODE_WIDTH, NODE_HEIGHT, arcade.color.BLUE)
                new_sprite.center_x = j * (NODE_WIDTH + MARGIN) + (NODE_WIDTH // 2 + MARGIN) + WINDOW_PADDING_X_LEFT
                new_sprite.center_y = i * (NODE_HEIGHT + MARGIN) + (NODE_HEIGHT // 2 + MARGIN) + WINDOW_PADDING_Y_TOP
                new_sprite.default_width = new_sprite.center_x
                new_sprite.default_height = new_sprite.center_y
                new_sprite.color = arcade.color.BLUE
                self.grid_nodes[i].append(new_sprite)
                self.grid_list.append(new_sprite)
        self.connect_nodes()

    # Draws objects on the screen
    def on_draw(self):
        self.clear()
        self.grid_list.draw()
        self.active_node.draw()
        self.wall_list.draw()
        self.start_node.draw()
        self.target_node.draw()
        self.mouse_sprite_list.draw()

    # Called every frame, updates mouse effect on grid
    def on_update(self, delta_time):
        node_hovered = arcade.check_for_collision_with_list(self.mouse_sprite, self.grid_list)
        if node_hovered:
            temp_node = Node(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
            temp_node.set_position(node_hovered[0].center_x, node_hovered[0].center_y)
            self.active_node = temp_node
        for node in node_hovered:
            node.width = NODE_WIDTH
            node.height = NODE_HEIGHT
            node.color = arcade.color.BLUE
            if self.active_node is node_hovered[0]:
                self.active_node.remove_from_sprite_lists()
        self.grid_list.update()

    # Called when a keyboard key is pressed
    # ESC - close window
    # C - Clear wall nodes
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        elif key == arcade.key.C:
            self.wall_list.clear()

    # Called when the mouse is moved
    # Draws mouse sprite at mouse position
    # Removes highlighted node when mouse isn't on screen
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y
        if x <= WINDOW_PADDING_X_LEFT or y <= WINDOW_PADDING_Y_TOP:
            self.active_node.kill()
        if x >= WINDOW_PADDING_X_RIGHT or y >= WINDOW_PADDING_Y_BOTTOM:
            self.active_node.kill()

    # Called when a mouse button is pressed, handles changing node
    # colors and adding/removing from lists
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == 4:
            if not modifiers and arcade.key.MOD_SHIFT:
                if self.start_node:
                    self.start_node.is_start = False
                    self.start_node.clear()
                self.active_node.is_start = True
                self.start_node.append(self.active_node)
                self.start_node.color = arcade.color.GREEN
            else:
                if self.target_node:
                    self.target_node.is_target = False
                    self.target_node.clear()
                self.active_node.is_target = True
                self.target_node.append(self.active_node)
                self.target_node.color = arcade.color.RED
        elif not self.active_node.collides_with_list(self.wall_list):
            self.active_node.is_wall = True
            self.wall_list.append(self.active_node)
            self.wall_list.color = arcade.color.ASH_GREY
        else:
            for node in self.wall_list:
                if x >= node.left and x <= node.right and y >= node.bottom and y <= node.top:
                    node.is_wall = False
                    self.wall_list.remove(node)

    # Called when the mouse enters the window
    # Creates mouse sprite at mouse position
    def on_mouse_enter(self, x: int, y: int):
        if not self.mouse_sprite_list:
            self.mouse_sprite_list.append(self.mouse_sprite)

    # Called when the mouse leaves the frame
    # Removes mouse sprite from screen
    def on_mouse_leave(self, x: int, y: int):
        if self.mouse_sprite_list:
            self.mouse_sprite_list.pop()

    # Called when the mouse is moved while clicked
    # Adds all nodes collided with to the wall list
    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.on_mouse_motion(x,y,dx,dy)
        if not self.active_node.collides_with_list(self.wall_list):
            self.wall_list.append(self.active_node)
            self.wall_list.color = arcade.color.ASH_GREY

    # Checks if the mouse is hovering over a node
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
    
    # Connects all nodes to their neighbors
    def connect_nodes(self):
        for i in range(0,4):
            if i == 0:
                for j in range(DEFAULT_NUM_NODES):
                    for k in range(DEFAULT_NUM_NODES-2,-1,-1):
                        self.grid_nodes[j][k].right_neighbor = self.grid_nodes[j][k+1]
            elif i == 1:
                for j in range(DEFAULT_NUM_NODES):
                    for k in range(1,DEFAULT_NUM_NODES):
                        self.grid_nodes[k][j].up_neighbor = self.grid_nodes[k-1][j]
            elif i == 2:
                for j in range(DEFAULT_NUM_NODES):
                    for k in range(DEFAULT_NUM_NODES-2,-1,-1):
                        self.grid_nodes[k][j].down_neighbor = self.grid_nodes[k+1][j]
            elif i == 3:
                for j in range(DEFAULT_NUM_NODES):
                    for k in range(1,DEFAULT_NUM_NODES):
                        self.grid_nodes[j][k].left_neighbor = self.grid_nodes[j][k-1]


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
        self.checked = False
        
        self.is_hovered = False

    def on_draw(self):
        pass

def main():
    Visualizer(WINDOW_WIDTH, WINDOW_HEIGHT).run()

if __name__ == '__main__':
    main()
