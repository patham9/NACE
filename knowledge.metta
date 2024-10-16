;PROPERTY GROUNDING:

;What it means to set the table:
!(AddBeliefEvent ((((u x T) --> up) ==> (table --> (IntSet prepared))) (1.0 0.9)))
!(AddBeliefEvent (((table --> (IntSet prepared)) ==> ((u x T) --> up)) (1.0 0.9)))

;What it means to deliver coffee:
!(AddBeliefEvent ((((u x G) --> up) ==> (coffee --> (IntSet made))) (1.0 0.9)))
!(AddBeliefEvent (((coffee --> (IntSet made)) ==> ((u x G) --> up)) (1.0 0.9)))

;What it means to store cup
!(AddBeliefEvent ((((H x u) --> up) ==> (container --> (IntSet stored))) (1.0 0.9)))
!(AddBeliefEvent (((container --> (IntSet stored)) ==> ((H x u) --> up)) (1.0 0.9)))

;What it means to for bird to go to sit at table
!(AddBeliefEvent ((((x x T) --> right) ==> ((bird x table) --> sit)) (1.0 0.9)))
!(AddBeliefEvent ((((bird x table) --> sit) ==> ((x x T) --> right)) (1.0 0.9)))

;CATEGORICAL INFORMATION

;Cups are containers
;!(AddBeliefEvent ((cup --> container) (1.0 0.9)))
!(AddBeliefEvent (((container --> $1) ==> (cup --> $1)) (1.0 0.9)))
!(AddBeliefEvent ((($1 --> container) ==> ($1 --> cup)) (1.0 0.9)))
!(AddBeliefEvent (((cup --> $1) ==> (container --> $1)) (1.0 0.5)))
!(AddBeliefEvent ((($1 --> container) ==> ($1 --> cup)) (1.0 0.5)))

;Tables are furniture
;!(AddBeliefEvent ((table --> furniture) (1.0 0.9)))
!(AddBeliefEvent (((furniture --> $1) ==> (table --> $1)) (1.0 0.9)))
!(AddBeliefEvent ((($1 --> furniture) ==> ($1 --> table)) (1.0 0.9)))
!(AddBeliefEvent (((table --> $1) ==> (furniture --> $1)) (1.0 0.5)))
!(AddBeliefEvent ((($1 --> furniture) ==> ($1 --> table)) (1.0 0.5)))

;Coffee is a drink
;!(AddBeliefEvent ((coffee --> drink) (1.0 0.9)))
!(AddBeliefEvent (((drink --> $1) ==> (coffee --> $1)) (1.0 0.9)))
!(AddBeliefEvent ((($1 --> drink) ==> ($1 --> coffee)) (1.0 0.9)))
!(AddBeliefEvent (((coffee --> $1) ==> (drink --> $1)) (1.0 0.5)))
!(AddBeliefEvent ((($1 --> drink) ==> ($1 --> coffee)) (1.0 0.5)))

;Coffee is black
;!(AddBeliefEvent ((coffee --> (IntSet black)) (1.0 0.9)))
!(AddBeliefEvent ((((IntSet black) --> $1) ==> (coffee --> $1)) (1.0 0.9)))
!(AddBeliefEvent ((($1 --> (IntSet black)) ==> ($1 --> coffee)) (1.0 0.9)))
!(AddBeliefEvent (((coffee --> $1) ==> ((IntSet black) --> $1)) (1.0 0.5)))
!(AddBeliefEvent ((($1 --> (IntSet black)) ==> ($1 --> coffee)) (1.0 0.5)))

;table is brown
;!(AddBeliefEvent ((table --> (IntSet brown)) (1.0 0.9)))
!(AddBeliefEvent ((((IntSet brown) --> $1) ==> (table --> $1)) (1.0 0.9)))
!(AddBeliefEvent ((($1 --> (IntSet brown)) ==> ($1 --> table)) (1.0 0.9)))
!(AddBeliefEvent (((table --> $1) ==> ((IntSet brown) --> $1)) (1.0 0.5)))
!(AddBeliefEvent ((($1 --> (IntSet brown)) ==> ($1 --> table)) (1.0 0.5)))
