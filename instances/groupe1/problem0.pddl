(define (problem glacier)
  (:domain glace)
  (:objects
    emplacement1 emplacement2 - emplacement
    frigo1 - frigo
    vanille chocolat fraise - parfum
    preparation1 preparation2 - preparation
    cornet pot -contenant
    client1 - client)
  (:init
    (in-emplacement chocolat emplacement1)
    (in-emplacement fraise emplacement2)
    (in-frigo vanille frigo1)
    (free-preparation preparation1)
    (free-preparation preparation2))
  (:goal (and
    (served2 client1 cornet chocolat vanille)))
)