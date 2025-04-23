;Fully MeTTa-controlled agent demo with atom spaces, featuring NACE + NARS
;Run with:
;python3 main.py world=9 spaces
!(import! &self spaces)
!(bind! &beliefs (new-space))
!(bind! &goals (new-space))
(= (InputInto $space $val) (add-atom $space $val))

;recent metta-nars beliefs and goals:
(= (AddGoalEvent $t $1) (InputInto &goals (GotAtTime $t $1)))
(= (.: $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (AddBeliefEvent $t $1) (InputInto &beliefs (GotAtTime $t $1)))
(= (!: $t $1) (InputInto &goals (GotAtTime $t $1)))

(= (Goal $t $A)
   (if (== (% $t 5) 0)
       (AddGoalEvent ($A (1.0 0.90)))
       (empty)))


(= (SequenceGoal $t $A $B)
   (case (match &beliefs (GotAtTime $someTime ($A ($Freq $Conf))) ok)
         ((Empty (Goal $t $A))
          ($Else (Goal $t $B)))))

(= (MakeAndBringCoffee $t)
   (bridgeinput (SequenceGoal $t (coffee --> (IntSet made)) (table --> (IntSet prepared)))))

(= (Step $t) (superpose ((MakeAndBringCoffee $t)
                         ;(bridgeinput (AddBeliefEvent ((table --> (IntSet prepared)) (1.0 0.90)))) ;test belief inject
                         (let* (($space (superpose (&beliefs &goals)))
                                ($Ev (get-atoms $space))
                                ((GotAtTime $t2 $task) $Ev))
                          (if (> (- $t 50) $t2)
                              (remove-atom $space $Ev) Empty)))))
