(define (problem strips-gripper-x-5)
   (:domain gripper-strips)
   (:objects rooma roomb roomc roomd roome roomf roomg roomh roomi roomj roomk rooml roomm roomn ball8 ball7 ball6
             ball5 ball4 ball3 ball2 ball1 left right)
   (:init (room rooma)
          (room roomb)
	  (room roomc)
	  (room roomd)
	  (room roome)
	  (room roomf)
	  (room roomg)
	  (room roomh)
	  (room roomi)
	  (room roomj)
	  (room roomk)
	  (room rooml)
	  (room roomn)
          (ball ball8)
          (ball ball7)
          (ball ball6)
          (ball ball5)
          (ball ball4)
          (ball ball3)
          (ball ball2)
          (ball ball1)
          (at-robby rooma)
          (free left)
          (free right)
          (at ball8 rooma)
          (at ball7 rooma)
          (at ball6 rooma)
          (at ball5 rooma)
          (at ball4 rooma)
          (at ball3 rooma)
          (at ball2 rooma)
          (at ball1 rooma)
          (gripper left)
          (gripper right))
   (:goal (and               (at ball8 roomb)
               (at ball7 roomb)
               (at ball6 roomb)
               (at ball5 roomb)
               (at ball4 roomb)
               (at ball3 roomb)
               (at ball2 roomb)
               (at ball1 roomb))))