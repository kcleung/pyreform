( define ( domain transport ) ( :requirements :typing :action-costs ) ( :types num - object location target locatable - object vehicle package - locatable capacity-number - object ) ( :action drive :parameters ( ?v - vehicle ?l1 ?l2 - location ) :precondition ( and ( at ?v ?l1 ) ( road ?l1 ?l2 ) ) :effect ( and ( not ( at ?v ?l1 ) ) ( at ?v ?l2 ) ( increase ( total-cost ) ( road-length ?l1 ?l2 ) ) ) ) ( :action pick-up :parameters ( ?num3 ?num2 ?num1 ?num0 - num ?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity-number ) :precondition ( and ( at ?v ?l ) ( capacity-predecessor ?s1 ?s2 ) ( capacity ?v ?s2 ) ( more ?num2 ?num3 ) ( more ?num1 ?num0 ) ( count ?p ?v ?num2 ) ( count ?p ?l ?num0 ) ) :effect ( and ( not ( count ?p ?l ?num0 ) ) ( count ?p ?l ?num1 ) ( not ( count ?p ?v ?num2 ) ) ( count ?p ?v ?num3 ) ( capacity ?v ?s1 ) ( not ( capacity ?v ?s2 ) ) ( increase ( total-cost ) 1 ) ) ) ( :action drop :parameters ( ?num3 ?num2 ?num1 ?num0 - num ?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity-number ) :precondition ( and ( at ?v ?l ) ( capacity-predecessor ?s1 ?s2 ) ( capacity ?v ?s1 ) ( more ?num2 ?num3 ) ( more ?num1 ?num0 ) ( count ?p ?l ?num2 ) ( count ?p ?v ?num0 ) ) :effect ( and ( not ( count ?p ?v ?num0 ) ) ( count ?p ?v ?num1 ) ( not ( count ?p ?l ?num2 ) ) ( count ?p ?l ?num3 ) ( capacity ?v ?s2 ) ( not ( capacity ?v ?s1 ) ) ( increase ( total-cost ) 1 ) ) ) )