;Tasks which one can enter in interactive mode (such as in world9):

;GOALS:

;cup above plate
!(AddGoalEvent (((u x _) --> up) (1.0 0.90)))

;goal above cup
!(AddGoalEvent (((H x u) --> up) (1.0 0.90)))

;cup above table
!(AddGoalEvent (((u x T) --> up) (1.0 0.90)))

;bird above plate
!(AddGoalEvent (((x x _) --> up) (1.0 0.90)))

;bird above table
!(AddGoalEvent (((x x T) --> up) (1.0 0.90)))

;HIGHER-LEVEL GOALS:

;the table should be set
!(AddGoalEvent ((table --> (IntSet set)) (1.0 0.90)))

;the coffee should be made
!(AddGoalEvent ((coffee --> (IntSet made)) (1.0 0.90)))

;the cup should be stored
!(AddGoalEvent ((cup --> (IntSet stored)) (1.0 0.90)))

;HIGHER-HIGHER-LEVEL GOALS:

;the container should be stored
!(AddGoalEvent ((container --> (IntSet stored)) (1.0 0.90)))

;the drink should be made
!(AddGoalEvent ((drink --> (IntSet made)) (1.0 0.90)))

;the furniture should be set
!(AddGoalEvent ((furniture --> (IntSet set)) (1.0 0.90)))

;BELIEFS:

;cup above plate
!(AddBeliefEvent (((u x _) --> up) (1.0 0.90)))

;goal above cup
!(AddBeliefEvent (((H x u) --> up) (1.0 0.90)))

;cup above table
!(AddBeliefEvent (((u x T) --> up) (1.0 0.90)))

;bird above plate
!(AddBeliefEvent (((x x _) --> up) (1.0 0.90)))

;bird above table
!(AddBeliefEvent (((x x T) --> up) (1.0 0.90)))

;HIGHER-LEVEL BELIEFS:

;the table is set
!(AddBeliefEvent ((table --> (IntSet set)) (1.0 0.90)))

;the coffee is made
!(AddBeliefEvent ((coffee --> (IntSet made)) (1.0 0.90)))

;the cup is stored
!(AddBeliefEvent ((cup --> (IntSet stored)) (1.0 0.90)))

;HIGHER-HIGHER-LEVEL BELIEFS:

;the container is stored
!(AddBeliefEvent ((container --> (IntSet stored)) (1.0 0.90)))

;the drink is made
!(AddBeliefEvent ((drink --> (IntSet made)) (1.0 0.90)))

;the furniture is set
!(AddBeliefEvent ((furniture --> (IntSet set)) (1.0 0.90)))
