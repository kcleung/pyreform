( define ( problem transport-l4-t1-p3---int100n150-m25---int100c110---s1---e0 ) ( :domain transport-strips ) ( :objects 3 2 1 0 - num l0 l1 l2 l3 - location t0 - truck p0 p2 - package level0 level1 level2 level3 level4 level5 level6 level7 level8 level9 level10 level11 level12 level13 level14 level15 level16 level17 level18 level19 level20 level21 level22 level23 level24 level25 level26 - fuellevel ) ( :init ( sum level0 level0 level0 ) ( sum level0 level1 level1 ) ( sum level0 level2 level2 ) ( sum level0 level3 level3 ) ( sum level0 level4 level4 ) ( sum level0 level5 level5 ) ( sum level0 level6 level6 ) ( sum level0 level7 level7 ) ( sum level0 level8 level8 ) ( sum level0 level9 level9 ) ( sum level0 level10 level10 ) ( sum level0 level11 level11 ) ( sum level0 level12 level12 ) ( sum level0 level13 level13 ) ( sum level0 level14 level14 ) ( sum level0 level15 level15 ) ( sum level0 level16 level16 ) ( sum level0 level17 level17 ) ( sum level0 level18 level18 ) ( sum level0 level19 level19 ) ( sum level0 level20 level20 ) ( sum level0 level21 level21 ) ( sum level0 level22 level22 ) ( sum level0 level23 level23 ) ( sum level0 level24 level24 ) ( sum level0 level25 level25 ) ( sum level0 level26 level26 ) ( sum level1 level0 level1 ) ( sum level1 level1 level2 ) ( sum level1 level2 level3 ) ( sum level1 level3 level4 ) ( sum level1 level4 level5 ) ( sum level1 level5 level6 ) ( sum level1 level6 level7 ) ( sum level1 level7 level8 ) ( sum level1 level8 level9 ) ( sum level1 level9 level10 ) ( sum level1 level10 level11 ) ( sum level1 level11 level12 ) ( sum level1 level12 level13 ) ( sum level1 level13 level14 ) ( sum level1 level14 level15 ) ( sum level1 level15 level16 ) ( sum level1 level16 level17 ) ( sum level1 level17 level18 ) ( sum level1 level18 level19 ) ( sum level1 level19 level20 ) ( sum level1 level20 level21 ) ( sum level1 level21 level22 ) ( sum level1 level22 level23 ) ( sum level1 level23 level24 ) ( sum level1 level24 level25 ) ( sum level1 level25 level26 ) ( sum level2 level0 level2 ) ( sum level2 level1 level3 ) ( sum level2 level2 level4 ) ( sum level2 level3 level5 ) ( sum level2 level4 level6 ) ( sum level2 level5 level7 ) ( sum level2 level6 level8 ) ( sum level2 level7 level9 ) ( sum level2 level8 level10 ) ( sum level2 level9 level11 ) ( sum level2 level10 level12 ) ( sum level2 level11 level13 ) ( sum level2 level12 level14 ) ( sum level2 level13 level15 ) ( sum level2 level14 level16 ) ( sum level2 level15 level17 ) ( sum level2 level16 level18 ) ( sum level2 level17 level19 ) ( sum level2 level18 level20 ) ( sum level2 level19 level21 ) ( sum level2 level20 level22 ) ( sum level2 level21 level23 ) ( sum level2 level22 level24 ) ( sum level2 level23 level25 ) ( sum level2 level24 level26 ) ( sum level3 level0 level3 ) ( sum level3 level1 level4 ) ( sum level3 level2 level5 ) ( sum level3 level3 level6 ) ( sum level3 level4 level7 ) ( sum level3 level5 level8 ) ( sum level3 level6 level9 ) ( sum level3 level7 level10 ) ( sum level3 level8 level11 ) ( sum level3 level9 level12 ) ( sum level3 level10 level13 ) ( sum level3 level11 level14 ) ( sum level3 level12 level15 ) ( sum level3 level13 level16 ) ( sum level3 level14 level17 ) ( sum level3 level15 level18 ) ( sum level3 level16 level19 ) ( sum level3 level17 level20 ) ( sum level3 level18 level21 ) ( sum level3 level19 level22 ) ( sum level3 level20 level23 ) ( sum level3 level21 level24 ) ( sum level3 level22 level25 ) ( sum level3 level23 level26 ) ( sum level4 level0 level4 ) ( sum level4 level1 level5 ) ( sum level4 level2 level6 ) ( sum level4 level3 level7 ) ( sum level4 level4 level8 ) ( sum level4 level5 level9 ) ( sum level4 level6 level10 ) ( sum level4 level7 level11 ) ( sum level4 level8 level12 ) ( sum level4 level9 level13 ) ( sum level4 level10 level14 ) ( sum level4 level11 level15 ) ( sum level4 level12 level16 ) ( sum level4 level13 level17 ) ( sum level4 level14 level18 ) ( sum level4 level15 level19 ) ( sum level4 level16 level20 ) ( sum level4 level17 level21 ) ( sum level4 level18 level22 ) ( sum level4 level19 level23 ) ( sum level4 level20 level24 ) ( sum level4 level21 level25 ) ( sum level4 level22 level26 ) ( sum level5 level0 level5 ) ( sum level5 level1 level6 ) ( sum level5 level2 level7 ) ( sum level5 level3 level8 ) ( sum level5 level4 level9 ) ( sum level5 level5 level10 ) ( sum level5 level6 level11 ) ( sum level5 level7 level12 ) ( sum level5 level8 level13 ) ( sum level5 level9 level14 ) ( sum level5 level10 level15 ) ( sum level5 level11 level16 ) ( sum level5 level12 level17 ) ( sum level5 level13 level18 ) ( sum level5 level14 level19 ) ( sum level5 level15 level20 ) ( sum level5 level16 level21 ) ( sum level5 level17 level22 ) ( sum level5 level18 level23 ) ( sum level5 level19 level24 ) ( sum level5 level20 level25 ) ( sum level5 level21 level26 ) ( sum level6 level0 level6 ) ( sum level6 level1 level7 ) ( sum level6 level2 level8 ) ( sum level6 level3 level9 ) ( sum level6 level4 level10 ) ( sum level6 level5 level11 ) ( sum level6 level6 level12 ) ( sum level6 level7 level13 ) ( sum level6 level8 level14 ) ( sum level6 level9 level15 ) ( sum level6 level10 level16 ) ( sum level6 level11 level17 ) ( sum level6 level12 level18 ) ( sum level6 level13 level19 ) ( sum level6 level14 level20 ) ( sum level6 level15 level21 ) ( sum level6 level16 level22 ) ( sum level6 level17 level23 ) ( sum level6 level18 level24 ) ( sum level6 level19 level25 ) ( sum level6 level20 level26 ) ( sum level7 level0 level7 ) ( sum level7 level1 level8 ) ( sum level7 level2 level9 ) ( sum level7 level3 level10 ) ( sum level7 level4 level11 ) ( sum level7 level5 level12 ) ( sum level7 level6 level13 ) ( sum level7 level7 level14 ) ( sum level7 level8 level15 ) ( sum level7 level9 level16 ) ( sum level7 level10 level17 ) ( sum level7 level11 level18 ) ( sum level7 level12 level19 ) ( sum level7 level13 level20 ) ( sum level7 level14 level21 ) ( sum level7 level15 level22 ) ( sum level7 level16 level23 ) ( sum level7 level17 level24 ) ( sum level7 level18 level25 ) ( sum level7 level19 level26 ) ( sum level8 level0 level8 ) ( sum level8 level1 level9 ) ( sum level8 level2 level10 ) ( sum level8 level3 level11 ) ( sum level8 level4 level12 ) ( sum level8 level5 level13 ) ( sum level8 level6 level14 ) ( sum level8 level7 level15 ) ( sum level8 level8 level16 ) ( sum level8 level9 level17 ) ( sum level8 level10 level18 ) ( sum level8 level11 level19 ) ( sum level8 level12 level20 ) ( sum level8 level13 level21 ) ( sum level8 level14 level22 ) ( sum level8 level15 level23 ) ( sum level8 level16 level24 ) ( sum level8 level17 level25 ) ( sum level8 level18 level26 ) ( sum level9 level0 level9 ) ( sum level9 level1 level10 ) ( sum level9 level2 level11 ) ( sum level9 level3 level12 ) ( sum level9 level4 level13 ) ( sum level9 level5 level14 ) ( sum level9 level6 level15 ) ( sum level9 level7 level16 ) ( sum level9 level8 level17 ) ( sum level9 level9 level18 ) ( sum level9 level10 level19 ) ( sum level9 level11 level20 ) ( sum level9 level12 level21 ) ( sum level9 level13 level22 ) ( sum level9 level14 level23 ) ( sum level9 level15 level24 ) ( sum level9 level16 level25 ) ( sum level9 level17 level26 ) ( sum level10 level0 level10 ) ( sum level10 level1 level11 ) ( sum level10 level2 level12 ) ( sum level10 level3 level13 ) ( sum level10 level4 level14 ) ( sum level10 level5 level15 ) ( sum level10 level6 level16 ) ( sum level10 level7 level17 ) ( sum level10 level8 level18 ) ( sum level10 level9 level19 ) ( sum level10 level10 level20 ) ( sum level10 level11 level21 ) ( sum level10 level12 level22 ) ( sum level10 level13 level23 ) ( sum level10 level14 level24 ) ( sum level10 level15 level25 ) ( sum level10 level16 level26 ) ( sum level11 level0 level11 ) ( sum level11 level1 level12 ) ( sum level11 level2 level13 ) ( sum level11 level3 level14 ) ( sum level11 level4 level15 ) ( sum level11 level5 level16 ) ( sum level11 level6 level17 ) ( sum level11 level7 level18 ) ( sum level11 level8 level19 ) ( sum level11 level9 level20 ) ( sum level11 level10 level21 ) ( sum level11 level11 level22 ) ( sum level11 level12 level23 ) ( sum level11 level13 level24 ) ( sum level11 level14 level25 ) ( sum level11 level15 level26 ) ( sum level12 level0 level12 ) ( sum level12 level1 level13 ) ( sum level12 level2 level14 ) ( sum level12 level3 level15 ) ( sum level12 level4 level16 ) ( sum level12 level5 level17 ) ( sum level12 level6 level18 ) ( sum level12 level7 level19 ) ( sum level12 level8 level20 ) ( sum level12 level9 level21 ) ( sum level12 level10 level22 ) ( sum level12 level11 level23 ) ( sum level12 level12 level24 ) ( sum level12 level13 level25 ) ( sum level12 level14 level26 ) ( sum level13 level0 level13 ) ( sum level13 level1 level14 ) ( sum level13 level2 level15 ) ( sum level13 level3 level16 ) ( sum level13 level4 level17 ) ( sum level13 level5 level18 ) ( sum level13 level6 level19 ) ( sum level13 level7 level20 ) ( sum level13 level8 level21 ) ( sum level13 level9 level22 ) ( sum level13 level10 level23 ) ( sum level13 level11 level24 ) ( sum level13 level12 level25 ) ( sum level13 level13 level26 ) ( sum level14 level0 level14 ) ( sum level14 level1 level15 ) ( sum level14 level2 level16 ) ( sum level14 level3 level17 ) ( sum level14 level4 level18 ) ( sum level14 level5 level19 ) ( sum level14 level6 level20 ) ( sum level14 level7 level21 ) ( sum level14 level8 level22 ) ( sum level14 level9 level23 ) ( sum level14 level10 level24 ) ( sum level14 level11 level25 ) ( sum level14 level12 level26 ) ( sum level15 level0 level15 ) ( sum level15 level1 level16 ) ( sum level15 level2 level17 ) ( sum level15 level3 level18 ) ( sum level15 level4 level19 ) ( sum level15 level5 level20 ) ( sum level15 level6 level21 ) ( sum level15 level7 level22 ) ( sum level15 level8 level23 ) ( sum level15 level9 level24 ) ( sum level15 level10 level25 ) ( sum level15 level11 level26 ) ( sum level16 level0 level16 ) ( sum level16 level1 level17 ) ( sum level16 level2 level18 ) ( sum level16 level3 level19 ) ( sum level16 level4 level20 ) ( sum level16 level5 level21 ) ( sum level16 level6 level22 ) ( sum level16 level7 level23 ) ( sum level16 level8 level24 ) ( sum level16 level9 level25 ) ( sum level16 level10 level26 ) ( sum level17 level0 level17 ) ( sum level17 level1 level18 ) ( sum level17 level2 level19 ) ( sum level17 level3 level20 ) ( sum level17 level4 level21 ) ( sum level17 level5 level22 ) ( sum level17 level6 level23 ) ( sum level17 level7 level24 ) ( sum level17 level8 level25 ) ( sum level17 level9 level26 ) ( sum level18 level0 level18 ) ( sum level18 level1 level19 ) ( sum level18 level2 level20 ) ( sum level18 level3 level21 ) ( sum level18 level4 level22 ) ( sum level18 level5 level23 ) ( sum level18 level6 level24 ) ( sum level18 level7 level25 ) ( sum level18 level8 level26 ) ( sum level19 level0 level19 ) ( sum level19 level1 level20 ) ( sum level19 level2 level21 ) ( sum level19 level3 level22 ) ( sum level19 level4 level23 ) ( sum level19 level5 level24 ) ( sum level19 level6 level25 ) ( sum level19 level7 level26 ) ( sum level20 level0 level20 ) ( sum level20 level1 level21 ) ( sum level20 level2 level22 ) ( sum level20 level3 level23 ) ( sum level20 level4 level24 ) ( sum level20 level5 level25 ) ( sum level20 level6 level26 ) ( sum level21 level0 level21 ) ( sum level21 level1 level22 ) ( sum level21 level2 level23 ) ( sum level21 level3 level24 ) ( sum level21 level4 level25 ) ( sum level21 level5 level26 ) ( sum level22 level0 level22 ) ( sum level22 level1 level23 ) ( sum level22 level2 level24 ) ( sum level22 level3 level25 ) ( sum level22 level4 level26 ) ( sum level23 level0 level23 ) ( sum level23 level1 level24 ) ( sum level23 level2 level25 ) ( sum level23 level3 level26 ) ( sum level24 level0 level24 ) ( sum level24 level1 level25 ) ( sum level24 level2 level26 ) ( sum level25 level0 level25 ) ( sum level25 level1 level26 ) ( sum level26 level0 level26 ) ( connected l0 l1 ) ( fuelcost level13 l0 l1 ) ( connected l0 l2 ) ( fuelcost level2 l0 l2 ) ( connected l0 l3 ) ( fuelcost level18 l0 l3 ) ( connected l1 l0 ) ( fuelcost level13 l1 l0 ) ( connected l1 l2 ) ( fuelcost level3 l1 l2 ) ( connected l1 l3 ) ( fuelcost level11 l1 l3 ) ( connected l2 l0 ) ( fuelcost level2 l2 l0 ) ( connected l2 l1 ) ( fuelcost level3 l2 l1 ) ( connected l2 l3 ) ( fuelcost level6 l2 l3 ) ( connected l3 l0 ) ( fuelcost level18 l3 l0 ) ( connected l3 l1 ) ( fuelcost level11 l3 l1 ) ( connected l3 l2 ) ( fuelcost level6 l3 l2 ) ( at t0 l2 ) ( fuel t0 level26 ) ( = ( total-cost ) 0 ) ( count p2 l1 1 ) ( count p2 l3 1 ) ( more 0 1 ) ( more 1 2 ) ( more 2 3 ) ( count p2 l0 0 ) ( count p2 l2 0 ) ( count p0 l0 1 ) ( count p0 l1 0 ) ( count p0 l2 0 ) ( count p0 l3 0 ) ( count p2 t0 0 ) ( count p0 t0 0 ) ) ( :goal ( and ( count p2 l0 2 ) ( count p0 l1 1 ) ) ) )