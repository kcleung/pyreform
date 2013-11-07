(define (domain no-mystery-strips)
   (:predicates
       (fuel-number ?x)
       (capacity-number ?x)
       (location ?x)
       (vehicle ?x)
       (package ?x)
       (connected ?n1 ?n2)
       (at ?v ?n)
       (in ?c ?v)
       (fuel ?n ?a)
       (capacity ?v ?s)
       (fuel-predecessor ?i ?j)
       (capacity-predecessor ?i ?j))

   (:action load
       :parameters (?c ?v ?n ?s1 ?s2)
       :precondition (and (package ?c)
			  (vehicle ?v)
			  (at ?c ?n)
                          (at ?v ?n)
			  (location ?n)
                          (capacity ?v ?s2)
			  (capacity-number ?s2)
			  (capacity-predecessor ?s1 ?s2)
                          (capacity-number ?s1))
       :effect (and (not (at ?c ?n))
                    (in ?c ?v)
                    (not (capacity ?v ?s2))
                    (capacity ?v ?s1)))
   (:action drive
       :parameters (?v ?n1 ?n2 ?l1 ?l2)
       :precondition (and (at ?v ?n1)
			  (location ?n1)
			  (vehicle ?v)
                          (connected ?n1 ?n2)
			  (location ?n2)
                          (fuel ?n1 ?l2)
                          (fuel-predecessor ?l1 ?l2))
       :effect (and (not (at ?v ?n1))
                    (at ?v ?n2)
                    (not (fuel ?n1 ?l2))
                    (fuel ?n1 ?l1)))
   (:action unload
       :parameters (?c ?v ?n ?s1 ?s2)
       :precondition (and (in ?c ?v)
			  (package ?c)
			  (vehicle ?v)
                          (at ?v ?n)
			  (location ?n)
			  (capacity ?v ?s1)
                          (capacity-predecessor ?s1 ?s2))
       :effect (and (not (in ?c ?v))
                    (at ?c ?n)
                    (not (capacity ?v ?s1))
                    (capacity ?v ?s2))))
