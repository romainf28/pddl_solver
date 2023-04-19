(define (problem military-race-0)
    (:domain military-race)
    (:objects
        pos11 - position
        pos12 - position
        pos13 - position

        pos21 - position
        pos22 - position
        pos23 - position

        pos31 - position
        pos32 - position
        pos33 - position

        pos41 - position
        pos42 - position
        pos43 - position

        pos51 - position
        pos52 - position
        pos53 - position

        pos61 - position
        pos62 - position
        pos63 - position
    )

    (:init
        (at pos62)
        (obstacle pos42)
        (obstacle pos21)
        (munition)

        (adjacent pos11 pos21)
        (adjacent pos11 pos12)
        (adjacent pos12 pos11)
        (adjacent pos12 pos22)
        (adjacent pos12 pos13)
        (adjacent pos13 pos23)
        (adjacent pos13 pos12)
        (adjacent pos21 pos22)
        (adjacent pos21 pos11)
        (adjacent pos21 pos31)
        (adjacent pos22 pos12)
        (adjacent pos22 pos21)
        (adjacent pos22 pos32)
        (adjacent pos22 pos23)
        (adjacent pos23 pos13)
        (adjacent pos23 pos33)
        (adjacent pos23 pos22)
        (adjacent pos31 pos32)
        (adjacent pos31 pos21)
        (adjacent pos31 pos41)
        (adjacent pos32 pos22)
        (adjacent pos32 pos31)
        (adjacent pos32 pos42)
        (adjacent pos32 pos33)
        (adjacent pos33 pos23)
        (adjacent pos33 pos43)
        (adjacent pos33 pos32)
        (adjacent pos41 pos42)
        (adjacent pos41 pos31)
        (adjacent pos41 pos51)
        (adjacent pos42 pos32)
        (adjacent pos42 pos41)
        (adjacent pos42 pos52)
        (adjacent pos42 pos43)
        (adjacent pos43 pos33)
        (adjacent pos43 pos53)
        (adjacent pos43 pos42)
        (adjacent pos51 pos52)
        (adjacent pos51 pos41)
        (adjacent pos51 pos61)
        (adjacent pos52 pos42)
        (adjacent pos52 pos51)
        (adjacent pos52 pos62)
        (adjacent pos52 pos53)
        (adjacent pos53 pos43)
        (adjacent pos53 pos63)
        (adjacent pos53 pos52)
        (adjacent pos61 pos51)
        (adjacent pos61 pos62)
        (adjacent pos62 pos61)
        (adjacent pos62 pos52)
        (adjacent pos62 pos63)
        (adjacent pos63 pos53)
        (adjacent pos63 pos62)
    )

    (:goal
        (at pos11)
    )
)
