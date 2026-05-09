from utils import load_game_data
from entities import Hero
from Map import DungeonWorld
import random
import json
from CS66adts import Looting
from CS66adts import Shop
from CS66adts import Combat

with open("game_data.json", 'r') as f:
    data = json.load(f)

with open("loot_table.json", 'r') as f:
    loot_table = json.load(f)

#this defines valid commands a user to input
VALID_COMMANDS = ["look", "move", "fight", "inventory", "use", "path", "help", "exit", "shop"]
button = ""
#this is the intro/starting scene this is O(1) at best and worst case
def showintro():
    print("==================================================DUNGEONEER==================================================")
    usrinput = input("Enter X to continue:")

    if usrinput == "X" or usrinput == "x":
        button = input("""You are a wanderer pulled into an ancient dungeon
beneath a ruined kingdom.

To escape, you must explore the dungeon, survive enemies,
collect useful items, and defeat the king in the
final chamber.

Most actions depend on dice rolls. A good roll may help you
move, fight, or find loot. A bad roll may cost you health.

Your goal:
Find the Ancient Relic and reach the final chamber alive.

Commands:
look        - inspect the current room
move        - travel to another connected room
fight       - fight an enemy in the room
inventory   - view your items
use         - use an item
quest       - view your quest log
path        - find a path to a destination
help        - show commands again
exit        - quit the game

Good luck.
==================================================

Enter X to begin...""")
        
       
    if button == "X" or button == "x":
        name = input("[you wake up in a dark cave and an old man walks out of the dark] Where did you come from? we dont see many poeple down here these days. What is your name?:" )
        if name is not None:
            print(f"hello! {name}. You look like a strong warrior, maybe you can help us. You are in a dungeon filled with monsters, the only way to leave is to defeat the king. here {name} take this blade and fight if you want to leave")
            
    return name


#this is the movecommand, it handles where the player moves on the map it is O(1) at best and O(n) at worst
def movecommand(game_state):
    
    currentroom = game_state["current_room"]
    world = game_state["map"]
    exits = world.rooms[currentroom]
    rooms = game_state["rooms"]
    print("you can go to")
    for room in exits:
        print(room)
    choice = input(f"where would you like to go?")
        
    if choice in exits:
        rooms[choice]["visited"] = True
        game_state["current_room"] = choice
        print(f"You move to {choice}.")
        fightcmd(game_state)
    else:
        print("You cannot move there from here.")
    
    return 
    
#pathcmd() finds a path between rooms using DFS pathfinding, with a best case of O(1) and a worst case of O(n).

def pathcmd(game_state):
    destination = input("where would you like to go? ")
    current_room = game_state["current_room"]
    map = game_state["map"]
    path = map.dfs_find_path(current_room, destination)
    print(path)
    return

#lookcmd() displays the description of the current room, with a best and worst case time complexity of O(1).
def lookcmd(game_state):
    current_room = game_state["current_room"]
    mapdesc = game_state["rooms"][current_room]["Roomdesc"]
    print(mapdesc)
    return
    

#winloss() checks whether the player has won or lost the game, with a best and worst case time complexity of O(1).
def winloss(game_state):
    hero = game_state["hero"]
    health = hero.hp
    currentroom = game_state["current_room"]
    bossroom = game_state["rooms"]["Boss Room"]
    boss = bossroom["enemy"]
    if health > 0:
        pass
    else:
        print("==================================================GAME=OVER==================================================")
        restart = input("would you like to restart?")
        game_state["game_over"] = True
        if restart is not None:
            showintro()
    
    if currentroom == "Boss Room" and boss is None:
        print("==================================================VICTORY==================================================")
        print("You have successfully slayed the king and beat dungeoneer")
        print("thank you for playing")
        game_state["victory"] = True

        


    pass

#fightcd() manages combat between the hero and enemies, with a best case of O(1) and a worst case of O(n) depending on combat rounds and inventory search.
def fightcmd(game_state):
    
    hero = game_state["hero"]
    rooms = game_state["rooms"]
    currentroom = game_state["current_room"]
    enemy = rooms[currentroom]["enemy"]

    if enemy is None:
        print("No enemy to fight right now.")
        return

    print(f"You encountered {enemy['name']}")

    choice = input("Would you like to fight or run? ")

    if choice == "run":
        movecommand(game_state)
        return

    if choice != "fight":
        print("Invalid choice.")
        return

    show_inventory(game_state)

    weapon_name = input("Choose a weapon: ")
    weapon = None

    for item in hero.inventory:
        if item["type"] == "Weapon" and item["name"] == weapon_name:
            weapon = item
            break

    if weapon is None:
        print("You do not have that weapon.")
        return

    combat = Combat()

    while enemy["hp"] > 0 and hero.hp > 0:
        player_damage = combat.damage_calculation(weapon["damage"])
        enemy["hp"] -= player_damage

        print(f"You hit {enemy['name']} for {player_damage} damage.")

        if enemy["hp"] <= 0:
            print(f"You defeated {enemy['name']}!")
            rooms[currentroom]["enemy"] = None

            hero.coins += 50
            print("You gained 50 coins.")

            loot = Looting()
            drop = loot.enemy_drop()

            if drop is not None:
                hero.inventory.append(drop)
                print(f"{enemy['name']} dropped {drop['name']}!")

            return

        enemy_damage = combat.damage_calculation(enemy["attack"])
        hero.hp -= enemy_damage

        print(f"{enemy['name']} hits you for {enemy_damage} damage.")
        print(f"Your HP: {hero.hp}")

        if hero.hp <= 0:
            winloss(game_state)
            return

