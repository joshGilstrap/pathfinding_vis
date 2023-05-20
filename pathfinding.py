# from random import randint
import arcade

'''NODE SETTINGS'''
NODE_WIDTH = 20
NODE_HEIGHT = 20
NUM_ROWS = 25
NUM_COLS = 25
MARGIN = 2

'''WINDOW SETTINGS'''
WINDOW_GRID_BORDER = 30
WINDOW_WIDTH = (NODE_WIDTH + MARGIN) * NUM_COLS + MARGIN
WINDOW_HEIGHT = (NODE_HEIGHT + MARGIN) * NUM_ROWS + MARGIN
WINDOW_PADDING_X_LEFT = WINDOW_WIDTH * 0.05
WINDOW_PADDING_Y_TOP = WINDOW_HEIGHT * 0.05
WINDOW_PADDING_X_RIGHT = WINDOW_WIDTH - WINDOW_PADDING_X_LEFT
WINDOW_PADDING_Y_BOTTOM = WINDOW_HEIGHT - WINDOW_PADDING_Y_TOP

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
        self.start_is_active = False
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
        
        for i in range(NUM_ROWS):
            self.grid_nodes.append([])
            for j in range(NUM_COLS):
                self.grid_nodes[i].append(0)
        
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                new_sprite = arcade.SpriteSolidColor(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
                new_sprite.center_x = j * (NODE_WIDTH + MARGIN) + (NODE_WIDTH // 2 + MARGIN)
                new_sprite.center_y = i * (NODE_HEIGHT + MARGIN) + (NODE_HEIGHT // 2 + MARGIN)
                self.grid_list.append(new_sprite)
                # new_sprite.set_texture(0)
                # self.grid_nodes[i].append(new_sprite)
                # new_sprite.default_width = new_sprite.center_x
                # new_sprite.default_height = new_sprite.center_y
        # self.connect_nodes()
    
    def grid_resync(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                position = row * NUM_COLS + col
                # color = self.grid_list[position].color
                # Neutral state
                if self.grid_nodes[row][col] == 0:
                    self.grid_list[position].color = arcade.color.BLUE
                # Obstacle
                if self.grid_nodes[row][col] == 1:
                    self.grid_list[position].color = arcade.color.ASH_GREY
                # Starting node
                if self.grid_nodes[row][col] == 2:
                    self.grid_list[position].color = arcade.color.GREEN
                # Target node
                if self.grid_nodes[row][col] == 3:
                    self.grid_list[position].color = arcade.color.RED
                # Node being searched
                if self.grid_nodes[row][col] == 4:
                    self.grid_list[position].color = arcade.color.ORANGE
                # Part of path
                if self.grid_nodes[row][col] == 5:
                    self.grid_list[position].color = arcade.color.YELLOW
                # Searched/not part of path
                if self.grid_nodes[row][col] == 6:
                    self.grid_list[position].color = arcade.color.DARK_BLUE

    # Draws objects on the screen
    def on_draw(self):
        self.clear()
        self.grid_list.draw()
        self.mouse_sprite_list.draw()

    # Called every frame, updates mouse effect on grid
    # def on_update(self, delta_time):
    #     # node_hovered = arcade.check_for_collision_with_list(self.mouse_sprite, self.grid_list)
    #     # if node_hovered:
    #     #     temp_node = Node(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
    #     #     temp_node.set_position(node_hovered[0].center_x, node_hovered[0].center_y)
    #     #     self.active_node = temp_node
    #     # for node in node_hovered:
    #     #     node.width = NODE_WIDTH
    #     #     node.height = NODE_HEIGHT
    #     #     node.color = arcade.color.BLUE
    #     #     if self.active_node is node_hovered[0]:
    #     #         self.active_node.remove_from_sprite_lists()
    #     node_holder = self.node_hovered()
    #     if node_holder:
    #         node_holder.is_hovered = True
    #         node_holder.set_texture(1)
    #     self.grid_list.on_update(delta_time)

    # Called when a keyboard key is pressed
    # ESC - close window
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        row = int(y // (NODE_HEIGHT + MARGIN))
        col = int(x // (NODE_WIDTH + MARGIN))
        if row >= NUM_ROWS or col >= NUM_COLS:
            return
        
        if modifiers & arcade.key.MOD_ACCEL and not self.grid_nodes[row][col] == 2 and not self.start_is_active:
            self.grid_nodes[row][col] = 2
            self.start_is_active = True
        if self.grid_nodes[row][col] == 0:
            self.grid_nodes[row][col] = 1
        elif self.grid_nodes[row][col] == 1:
            self.grid_nodes[row][col] = 0
            
        self.grid_resync()
            

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
        # hovered_node = self.node_hovered()
        # if not hovered_node.is_wall:
        #     hovered_node.is_wall = True
        #     # hovered_node.color = arcade.color.ASH_GREY

    # Checks if the mouse is hovering over a node
    # def is_on_node(self, x: int, y: int):
    #     for i in range(DEFAULT_NUM_NODES):
    #         for j in range(DEFAULT_NUM_NODES):
    #             node_l = self.grid_nodes[i][j].center_x - NODE_WIDTH // 2
    #             node_r = self.grid_nodes[i][j].center_x + NODE_WIDTH // 2
    #             node_b = self.grid_nodes[i][j].center_y - NODE_HEIGHT // 2
    #             node_t = self.grid_nodes[i][j].center_y + NODE_HEIGHT // 2
    #             if (x >= node_l and x <= node_r) and (y >= node_b and y <= node_t):
    #                 return True
    #     return False
    
    # Connects all nodes to their neighbors
    # def connect_nodes(self):
    #     for i in range(0,4):
    #         if i == 0:
    #             for j in range(DEFAULT_NUM_NODES):
    #                 for k in range(DEFAULT_NUM_NODES-2,-1,-1):
    #                     self.grid_nodes[j][k].right_neighbor = self.grid_nodes[j][k+1]
    #         elif i == 1:
    #             for j in range(DEFAULT_NUM_NODES):
    #                 for k in range(1,DEFAULT_NUM_NODES):
    #                     self.grid_nodes[k][j].up_neighbor = self.grid_nodes[k-1][j]
    #         elif i == 2:
    #             for j in range(DEFAULT_NUM_NODES):
    #                 for k in range(DEFAULT_NUM_NODES-2,-1,-1):
    #                     self.grid_nodes[k][j].down_neighbor = self.grid_nodes[k+1][j]
    #         elif i == 3:
    #             for j in range(DEFAULT_NUM_NODES):
    #                 for k in range(1,DEFAULT_NUM_NODES):
    #                     self.grid_nodes[j][k].left_neighbor = self.grid_nodes[j][k-1]

    # def node_hovered(self):
    #     for _, e in enumerate(self.grid_list):
    #         if e.collides_with_sprite(self.mouse_sprite):
    #             return e
    #     return None


# class Node(arcade.Sprite):
#     def __init__(self, width, height):
#         super().__init__(image_width=width,image_height=height)
#         self.default_width = width
#         self.default_height = height

#         self.up_neighbor = None
#         self.down_neighbor= None
#         self.left_neighbor= None
#         self.right_neighbor= None

#         self.is_start = False
#         self.is_target = False
#         self.is_wall = False
#         self.checked = False
#         self.is_hovered = False
        
#         self.add_textures()
    
#     def draw(self):
#         super().draw()
    
#     def on_update(self, delta_time):
#         super().on_update(delta_time)
#         if self.is_wall:
#             self._color = (130,130,130)
#         if self.is_hovered:
#             self._color = (255,255,255)
#         if self.is_target:
#             self._color = (255,0,0)
#         if self.is_start:
#             self._color = (0,255,0)
    
#     def add_textures(self):
#         self.append_texture(arcade.color.BLUE)
#         self.append_texture(arcade.color.WHITE)
#         self.append_texture(arcade.color.RED)
#         self.append_texture(arcade.color.GREEN)
#         self.append_texture(arcade.color.ORANGE)
#         self.append_texture(arcade.color.YELLOW)
        

def main():
    Visualizer(WINDOW_WIDTH, WINDOW_HEIGHT).run()

if __name__ == '__main__':
    main()
