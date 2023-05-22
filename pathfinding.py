# from random import randint
import arcade

'''NODE SETTINGS'''
NODE_WIDTH = 20
NODE_HEIGHT = 20
NUM_ROWS = 25
NUM_COLS = 25
MARGIN_X = 2
MARGIN_Y = 2

'''WINDOW SETTINGS'''
WINDOW_GRID_BORDER = 30
WINDOW_WIDTH = (NODE_WIDTH + MARGIN_X) * NUM_COLS + MARGIN_X
WINDOW_HEIGHT = (NODE_HEIGHT + MARGIN_Y) * NUM_ROWS + MARGIN_Y
WINDOW_PADDING_X_LEFT = WINDOW_WIDTH * 0.05
WINDOW_PADDING_Y_TOP = WINDOW_HEIGHT * 0.05
WINDOW_PADDING_X_RIGHT = WINDOW_WIDTH - WINDOW_PADDING_X_LEFT
WINDOW_PADDING_Y_BOTTOM = WINDOW_HEIGHT - WINDOW_PADDING_Y_TOP
WINDOW_TITLE = 'Pathfinding Visualizer'

'''SCALING'''
MOUSE_SPRITE_SCALING = 0.4

class Visualizer(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        
        self.mouse_sprite = None
        self.mouse_sprite_list = []
        
        self.grid_nodes = []
        self.grid_list = None
        
        # Starting node info
        self.start_node_row = None
        self.start_node_col = None
        self.start_is_active = False
        
        #Target node info
        self.target_node_row = None
        self.target_node_col = None
        self.target_is_active = False
        
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(False)
        self.setup()

    # Sets up scene, assigns variables context
    # Creates grid of Nodes
    def setup(self):
        self.scene = arcade.Scene()
        
        # Create small square for mouse cursor
        self.mouse_sprite = arcade.SpriteSolidColor(int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    int(NODE_WIDTH*MOUSE_SPRITE_SCALING),
                                                    arcade.color.PURPLE)
        self.mouse_sprite_list = arcade.SpriteList()
        self.mouse_sprite_list.append(self.mouse_sprite)
        
        self.grid_list = arcade.SpriteList()
        
        # 2D grid of integers. Used to define color matrix
        # Ex: one row of [1, 0 ,0 ,0, 2] is 
        # [wall, open, open, open, start]
        for i in range(NUM_ROWS):
            self.grid_nodes.append([])
            for j in range(NUM_COLS):
                self.grid_nodes[i].append(0)
        
        # Sprite list of nodes. The sprite equivalent to
        # self.grid_nodes, 1D array.
        pos_counter = 0
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                pos_counter = pos_counter + 1
                new_sprite = arcade.SpriteSolidColor(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
                new_sprite.center_x = j * (NODE_WIDTH + MARGIN_X) + (NODE_WIDTH // 2 + MARGIN_X)
                new_sprite.center_y = i * (NODE_HEIGHT + MARGIN_Y) + (NODE_HEIGHT // 2 + MARGIN_Y)
                new_sprite.properties[0] = pos_counter
                self.grid_list.append(new_sprite)
        self.grid_resync()
    
    # Update the color of the nodes
    def grid_resync(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                position = row * NUM_COLS + col
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

    # Called when a keyboard key is pressed
    # ESC - close window
    # C - Clear all walls
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.C:
            for i in range(NUM_ROWS):
                for j in range(NUM_COLS):
                    if self.grid_nodes[i][j] == 1:
                        self.grid_nodes[i][j] = 0
            self.grid_resync()

    # Make sure the mosue sprite updats with mouse movement
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    # Change single node color
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        row = int(y // (NODE_HEIGHT + MARGIN_Y))
        col = int(x // (NODE_WIDTH + MARGIN_X))
        if row >= NUM_ROWS or col >= NUM_COLS:
            return
        
        # control-click
        if modifiers & arcade.key.MOD_ACCEL:
            # Right click
            if button == 4:
                self.handle_target_node_placement(row, col)
            else:    
                self.handle_start_node_placement(row, col)
        elif self.grid_nodes[row][col] == 0:
            self.grid_nodes[row][col] = 1
        elif self.grid_nodes[row][col] == 1:
            self.grid_nodes[row][col] = 0
            
        self.grid_resync()
    
    # Check for three starting node cases:
    # 1. The node isn't the start node and there is no start node,
    #    meaning the node is now the start node
    # 2. The node is the start node and needs to be deactivated
    # 3. The node isn't a start node and there is a start node,
    #    meaning the node is now the start node and the last
    #    start node needs to be deactivated
    # Checks in that order
    def handle_start_node_placement(self, row, col):
        if not self.start_is_active and not self.grid_nodes[row][col] == 2:
            self.start_node_row = row
            self.start_node_col = col
            self.grid_nodes[row][col] = 2
            self.start_is_active = True
        elif self.grid_nodes[row][col] == self.grid_nodes[self.start_node_row][self.start_node_col]:
            for temp_row in range(NUM_ROWS):
                for temp_col in range(NUM_COLS):
                    if self.grid_nodes[temp_row][temp_col] == 2:
                        self.grid_nodes[temp_row][temp_col] == 0;
            self.grid_nodes[row][col] = 0
            self.start_is_active = False
        else:
            temp_row = self.start_node_row
            temp_col = self.start_node_col
            self.grid_nodes[temp_row][temp_col] = 0
            self.start_node_row = row
            self.start_node_col = col
            self.grid_nodes[row][col] = 2
            self.start_is_active = True
    
    # Exactly the same as handle_start_node_placement but ith
    # target
    def handle_target_node_placement(self, row, col):
        if not self.target_is_active and not self.grid_nodes[row][col] == 3:
            self.target_node_row = row
            self.target_node_col = col
            self.grid_nodes[row][col] = 3
            self.target_is_active = True
        elif self.grid_nodes[row][col] == self.grid_nodes[self.target_node_row][self.target_node_col]:
            for temp_row in range(NUM_ROWS):
                for temp_col in range(NUM_COLS):
                    if self.grid_nodes[temp_row][temp_col] == 3:
                        self.grid_nodes[temp_row][temp_col] == 0;
            self.grid_nodes[row][col] = 0
            self.target_is_active = False
        else:
            temp_row = self.target_node_row
            temp_col = self.target_node_col
            self.grid_nodes[temp_row][temp_col] = 0
            self.target_node_row = row
            self.target_node_col = col
            self.grid_nodes[row][col] = 3
            self.target_is_active = True

    # Add the mouse sprite whenever the mouse enters
    # the view
    def on_mouse_enter(self, x: int, y: int):
        if not self.mouse_sprite_list:
            self.mouse_sprite_list.append(self.mouse_sprite)

    # Kill the mouse sprite whenever the mouse exits
    # the view
    def on_mouse_leave(self, x: int, y: int):
        if self.mouse_sprite_list:
            self.mouse_sprite_list.pop()

    # Draw multiple wall nodes in a row based on clicked mouse
    # movement. Checks with list collision and doesn't draw
    # on start or target nodes
    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.on_mouse_motion(x,y,dx,dy)
        nodes_dragged = arcade.check_for_collision_with_list(self.mouse_sprite, self.grid_list, 3)
        for node in nodes_dragged:
            x_coor = ((node.center_x) // (NODE_WIDTH + MARGIN_X))
            y_coor = ((node.center_y) // (NODE_HEIGHT + MARGIN_Y))
            if self.grid_nodes[y_coor][x_coor] == 2 or self.grid_nodes[y_coor][x_coor] == 3: return
            self.grid_nodes[y_coor][x_coor] = 1
        self.grid_resync()

# Basic enter screen for view practice and ego boosting
class StartView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLUE)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text('PATHFINDING VISUALIZER', self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center", italic=True,
                         font_name="Kenney Pixel",)
        arcade.draw_text('CLICK TO BEGIN', self.window.width / 2, self.window.height / 2-45,
                         arcade.color.BLACK, font_size=40, anchor_x="center", italic=True,
                         font_name="Kenney Pixel")
        arcade.draw_text('AUTHOR: JOSH GILSTRAP', self.window.width / 2, self.window.height / 2 - 110,
                         arcade.color.BLACK, font_size=30, anchor_x="center", bold=True, italic=True,
                         font_name="Kenney Pixel")
        
    def on_mouse_press(self, x, y, button, modifiers):
        vis_view = Visualizer()
        vis_view.setup()
        self.window.show_view(vis_view)
    
    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.exit()

def main():
    win = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start = StartView()
    win.show_view(start)
    arcade.run()

if __name__ == '__main__':
    main()
