!(import! &self spaces)
!(bind! &beliefs (new-space))
!(bind! &goals (new-space))
(= (InputInto $space $val) (add-atom $space $val))

;metta-nars inputs and derivations:

(= (AddGoalEvent $t $1) (InputInto &goals (GotAtTime $t $1)))
(= (.: $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (AddBeliefEvent $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (!: $t $1) (InputInto &goals (GotAtTime $t $1)))

(= (MakeAndBringCoffee)
   (bridgeinput (case (match &beliefs (GotAtTime $someTime ((coffee --> (IntSet made)) ($SomeFreq $SomeConf))) ok)
                                ((Empty (AddGoalEvent ((coffee --> (IntSet made)) (1.0 0.90))))
                                 ($Else (AddGoalEvent ((table --> (IntSet prepared)) (1.0 0.90))))))))
(= (Step $t) (MakeAndBringCoffee))
