;PROPERTY GROUNDING:

;What it means to set the table:
!(AddBeliefEternal ((((u x T) --> up) ==> (table --> (IntSet prepared))) (1.0 0.9)))
!(AddBeliefEternal (((table --> (IntSet prepared)) ==> ((u x T) --> up)) (1.0 0.9)))

;What it means to deliver coffee:
!(AddBeliefEternal ((((u x G) --> up) ==> (coffee --> (IntSet made))) (1.0 0.9)))
!(AddBeliefEternal (((coffee --> (IntSet made)) ==> ((u x G) --> up)) (1.0 0.9)))

;What it means to store cup
!(AddBeliefEternal ((((H x u) --> up) ==> (container --> (IntSet stored))) (1.0 0.9)))
!(AddBeliefEternal (((container --> (IntSet stored)) ==> ((H x u) --> up)) (1.0 0.9)))

;What it means to for bird to go to sit at table
!(AddBeliefEternal ((((x x T) --> right) ==> ((bird x table) --> sit)) (1.0 0.9)))
!(AddBeliefEternal ((((bird x table) --> sit) ==> ((x x T) --> right)) (1.0 0.9)))

;CATEGORICAL INFORMATION

;Cups are containers
;!(AddBeliefEternal ((cup --> container) (1.0 0.9)))
!(AddBeliefEternal (((container --> $1) ==> (cup --> $1)) (1.0 0.9)))
!(AddBeliefEternal ((($1 --> cup) ==> ($1 --> container)) (1.0 0.9)))
!(AddBeliefEternal (((cup --> $1) ==> (container --> $1)) (1.0 0.5)))
!(AddBeliefEternal ((($1 --> container) ==> ($1 --> cup)) (1.0 0.5)))

;Tables are furniture
;!(AddBeliefEternal ((table --> furniture) (1.0 0.9)))
!(AddBeliefEternal (((furniture --> $1) ==> (table --> $1)) (1.0 0.9)))
!(AddBeliefEternal ((($1 --> table) ==> ($1 --> furniture)) (1.0 0.9)))
!(AddBeliefEternal (((table --> $1) ==> (furniture --> $1)) (1.0 0.5)))
!(AddBeliefEternal ((($1 --> furniture) ==> ($1 --> table)) (1.0 0.5)))

;Coffee is a drink
;!(AddBeliefEternal ((coffee --> drink) (1.0 0.9)))
!(AddBeliefEternal (((drink --> $1) ==> (coffee --> $1)) (1.0 0.9)))
!(AddBeliefEternal ((($1 --> coffee) ==> ($1 --> drink)) (1.0 0.9)))
!(AddBeliefEternal (((coffee --> $1) ==> (drink --> $1)) (1.0 0.5)))
!(AddBeliefEternal ((($1 --> drink) ==> ($1 --> coffee)) (1.0 0.5)))

;Coffee is black
;!(AddBeliefEternal ((coffee --> (IntSet black)) (1.0 0.9)))
!(AddBeliefEternal ((((IntSet black) --> $1) ==> (coffee --> $1)) (1.0 0.9)))
!(AddBeliefEternal ((($1 --> coffee) ==> ($1 --> (IntSet black))) (1.0 0.9)))
!(AddBeliefEternal (((coffee --> $1) ==> ((IntSet black) --> $1)) (1.0 0.5)))
!(AddBeliefEternal ((($1 --> (IntSet black)) ==> ($1 --> coffee)) (1.0 0.5)))

;table is brown
;!(AddBeliefEternal ((table --> (IntSet brown)) (1.0 0.9)))
!(AddBeliefEternal ((((IntSet brown) --> $1) ==> (table --> $1)) (1.0 0.9)))
!(AddBeliefEternal ((($1 --> table) ==> ($1 --> (IntSet brown))) (1.0 0.9)))
!(AddBeliefEternal (((table --> $1) ==> ((IntSet brown) --> $1)) (1.0 0.5)))
!(AddBeliefEternal ((($1 --> (IntSet brown)) ==> ($1 --> table)) (1.0 0.5)))
