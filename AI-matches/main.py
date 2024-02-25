# J4F - "Just For Fun", or "5-minute evening projects"
# AI-matches console game, or how to create a neural network using matchboxes without a computer ;)
# Homepage: https://github.com/greentracery/J4F
# Requirements:
# - python 3.6.x or higher
#

from mem import MemModel
import random

intro = """
# Wellcome to AI-matches - simplest console self-learning game!
# Rules: there are a certain number of matches, 
#     each player can take from 1 to 3 in one turn.
# The winner is the one who took the last match/matches. 
# The player who goes first is chosen randomly.

"""

commands = ('play', 'list', 'load', 'save', 'delete', 'show', 'clear', 'help', 'exit')

commands_help = """
# Command's Help:
#
# 1. play [learn | nolearn] - start new game with self-learning 
#      (default) or without self-learning,
#      parameter 'learn'|'nolearn' works like a toggle affecting subsequent 
#      games in session until it is changed again
# 2. list - show the list of saved model state's snapshots
# 3. load snapshot_name - loads model state snapshot 
#      with the specified name from storage
# 4. save snapshot_name - save current model state to snapshot 
#      with the specified name into the storage
# 5. delete snapshot_name - delete model state snapshot 
#      with the specified name from storage
# 6. show - show the current model state (just for curiosity) ;)
# 7. clear - reset current model state to defaults
# 8. help - show this command list
# 9. exit - exit the program
"""

learning = True # self-learning is available by default

def get_command():
    while True:
        a = input("Enter command (or print 'help' to get command's help): ")
        s = a.split(" ")
        if len(s) and s[0] in commands : return s 
        else : print(f"Unknown command '{a}'")
        
def thanks_and_exit():
    """ exit """
    print('#### Thank You!', 'Good Bye! ####')
    exit(0)

def model_states_list():
    """ get list of saved model states """
    states = m.get_states_list()
    if len(states):
        i = 1
        for state in states:
            print(i, state)
            i+=1
    else:
        print ("States list is empty.")

def load_model_state(cmd: list):
    """ load one of saved model states """
    if len(cmd) > 1 and cmd[1] is not None:
        result = m.load_state(cmd[1])
        if result:
            print(f"Model state '{cmd[1]}' was loaded successfully.") 
        else:
            print(f"Error: model state '{cmd[1]}' was not loaded.")
    else:
        print("Model state name is not set. Use command 'list' to see all avalaible states.")

def save_model_state(cmd: list):
    """ save couuert model state """
    if len(cmd) > 1 and cmd[1] is not None:
        result = m.save_state(cmd[1])
        if result:
            print(f"Model state '{cmd[1]}' was saved successfully.") 
        else:
            print(f"Error: model state '{cmd[1]}' was not saved.")
    else:
        print("Model state name is not set. Use command 'list' to see all avalaible states.")

def delete_model_state(cmd: list):
    """ delete one of saved model states """
    while True:
        a = input("Are You shure? (y/n): ")
        if a.lower() in ('y', 'n'):
            break
        else:
            print("Please choose 'y' on 'n'")
    if a.lower() == 'n':
        return
    if len(cmd) > 1 and cmd[1] is not None:
        result = m.del_state(cmd[1])
        if result:
            print(f"Model state '{cmd[1]}' was deleted successful.") 
        else:
            print(f"Error: model state '{cmd[1]}' was not deleted.")
    else:
        print("Model state name is not set. Use command 'list' to see all avalaible states.")

def get_turn_value(n = None):
    """ get player's turn choice """
    while True:
        j = input(f"Enter your choice {m.default_values}: ")
        if j.isdigit() and int(j) in m.default_values: 
            if n is None or int(j) <= int(n):
                return int(j)

def play(cmd: list):
    """ stat gameplay """
    global learning
    if len(cmd) > 1 and cmd[1] == 'nolearn':
        learning = False
    elif len(cmd) > 1 and cmd[1] == 'learn':
        learning = True
    if not learning:
        print("#### START NEW GAME WITHOUT SELF-LEARNING ####")
    else:
        print("#### START NEW GAME WITH SELF-LEARNING ####")
    n = len(m.model) + 1
    print(f"We have {n} matches: ", "|" * n )
    print("Randomly choose the right to make the first turn in the game...")
    my_turn = bool(random.randint(0, 1))
    if my_turn:
        j = random.randint(min(m.default_values), max(m.default_values))
        print(f"...the first turn is mine. My choice is: {j}")
    else:
        print(f"...the first turn is yours.")
        j = get_turn_value()
    n = n - j
    print(f"{n} matches left: ", "|" * n )
    my_turn = not my_turn
    while n > 0:
        if my_turn:
            j = m.choice(n)
            if j != 0:
                print(f"My choice is: {j}")
            else:
                print("I know You can win on next turn. Congratulations!")
                print("(It doesn't matter anymore, but I'll take 1 match)")
                j = 1
        else:
            j = get_turn_value(n)
        n = n - j
        print(f"{n} matches left: ", "|" * n )
        my_turn = not my_turn
    if my_turn:
        print("You took the last matches, so... YOU WIN!")
        if learning: m.punishment() 
    else:
        print("I took the last matches, so... YOU LOSE.")
        if learning: m.encouragement()
    m.clear_steps()

def i_need_help():
    print(commands_help)
    
def show_model():
    for matchbox in m.model.items():
        print(matchbox[0], matchbox[1])

def clear_model():
    while True:
        a = input("Are You shure? (y/n): ")
        if a.lower() in ('y', 'n'):
            break
        else:
            print("Please choose 'y' on 'n'")
    if a.lower() == 'y':
        i = len(m.model)
        m.get_new_model(i)
        print("Done!")
    else:
        return

print(intro)

m = MemModel()

while True:
    s = get_command()
    if s[0] == 'exit': thanks_and_exit()
    if s[0] == 'help': i_need_help()
    if s[0] == 'show': show_model()
    if s[0] == 'clear': clear_model()
    if s[0] == 'list': model_states_list()
    if s[0] == 'load' : load_model_state(s)
    if s[0] == 'save' : save_model_state(s)
    if s[0] == 'delete' : delete_model_state(s)
    if s[0] == 'play' : play(s)
