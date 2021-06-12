from sources import player as pl # type: ignore 


def main():
    """
    The fuction starts with opening the log file and writing the location of the first event of the game.
    It initiates an object play of the class player, that contains all the necessary functions of the game.
    It then uses a while loop to access the function getaction from the class Player. 
    When out of the loop, the function then cleans both the inventory.txt and log.txt files.

    Raises
    ------

    It raises an exception for the getaction function. Which is caused by the player Input.
    In this case it passes the function getaction another time, to get another acceptable input.
    """
    with open("log.txt",'w') as f:
        f.write("Prison Cell")
        f.write('\n')
    game_is_going = True
    print("You woke up dizzy, the cold grey floor is uncomfortable beneath you.\n You feel dread. Terrified, you do not remember anything!")
    play = pl.Player()
    while game_is_going:
        try:
            game_is_going = play.get_action()
        except Exception:
            print("I did not understand!")
            game_is_going = play.get_action()

    with open('log.txt','w') as f:
        f.truncate(0)
        f.close()
    with open('sources/items/inventory.txt', 'w') as f:
        f.truncate(0)
        f.close()

if __name__ == '__main__':
    main()

