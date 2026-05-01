from utils import load_game_data, get_safe_input
from entities import Hero

#this defines valid commands a user to input
VALID_COMMANDS = ["look", "move", "fight", "inventory", "use", "quest", "path", "help", "exit"]
button = ""
#this is the intro/starting scene
def showintro():
    print("==================================================DUNGEONEER==================================================")
    usrinput = input("Enter X to continue:")

    if usrinput == "X" or usrinput == "x":
        button = input("""You are a wanderer pulled into an ancient dungeon
beneath a ruined kingdom.

To escape, you must explore the dungeon, survive enemies,
collect useful items, and find the relic hidden beyond the
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


#gamestate
def movecommand():
    #get current room
    #get adjacent rooms
    #move to room command
    pass

def usecmd():
    #call the inventory
    #let the user choose
    #use the item on entity
    pass
def lookcmd():
    #display current room
    pass

def questcmd():
    #get current quests
    pass

def healthcmd():
    #from hero get health
    #if enemy attacks get attack dmg - player health
    #display health
    pass
def winloss():
    # if health <= 0 gameover
        #else pass
    pass
def fightcmd():
    #get item
    #get item dmg
    #get enemy health
    #enemy health - item dmg
    #get enemy dmg
    #enemy dmg - hero health
    #block / enemy dmg by 50% to 100% random
    pass
    
def show_inventory(hero):
    if len(hero.inventory) == 0:
        print("your inventory is empty")
    else:
        print("here are the items in your inventory")
        for i in hero.inventory:
            print(i)
    pass

def use_item(hero):
    items = []
    for i in hero.inventory:
        items.append(i)

    input(f"what item would you like to use?{items}")
    #call use item function
    pass





def gameloop(game_state):
    while game_state["game_over"] == False:
        command = input("what do you do?:")
        if command == "help":
            print("Commands: look, move, fight, inventory, use, quest, path, help, exit")
        elif command == "inventory":
            show_inventory(game_state["hero"])
        elif command == "look":
            print(f"You are currently in the {game_state['current_room']}.")
        elif command == "exit":
            print("You leave the dungeon behind.")
            game_state["game_over"] = True
        elif command == "fight":
            pass
        elif command == "use":
            pass
        elif command == "quest":
            pass
        elif command == "path":
            print ("")
        elif command == "move":
            move = input("where would you like to go?")
            #movecommand(move)
        
        game_state["turn_count"] += 1

    

def main():
    name = showintro()
    data = load_game_data("game_data.json")
    
    hero = Hero(name, data)
    
    game_state = {
        "hero": hero,
        "current_room": "tavern",
        "game_over": False,
        "victory": False,
        "turn_count": 0,
        "visited_rooms": set()
        }
    hero.inventory.append("Old Blade")
    if len(hero.inventory) == 0:
        print("Your inventory is empty.")
    else:
        print("Inventory:")
        for item in hero.inventory:
            print(f"- {item}")

    gameloop(game_state)
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




    
