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
WINDOW_TITLE = 'Pathfinding Visualizer'

'''SCALING'''
MOUSE_SPRITE_SCALING = 0.5

class Visualizer(arcade.View):
    # Initialize the window and all self variables
    # Set background color
    def __init__(self):
        super().__init__()
        self.scene = None
        
        self.mouse_sprite = None
        self.mouse_sprite_list = []
        
        self.grid_nodes = []
        self.grid_list = None
        
        self.start_node_pos = None
        self.start_node_row = None
        self.start_node_col = None
        self.start_is_active = False
        
        self.target_node_pos = None
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
        
        pos_counter = 0
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                pos_counter = pos_counter + 1
                new_sprite = arcade.SpriteSolidColor(NODE_WIDTH, NODE_HEIGHT, arcade.color.WHITE)
                new_sprite.center_x = j * (NODE_WIDTH + MARGIN) + (NODE_WIDTH // 2 + MARGIN)
                new_sprite.center_y = i * (NODE_HEIGHT + MARGIN) + (NODE_HEIGHT // 2 + MARGIN)
                new_sprite.properties[0] = pos_counter
                self.grid_list.append(new_sprite)
    
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
        
        if modifiers & arcade.key.MOD_ACCEL:
            if button == 4:
                self.handle_target_node_placement(row, col)
            else:    
                self.handle_start_node_placement(row, col)
        elif self.grid_nodes[row][col] == 0:
            self.grid_nodes[row][col] = 1
        elif self.grid_nodes[row][col] == 1:
            self.grid_nodes[row][col] = 0
            
        self.grid_resync()
    
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

    def on_mouse_enter(self, x: int, y: int):
        if not self.mouse_sprite_list:
            self.mouse_sprite_list.append(self.mouse_sprite)

    def on_mouse_leave(self, x: int, y: int):
        if self.mouse_sprite_list:
            self.mouse_sprite_list.pop()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.on_mouse_motion(x,y,dx,dy)


class StartView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLUE)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text('Pathfinding Visualizer', self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text('Click the mouse to begin', self.window.width / 2, self.window.height / 2-45,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        
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
