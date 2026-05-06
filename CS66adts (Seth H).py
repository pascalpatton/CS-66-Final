import random
import json
from tkinter import N

from annotated_types import LowerCase

#Reads the json file for the loot table
with open("loot_table.json", 'r') as f:
    loot_table = json.load(f)

#ADT for the combat system
class Combat:
    def __init__(self):
        self.temproll = 0 #placeholder for the 20 sided-dice rolls

    def roll_20(self): # A 20 sided dice for damage calculations
        self.temproll = random.randint(1,20)

    def roll_6(self): # A 6 sided dice to determine move order for the fight
        self.temproll = random.randint(1,6)

    def item_use(self, item_type, damage_or_heal):
        #checks to see if the item we are using is a weapon (Check loot_table.json to see how it is implemented)
        if item_type == "weapon":
            #Use the damage_calculation function to deal damage
            damage = self.damage_calculation(damage_or_heal)
            return damage
        
        #Similarly to the weapon item type, this checks if the item is a healing potion
        if item_type == "Potion":
            heal = damage_or_heal
            return heal

    def damage_calculation(self, weapon): # The damage calculations to determine how much damage the player will do
        self.roll_20()

        #Dodge / 0% damage
        if self.temproll == 1:
            damage = 0
            self.temproll = 0
            return damage
        
        #Weak attack / 50% damage
        elif self.temproll >= 2 and self.temproll <= 9:
            damage = weapon/2
            self.temproll = 0
            return damage
        
        #Okay attack / 75% damage
        elif self.temproll >= 10 and self.temproll <= 14:
            damage = (weapon/4)*3
            self.temproll = 0
            return damage

        #Normal attack / 100% damage
        elif self.temproll >= 15 and self.temproll <= 19:
            damage = weapon
            self.temproll = 0
            return damage

        #Critical attack / 150% damage
        elif self.temproll == 20:
            damage = weapon*1.5
            self.temproll = 0
            return damage

        #This shouldn't happen, but just in case it does, it will deal no damage
        else:
            print("Magic prevents you from doing that")
            return 0
    
    def turn_order(self): # Determines the move order based on the 6 sided dice
        first = None

        while first is None:
            player_roll = self.roll_6()
            enemy_roll = self.roll_6()

            if player_roll > enemy_roll:
                #player moves first
                first = "Player"

            elif player_roll < enemy_roll:
                #enemy moves first
                order = "Enemy"

            elif player_roll == enemy_roll:
                #keep rolling until order is determined
                pass

        return order
    
#ADT for mob drops
class Looting:
    def __init__(self, loot_table = loot_table): #Made loot_table (loot_table.json) a fixed parameter since thats the only loot table I want to pull from
        self.coins = 0 #Placeholder until you can get the Heros coins
        self.loot_table = loot_table
        self.temp_roll = 0
        self.loot = None
        

    def roll_100(self): #A 100 sided dice to make rarities easier to distinguish
        roll = random.randint(1,100)
        return roll

    def enemy_coin_drop(self):
        self.coins += 50
        return self.coins

    #What loot any enemy will drop after defeat
    def enemy_drop(self):
        enemy_hp = 0 #placeholder until this adt gets implemented

        #When the enemy is dead
        if enemy_hp == 0:
            self.coins += self.enemy_coin_drop()
            roll = self.roll_100()

            #45% to get a Common item
            if roll >= 1 and roll <= 45:
                self.loot = random.choice(self.loot_table["loot"]["common"])#Chooses a random item from the common list 

            #35% to get an Uncommon item
            elif roll >= 46 and roll <= 80:
                    self.loot = random.choice(self.loot_table["loot"]["uncommon"])#Chooses a random item from the uncommon list


            #14% to get a Rare item (Unfortunate part of having a 1% chance somewhere)
            elif roll >= 81 and roll <= 94:
                    self.loot = random.choice(self.loot_table["loot"]["rare"])#Chooses a random item from the rare list

            #5% to get an Epic item    
            elif roll >= 95 and roll <= 99:
                    self.loot = random.choice(self.loot_table["loot"]["epic"])#Chooses a random item from the epic list

            #1% to get a Legendary item
            elif roll == 100:
                    self.loot = random.choice(self.loot_table["loot"]["legendary"])#Chooses a random item from the legendary list
        
        #self.temp_roll = 0
        return self.loot 


#Unit tests to see if the Looting class works
#lt = Looting(loot_table)

#print(lt.roll_100()) #does not affect the outcome of enemy_drop

