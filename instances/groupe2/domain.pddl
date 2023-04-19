(define (domain military-race)

    (:predicates (at ?pos) (adjacent ?pos1 ?pos2) (wall ?pos) (obstacle ?pos) (munition)
    )
    
    (:action move
        :parameters (?pos1 ?pos2)
        :precondition (and (adjacent ?pos1 ?pos2) (at ?pos1) (not (wall ?pos2)) (not (obstacle ?pos2))
        )
        :effect (and (at ?pos2) (not (at ?pos1))
        )
    )
    
    (:action shoot
        :parameters (?pos1 ?pos2)
        :precondition (and (adjacent ?pos1 ?pos2) (at ?pos1) (not (wall ?pos2)) (munition)
        )
        :effect (and (not (obstacle ?pos2)) (not (munition))
        )
    )
)