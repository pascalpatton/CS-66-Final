import random

class Combat:
    def __init__(self):
        self.temproll = 0 #placeholder for the 20 sided-dice rolls

    def roll_20(self): # A 20 sided dice for damage calculations
        self.temproll = random.randint(1,20)

    def roll_6(self): # A 6 sided dice to determine move order for the fight
        self.temproll = random.randint(1,6)

    def item_use(self, item_type, weapon_damage, potion_heal):
        if item_type == "weapon":
            damage = self.damage_calculation(weapon_damage)
            return damage
        
        if item_type == "Potion":
            heal = potion_heal#Will need the value of the healing potion
            return heal

    def damage_calculation(self, weapon): # The damage calculations to determine how much damage the player will do
        self.roll_20

        #Enemy Dodge / 0% damage
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
        order = False

        while order is False:
            player_roll = self.roll_6
            enemy_roll = self.roll_6

            if player_roll > enemy_roll:
                #player moves first
                order = True

            elif player_roll < enemy_roll:
                #enemy moves first
                order = True

            elif player_roll == enemy_roll:
                #keep rolling until order is determined
                pass

        return order