#show_inventory() displays all items currently in the player inventory, with a best case of O(1) and a worst case of O(n).


def show_inventory(game_state):
    hero = game_state["hero"]
    if len(hero.inventory) == 0:
        print("your inventory is empty")
    else:
        print("here are the items in your inventory")
        for i in hero.inventory:
            print(i["name"])
    pass

#use_item searches for and uses an item from the player inventory, with a best case of O(1) and a worst case of O(n).

def use_item(game_state):
    hero = game_state["hero"]
    useable_items = ["Small Potion", "Medium Potion", "Large Potion", "Big Potion", "Super Potion"]
    inventory = hero.inventory
    print(f"here is your inventory {inventory}")
    item = input(f"what item would you like to use? ")
    for i in inventory:
        if i["name"].lower() == item.lower():
            if item == "Small Potion":
                health_gain = i["heal"]
                hero.hp += health_gain 
                if hero.hp > 100:
                    hero.hp = 100
                print(f"you used a{item}")
                inventory.remove(i)
            elif item == "Medium Potion":
                health_gain = i["heal"]
                hero.hp += health_gain 
                if hero.hp > 100:
                    hero.hp = 100
                print(f"you used a{item}")
                inventory.remove(i)
            elif item == "Large Potion":
                health_gain = i["heal"]
                hero.hp += health_gain 
                if hero.hp > 100:
                    hero.hp = 100
                print(f"you used a{item}")
                inventory.remove(i)
            elif item == "Big Potion":
                health_gain = i["heal"]
                hero.hp += health_gain 
                if hero.hp > 100:
                    hero.hp = 100
                print(f"you used a{item}")
                inventory.remove(i)
            elif item == "Super potion":
                health_gain = i["heal"]
                hero.hp += health_gain 
                if hero.hp > 100:
                    hero.hp = 100
                print(f"you used a{item}")
                inventory.remove(i)
            else:
                print("unable to use item")

    
    return
#shop opens the shop system and processes inventory transactions, with a best case of O(1) and a worst case of O(n).
def shop(game_state):
    hero = game_state["hero"]

    print(f"You have {hero.coins} coins.")

    shop = Shop(hero.coins, hero.inventory)

    hero.coins = shop.coins

#maingame loop continuously processes player commands until the game ends, with a best case of O(1) and a worst case of O(n).
def gameloop(game_state):
    while game_state["game_over"] == False:
        command = input("what do you do?:")
        if command == "help":
            print("Commands: look, move, fight, inventory, use, path, help, exit, shop")
        elif command == "inventory":
            show_inventory(game_state)
        elif command == "look":
            lookcmd(game_state)
        elif command == "exit":
            print("You leave the dungeon behind.")
            game_state["game_over"] = True
        elif command == "fight":
            fightcmd(game_state)
        elif command == "use":
            use_item(game_state)
        elif command == "path":
            pathcmd(game_state)
        elif command == "move":
            movecommand(game_state)
        elif command == "shop":
            shop(game_state)

          
        
        game_state["turn_count"] += 1
#build_dungeon_world creates and connects all dungeon rooms in the map, with a best and worst case time complexity of O(1).
def build_dungeon_world():
    dungeon = DungeonWorld()

    dungeon.connect_rooms("Entrance", "Hallway")
    dungeon.connect_rooms("Entrance", "Armory")

    dungeon.connect_rooms("Hallway", "Library")
    dungeon.connect_rooms("Hallway", "Crypt")

    dungeon.connect_rooms("Armory", "Morgue")
    dungeon.connect_rooms("Trap Room", "Morgue")
    
    dungeon.connect_rooms("Library", "Treasure Room")
    dungeon.connect_rooms("Morgue", "Boss Room")

    return dungeon




    #main() starts the game state, hero, dungeon, and game loop, with a best case of O(1) and a worst case of O(n).

