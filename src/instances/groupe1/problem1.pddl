(define (problem glacier)
  (:domain glace)
  (:objects
    emplacement1 emplacement2 - emplacement
    frigo1 - frigo
    vanille chocolat fraise menthe cafe - parfum
    preparation1 preparation2 - preparation
    cornet pot - contenant
    client1 client2 client3 - client)
  (:init
    (in-emplacement chocolat emplacement1)
    (in-emplacement fraise emplacement2)
    (in-frigo vanille frigo1)
    (in-frigo menthe frigo1)
    (in-frigo cafe frigo1)
    (free-preparation preparation1)
    (free-preparation preparation2))
  (:goal (and
    (served2 client1 cornet chocolat vanille)
    (served3 client2 pot chocolat vanille fraise)
    (served2 client2 cornet menthe cafe)
    (served1 client2 pot cafe)
    (served3 client3 cornet fraise chocolat chocolat)))
)