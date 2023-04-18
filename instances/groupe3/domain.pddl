(define (domain rubik)
    (:requirements :strips :typing)
    (:types color)
    (:predicates
        (face1 ?f ?l ?d - color)
        (face2 ?f ?r ?d - color)
        (face3 ?b ?l ?d - color)
        (face4 ?b ?r ?d - color)
        (face5 ?f ?l ?u - color)
        (face6 ?f ?r ?u - color)
        (face7 ?b ?l ?u - color)
        (face8 ?b ?r ?u - color)
    )

    (:action R
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f2 ?r2 ?d2 - color) (when (face2 ?f2 ?r2 ?d2)
                (and
                    (not (face2 ?f2 ?r2 ?d2))
                    (face6 ?d2 ?r2 ?f2)
                ))
            )
            (forall (?b4 ?r4 ?d4 - color) (when (face4 ?b4 ?r4 ?d4)
                (and
                    (not (face4 ?b4 ?r4 ?d4))
                    (face2 ?d4 ?r4 ?b4)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face8 ?u6 ?r6 ?f6)
                ))
            )
            (forall (?b8 ?r8 ?u8 - color) (when (face8 ?b8 ?r8 ?u8)
                (and
                    (not (face8 ?b8 ?r8 ?u8))
                    (face4 ?u8 ?r8 ?b8)
                ))
            )
        )
    )

    (:action R_p
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f2 ?r2 ?d2 - color) (when (face2 ?f2 ?r2 ?d2)
                (and
                    (not (face2 ?f2 ?r2 ?d2))
                    (face4 ?d2 ?r2 ?f2)
                ))
            )
            (forall (?b4 ?r4 ?d4 - color) (when (face4 ?b4 ?r4 ?d4)
                (and
                    (not (face4 ?b4 ?r4 ?d4))
                    (face8 ?d4 ?r4 ?b4)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face2 ?u6 ?r6 ?f6)
                ))
            )
            (forall (?b8 ?r8 ?u8 - color) (when (face8 ?b8 ?r8 ?u8)
                (and
                    (not (face8 ?b8 ?r8 ?u8))
                    (face6 ?u8 ?r8 ?b8)
                ))
            )
        )
    )

    (:action U
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f5 ?l5 ?u5 - color) (when (face5 ?f5 ?l5 ?u5)
                (and
                    (not (face5 ?f5 ?l5 ?u5))
                    (face7 ?l5 ?f5 ?u5)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face5 ?r6 ?f6 ?u6)
                ))
            )
            (forall (?b7 ?l7 ?u7 - color) (when (face7 ?b7 ?l7 ?u7)
                (and
                    (not (face7 ?b7 ?l7 ?u7))
                    (face8 ?l7 ?b7 ?u7)
                ))
            )
            (forall (?b8 ?r8 ?u8 - color) (when (face8 ?b8 ?r8 ?u8)
                (and
                    (not (face8 ?b8 ?r8 ?u8))
                    (face6 ?r8 ?b8 ?u8)
                ))
            )
        )
    )

    (:action U_p
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f5 ?l5 ?u5 - color) (when (face5 ?f5 ?l5 ?u5)
                (and
                    (not (face5 ?f5 ?l5 ?u5))
                    (face6 ?l5 ?f5 ?u5)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face8 ?r6 ?f6 ?u6)
                ))
            )
            (forall (?b7 ?l7 ?u7 - color) (when (face7 ?b7 ?l7 ?u7)
                (and
                    (not (face7 ?b7 ?l7 ?u7))
                    (face5 ?l7 ?b7 ?u7)
                ))
            )
            (forall (?b8 ?r8 ?u8 - color) (when (face8 ?b8 ?r8 ?u8)
                (and
                    (not (face8 ?b8 ?r8 ?u8))
                    (face7 ?r8 ?b8 ?u8)
                ))
            )
        )
    )

    (:action F
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f1 ?l1 ?d1 - color) (when (face1 ?f1 ?l1 ?d1)
                (and
                    (not (face1 ?f1 ?l1 ?d1))
                    (face5 ?f1 ?d1 ?l1)
                ))
            )
            (forall (?f2 ?r2 ?d2 - color) (when (face2 ?f2 ?r2 ?d2)
                (and
                    (not (face2 ?f2 ?r2 ?d2))
                    (face1 ?f2 ?d2 ?r2)
                ))
            )
            (forall (?f5 ?l5 ?u5 - color) (when (face5 ?f5 ?l5 ?u5)
                (and
                    (not (face5 ?f5 ?l5 ?u5))
                    (face6 ?f5 ?u5 ?l5)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face2 ?f6 ?u6 ?r6)
                ))
            )
        )
    )

    (:action F_p
        :parameters ()
        :precondition (and)
        :effect (and
            (forall (?f1 ?l1 ?d1 - color) (when (face1 ?f1 ?l1 ?d1)
                (and
                    (not (face1 ?f1 ?l1 ?d1))
                    (face2 ?f1 ?d1 ?l1)
                ))
            )
            (forall (?f2 ?r2 ?d2 - color) (when (face2 ?f2 ?r2 ?d2)
                (and
                    (not (face2 ?f2 ?r2 ?d2))
                    (face6 ?f2 ?d2 ?r2)
                ))
            )
            (forall (?f5 ?l5 ?u5 - color) (when (face5 ?f5 ?l5 ?u5)
                (and
                    (not (face5 ?f5 ?l5 ?u5))
                    (face1 ?f5 ?u5 ?l5)
                ))
            )
            (forall (?f6 ?r6 ?u6 - color) (when (face6 ?f6 ?r6 ?u6)
                (and
                    (not (face6 ?f6 ?r6 ?u6))
                    (face5 ?f6 ?u6 ?r6)
                ))
            )
        )
    )

)