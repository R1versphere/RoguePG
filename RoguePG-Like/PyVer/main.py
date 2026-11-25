# The three nessissary imports
import random
import os
from sys import platform


# Automatically clears the terminal
def clear():
    try:
        os.system("cls" if platform == "win" else "clear")
    except Exception:
        print("\033[2J")
    else:
        print("\033[2J")


# Defining some stuff for the Enemy,
# Items you can be given,
# and the number of rounds
dead = False 
all_items = ["Healing Potion", "Silver Blade", "Sheild"]
enemy_hp = random.randint(5, 8)
enemy_dmg = random.randint(1, 3)
enemy_xp_to_give = random.randint(25, 75)
enemy_ac = 3
rounds = 0


# The player class, bundles everything together
class Player:
    def __init__(self):
        self.items = []
        self.weapon = ""
        self.attack_options = ["Strike"]
        self.clas = ""
        self.hp = 10
        self.dmg_blocking = 0
        self.xp = 0
        self.can_use_magic = False
        self.ac = 3

    def take_damage(self, damage_source): # Gives you damage
        self.hp -= (damage_source - self.dmg_blocking)
        self.dmg_blocking = 0

    def heal(self, hit_points_recovered): # Gives you FREE HP!!!
        self.hp += hit_points_recovered

    def gain_xp(self, enemy_strength): # Gives you xp!
        self.xp += enemy_strength

    def check_for_death(self): # Asks, 'Are you dead?' If your reading this, then no
        if self.hp <= 0:
            global dead
            dead = True

    def get_new_item(self, new_item): # Gives free stuff!
        self.items.append(new_item)

    def deal_damage(self, attack_type): # Deals Damage to others!
        dmg = 0
        match attack_type:
            case "Strike":
                if self.weapon == "": dmg = 1
                elif self.weapon == "Silver Blade": dmg = 5

            case "Parry":
                if self.weapon == "": 
                    self.dmg_blocking = 1
                    dmg =  1
                elif self.weapon == "Silver Blade": 
                    self.dmg_blocking = 3
                    dmg =  3

            case "Sneak Strike":
                if self.weapon == "":
                    dmg = 1
                elif self.weapon == "Silver Blade":
                    dmg = 5

                dmg += int(self.xp // 10)

            case "Magic Missile":
                dmg = 2 + ((int(self.xp // 10)) / 2)

            case "Fire Bolt":
                dmg = 2 + (self.hp/2)

        return dmg


    def get_class(self): # Gives you a class once you reach level 3, or 300 xp
        if self.xp == 300:
            self.clas = input("Which Class do you take: Warrior, Rogue, or Mage?")

            match self.clas.lower():
                case "warrior":
                    self.clas == "Warrior"
                    self.attack_options.append("Parry")

                case "rogue":
                    self.clas == "Rogue"
                    self.attack_options.append("Sneak Strike")

                case "mage":
                    self.clas == "Mage"
                    self.attack_options.append("Magic Missile")
                    self.attack_options.append("Fire Bolt")
                    self.can_use_magic = True

# Initiates the Player
player = Player()

clear()
clear()

while not dead: # If your not dead...
    rounds += 1
    print(f"HP: {player.hp}, {enemy_hp}")
    print(f"Class: {player.clas if player.clas != "" else "No class yet"}")
    print(f"XP: {player.xp}")
    print("Actions:" 
    "\n- Attack"
    "\n- Use Ability"
    "\n- Quit")

    choice = input("\n")

    if choice.lower() == "attack":
        print("Choose an attack:\n")
        for item in player.attack_options:
            print(f"- {item}\n")
        attack_type = input().strip().title()
        if (random.randint(1, 6) >= enemy_ac):
            enemy_hp -= player.deal_damage(attack_type)
            print("Hit!")
        else:
            print("Miss!")

    elif choice.lower() == "ability":
        print("All Items:\n")
        for item in player.items:
            print(f"- {item}")

        chose = input()

        if chose.lower() in ("health potion", "drink potion"):
            player.heal(3)


    elif choice.lower() in ("quit", "end"):
        break


    if enemy_hp <= 0:
        player.items.append(random.choice(all_items))
        player.xp += enemy_xp_to_give
        player.get_class()

        enemy_hp = random.randint(5, 15)
        enemy_ac = random.randint(1, 5)
        enemy_xp_to_give = random.randint(25, 75)
        enemy_dmg = random.randint(1, 5)


    if random.randint(1, 6) >= player.ac:
        print("You get hit!")
        player.take_damage(enemy_dmg)
    else:
        print("The enemy misses you!")
        pass

    player.check_for_death()

clear()
print(f"You lasted {rounds} rounds!")