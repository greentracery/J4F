# AI-matches - simplest console self-learning game
## Or reflections on the topic "How to create a neural network using matchboxes without a computer" ;)

### Requirements:

    python 3.6.x or higher

### Rules:

    There are a certain number of matches, each player can take from 1 to 3 in one turn.
    
    The winner is the one who took the last match/matches. 
    
    The player who goes first is chosen randomly.

### Commands:

    - play [learn | nolearn] - start new game with self-learning 
        (default) or without self-learning,
        parameter 'learn'|'nolearn' works like a toggle affecting subsequent 
        games in session until it is changed again
        
    - list - show the list of saved model state's snapshots
    
    - load snapshot_name - loads model state snapshot 
        with the specified name from storage
        
    - save snapshot_name - save current model state to snapshot 
        with the specified name into the storage
        
    - delete snapshot_name - delete model state snapshot 
        with the specified name from storage
        
    - show - show the current model state (just for curiosity) ;)
    
    - clear - reset current model state to defaults
    
    - help - show this command list
    
    - exit - exit the program
    
