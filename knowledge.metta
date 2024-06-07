;What it means to set the table:
!(AddBeliefEvent (((((u x T) --> up) &/ (^ nop)) =/> (table --> (IntSet set))) (1.0 0.9)))
!(AddBeliefEvent (((table --> (IntSet set)) ==> ((u x T) --> up)) (1.0 0.9)))

;What it means to deliver coffee:
!(AddBeliefEvent (((((u x _) --> up) &/ (^ nop)) =/> (coffee --> (IntSet made))) (1.0 0.9)))
!(AddBeliefEvent (((coffee --> (IntSet made)) ==> ((u x _) --> up)) (1.0 0.9)))

;What it means to store cup
!(AddBeliefEvent (((((H x u) --> up) &/ (^ nop)) =/> (cup --> (IntSet stored))) (1.0 0.9)))
!(AddBeliefEvent (((cup --> (IntSet stored)) ==> ((H x u) --> up)) (1.0 0.9)))