def main():
    dungeonschema = build_dungeon_world()
    name = showintro()
    data = load_game_data("game_data.json")
    
    hero = Hero(name, data)
    visitedrooms = []
    enemies = data["assets"]["enemies"]
    

    rooms = {
        "Entrance": {"enemy": None,"visited": False, "Roomdesc": "This is a dark and dreary room with torches lining the walls, the room has two doors at the backend of the room"},
        "Hallway": {"enemy": enemies[1].copy(),"visited": False,  "Roomdesc": "This is a long hallway with torches lining the walls, the air smells of mildew and death. The room has two doors on the left side"},
        "Armory": {"enemy": None, "visited": False, "Roomdesc": "This is a small room lined with swords, shields, and other various weapons. This room has one door in the back"},
        "Library": {"enemy": enemies[2].copy(),"visited": False,  "Roomdesc": "This is a bright yet ominous room with a harth of the left side. lining the walls are a seemingly endless amount of books, the room has one door at the back of the room"},
        "Morgue": {"enemy": enemies[3].copy(), "visited": False,  "Roomdesc": "This is a dark room that reeks of blood. a deadbody lays on a gernie and the left wall is lined with coffins, on the right wall is a small kitchen. this room has one large door in the back"},
        "Crypt": {"enemy": enemies[3].copy(),"visited": False,  "Roomdesc": "This is a large room filled with the graves of dead monsters, each mosolium has a gold engraving on it detailing their name. this room is a deadend"},
        "Treasure Room": {"enemy": None, "visited": False,  "Roomdesc": "This is a massive room filled to the brim with gold. this room is a deadend"},
        "Trap Room": { "enemy": enemies[0].copy(),"visited": False,  "Roomdesc": "This room is filled with various traps like bear traps, snares, and nets. the room has one door on the right side"},
        "Boss Room": { "enemy": enemies[4].copy(),"visited": False,  "Roomdesc": "This is a massive room with tapestries and torches lining the walls, at the back sits a giant throne and a small door behind it"},
        }
    game_state = {
        "visitedrooms": visitedrooms,
        "map": dungeonschema,
        "hero": hero,
        "current_room": "Entrance",
        "game_over": False,
        "victory": False,
        "turn_count": 0,
        "visited_rooms": set(),
        "rooms": rooms
        }
            
    hero.inventory.append({
        "name": "Old Blade",
        "type": "Weapon",
        "rarity": "Starter",
        "damage": 5
    })
    
    if len(hero.inventory) == 0:
        print("Your inventory is empty.")
    else:
        print("Inventory:")
        for item in hero.inventory:
            print(f"{item}")
    
    gameloop(game_state)
    return
main()























    
#load game data
#create hero
#set starting room
#start game loop


#game loop
    #show current room
    #ask for commands
    #process comand
    #update game state
    #check win
    #check death


"""

while not game_over:
    display current room
    command = get player input
    cleaned_command = process input

    if command is valid:
        run command
    else:
        show error message

    check if hero is dead
    check if player won
    
"""

"""
    run_game_loop(game_state)

def gameloop(game_state):
    while game_state["gameover"] is False:
        
print current room
        ask player what they want to do
        clean the command

        if command is help:
            show help menu

        else if command is look:
            show current room description

        else if command is inventory:
            show hero inventory

        else if command is move:
            placeholder for movement

        else if command is fight:
            placeholder for combat

        else if command is path:
            placeholder for DFS

        else if command is exit:
            set game_over to True

        else:
            print unknown command

        increase turn count

        check if hero HP is 0 or below
        check if player has won"""


"""
#gamestate
    #hero
    #current_room
    #visited rooms
    #Game_over
    #victory
    #Turn count
#room interactions 


current room description
available exits
enemy in room
items in room
locked doors
special events

"""
#commands
    #look
    #move
    #roll
    #fight
    #inventory
    #use
    #quest
    #path
    #help
    #exit



"""
commands = {
    "look": look_function,
    "move": move_function,
    "fight": fight_function,
    ...
}
"""

#movement 

"""
player chooses direction
roll dice
if roll succeeds:
    ask world system if move is valid
    update current_room
else:
    trigger failure message or trap
    
    """

#Combat
"""
if current room has enemy:
    call combat system
    if enemy defeated:
        update quest log
        roll loot
        """

#inventory
"""
inventory shows items
use potion heals player
use key unlocks door
use weapon equips item
"""

#win/loss
"""
if hero hp <= 0:
    game_over = true
    print death message

if hero has relic and current_room == final_room:
    victory = true
    game_over = true
    print win message
"""

#data structures 
    #GameState class or dictionary
    #Command dictionary
    #Visited rooms set
    #Inventory list
    #Current room string/id

