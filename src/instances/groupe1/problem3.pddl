(define (problem glacier)
  (:domain glace)
  (:objects
    emplacement1 emplacement2 emplacement3 - emplacement
    frigo1 - frigo
    vanille chocolat fraise menthe cafe framboise poire coco citron mangue - parfum
    preparation1 preparation2 preparation3 - preparation
    cornet pot - contenant
    client1 client2 client3 client4 client5 client6 client7 client8 client9 client10 - client)
  (:init
    (in-emplacement chocolat emplacement1)
    (in-emplacement fraise emplacement2)
    (in-emplacement framboise emplacement3)
    (in-frigo vanille frigo1)
    (in-frigo menthe frigo1)
    (in-frigo cafe frigo1)
    (in-frigo poire frigo1)
    (in-frigo coco frigo1)
    (in-frigo citron frigo1)
    (in-frigo mangue frigo1)
    (free-preparation preparation1)
    (free-preparation preparation2)
    (free-preparation preparation3))
  (:goal (and
    (served2 client1 cornet mangue vanille)
    (served1 client1 cornet coco)
    (served3 client2 pot framboise vanille menthe)
    (served3 client2 pot menthe citron fraise)
    (served3 client3 cornet chocolat vanille chocolat)
    (served3 client3 cornet fraise vanille vanille)
    (served1 client4 pot menthe)
    (served2 client4 cornet fraise fraise)
    (served3 client5 cornet framboise coco cafe)
    (served3 client6 cornet vanille fraise poire)
    (served1 client6 pot vanille)
    (served2 client6 cornet poire cafe)
    (served3 client6 pot citron fraise chocolat)
    (served2 client7 pot mangue mangue)
    (served1 client8 cornet fraise)
    (served2 client8 cornet coco chocolat)
    (served3 client9 pot poire fraise poire)
    (served3 client10 pot cafe cafe cafe)))
)