(define (problem glacier)
  (:domain glace)
  (:objects
    emplacement1 emplacement2 emplacement3 - emplacement
    frigo1 - frigo
    vanille chocolat fraise menthe cafe framboise - parfum
    preparation1 preparation2 - preparation
    cornet pot -contenant
    client1 client2 client3 client4 client5 - client)
  (:init
    (in-emplacement chocolat emplacement1)
    (in-emplacement fraise emplacement2)
    (in-emplacement framboise emplacement3)
    (in-frigo vanille frigo1)
    (in-frigo menthe frigo1)
    (in-frigo cafe frigo1)
    (free-preparation preparation1)
    (free-preparation preparation2))
  (:goal (and
    (served2 client1 cornet chocolat vanille)
    (served1 client1 cornet framboise)
    (served3 client2 pot chocolat vanille menthe)
    (served3 client2 pot menthe framboise fraise)
    (served3 client3 cornet chocolat vanille chocolat)
    (served3 client3 cornet fraise vanille vanille)
    (served1 client4 pot menthe)
    (served2 client4 cornet vanille fraise)
    (served3 client5 cornet cafe cafe cafe)))
)