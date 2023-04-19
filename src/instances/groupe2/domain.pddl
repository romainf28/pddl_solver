(define (domain military-race)

    (:types
    position
    )

    (:predicates (at ?pos) (adjacent ?pos1 ?pos2) (obstacle ?pos) (munition)
    )
    
    (:action move
        :parameters (?pos1 - position ?pos2 - position)
        :precondition (and (adjacent ?pos1 ?pos2) (at ?pos1) (not (obstacle ?pos2))
        )
        :effect (and (at ?pos2) (not (at ?pos1))
        )
    )
    
    (:action shoot
        :parameters (?pos1 - position ?pos2 - position)
        :precondition (and (adjacent ?pos1 ?pos2) (at ?pos1) (munition)
        )
        :effect (and (not (obstacle ?pos2)) (not (munition))
        )
    )
)