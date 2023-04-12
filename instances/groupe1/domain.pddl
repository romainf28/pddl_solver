(define (domain glace)
    (:requirements :typing) 
    (:types emplacement frigo parfum preparation contenant client)
    (:predicates
	    (in-emplacement ?parfum - parfum ?emplacement - emplacement)
		(in-frigo ?parfum - parfum ?frigo - frigo)
		(free-emplacement ?emplacement - emplacement)
		
		(free-preparation ?preparation - preparation)
		(contains-contenant ?preparation - preparation ?contenant - contenant)
		(has-contenant ?preparation - preparation)
		(contains-scoop1 ?preparation - preparation ?parfum - parfum)
		(has-1scoop ?preparation - preparation)
		(contains-scoop2 ?preparation - preparation ?parfum - parfum)
		(has-2scoop ?preparation - preparation)
		(contains-scoop3 ?preparation - preparation ?parfum - parfum)
		(has-3scoop ?preparation - preparation)
		
		(served1 ?client - client ?contenant - contenant ?parfum1 - parfum)
        (served2 ?client - client ?contenant - contenant ?parfum1 ?parfum2 - parfum)
        (served3 ?client - client ?contenant - contenant ?parfum1 ?parfum2 ?parfum3 - parfum)
    )

    (:action move-emplacement
        :parameters
        (?parfum - parfum ?from - emplacement ?to - frigo)
        :precondition
        (in-emplacement ?parfum ?from)
        :effect
        (and (not (in-emplacement ?parfum ?from)) (in-frigo ?parfum ?to) (free-emplacement ?from))
    )
    
    (:action move-frigo
        :parameters
        (?parfum - parfum ?from - frigo ?to - emplacement)
        :precondition
        (and (in-frigo ?parfum ?from) (free-emplacement ?to))
        :effect
        (and (not (in-frigo ?parfum ?from)) (in-emplacement ?parfum ?to) (not (free-emplacement ?to)))
    )
    
    (:action add-contenant
        :parameters
        (?preparation - preparation ?contenant - contenant)
        :precondition
        (free-preparation ?preparation)
        :effect
        (and (not (free-preparation ?preparation)) (contains-contenant ?preparation ?contenant) (has-contenant ?preparation))
    )
    
    (:action add-scoop1
        :parameters
        (?preparation - preparation ?parfum - parfum ?emplacement - emplacement)
        :precondition
        (and (has-contenant ?preparation) (in-emplacement ?parfum ?emplacement))
        :effect
        (and (contains-scoop1 ?preparation ?parfum) (has-1scoop ?preparation) (not (has-contenant ?preparation)))
    )
    
    (:action add-scoop2
        :parameters
        (?preparation - preparation ?parfum - parfum ?emplacement - emplacement)
        :precondition
        (and (has-1scoop ?preparation) (in-emplacement ?parfum ?emplacement))
        :effect
        (and (contains-scoop2 ?preparation ?parfum) (has-2scoop ?preparation) (not (has-1scoop ?preparation)))
    )
    
    (:action add-scoop3
        :parameters
        (?preparation - preparation ?parfum - parfum ?emplacement - emplacement)
        :precondition
        (and (has-2scoop ?preparation) (in-emplacement ?parfum ?emplacement))
        :effect
        (and (contains-scoop3 ?preparation ?parfum) (has-3scoop ?preparation) (not (has-2scoop ?preparation)))
    )
    
    (:action throw
    :parameters
        (?preparation - preparation)
        :precondition
        (not (free-preparation ?preparation))
        :effect
        (and (free-preparation ?preparation) (not (has-contenant ?preparation)) (not (has-1scoop ?preparation)) (not (has-2scoop ?preparation)) (not (has-3scoop ?preparation)))
    )
    
    (:action serve1
        :parameters
        (?preparation - preparation ?client - client ?contenant - contenant ?parfum1 - parfum)
        :precondition
        (and (has-1scoop ?preparation) (contains-contenant ?preparation ?contenant) (contains-scoop1 ?preparation ?parfum1))
        :effect
        (and (free-preparation ?preparation) (not (has-1scoop ?preparation)) (served1 ?client ?contenant ?parfum1))
    )
    
    (:action serve2
        :parameters
        (?preparation - preparation ?client - client ?contenant - contenant ?parfum1 ?parfum2 - parfum)
        :precondition
        (and (has-2scoop ?preparation) (contains-contenant ?preparation ?contenant) (contains-scoop1 ?preparation ?parfum1) (contains-scoop2 ?preparation ?parfum2))
        :effect
        (and (free-preparation ?preparation) (not (has-2scoop ?preparation)) (served2 ?client ?contenant ?parfum1 ?parfum2))
    )
    
    (:action serve3
        :parameters
        (?preparation - preparation ?client - client ?contenant - contenant ?parfum1 ?parfum2 ?parfum3 - parfum)
        :precondition
        (and (has-3scoop ?preparation) (contains-contenant ?preparation ?contenant) (contains-scoop1 ?preparation ?parfum1) (contains-scoop2 ?preparation ?parfum2) (contains-scoop3 ?preparation ?parfum3))
        :effect
        (and (free-preparation ?preparation) (not (has-3scoop ?preparation)) (served3 ?client ?contenant ?parfum1 ?parfum2 ?parfum3))
    )
    
)