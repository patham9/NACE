;Tasks which one can enter in interactive mode (such as in world9):

;GOALS:

;cup is above plate
!(AddGoalEvent (((u x G) --> up) (1.0 0.90)))

;goal is above cup
!(AddGoalEvent (((H x u) --> up) (1.0 0.90)))

;cup is above table
!(AddGoalEvent (((u x T) --> up) (1.0 0.90)))

;bird is above plate
!(AddGoalEvent (((x x G) --> up) (1.0 0.90)))

;bird is above table
!(AddGoalEvent (((x x T) --> up) (1.0 0.90)))

;HIGHER-LEVEL GOALS:

;the table should be prepared
!(AddGoalEvent ((table --> (IntSet prepared)) (1.0 0.90)))

;the coffee should be made
!(AddGoalEvent ((coffee --> (IntSet made)) (1.0 0.90)))

;the cup should be stored
!(AddGoalEvent ((cup --> (IntSet stored)) (1.0 0.90)))

;the bird should sit at the table
!(AddGoalEvent (((bird x table) --> sit) (1.0 0.90)))

;HIGHER-HIGHER-LEVEL GOALS:

;the container should be stored
!(AddGoalEvent ((container --> (IntSet stored)) (1.0 0.90)))

;the drink should be made
!(AddGoalEvent ((drink --> (IntSet made)) (1.0 0.90)))

;the furniture should be prepared
!(AddGoalEvent ((furniture --> (IntSet prepared)) (1.0 0.90)))

;something black should be made
!(AddGoalEvent (((IntSet black) --> (IntSet made)) (1.0 0.90)))

;BELIEFS:

;cup should be above plate
!(AddBeliefEvent (((u x G) --> up) (1.0 0.90)))

;goal should be above cup
!(AddBeliefEvent (((H x u) --> up) (1.0 0.90)))

;cup should be above table
!(AddBeliefEvent (((u x T) --> up) (1.0 0.90)))

;bird should be above plate
!(AddBeliefEvent (((x x G) --> up) (1.0 0.90)))

;bird should be above table
!(AddBeliefEvent (((x x T) --> up) (1.0 0.90)))

;HIGHER-LEVEL BELIEFS:

;the table is prepared
!(AddBeliefEvent ((table --> (IntSet prepared)) (1.0 0.90)))

;the coffee is made
!(AddBeliefEvent ((coffee --> (IntSet made)) (1.0 0.90)))

;the cup is stored
!(AddBeliefEvent ((cup --> (IntSet stored)) (1.0 0.90)))

;the bird sits at the table
!(AddBeliefEvent (((bird x table) --> (IntSet sit)) (1.0 0.90)))

;HIGHER-HIGHER-LEVEL BELIEFS:

;the container is stored
!(AddBeliefEvent ((container --> (IntSet stored)) (1.0 0.90)))

;the drink is made
!(AddBeliefEvent ((drink --> (IntSet made)) (1.0 0.90)))

;the furniture is prepared
!(AddBeliefEvent ((furniture --> (IntSet prepared)) (1.0 0.90)))

;MIXED BELIEFS:

;something black is made
!(AddBeliefEvent (((IntSet black) --> (IntSet made)) (1.0 0.90)))
