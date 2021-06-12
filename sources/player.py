"""
Contains everything necessary for organising the possible actions performed by the player during the game.

Classes:
--------
Player

"""


import json

class Player:
    """
    A class to represent the player and all the actions he can make during the game.

    Attributes:
    -----------
    location : str
        The location of the player (The Room he is in right now)
    action : str
        The command entered by the player. It determines what he would like to do.
    player_pos_x : int
        A numerical value that determines the horizontal position of the player.
    player_pos_y : int
        A numerical value that determines the vertical position of the player.
    width : int
        It determines the max space that a player can move in horizontaly. (It depends on the location)
    length: int
        It determines the max space that a player can move in verticaly. (It depends on the location)
    items: List
        A list of available items in the space. (It depends on the location)
    scenes: List
        A list of the available locations.

    Methods:
    --------
    locater():
        gets the location of the player.
    get_action():
        gets the action of the player, and determines what method to use depending on the action provided.
    move():
        determines how the player can move. It changes the player_pos_x and player_pos_y attributes.
    get():
        If it is what the player wants it adds the intended item to the inventory(inventory.txt).
    use():
        It uses an available item. Either in the inventory or in the location.
    Look():
        It provides a description of the location.
    examine():
        It provides a description of the item.
    location_fun():
        It displays the location and the position of the player.
    shove():
        The player can use it to get a helpful reaction from the item. A clue.
    inventory():
        It displays the content of the inventory.

    """

    def locater(self):
        """
        From the last line written in the log.txt file it determines the location of the player.

        Returns:
        --------
        location : str
            A string containing the location of the player.
        """
        location = ''
        with open('log.txt') as f:
            lines = f.readlines()
        location = lines[-1]
        return location

    def __init__(self):
        """
        It immediatley gets the location of the player using the method locater()

        """
        self.location = self.locater()

    def get_action(self):
        """
        It asks the player for his action. The action will then be inputted as a form of a string.
        The action will be then entered in the log.txt file, and assigned to action attribute in the class.
        Based on the action entered, a method will be assigned to determine the reaction of the game.
        After the reaction is handled, it will write the location as the last line of the log.txt file.

        Returns:
        True for all possible actions except for "exit", which will return a False boolean.
        This will help in determining to exit or stay in the game.

        """
        action_fun = input("What to do? ")
        self.action = action_fun
        with open('log.txt','a') as f:
            action_start = action_fun.split(" ")[0]
            if action_start.lower() == "move":
                self.move()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_fun.lower() == "look":
                self.look()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_fun.lower() == "location":
                self.location_fun()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_fun.lower() == "inventory":
                self.inventory()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_start.lower() == "get":
                self.get()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_start.lower() == "shove":
                self.shove()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_start.lower() == "examine":
                self.examine()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_start.lower() == "use":
                self.use()
                f.write(action_fun)
                f.write('\n')
                f.write(self.location)
                return True
            if action_fun.lower() == "exit":
                f.write(action_fun)
                f.write('\n')
                return False
            else: 
                print("I did not understand")
                return True

    action = " "
    player_pos_x = 0
    player_pos_y = 0
    location = " "


    width = 10
    length = 10
    with open('sources/items/items.json') as f:
        items = json.load(f)
        f.close()
    with open('sources/Scenes/scenes.json') as f:
        scenes = json.load(f)
        f.close()

    if location == 'Prison Cell':
        width = 10
        length = 10
    elif location == 'Tunnel':
        width = 1
        length = 10

    def move(self):
        """
        using the action attribute of the class. It determines how movements should be handled, and it
        edits either the attribute player_pos_x or the attribute player_pos_y accordingly.
        It also determines walls based on the attributes width and length.

        Returns:
        --------
        None
        """
        movement = self.action
        if movement.lower() == "move east" or movement.lower() == 'e':
            print("You are moving to the east")
            if self.player_pos_x< self.width  :
                self.player_pos_x += 1
            else:
                print("You have reached the wall!")
        elif movement.lower() == "move west" or movement.lower() == 'w':
            print("You are moving to the west")
            if self.player_pos_x > 1:
                self.player_pos_x -= 1
            else:
                print("You have reached the wall!")
        elif movement.lower() == "move north" or movement.lower() == 'n':
            print("you are moving to the north")
            if self.player_pos_y < self.length:
                self.player_pos_y += 1
            else:
                print("You have reached the wall!")

        elif movement.lower() == "move south" or movement.lower() == 's':
            print("You are moving to the south")
            if self.player_pos_y > 0:
                self.player_pos_y -= 1
            else:
                print("You have reached the wall!")
        else:
            print("invalid movement!")

    def get(self):
        """
        Using the action attribute from the class, it assigns it to a string variable s.
        Since this method can be only accessed if the first word of the action attribute is get,
        s is determined using the second and the third word (if possible).
        Depending on conditions, determined in the items attribute, it then appends the possible items
        into a list called gettable_items.
        It then uses the s string to determine which element from the gettable_items list to be added to the
        inventory.txt file.
        It uses a boolean variable gotted to determine if any items where added to the inventory. If none are added
        it will print a statement "get what?" to let the player know that he could not add the item to his inventory, 
        or it is not possible to do so.

        Raises:
        -------
        IndexError: It is possible that the item is identified using one word or two words. Since we can not know this,
            an IndexError is used when assigning the value to s. 

        """
        s = ' '
        getting = self.action
        element_getting = getting.split(" ")

        try:
            s = element_getting[1] + " " + element_getting[2]
        except IndexError:
            s = element_getting[1]

        gettable_items = []
        gotted = False

        for i in self.items:
            if i["gettable"] == True and i["Room"] == self.location.strip("\n") and i["visible"] == True and i["name"].lower() == s.lower():
                gettable_items.append(i)
                print("you got :" + i["name"])
                gotted = True

        for g in gettable_items:
            if g["name"].lower() == s.lower():
                with open('sources/items/inventory.txt', 'a') as f:
                    f.write(g['name'])
                    f.write("\n")

        if gotted == False:
            print("get what ?")

    def location_fun(self):
        """
        It displays the values of the attributes: location, player_pos_x and player_pos_y.

        """
        print(self.location + " (" + str(self.player_pos_x) + ", " + str(self.player_pos_y) + ") ")


    def use(self):
        """
        Based on the attribute action, the function determines which items the player wants to use.
        This item is the assigned to the string s.
        This function is then divided into two parts.
        The first part:
            If the desirable item to use can not be added to the inventory.
            In this case, the function loops through the items list and depending on certain conditions and s,
            it determines which item to use and what will happen when this item is used.
        The secon part:
            If the desirbale item to use is available in the inventory.
            In this case, the function opens the file inventory.txt, it then reads its contents. If s is 
            present, it removes it from the inventory. And it determines what will happen when this item is used.

        Raises:
        -------
        IndexError: It is possible that the item is identified using one word or two words. Since we can not know this,
            an IndexError is used when assigning the value to s. 

        """
        using = self.action
        element_using = using.split(" ")
        fifi = False
        try:
            s = element_using[1] + " " + element_using[2]
        except IndexError:
            s = element_using[1]
            
        for i in self.items:
            if i["Room"] == self.location.strip("\n") and i["usable"] == True and i["name"].lower() == s.lower() and i["visible"] == True:
                print("You have used " + i["name"] + "!")
                fifi = True
                print(i["used"])
                
                if i["name"] == "Tunnel":
                    self.location = "Tunnel"
                    fifi = True
                    print("You have used: " + i["name"])
                
                if i["name"] == "Screw Driver":
                    for j in self.items:
                        if j["name"] == "Tunnel":
                            j["usable"] = True
                            print("The Tunnel is open now!")

        if s.lower() != "screw driver":
            with open("sources/items/inventory.txt", 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for l in lines:
                    
                    if l.strip('\n').lower() != s.lower():
                        f.write(l)
                    else:
                        print("You have used: " + s)
                        fifi = True
                f.truncate()

        if fifi == False:
            print("It is unusable!")



    def shove(self):
        """
        Based on the attribute action, the function determines which items the player wants to shove.
        This item is then assigned to the string s.
        The function loops through the items list and depending on certain conditions and s,
        it determines which item to shove and what will happen when this item is shoved.

        Raises:
        -------
        IndexError: It is possible that the item is identified using one word or two words. Since we can not know this,
            an IndexError is used when assigning the value to s. 

        """
        shoving = self.action
        element_shoving = shoving.split(" ")
        try:
            s = element_shoving[1] + " " + element_shoving[2]
        except IndexError:
            s = element_shoving[1]
        mattr = False
        for i in self.items:
            if i["Shovable"] == True and i["Room"] == self.location.strip("\n") and i["name"].lower() == s.lower() and i["visible"] == True:
                print("You have shoved: " + s)
                if s.lower() == "mattress":
                    mattr = True
                if i["name"] == "toilet":
                    print("Oh! This toilet is almost loose. I can probably screw it loose!")
                    for j in self.items:
                        if j["name"] == "Tunnel":
                            j["visible"] = True
                        if j["name"] == "Screw Driver":
                            j["usable"] = True
        if mattr:
            print("Oh shit! The mattress was heavy! But at least I can use this screw driver!")
            for i in self.items:
                if i["name"] == "Screw Driver":
                    i["visible"] = True
            

    def look(self):
        """
        It provides a description of the scene based on the location of the player.
        """
        for s in self.scenes:
            if s["name"] == self.location.strip("\n"):
                print(s["Description"])

    def examine(self):
        """
        Based on the attribute action, the function determines which items the player wants to examine.
        Meaning, which item the player wants to provide further description to.
        The attribute is then assigned to the string s. 
        Based on certain conditions and s, the function then displays the description of the item.

        Raises:
        -------
        IndexError: It is possible that the item is identified using one word or two words. Since we can not know this,
            an IndexError is used when assigning the value to s. 

        """
        examination = self.action
        element_examination = examination.split(" ")

        try:
            s = element_examination[1] + element_examination[2]
        except IndexError:
            s = element_examination[1]

        for i in self.items:
            if i["name"].lower() == s.lower() and i["Room"] == self.location.strip("\n") and i["visible"] == True:
                print(i["Description"])
        

    def inventory(self):
        """
        It opens the inventory.txt file and then displays its contents.
        """
        path = 'sources/items/inventory.txt'
        print("You have in your inventory: ")
        with open(path) as f:
            lines = f.readlines()
        for l in lines:
            print(l)


