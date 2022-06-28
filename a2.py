from __future__ import annotations
from typing import Optional, Text
from a2_support import UserInterface, TextInterface
from constants import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog. 
__version__ = 1.0

# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

def load_game(filename: str) -> list['Level']:
    """ Reads a game file and creates a list of all the levels in order.
        
    Parameters:
        filename: The path to the game file
        
    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels


class Tile():
    """ 
    Represents the floor for a (row, column) position.
    """
    def __init__(self) -> None:
        """ Initiate an instance of class Tile.
        
        Parameters:
            self: instance itself
            
        Returns:
            None
        """
        self.id = "AT"

    def is_blocking(self) -> bool:
        """ A tile is blocking if a player would not be allowed to move onto the position
            it occupies. By default, tile's are not blocking..
        
        Parameters:
            self: instance itself
            
        Returns:
            boolean (True or False)
        """
        blocking = False
        if self.id == WALL:
            blocking = True
        elif self.id == DOOR:
            blocking = True
        return blocking

    def damage(self) -> int:
        """ The damage done to a player if they step on this tile
        
        Parameters:
            self: instance itself
            
        Returns:
            An integer that stores the damage value
        """
        dmg = 0
        if self.id == LAVA:
            dmg = 5
        return dmg

    def get_id(self) -> str:
        """ The ID of the tile
        
        Parameters:
            self: instance itself
            
        Returns:
            A string for the tile ID
        """
        return self.id

    def __str__(self) -> str:
        """ The string representation of the tile
        
        Parameters:
            self: instance itself
            
        Returns:
            A string for the tile ID
        """

        return self.id

    def __repr__(self) -> str:
        """ The string to create a new instance of this class
        
        Parameters:
            self: instance itself
            
        Returns:
            A string required to create a new instance
        """
        return self.__class__.__name__+"()"

class Wall(Tile):
    """ 
    Wall is a type of Tile that is blocking.
    """
    def __init__(self) -> None:
        super(Wall,self).__init__()
        self.id = WALL

class Empty(Tile):
    """ 
    Empty is a type of Tile that does not contain anything special. 
    A player can move freely over empty tiles without taking any damage.
    """
    def __init__(self) -> None:
        super(Empty,self).__init__()
        self.id = EMPTY

class Lava(Tile):
    """ 
    Lava is a type of Tile that is not blocking, but does a damage of 5 to 
    the player's HP when stepped on
    """
    def __init__(self) -> None:
        super(Lava,self).__init__()
        self.id = LAVA

class Door(Tile):
    """ 
    Door is a type of Tile that starts as locked (blocking). 
    Once the player has collected all coins in a given maze, the door is 'unlocked'.
    """
    def __init__(self) -> None:
        super(Door,self).__init__()
        self.id = DOOR
    def unlock(self) -> None:
        """ Unlocks the door
        
        Parameters:
            self: instance itself
            
        Returns:
            None
        """
        self.id = EMPTY

class Entity():
    """ 
    Provides base functionality for all entities in the game.
    """
    id = "E"
    def __init__(self,position: tuple[int,int]) -> None:
        """ Sets up this entity at the given (row, column) position.

        Parameters:
            self: instance itself
            position: the coordinates (row and column)
            
        Returns:
            None
        """
        self.row = position[0]
        self.column = position[1]
        

    def get_position(self) -> tuple[int,int]:
        """ Returns this entities (row, column) position.

        Parameters:
            self: instance itself
            
        Returns:
            Coordinates for the position of the entity (tuple of two integers)
        """
        return (self.row,self.column)

    def get_name(self) -> str:
        """ Returns the name of the class to which this entity belongs.

        Parameters:
            self: instance itself
            
        Returns:
            string
        """
        return self.class_name
    
    def get_id(self) -> str:
        """ Returns the ID of this entity. For all non-abstract subclasses, 
            this should be a single character representing the type of the entity.

        Parameters:
            self: instance itself
            
        Returns:
            String
        """
        return self.id

    def __str__(self) -> str:
        """ Returns the string representation for this entity (the ID).

        Parameters:
            self: instance itself
            
        Returns:
            String
        """
        return self.id

    def __repr__(self) -> str:
        """ Returns the text that would be required to make a new instance of this 
            class that looks identical (where possible) to self.

        Parameters:
            self: instance itself
            
        Returns:
            String
        """
        return f"{self.__class__.__name__}(({self.row}, {self.column}))"

class DynamicEntity(Entity):
    """ 
    DynamicEntity is an abstract class which provides base functionality for special types 
    of Entities that are dynamic (e.g. can move from their original position).
    """
    def set_position(self,new_position: tuple[int,int]) -> None:
        """ Updates the DynamicEntity's position to new_position, assuming it is a valid position.

        Parameters:
            self: instance itself
            new_position: new coordinates for updating the position
            
        Returns:
            None
        """
        self.row = new_position[0]
        self.column = new_position[1]


class Player(DynamicEntity):
    """ 
    Player is a DynamicEntity that is controlled by the user, and must move 
    from its original position to the end of each maze.
    """
    hunger = 0
    thirst = 0
    hp = 100
    inventory = None

    def get_hunger(self) -> int:
        """ Returns the player's current hunger level.

        Parameters:
            self: instance itself
            
        Returns:
            Integer
        """
        return self.hunger 
    
    def get_thirst(self) -> int:
        """ Returns the player's current thirst level.

        Parameters:
            self: instance itself
            
        Returns:
            Integer
        """
        return self.thirst

    def get_health(self) -> int:
        """ Returns the player's current health level.

        Parameters:
            self: instance itself
            
        Returns:
            Integer
        """
        return self.hp

    def change_hunger(self, amount: int) -> None:
        """ Alters the player's hunger level by the given amount.

        Parameters:
            self: instance itself
            amount: integer value for the delta hunger value
            
        Returns:
            None
        """
        diff = self.hunger + amount
        if diff <= 0:
            self.hunger = 0
        elif diff >= MAX_HUNGER:
            self.hunger = MAX_HUNGER
        else:
            self.hunger = diff

    def change_thirst(self, amount: int) -> None:
        """ Alters the player's thirst level by the given amount.

        Parameters:
            self: instance itself
            amount: integer value for the delta thirst value
            
        Returns:
            None
        """
        diff = self.thirst + amount
        if diff <= 0:
            self.thirst = 0
        elif diff >= MAX_THIRST:
            self.thirst = MAX_THIRST
        else:
            self.thirst = diff

    def change_health(self, amount: int) -> None:
        """ Alters the player's health level by the given amount.

        Parameters:
            self: instance itself
            amount: integer value for the delta health value
            
        Returns:
            None
        """
        diff = self.hp + amount
        if diff <= 0:
            self.hp = 0
        elif diff >= MAX_HEALTH:
            self.hp = MAX_HEALTH
        else:
            self.hp = diff

    def get_inventory(self) -> Inventory:
        """ Returns the player's Inventory instance

        Parameters:
            self: instance itself
            
        Returns:
            Inventory
        """
        if self.inventory == None:
            self.inventory = Inventory()
        return self.inventory

    def add_item(self, item: Item) -> None:
        """ Adds the given item to the player's Inventory instance.

        Parameters:
            self: instance itself
            item: An Item instance
            
        Returns:
            None
        """
        self.inventory.add_item(item)

class Item(Entity):
    """ 
    Subclass of Entity which provides base functionality for all items in the game.
    """

    def apply(self, player: Player) -> None:
        """ Applies the items effect, if any, to the given player.

        Parameters:
            self: instance itself
            player: A Player instance
            
        Returns:
            None
        """
        raise NotImplementedError

class Potion(Item):
    """ 
    Inherits from Item. A potion is an item that increases the player's HP by 20 when applied.
    """
    id = POTION

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hp += POTION_AMOUNT
        if self.player.hp > 100:
            self.player.hp = 100

class Coin(Item):
    """ 
    Inherits from Item. A coin is an item that has no effect when applied to a player.
    """
    id = COIN
    def apply(self, player: Player) -> None:
        pass

class Water(Item):
    """ 
    Inherits from Item. Water is an item that will decrease the player's thirst by 5 when applied.
    """
    id = WATER
    def apply(self, player: Player) -> None:
        self.player = player
        self.player.thirst += WATER_AMOUNT
        if self.player.thirst < 0:
            self.player.thirst = 0

class Food(Item):
    """ 
    Inherits from Item. Food is an abstract class. 
    Food subclasses implement an apply method that decreases the players hunger by a certain amount, depending on the type of food.
    """
    id = FOOD
    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger -= 0
        if self.player.hunger < 0:
            self.player.hunger = 0

class Apple(Food):
    """ 
    Inherits from Food. Apple is a type of food that decreases the player's hunger by 1 when applied.
    """
    id = APPLE
    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger += APPLE_AMOUNT
        if self.player.hunger < 0:
            self.player.hunger = 0

class Honey(Food):
    """ 
    Inherits from Food. Honey is a type of food that decreases the player's hunger by 5 when applied.
    """
    id = HONEY
    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger += HONEY_AMOUNT
        if self.player.hunger < 0:
            self.player.hunger = 0

class Inventory():
    """ 
    An Inventory contains and manages a collection of items.
    """
    def __init__(self, initial_items: Optional[list] = None) -> None:
        """ Sets up initial inventory. If no initial_items is provided, 
            inventory starts with an empty dictionary for the items. 
            Otherwise, the initial dictionary is set up from the initial_items 
            list to be a dictionary mapping item names to a list of item instances 
            with that name.

        Parameters:
            self: instance itself
            initial_items: An optional list of Item instances
            
        Returns:
            None
        """
        self.inventory_dct = dict()
        if initial_items is not None:
            for i in initial_items:
                class_name = i.__class__.__name__
                if class_name in self.inventory_dct:
                    self.inventory_dct[class_name].append(i)
                else:
                    self.inventory_dct[class_name] = [i]
        
    def add_item(self, item: Item) -> None:
        """ Adds the given item to this inventory's collection of items.

        Parameters:
            self: instance itself
            item: an Item instance
            
        Returns:
            None
        """
        class_name = item.__class__.__name__
        if class_name in self.inventory_dct:
            self.inventory_dct[class_name].append(item)
        else:
            self.inventory_dct[class_name] = [item]

    def get_items(self) -> dict[str,list]:
        """ Returns a dictionary mapping the names of all items in the inventory to 
            lists containing each instance of the item with that name.

        Parameters:
            self: instance itself
            
        Returns:
            Dictionary
        """
        return self.inventory_dct

    def remove_item(self, item_name: str) -> Optional[Item]:
        """ Removes and returns the first instance of the item with the given item_name from the inventory. 
            If no item exists in the inventory with the given name, then this method returns None.

        Parameters:
            self: instance itself
            item_name: a string representation of an item
            
        Returns:
            Either an Item instance or None
        """
        output = None
        if item_name in self.inventory_dct:
            output = self.inventory_dct[item_name].pop(0)
            if len(self.inventory_dct[item_name]) == 0:
                del self.inventory_dct[item_name]
        return output

    def __str__(self) -> str:
        """ Returns a string containing information about quantities of items available in the inventory.

        Parameters:
            self: instance itself
            
        Returns:
            String
        """
        output_str = ""
        for key in self.inventory_dct:
            output_str += key + ": " + str(len(self.inventory_dct[key]))
            if key != list(self.inventory_dct)[-1]:
                output_str += "\n"
        return output_str
    
    def __repr__(self) -> str:
        """ Returns a string that could be used to construct a new instance of Inventory containing 
            the same items as self currently contains.

        Parameters:
            self: instance itself
            
        Returns:
            String
        """
        items = []
        for key in self.inventory_dct:
            for val in self.inventory_dct[key]:
                items.append(val)
        return f"{__class__.__name__}(initial_items={items})"

class Maze():
    """ 
    A Maze instance represents the space in which a level takes place.
    """
    def __init__(self,dimensions: tuple[int,int]) -> None:
        """ Sets up an empty maze of given dimensions (a tuple of the number of rows and number of columns).

        Parameters:
            self: instance itself
            dimensions: two integers that indicate the number of rows and number of columns of a maze
            
        Returns:
            None
        """
        self.num_rows = dimensions[0]
        self.num_columns = dimensions[1]
        self.maze = [[]*self.num_columns for _ in range(self.num_rows)]
        self.tile_maze = []
        

    def get_dimensions(self) -> tuple[int,int]:
        """ Returns the (#rows, #columns) in the maze.

        Parameters:
            self: instance itself
            
        Returns:
            Tuple
        """
        return (self.num_rows,self.num_columns)

    def add_row(self, row: str) -> None:
        """ Adds a row of tiles to the maze.
        
        Parameters:
            self: instance itself
            row: a string where each character is a column value
            
        Returns:
            None
        """
        tiles = [WALL,LAVA,EMPTY,DOOR]
        if len(row) == self.num_columns:
            for i in range(len(row)):
                if row[i] not in tiles:
                    row[i].replace(row[i],EMPTY)
            for i in range(len(self.maze)):
                if len(self.maze[i]) == 0:
                    self.maze[i] = row
                    break
        return
    
    def get_tiles(self) -> list[list[Tile]]:
        """ Returns the Tile instances in this maze. Each element is a row (list of Tile instances in order).
        
        Parameters:
            self: instance itself
            
        Returns:
            2-D array of Tile instances
        """
        self.tile_maze = []
        x = 0
        for row in self.maze:
            if len(row)==0:
                x += 1
        
        if x != len(self.maze):
            for r in range(len(self.maze)):
                if len(self.maze[r]) == 0: continue
                self.tile_maze.append([])
                for c in range(len(self.maze[r])):
                    self.tile_maze[r].append([])
                    if self.maze[r][c] == DOOR:
                        self.tile_maze[r][c] = Door()
                    elif self.maze[r][c] == LAVA:
                        self.tile_maze[r][c] = Lava()
                    elif self.maze[r][c] == WALL:
                        self.tile_maze[r][c] = Wall()
                    else:
                        self.tile_maze[r][c] = Empty()
        print(self.tile_maze)
        return self.tile_maze


    def unlock_door(self) -> None:
        """ Unlocks any doors that exist in the maze.
        
        Parameters:
            self: instance itself
            
        Returns:
            None
        """
        for row in range(len(self.maze)):
            for column in range(len(self.maze[row])):
                if self.maze[row][column] == DOOR:
                    self.maze[row] = self.maze[row].replace(self.maze[row][column],EMPTY)
                    break

    def get_tile(self, position: tuple[int,int]) -> Tile:
        """ Returns the Tile instance at the given position.
        
        Parameters:
            self: instance itself
            position: the coordinate of the tile (tuple)
            
        Returns:
            Tile instance
        """
        self.tile_maze = []
        x = 0
        for row in self.maze:
            if len(row)==0:
                x += 1
        row = position[0]
        column = position[1]
        
        
        if x != len(self.maze):
            for r in range(len(self.maze)):
                self.tile_maze.append([])
                for c in range(len(self.maze[r])):
                    self.tile_maze[r].append([])
                    if self.maze[r][c] == DOOR:
                        self.tile_maze[r][c] = Door()
                    elif self.maze[r][c] == LAVA:
                        self.tile_maze[r][c] = Lava()
                    elif self.maze[r][c] == WALL:
                        self.tile_maze[r][c] = Wall()
                    else:
                        self.tile_maze[r][c] = Empty()
        return self.tile_maze[row][column]

    def __str__(self) -> str:
        """ Returns the Tile instance at the given position.
        
        Parameters:
            self: instance itself
            position: the coordinate of the tile (tuple)
            
        Returns:
            Tile instance
        """
        output_str = ""
        for idx,row in enumerate(self.maze):
            if len(row) == 0: continue
            output_str += row
            if idx == len(self.maze)-1:
                continue
            output_str += "\n"
        return output_str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(({self.num_rows}, {self.num_columns}))"

class Level():

    def __init__(self,dimensions:tuple[int,int]) -> None:
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.maze = Maze((self.rows,self.columns))
        self.item_map = dict()

    def get_maze(self) -> Maze:
        return self.maze

    def attempt_unlock_door(self) -> None:
        coins_avail = 0
        door_row = 0
        door_column = 0
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                if self.maze.maze[row][col] == COIN:
                    coins_avail += 1
                elif self.maze.maze[row][col] == DOOR:
                    door_row = row
                    door_column = col
        if coins_avail == 0:
            door_tile = self.maze.get_tile((door_row,door_column))
            door_tile.unlock()
            self.maze.maze[door_row] = self.maze.maze[door_row][:door_column] + " " + self.maze.maze[door_row][door_column+1:]

    def add_row(self, row: str) -> None:
        self.maze.add_row(row)
        if len(self.maze.maze) == self.maze.num_rows:
            self.orig_maze = self.maze

    def add_entity(self, position: tuple[int,int], entity_id: str) -> None:
        row = position[0]
        column = position[1]
        items = [COIN,POTION,APPLE,HONEY,WATER]
        try:
            if self.maze.maze[row][column] in items or self.maze.maze[row][column] == EMPTY:
                output_str = self.maze.maze[row][:column] + entity_id + self.maze.maze[row][column+1:]
                self.maze.maze[row] = output_str
        except:
            output_str = " " * self.maze.num_columns
            output_str = output_str[:column] + entity_id + output_str[column+1:]
            self.maze.maze[row] = output_str

    def get_dimensions(self) -> tuple[int,int]:
        return self.maze.get_dimensions()

    def get_items(self) -> dict[tuple[int,int],Item]:
        x = 0
        for row in self.maze.maze:
            if len(row)==0:
                x += 1

        if x != len(self.maze.maze):
            for row in range(len(self.maze.maze)):
                for column in range(len(self.maze.maze[row])):
                    if self.maze.maze[row][column] == COIN:
                        self.item_map[(row,column)] = Coin((row,column))
                    elif self.maze.maze[row][column] == POTION:
                        self.item_map[(row,column)] = Potion((row,column))
                    elif self.maze.maze[row][column] == HONEY:
                        self.item_map[(row,column)] = Honey((row,column))
                    elif self.maze.maze[row][column] == APPLE:
                        self.item_map[(row,column)] = Apple((row,column))
                    elif self.maze.maze[row][column] == WATER:
                        self.item_map[(row,column)] = Water((row,column))

        return self.item_map

    def remove_item(self, position: tuple[int,int]) -> None:
        row = position[0]
        column = position[1]
        items = [COIN,POTION,APPLE,HONEY,WATER]
        if self.maze[row][column] in items:
            self.maze[row][column] = EMPTY

    def add_player_start(self,position: tuple[int,int]) -> None:
        row = position[0]
        column = position[1]
        new_str = self.maze.maze[row]
        if len(self.maze.maze[row]) == 0:
            new_str = " " * self.columns
        self.maze.maze[row] = new_str[:column] + PLAYER + new_str[column+1:]
        self.player_start = (row,column)

    def get_player_start(self) -> Optional[tuple[int,int]]:
        
        for row in range(len(self.maze.maze)):
            for column in range(len(self.maze.maze[row])):
                if self.maze.maze[row][column] == PLAYER:
                    try:
                        return self.player_start    
                    except:
                        try:
                            for row2 in range(len(self.orig_maze.maze)):
                                for column2 in range(len(self.orig_maze.maze[row2])):
                                    if self.orig_maze.maze[row2][column2] == PLAYER:
                                        return (row2,column2)
                        except:
                            return (row,column)    
                        
                        
        return None

    def __str__(self) -> str:
        output_str = ""
        for row in self.maze.maze:
            if len(row) == 0: continue
            output_str += row + "\n"
        output_str += f"\nItems: {self.get_items()}\nPlayer start: {self.get_player_start()}"
        
        return "Maze: "+ output_str
    
    def __repr__(self) -> str:
        
        return f"Level(({self.rows},{self.columns}))"

class Model():
    
    def __init__(self,game_file: str):
        self.game_file = game_file
        self.levels = load_game(game_file)
        self.curr_level = self.levels[0]
        self.levelled_up = False
        self.move_streak = 0
        self.start_player_pos = self.curr_level.get_player_start()
        self.player = Player(self.start_player_pos)
        self.player.inventory = Inventory()
        self.can_levelup = False
        self.index = 0
    
    def has_won(self) -> bool:
        decision = False
        if self.index == len(self.levels):
            decision = True

        return decision

    def has_lost(self) -> bool:
        decision = False
        if self.player.get_health() == 0:
            decision = True
        if self.player.get_hunger() == MAX_HUNGER:
            decision = True
        if self.player.get_thirst() == MAX_THIRST:
            decision = True
        return decision

    def get_level(self) -> Level:
        return self.curr_level

    def level_up(self) -> None:
        self.index += 1
        if self.has_won():
            print(WIN_MESSAGE)
            exit()

        index = self.levels.index(self.curr_level)
        self.curr_level = self.levels[index+1]
        self.start_player_pos = self.curr_level.get_player_start()
        self.player.set_position(self.start_player_pos)
        self.levelled_up = False
        
    
    def did_level_up(self) -> bool:
        return self.levelled_up

    def move_player(self, delta: tuple[int,int]) -> None:
        move_pos_row = delta[0]
        move_pos_col = delta[1]
        self.can_levelup = True

        for idx,row in enumerate(self.curr_level.maze.maze):
            if PLAYER in row:
                col = row.index(PLAYER)
                self.player_curr_pos = (idx,col)
                break

        new_pos_row = idx + move_pos_row
        new_pos_col = col + move_pos_col

        current_items = self.get_current_items()
        for v in current_items.values():
            if isinstance(v,Coin):
                self.can_levelup = False
                break
                   
        tile = self.curr_level.maze.get_tile((new_pos_row,new_pos_col))
        if tile.get_id() == DOOR:
            if self.can_levelup:
                tile.unlock()
                self.levelled_up = True
                

        if tile.is_blocking(): return
        self.attempt_collect_item((new_pos_row,new_pos_col))

        self.curr_level.maze.maze[idx] = row[:col] + " " + row[col+1:]
        string = self.curr_level.maze.maze[new_pos_row]
        self.curr_level.maze.maze[new_pos_row] = string[:new_pos_col] + PLAYER + string[new_pos_col+1:]
        self.move_streak += 1
        if self.move_streak == 5:
            self.player.change_hunger(1)
            self.player.change_thirst(1)
            self.move_streak = 0

        if tile.get_id() == LAVA:
            self.player.change_health(tile.damage())
        self.player.change_health(-1)

        self.player_curr_pos = (new_pos_row,new_pos_col)
        self.player.row = self.player_curr_pos[0]
        self.player.column = self.player_curr_pos[1]

        if self.levelled_up:
            self.level_up()
        
        
    def attempt_collect_item(self, position: tuple[int,int]) -> None:
        move_pos_row = position[0]
        move_pos_col = position[1]

        if self.curr_level.maze.maze[move_pos_row][move_pos_col] == POTION:
            self.player.add_item(Potion(self.player_curr_pos))
        elif self.curr_level.maze.maze[move_pos_row][move_pos_col] == COIN:
            self.player.add_item(Coin(self.player_curr_pos))
        elif self.curr_level.maze.maze[move_pos_row][move_pos_col] == HONEY:
            self.player.add_item(Honey(self.player_curr_pos))
        elif self.curr_level.maze.maze[move_pos_row][move_pos_col] == APPLE:
            self.player.add_item(Apple(self.player_curr_pos))
        elif self.curr_level.maze.maze[move_pos_row][move_pos_col] == WATER:
            self.player.add_item(Water(self.player_curr_pos))    

    def get_player(self) -> Player:
        return self.player
    
    def get_player_stats(self) -> tuple[int,int,int]:
        tuple_stats = (self.player.get_health(),self.player.get_hunger(),self.player.get_thirst())
        return tuple_stats

    def get_player_inventory(self) -> Inventory:
        return self.player.get_inventory()

    def get_current_maze(self) -> Maze:
        return self.curr_level.maze
    
    def get_current_items(self) -> dict[tuple[int,int], Item]:
        x = 0
        for row in self.curr_level.maze.maze:
            if len(row)==0:
                x += 1
        self.curr_level.item_map = dict()
        if x != len(self.curr_level.maze.maze):
            for row in range(len(self.curr_level.maze.maze)):
                for column in range(len(self.curr_level.maze.maze[row])):
                    if self.curr_level.maze.maze[row][column] == COIN:
                        self.curr_level.item_map[(row,column)] = Coin((row,column))
                    elif self.curr_level.maze.maze[row][column] == POTION:
                        self.curr_level.item_map[(row,column)] = Potion((row,column))
                    elif self.curr_level.maze.maze[row][column] == HONEY:
                        self.curr_level.item_map[(row,column)] = Honey((row,column))
                    elif self.curr_level.maze.maze[row][column] == APPLE:
                        self.curr_level.item_map[(row,column)] = Apple((row,column))
                    elif self.curr_level.maze.maze[row][column] == WATER:
                        self.curr_level.item_map[(row,column)] = Water((row,column))
        return self.curr_level.item_map

    def __str__(self) -> str:
        return "Model('"+self.game_file+"')"
    
    def __repr__(self) -> str:
        return "Model('"+self.game_file+"')"
    
class MazeRunner():

    def __init__(self, game_file: str, view: UserInterface) -> None:
        self.model = Model(game_file)
        self.view = view

    def play(self) -> None:
        
        while True:
            maze = self.model.curr_level.get_maze()
            items = self.model.get_current_items()
            inventory = self.model.get_player_inventory()
            player_pos = self.model.player.get_position()
            stats = self.model.get_player_stats()

            self.view.draw(maze,items,player_pos,inventory,stats)
            
            if self.model.has_lost():
                print(LOSS_MESSAGE)
                exit()

            self.move_player()        

    def move_player(self) -> None:
        while True:
            move = input("\nEnter a move: ")
            if move in MOVE_DELTAS:
                self.model.move_player(MOVE_DELTAS[move])
                break
            elif "i " in move:
                inventory = self.model.get_player_inventory()
                item_name = move[2:]
                all_items = inventory.get_items()
                if item_name in all_items:
                    item = inventory.remove_item(item_name)
                    item.apply(self.model.player) 
                    if len(all_items[item_name]) == 0:
                        del self.model.get_player_inventory().get_items()[item_name]
                else:
                    print(ITEM_UNAVAILABLE_MESSAGE)
                break
            


def main():

    '''
    filename = input("Enter game file: ")
    ui = TextInterface()
    game = MazeRunner(filename,ui)
    game.play()
    '''

    level = Level((3, 5))         
    rows = [             
        "#####",             
        "P M D",             
        "#####",         
        ]         
    expected = "Level((3,5))"
    print(level.__repr__()==expected)


if __name__ == '__main__':
    main()
