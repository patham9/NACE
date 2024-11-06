
class Logger():
    LINE_SEP = '-'*85
    @staticmethod
    def init_message(debug):
        print(Logger.LINE_SEP)
        print("{0:>42}".format("Welcome to NACE!"))
        print(Logger.LINE_SEP)
        if debug:
            print("Debugger:{0}"\
                  "enter this mode to let agent World_Move{0}" \
                  "w/a/s/d : manual World_Movement in simulated world{0}" \
                  "v       : switch to imagined world{0}" \
                  "l       : list hypotheses{0}" \
                  "p       : look through the predicted plan step-wise{0}" \
                  "q       : exit imagined world".format('\n\t'))
        else:
            print("COMMAND-LINE PARAMETERS:{0}" \
                  "\"debug\"         : interactive debugging{0}" \
                  "\"silent\"        : hiding hypothesis formation output{0}" \
                  "\"manual\"        : trying the environment as a human{0}" \
                  "\"nosleep\"       : removes simulation visualization delay{0}" \
                  "\"nopredictions\" : hides prediction rectangles{0}" \
                  "\"nogui\"         : hidea GUI{0}" \
                  "\"notextures\"    : renders textures in GUI{0}" \
                  "\"colors\"        : renders colors{0}" \
                  "\"interactive\"   : enables MeTTa-NARS bridge with shell{0}" \
                  "\"adversary\"     : adda shell-controllable player character{0}" \
                  "\"frames=b\"      : creates a gif file including frames until frame b{0}" \
                  "\"startframe=a\"  : optional to let the gif start later{0}" \
                  "\"world=k\"       : starts world k without asking for the world input{0}" \
                  "\"ona\"           : uses ONA with MeTTa interface in world=9 instead of MeTTa-NARS{0}" \
                  "\"narsese\"       : allows Narsese input instead of MeTTa to use the Bridge.".format('\n\t'))

    @staticmethod
    def world_init_message(manual, challenge_input):
        print(Logger.LINE_SEP)
        if manual:
            if challenge_input:
                print("Enter one of 1-9 to try a world:")
        else:
            print("Input the desired world number from below and press enter.{0}" \
                  "WORLDS:{0}" \
                  "{1}1: Food collecting{0}" \
                  "{1}2: Cup on table challenge{0}" \
                  "{1}3: Doors and keys{0}" \
                  "{1}4: Food collecting with moving object{0}" \
                  "{1}5: Pong game{0}" \
                  "{1}6: Bring eggs to chicken {0}" \
                  "{1}7: Soccer{0}" \
                  "{1}8: Shock world{0}" \
                  "BRIDGE WORLDS:{0}" \
                  "{1}9: world with MeTTa-Narsese console input demanding NARS installation{0}" \
                  "MINIGRID WORLDS:{0}" \
                  "{1}11-20: Interesting MiniGrids{0}" \
                  "{1}30-37: Empty grids{0}" \
                  "NEW WORLDS:{0}" \
                  "{1}-1: Puzzleworld \"minus 1 indeed\"{0}".format('\n\t', '  '))
