(define (problem hanoi-problem) (:domain hanoi-domain)
    (:objects
        tower1 tower2 tower3
        disk1 disk2 disk3 
    )
    
    (:init
        (tower tower1)
        (tower tower2)
        (tower tower3)
        (disk disk1)
        (on-disk disk1 disk2)
        (smaller disk1 disk2)
        (smaller disk1 disk3)
        (disk disk2)
        (on-disk disk2 disk3)
        (smaller disk2 disk3)
        (disk disk3)
        (on-tower disk3 tower1)
        (not (empty tower1))
        (empty tower2)
        (empty tower3)
        (on-top disk1 tower1)
    )
        
    (:goal (and
        (empty tower1)
        (empty tower2)
        (on-top disk1 tower3)
        (on-disk disk1 disk2)
        (on-disk disk2 disk3)
        (on-tower disk3 tower3)
        )
    )
)