( define ( problem strips-gripper-x-10 ) ( :domain gripper-strips ) ( :objects 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0 rooma roomb ball1 left right ) ( :init ( room rooma ) ( room roomb ) ( ball ball1 ) ( at-robby rooma ) ( free left ) ( free right ) ( gripper left ) ( gripper right ) ( count ball1 rooma 22 ) ( more 0 1 ) ( more 1 2 ) ( more 2 3 ) ( more 3 4 ) ( more 4 5 ) ( more 5 6 ) ( more 6 7 ) ( more 7 8 ) ( more 8 9 ) ( more 9 10 ) ( more 10 11 ) ( more 11 12 ) ( more 12 13 ) ( more 13 14 ) ( more 14 15 ) ( more 15 16 ) ( more 16 17 ) ( more 17 18 ) ( more 18 19 ) ( more 19 20 ) ( more 20 21 ) ( more 21 22 ) ( count ball1 roomb 0 ) ) ( :goal ( and ( count ball1 roomb 22 ) ) ) )