!(import! &self spaces)
!(bind! &beliefs (new-space))
!(bind! &goals (new-space))
(= (InputInto $space $val) (add-atom $space $val))

;metta-nars inputs and derivations:

(= (AddGoalEvent $t $1) (InputInto &goals (GotAtTime $t $1)))
(= (.: $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (AddBeliefEvent $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (!: $t $1) (InputInto &goals (GotAtTime $t $1)))

(= (Goal $A)
   (case (match &goals (GotAtTime $someTime ($A ($SomeFreq $SomeConf))) ok)
                                ((Empty (AddGoalEvent ($A (1.0 0.90))))
                                 ($Else Empty))))

(= (SequenceGoal $A $B)
   (case (match &beliefs (GotAtTime $someTime ($A ($SomeFreq $SomeConf))) ok)
                                ((Empty (Goal $A))
                                 ($Else (Goal $B)))))

(= (MakeAndBringCoffee)
   (bridgeinput (SequenceGoal (coffee --> (IntSet made)) (table --> (IntSet prepared)))))

(= (Step $t) (MakeAndBringCoffee))
