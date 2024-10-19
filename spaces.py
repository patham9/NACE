from hyperon import *

def space_init():
    global runner
    metta_code = """
!(bind! &input_beliefs (new-space))
!(bind! &input_goals (new-space))
!(bind! &derived_beliefs (new-space))
!(bind! &derived_goals (new-space))
(= (InputInto $space $val) (add-atom $space $val))
(= (AddGoalEvent $t $1) (InputInto &input_goals (GotAtTime $t $1)))
(= (.: $t $1) (InputInto &derived_beliefs (GotAtTime $t $1)))
(= (AddBeliefEvent $t $1) (InputInto &input_beliefs (GotAtTime $t $1)))
(= (!: $t $1) (InputInto &derived_goals (GotAtTime $t $1)))

(= (Step $t) PutExecutionCodeHere) 
;todo call BRIDGE_Input($something, observed_world, NACEToNARS=False, ForceMeTTa=True) 
;with some AddBeliefEvent or AddGoalEvent to show ability to call into agent
    """
    runner = MeTTa()
    runner.run(metta_code)

time = 0
def space_input(metta):
    global time
    time+=1
    if metta.strip() == "":
        return
    print("MeTTa input:", metta)
    #states printing is broken prints the old state after change-state!, so inject current time this way instead:
    metta = metta.replace("AddGoalEvent", f"AddGoalEvent {time} ").replace("AddBeliefEvent", f"AddBeliefEvent {time} ").replace("(.:", f"!(.: {time} ").replace("(!:", f"!(!: {time} ")
    runner.run(metta)
    runner.run(f"!(Step {time})")
    runner.run(f"!(change-state! &currentTime {time})")
    print("Input beliefs:", runner.run("!(get-atoms &input_beliefs)"))
    print("Derived beliefs:", runner.run("!(get-atoms &derived_beliefs)"))
    print("Input goals:", runner.run("!(get-atoms &input_goals)"))
    print("Derived goals:", runner.run("!(get-atoms &derived_goals)"))
