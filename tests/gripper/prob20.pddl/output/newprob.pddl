( define ( problem strips-gripper-x-20 ) ( :domain gripper-strips ) ( :objects 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0 rooma roomb ball1 left right ) ( :init ( room rooma ) ( room roomb ) ( ball ball1 ) ( at-robby rooma ) ( free left ) ( free right ) ( gripper left ) ( gripper right ) ( count ball1 rooma 42 ) ( more 0 1 ) ( more 1 2 ) ( more 2 3 ) ( more 3 4 ) ( more 4 5 ) ( more 5 6 ) ( more 6 7 ) ( more 7 8 ) ( more 8 9 ) ( more 9 10 ) ( more 10 11 ) ( more 11 12 ) ( more 12 13 ) ( more 13 14 ) ( more 14 15 ) ( more 15 16 ) ( more 16 17 ) ( more 17 18 ) ( more 18 19 ) ( more 19 20 ) ( more 20 21 ) ( more 21 22 ) ( more 22 23 ) ( more 23 24 ) ( more 24 25 ) ( more 25 26 ) ( more 26 27 ) ( more 27 28 ) ( more 28 29 ) ( more 29 30 ) ( more 30 31 ) ( more 31 32 ) ( more 32 33 ) ( more 33 34 ) ( more 34 35 ) ( more 35 36 ) ( more 36 37 ) ( more 37 38 ) ( more 38 39 ) ( more 39 40 ) ( more 40 41 ) ( more 41 42 ) ( count ball1 roomb 0 ) ) ( :goal ( and ( count ball1 roomb 42 ) ) ) )