from turtle import pos
from constants import *
from typing import Optional


class Tile():
    def __init__(self) -> None:
        self.id = ""

    def is_blocking(self) -> bool:
        blocking = False
        if self.id == WALL:
            blocking = True
        elif self.id == DOOR:
            blocking = True
        return blocking

    def damage(self) -> int:
        dmg = 0
        if self.id == LAVA:
            dmg = 5
        return dmg

    def get_id(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.__class__.__name__+"()"

class Wall(Tile):
    def __init__(self) -> None:
        super(Wall,self).__init__()
        self.id = WALL

class Empty(Tile):
    def __init__(self) -> None:
        super(Empty,self).__init__()
        self.id = EMPTY

class Lava(Tile):
    def __init__(self) -> None:
        super(Lava,self).__init__()
        self.id = LAVA

class Door(Tile):
    def __init__(self) -> None:
        super(Door,self).__init__()
        self.id = DOOR
    def unlock(self) -> None:
        self.id = EMPTY

class Entity():

    def __init__(self,position: tuple[int,int]):
        self.row = position[0]
        self.column = position[1]
        self.id = "E"

    def get_position(self) -> tuple[int,int]:
        return (self.row,self.column)

    def get_name(self) -> str:
        return self.class_name
    
    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(({self.row}, {self.column}))"

class DynamicEntity(Entity):

    def set_position(self,new_position: tuple[int,int]) -> None:
        self.row = new_position[0]
        self.column = new_position[1]


class Player(DynamicEntity):

    hunger = 0
    thirst = 0
    hp = 100

    def get_hunger(self) -> int:
        return self.hunger 
    
    def get_thirst(self) -> int:
        return self.thirst

    def get_health(self) -> int:
        return self.hp

    def change_hunger(self, amount: int) -> None:
        diff = self.hunger + amount
        if diff <= 0:
            self.hunger = 0
        elif diff >= MAX_HUNGER:
            self.hunger = MAX_HUNGER
        else:
            self.hunger = diff

    def change_thirst(self, amount: int) -> None:
        diff = self.thirst + amount
        if diff <= 0:
            self.thirst = 0
        elif diff >= MAX_THIRST:
            self.thirst = MAX_THIRST
        else:
            self.thirst = diff

    def change_health(self, amount: int) -> None:
        diff = self.hp + amount
        if diff <= 0:
            self.hp = 0
        elif diff >= MAX_HEALTH:
            self.hp = MAX_HEALTH
        else:
            self.hp = diff

    '''
    def get_inventory(self) -> Inventory:
        pass

    def add_item(self, item: Item) -> None:
        pass'''

class Item(Entity):

    def apply(self, player: Player) -> None:
        self.player = player

class Potion(Item):

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hp += POTION_AMOUNT
        if self.player.hp > 100:
            self.player.hp = 100

class Coin(Item):

    pass

class Water(Item):

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.thirst -= WATER_AMOUNT
        if self.player.thirst < 0:
            self.player.thirst = 0

class Food(Item):

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger -= 0
        if self.player.hunger < 0:
            self.player.hunger = 0

class Apple(Food):

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger -= APPLE_AMOUNT
        if self.player.hunger < 0:
            self.player.hunger = 0

class Honey(Food):

    def apply(self, player: Player) -> None:
        self.player = player
        self.player.hunger -= HONEY_AMOUNT
        if self.player.hunger < 0:
            self.player.hunger = 0

class Inventory():

    def __init__(self, initial_items: Optional[list] = None) -> None:
        self.inventory_dct = dict()
        if initial_items is not None:
            for i in initial_items:
                class_name = i.__class__.__name__
                if class_name in self.inventory_dct:
                    self.inventory_dct[class_name].append(i)
                else:
                    self.inventory_dct[class_name] = [i]
        
    def add_item(self, item: Item) -> None:
        class_name = item.__class__.__name__
        if class_name in self.inventory_dct:
            self.inventory_dct[class_name].append(item)
        else:
            self.inventory_dct[class_name] = [item]

    def get_items(self) -> dict[str,list]:
        return self.inventory_dct

    def remove_item(self, item_name: str) -> Optional[Item]:
        output = None
        if item_name in self.inventory_dct:
            output = self.inventory_dct[item_name].pop(0)
            if len(self.inventory_dct[item_name]) == 0:
                del self.inventory_dct[item_name]
        return output

    def __str__(self) -> str:
        total_quantity = 0
        for key in self.inventory_dct:
            amount = len(self.inventory_dct[key])
            total_quantity += amount
        return "Total number of items: "+str(total_quantity)
    
    def __repr__(self) -> str:
        items = []
        for key in self.inventory_dct:
            for val in self.inventory_dct[key]:
                items.append(val)
        return f"{__class__.__name__}(initial_items={items})"

class Maze():
    
    def __init__(self,dimensions: tuple[int,int]) -> None:
        self.num_rows = dimensions[0]
        self.num_columns = dimensions[1]
        self.maze = [[]*self.num_columns for _ in range(self.num_rows)]
        self.tile_maze = []
        

    def get_dimensions(self) -> tuple[int,int]:
        return (self.num_rows,self.num_columns)

    def add_row(self, row: str) -> None:
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
        return self.tile_maze


    def unlock_door(self) -> None:
        for row in range(self.maze):
            for column in range(self.maze[row]):
                if self.maze[row][column] == DOOR:
                    self.maze[row][column] = EMPTY

    def get_tile(self, position: tuple[int,int]) -> Tile:
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
        output_str = ""
        for row in self.maze:
            if len(row) == 0: continue
            output_str += row
            if self.maze.index(row) == len(self.maze)-1:
                continue
            output_str += "\n"
        return output_str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(({self.num_rows},{self.num_columns}))"

class Level():

    def __init__(self,dimensions:tuple[int,int]) -> None:
        rows = dimensions[0]
        columns = dimensions[1]
        self.maze = Maze((rows,columns))
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
        if self.maze.maze[row][column] in items or self.maze.maze[row][column] == EMPTY:
            output_str = self.maze.maze[row][:column] + entity_id + self.maze.maze[row][column+1:]
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
        self.maze.maze[row][column] = PLAYER
        self.player_start = (row,column)

    def get_player_start(self) -> Optional[tuple[int,int]]:
        
        for row in range(len(self.maze.maze)):
            for column in range(len(self.maze.maze[row])):
                if self.maze.maze[row][column] == PLAYER:
                    try:
                        return self.player_start
                        
                    except:
                        try:
                            for row in range(len(self.orig_maze.maze)):
                                for column in range(len(self.orig_maze.maze[row])):
                                    if self.orig_maze.maze[row][column] == PLAYER:
                                        return (row,column)
                        except:
                            return (row,column)    
                        
                        
        return None

    def __str__(self) -> str:
        output_str = ""
        for row in self.maze.maze:
            if len(row) == 0: continue
            output_str += row
            if self.maze.maze.index(row) == len(self.maze.maze)-1:
                continue
            output_str += "\n"
        return output_str
    
    def __repr__(self) -> str:
        output_str = ""
        for row in self.maze.maze:
            if len(row) == 0: continue
            output_str += row + "\n"
        output_str += f"Items: {self.get_items()}\nPlayer start: {self.get_player_start()}"
        
        return "Maze: "+output_str

class Model():
    pass


player= Player((3,3))         
player.get_inventory().get_items() == {}                  
potion1 = Potion((1,3))         
coin1 = Coin((4,3))         
apple1 = Apple((2,1))
player.add_item(potion1)         
player.add_item(coin1)         
player.add_item(apple1)
