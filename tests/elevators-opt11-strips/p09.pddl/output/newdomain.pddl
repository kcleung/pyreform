( define ( domain elevators-sequencedstrips ) ( :requirements :typing :action-costs ) ( :types num - object elevator - object slow-elevator fast-elevator - elevator passenger - object count - object ) ( :action move-up-slow :parameters ( ?lift - slow-elevator ?f1 - count ?f2 - count ) :precondition ( and ( lift-at ?lift ?f1 ) ( above ?f1 ?f2 ) ( reachable-floor ?lift ?f2 ) ) :effect ( and ( lift-at ?lift ?f2 ) ( not ( lift-at ?lift ?f1 ) ) ( increase ( total-cost ) ( travel-slow ?f1 ?f2 ) ) ) ) ( :action move-down-slow :parameters ( ?lift - slow-elevator ?f1 - count ?f2 - count ) :precondition ( and ( lift-at ?lift ?f1 ) ( above ?f2 ?f1 ) ( reachable-floor ?lift ?f2 ) ) :effect ( and ( lift-at ?lift ?f2 ) ( not ( lift-at ?lift ?f1 ) ) ( increase ( total-cost ) ( travel-slow ?f2 ?f1 ) ) ) ) ( :action move-up-fast :parameters ( ?lift - fast-elevator ?f1 - count ?f2 - count ) :precondition ( and ( lift-at ?lift ?f1 ) ( above ?f1 ?f2 ) ( reachable-floor ?lift ?f2 ) ) :effect ( and ( lift-at ?lift ?f2 ) ( not ( lift-at ?lift ?f1 ) ) ( increase ( total-cost ) ( travel-fast ?f1 ?f2 ) ) ) ) ( :action move-down-fast :parameters ( ?lift - fast-elevator ?f1 - count ?f2 - count ) :precondition ( and ( lift-at ?lift ?f1 ) ( above ?f2 ?f1 ) ( reachable-floor ?lift ?f2 ) ) :effect ( and ( lift-at ?lift ?f2 ) ( not ( lift-at ?lift ?f1 ) ) ( increase ( total-cost ) ( travel-fast ?f2 ?f1 ) ) ) ) ( :action board :parameters ( ?num1 ?num0 - num ?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count ) :precondition ( and ( lift-at ?lift ?f ) ( passengers ?lift ?n1 ) ( next ?n1 ?n2 ) ( can-hold ?lift ?n2 ) ( more ?num1 ?num0 ) ( count ?p ?f ?num0 ) ) :effect ( and ( not ( count ?p ?f ?num0 ) ) ( count ?p ?f ?num1 ) ( boarded ?p ?lift ) ( not ( passengers ?lift ?n1 ) ) ( passengers ?lift ?n2 ) ) ) ( :action leave :parameters ( ?num1 ?num0 - num ?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count ) :precondition ( and ( lift-at ?lift ?f ) ( boarded ?p ?lift ) ( passengers ?lift ?n1 ) ( next ?n2 ?n1 ) ( more ?num0 ?num1 ) ( count ?p ?f ?num0 ) ) :effect ( and ( not ( count ?p ?f ?num0 ) ) ( count ?p ?f ?num1 ) ( not ( boarded ?p ?lift ) ) ( not ( passengers ?lift ?n1 ) ) ( passengers ?lift ?n2 ) ) ) )