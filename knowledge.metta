;PROPERTY GROUNDING:

;What it means to set the table:
!(AddBeliefEvent (((table --> (IntSet set)) <=> ((u x T) --> up)) (1.0 0.9)))

;What it means to deliver coffee:
!(AddBeliefEvent (((coffee --> (IntSet made)) <=> ((u x _) --> up)) (1.0 0.9)))

;What it means to store cup
!(AddBeliefEvent (((cup --> (IntSet stored)) <=> ((H x u) --> up)) (1.0 0.9)))

;CATEGORICAL INFORMATION

;Cups are containers
!(AddBeliefEvent ((cup --> container) (1.0 0.9)))

;Tables are furniture
!(AddBeliefEvent ((table --> furniture) (1.0 0.9)))

;Coffee is a drink
!(AddBeliefEvent ((coffee --> drink) (1.0 0.9)))
