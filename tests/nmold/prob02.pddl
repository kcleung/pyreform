(define
  (problem strips-mysty-x-2)
  (:domain no-mystery-strips)
  (:objects guendlingen denzlingen haltingen bahlingen loerrach
      merdingen sexau pferdetransport feuerwehr kuebelwagen
      motorroller kuechenmaschine fernseher feinkost-bratling
      kaesebaellchen faschiertes kiste-bier leipziger-allerlei
      wensleydale terrorist schlagobers gruenkohl radio tuete-pommes
      aschenbecher zamomin kaesefondue seitenbacher-muesli
      taschenrechner halbgefrorenes zuckerstange fuel-0 fuel-1 fuel-2
      fuel-3 fuel-4 capacity-0 capacity-1 capacity-2 capacity-3)
  (:init
    (at aschenbecher bahlingen)
    (at faschiertes guendlingen)
    (at feinkost-bratling guendlingen)
    (at fernseher guendlingen)
    (at feuerwehr bahlingen)
    (at gruenkohl haltingen)
    (at halbgefrorenes sexau)
    (at kaesebaellchen guendlingen)
    (at kaesefondue merdingen)
    (at kiste-bier denzlingen)
    (at kuebelwagen loerrach)
    (at kuechenmaschine guendlingen)
    (at leipziger-allerlei denzlingen)
    (at motorroller sexau)
    (at pferdetransport denzlingen)
    (at radio haltingen)
    (at schlagobers haltingen)
    (at seitenbacher-muesli sexau)
    (at taschenrechner sexau)
    (at terrorist haltingen)
    (at tuete-pommes bahlingen)
    (at wensleydale denzlingen)
    (at zamomin loerrach)
    (at zuckerstange sexau)
    (capacity feuerwehr capacity-2)
    (capacity kuebelwagen capacity-2)
    (capacity motorroller capacity-3)
    (capacity pferdetransport capacity-1)
    (capacity-number capacity-0)
    (capacity-number capacity-1)
    (capacity-number capacity-2)
    (capacity-number capacity-3)
    (capacity-predecessor capacity-0 capacity-1)
    (capacity-predecessor capacity-1 capacity-2)
    (capacity-predecessor capacity-2 capacity-3)
    (connected bahlingen haltingen)
    (connected bahlingen loerrach)
    (connected denzlingen guendlingen)
    (connected denzlingen loerrach)
    (connected denzlingen merdingen)
    (connected guendlingen denzlingen)
    (connected guendlingen haltingen)
    (connected guendlingen loerrach)
    (connected haltingen bahlingen)
    (connected haltingen guendlingen)
    (connected haltingen merdingen)
    (connected haltingen sexau)
    (connected loerrach bahlingen)
    (connected loerrach denzlingen)
    (connected loerrach guendlingen)
    (connected merdingen denzlingen)
    (connected merdingen haltingen)
    (connected merdingen sexau)
    (connected sexau haltingen)
    (connected sexau merdingen)
    (fuel bahlingen fuel-2)
    (fuel denzlingen fuel-3)
    (fuel guendlingen fuel-4)
    (fuel haltingen fuel-2)
    (fuel loerrach fuel-4)
    (fuel merdingen fuel-2)
    (fuel sexau fuel-4)
    (fuel-number fuel-0)
    (fuel-number fuel-1)
    (fuel-number fuel-2)
    (fuel-number fuel-3)
    (fuel-number fuel-4)
    (fuel-predecessor fuel-0 fuel-1)
    (fuel-predecessor fuel-1 fuel-2)
    (fuel-predecessor fuel-2 fuel-3)
    (fuel-predecessor fuel-3 fuel-4)
    (location bahlingen)
    (location denzlingen)
    (location guendlingen)
    (location haltingen)
    (location loerrach)
    (location merdingen)
    (location sexau)
    (package aschenbecher)
    (package faschiertes)
    (package feinkost-bratling)
    (package fernseher)
    (package gruenkohl)
    (package halbgefrorenes)
    (package kaesebaellchen)
    (package kaesefondue)
    (package kiste-bier)
    (package kuechenmaschine)
    (package leipziger-allerlei)
    (package radio)
    (package schlagobers)
    (package seitenbacher-muesli)
    (package taschenrechner)
    (package terrorist)
    (package tuete-pommes)
    (package wensleydale)
    (package zamomin)
    (package zuckerstange)
    (vehicle feuerwehr)
    (vehicle kuebelwagen)
    (vehicle motorroller)
    (vehicle pferdetransport))
  (:goal
    (and
      (at kaesefondue guendlingen)
      (at seitenbacher-muesli guendlingen))))
