(define (problem military-race-2)
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
        pos91
        pos92
        pos93
        pos94
        pos101
        pos102
        pos103
        pos104
        pos111
        pos112
        pos113
        pos114
        pos121
        pos122
        pos123
        pos124
        pos131
        pos132
        pos133
        pos134
        pos141
        pos142
        pos143
        pos144
        pos151
        pos152
        pos153
        pos154
    )

    (:init
        (at pos152)
        (obstacle pos52)
        (obstacle pos53)
        (obstacle pos54)
        (obstacle pos32)
        (obstacle pos22)
        (obstacle pos11)
        (obstacle pos82)
        (obstacle pos84)
        (obstacle pos131)
        (obstacle pos132)
        (obstacle pos133)
        (obstacle pos142)

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
        (adjacent pos81 pos82)
        (adjacent pos81 pos71)
        (adjacent pos81 pos91)
        (adjacent pos82 pos72)
        (adjacent pos82 pos81)
        (adjacent pos82 pos92)
        (adjacent pos82 pos83)
        (adjacent pos83 pos73)
        (adjacent pos83 pos82)
        (adjacent pos83 pos93)
        (adjacent pos83 pos84)
        (adjacent pos84 pos74)
        (adjacent pos84 pos94)
        (adjacent pos84 pos83)
        (adjacent pos91 pos92)
        (adjacent pos91 pos81)
        (adjacent pos91 pos101)
        (adjacent pos92 pos82)
        (adjacent pos92 pos91)
        (adjacent pos92 pos102)
        (adjacent pos92 pos93)
        (adjacent pos93 pos83)
        (adjacent pos93 pos92)
        (adjacent pos93 pos103)
        (adjacent pos93 pos94)
        (adjacent pos94 pos84)
        (adjacent pos94 pos104)
        (adjacent pos94 pos93)
        (adjacent pos101 pos102)
        (adjacent pos101 pos91)
        (adjacent pos101 pos111)
        (adjacent pos102 pos92)
        (adjacent pos102 pos101)
        (adjacent pos102 pos112)
        (adjacent pos102 pos103)
        (adjacent pos103 pos93)
        (adjacent pos103 pos102)
        (adjacent pos103 pos113)
        (adjacent pos103 pos104)
        (adjacent pos104 pos94)
        (adjacent pos104 pos114)
        (adjacent pos104 pos103)
        (adjacent pos111 pos112)
        (adjacent pos111 pos101)
        (adjacent pos111 pos121)
        (adjacent pos112 pos102)
        (adjacent pos112 pos111)
        (adjacent pos112 pos122)
        (adjacent pos112 pos113)
        (adjacent pos113 pos103)
        (adjacent pos113 pos112)
        (adjacent pos113 pos123)
        (adjacent pos113 pos114)
        (adjacent pos114 pos104)
        (adjacent pos114 pos124)
        (adjacent pos114 pos113)
        (adjacent pos121 pos122)
        (adjacent pos121 pos111)
        (adjacent pos121 pos131)
        (adjacent pos122 pos112)
        (adjacent pos122 pos121)
        (adjacent pos122 pos132)
        (adjacent pos122 pos123)
        (adjacent pos123 pos113)
        (adjacent pos123 pos122)
        (adjacent pos123 pos133)
        (adjacent pos123 pos124)
        (adjacent pos124 pos114)
        (adjacent pos124 pos134)
        (adjacent pos124 pos123)
        (adjacent pos131 pos132)
        (adjacent pos131 pos121)
        (adjacent pos131 pos141)
        (adjacent pos132 pos122)
        (adjacent pos132 pos131)
        (adjacent pos132 pos142)
        (adjacent pos132 pos133)
        (adjacent pos133 pos123)
        (adjacent pos133 pos132)
        (adjacent pos133 pos143)
        (adjacent pos133 pos134)
        (adjacent pos134 pos124)
        (adjacent pos134 pos144)
        (adjacent pos134 pos133)
        (adjacent pos141 pos142)
        (adjacent pos141 pos131)
        (adjacent pos141 pos151)
        (adjacent pos142 pos132)
        (adjacent pos142 pos141)
        (adjacent pos142 pos152)
        (adjacent pos142 pos143)
        (adjacent pos143 pos133)
        (adjacent pos143 pos142)
        (adjacent pos143 pos153)
        (adjacent pos143 pos144)
        (adjacent pos144 pos134)
        (adjacent pos144 pos154)
        (adjacent pos144 pos143)
        (adjacent pos151 pos141)
        (adjacent pos151 pos152)
        (adjacent pos152 pos151)
        (adjacent pos152 pos142)
        (adjacent pos152 pos153)
        (adjacent pos153 pos152)
        (adjacent pos153 pos143)
        (adjacent pos153 pos154)
        (adjacent pos154 pos144)
        (adjacent pos154 pos153)
        
    )

    (:goal
        (at pos11)
    )
)