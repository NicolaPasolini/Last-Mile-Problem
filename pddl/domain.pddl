(define (domain trasporto)
  (:requirements :strips :typing :fluents :negative-preconditions :action-costs)
  
  ;; Tipi
  (:types 
    location - object
  )
  
  ;; Predicati - vero/falso
  (:predicates
    (at ?loc - location)
    (connected ?from ?to - location)
    (delivered ?loc - location)
)
  
 ;; Funzioni
  (:functions
    (distance ?from ?to - location) - number
    (total-cost)- number
  )


  ;; Azioni
  (:action move
    :parameters (?from ?to - location )
    :precondition (and 
                    (at ?from )
                    (connected ?from ?to)
    )
    :effect (and
               (not (at ?from))
               (at ?to) 
               (increase (total-cost) (distance ?from ?to))
             )
  )
  
  (:action deliver
    :parameters (?loc - location)
    :precondition (and (at ?loc) (not (delivered ?loc)))
    :effect (and
              (delivered ?loc)
              (increase (total-cost) 1)
            )
  )
)
