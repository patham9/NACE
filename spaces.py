from hyperon.ext import register_atoms
from hyperon import *

class PatternOperation(OperationObject):
    def __init__(self, name, op, unwrap=False, rec=False):
        super().__init__(name, op, unwrap)
        self.rec = rec
    def execute(self, *args, res_typ=AtomType.UNDEFINED):
        return super().execute(*args, res_typ=res_typ)

def wrapnpop(func):
    def wrapper(*args):
        a = [str("'"+arg) if arg is SymbolAtom else str(arg) for arg in args]
        res = func(*a)
        return [res]
    return wrapper

def call_bridgeinput(*a):
    from bridge import BRIDGE_Input
    tokenizer = globalmetta.tokenizer()
    parser = SExprParser("(Task injected via MeTTa)")
    BRIDGE_Input("!"+str(a[0]), None, False, False, True) #TODO pass observed_world for belief input
    return parser.parse(tokenizer)

@register_atoms(pass_metta=True)
def spaces_atoms(metta):
    global globalmetta
    globalmetta = metta
    call_bridgeinput_atom = G(PatternOperation('bridgeinput', wrapnpop(call_bridgeinput), unwrap=False))
    return { r"bridgeinput": call_bridgeinput_atom }

def space_init():
    global runner
    with open("spaces.metta", "r") as f:
        metta_code = f.read()
    runner = MeTTa()
    runner.run(metta_code)


time = 0
def space_input(metta):
    if metta.strip() == "":
        return
    print("MeTTa input:", metta)
    #states printing is broken prints the old state after change-state!, so inject current time this way instead:
    metta = metta.replace("AddGoalEvent", f"AddGoalEvent {time} ").replace("AddBeliefEvent", f"AddBeliefEvent {time} ").replace("(.:", f"!(.: {time} ").replace("(!:", f"!(!: {time} ")
    runner.run(metta)
    #print("Beliefs:", runner.run("!(get-atoms &beliefs)"))
    #print("Goals:", runner.run("!(get-atoms &goals)"))

def space_tick():
    global time
    time+=1
    print(runner.run(f"!(Step {time})"));