#drop = lt.enemy_drop()

#if drop['type'] == "Weapon": 
    #print(f"You got: {drop['name']} ({drop['rarity']}), Deals: {drop['damage']} damage!")

#if drop['type'] == "Potion":
    #print(f"You got: {drop['name']} ({drop['rarity']}), Heals: {drop['heal']} health!")

#print(drop)

class Shop:
    def __init__(self, hero_coins, inventory):
        self.coins = hero_coins #Takes the value of however many
        self.inventory = inventory #To add items you buy or sell items you want for money
        first_time = True
        stay = True

        if first_time == True:
            #Could create some cool dialogue to welcome the player for the first time
            print("Cool!")
            first_time = False

        else:
            print("Welcome Back!")

        #Infinite loop in case you want to buy or sell more items
        while stay == True:
            option = input("----------------------------------------------------\n"
                "What would you like to do? (Buy, Sell, Leave) ")

            if option.lower() == "buy":
                self.buy()
            
            elif option.lower() == "sell":
                self.sell()

            elif option.lower() == "leave":
                stay = False

    def buy(self):
        #Can only buy potions for now but could add something else later
        choice = input("----------------------------------------------------\n"
        f"What would you like to buy? Coins Available: {self.coins}\n"
        "----------------------------------------------------\n"
        "1. Small Potion: 100 Coins\n" 
        "2. Medium Potion: 200 Coins\n" 
        "3. Large Potion: 300 Coins\n" 
        "4. Big Potion: 400 Coins\n" 
        "5. Super Potion: 500 Coins\n"
        "6. Back: ")
        
        #Buying a Small Potion
        if choice == "1":
            if self.coins >= 100:
                self.coins -= 100 #Takes 100 coins from the player
                print("Thank you for your purchase!")
                self.inventory.append(loot_table["loot"]["common"][1]) #Puts the Small Potion in the players inventory

            else:
                print("You dont have enough coins.")

        #Buying a Medium Potion
        elif choice == "2":
            if self.coins >= 200:
                self.coins -= 200 #Takes 200 coins from the player
                print("Thank you for your purchase!")
                self.inventory.append(loot_table["loot"]["uncommon"][1])#Puts the Medium Potion in the players inventory

            else:
                print("You dont have enough coins.")

        #Buing a Large Potion
        elif choice == "3":
            if self.coins >= 300:
                self.coins -= 300 #Takes 300 coins from the player
                print("Thank you for your purchase!")
                self.inventory.append(loot_table["loot"]["rare"][1])#Puts the Large Potion in the players inventory

            else:
                print("You dont have enough coins.")

        #Buying a Big Potion
        elif choice == "4":
            if self.coins >= 400:
                self.coins -= 400 #Takes 400 coins from the player
                print("Thank you for your purchase!")
                self.inventory.append(loot_table["loot"]["epic"][1])#Puts the Big Potion in the players inventory

            else:
                print("You dont have enough coins.")

        #Buying a Super Potion
        elif choice == "5":
            if self.coins >= 500:
                self.coins -= 500 #Takes 500 coins from the player
                print("Thank you for your purchase!")
                self.inventory.append(loot_table["loot"]["legendary"][1])#Puts the Super Potion in the players inventory

            else:
                print("You dont have enough coins.")

        #Leaves the buying station
        elif choice.lower() == "6" or "back":
            pass

        else:
            pass

    def sell(self):
        print("----------------------------------------------------")
        for item in self.inventory:
            print(f"{item["name"]}: {item["value"]} coins")
        choice = input("----------------------------------------------------\n"
            "What would you like to sell?\n").strip().lower()#Strip makes sure there are no extra or unnecessary spaces or lines for the item, lower makes it easier to find the item you are looking for
        
        for item in self.inventory:
            #Can check for any item
            if item["name"].lower() == choice:
                #You cant sell an item if it doesn't have a value
                if item["value"] is "None":
                    print("You cant sell that item.")
                    break #so the sell() function doesn't keep running
                else:
                    #Sells the item and removes it from the inventory
                    self.coins += item["value"]
                    self.inventory.remove(item)#Pop needs a position where remove can remove an item based off of a name
                    print("Thank you for your sale!")

                

                
        

Shop(500,[{"name": "Rusty Sword", "type": "Weapon", "rarity": "Common", "damage": 7, "value": 50},{"name": "Bone Sword", "type": "Weapon", "rarity": "Uncommon", "damage": 12, "value": 150}])