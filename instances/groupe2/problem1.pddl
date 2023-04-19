(define (problem military-race-1)
    (:domain military-race)
    (:objects
        pos11
        pos12
        pos13
        pos14
        
        pos21
        pos22
        pos23
        pos24
        
        pos31
        pos32
        pos33
        pos34
        
        pos41
        pos42
        pos43
        pos44
        
        pos51
        pos52
        pos53
        pos54
        
        pos61
        pos62
        pos63
        pos64
        
        pos71
        pos72
        pos73
        pos74
        
        pos81
        pos82
        pos83
        pos84
    )

    (:init
        (at pos82)
        (obstacle pos51)
        (obstacle pos52)
        (obstacle pos72)
        (obstacle pos43)
        (munition)

        (adjacent pos11 pos21)
        (adjacent pos11 pos12)
        (adjacent pos12 pos11)
        (adjacent pos12 pos22)
        (adjacent pos12 pos13)
        (adjacent pos13 pos12)
        (adjacent pos13 pos23)
        (adjacent pos13 pos14)
        (adjacent pos14 pos24)
        (adjacent pos14 pos13)
        (adjacent pos21 pos22)
        (adjacent pos21 pos11)
        (adjacent pos21 pos31)
        (adjacent pos22 pos12)
        (adjacent pos22 pos21)
        (adjacent pos22 pos32)
        (adjacent pos22 pos23)
        (adjacent pos23 pos13)
        (adjacent pos23 pos22)
        (adjacent pos23 pos33)
        (adjacent pos23 pos24)
        (adjacent pos24 pos14)
        (adjacent pos24 pos34)
        (adjacent pos24 pos23)
        (adjacent pos31 pos32)
        (adjacent pos31 pos21)
        (adjacent pos31 pos41)
        (adjacent pos32 pos22)
        (adjacent pos32 pos31)
        (adjacent pos32 pos42)
        (adjacent pos32 pos33)
        (adjacent pos33 pos23)
        (adjacent pos33 pos32)
        (adjacent pos33 pos43)
        (adjacent pos33 pos34)
        (adjacent pos34 pos24)
        (adjacent pos34 pos44)
        (adjacent pos34 pos33)
        (adjacent pos41 pos42)
        (adjacent pos41 pos31)
        (adjacent pos41 pos51)
        (adjacent pos42 pos32)
        (adjacent pos42 pos41)
        (adjacent pos42 pos52)
        (adjacent pos42 pos43)
        (adjacent pos43 pos33)
        (adjacent pos43 pos42)
        (adjacent pos43 pos53)
        (adjacent pos43 pos44)
        (adjacent pos44 pos34)
        (adjacent pos44 pos54)
        (adjacent pos44 pos43)
        (adjacent pos51 pos52)
        (adjacent pos51 pos41)
        (adjacent pos51 pos61)
        (adjacent pos52 pos42)
        (adjacent pos52 pos51)
        (adjacent pos52 pos62)
        (adjacent pos52 pos53)
        (adjacent pos53 pos43)
        (adjacent pos53 pos52)
        (adjacent pos53 pos63)
        (adjacent pos53 pos54)
        (adjacent pos54 pos44)
        (adjacent pos54 pos64)
        (adjacent pos54 pos53)
        (adjacent pos61 pos62)
        (adjacent pos61 pos51)
        (adjacent pos61 pos71)
        (adjacent pos62 pos52)
        (adjacent pos62 pos61)
        (adjacent pos62 pos72)
        (adjacent pos62 pos63)
        (adjacent pos63 pos53)
        (adjacent pos63 pos62)
        (adjacent pos63 pos73)
        (adjacent pos63 pos64)
        (adjacent pos64 pos54)
        (adjacent pos64 pos74)
        (adjacent pos64 pos63)
        (adjacent pos71 pos72)
        (adjacent pos71 pos61)
        (adjacent pos71 pos81)
        (adjacent pos72 pos62)
        (adjacent pos72 pos71)
        (adjacent pos72 pos82)
        (adjacent pos72 pos73)
        (adjacent pos73 pos63)
        (adjacent pos73 pos72)
        (adjacent pos73 pos83)
        (adjacent pos73 pos74)
        (adjacent pos74 pos64)
        (adjacent pos74 pos84)
        (adjacent pos74 pos73)
        (adjacent pos81 pos71)
        (adjacent pos81 pos82)
        (adjacent pos82 pos81)
        (adjacent pos82 pos72)
        (adjacent pos82 pos83)
        (adjacent pos83 pos82)
        (adjacent pos83 pos73)
        (adjacent pos83 pos84)
        (adjacent pos84 pos74)
        (adjacent pos84 pos83)
        
    )

    (:goal
        (at pos11)
    )
)
