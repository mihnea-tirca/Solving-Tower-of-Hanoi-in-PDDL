import sys, os, argparse

def write_pddl_domain():
    f = open("hanoi-domain.pddl", "w")
    f.write("""(define (domain hanoi-domain)
    (:predicates 
        (on-tower ?d ?t) ; disk d is on tower t
        (on-disk ?d1 ?d2) ; disk d1 is on disk d2
        (disk ?d) ; d is a disk
        (tower ?t) ; t is a tower
        (empty ?t) ; tower t is empty
        (smaller ?d1 ?d2) ; disk d1 is smaller than disk d2
        (on-top ?d ?t) ; disk d is on top of tower t
    )
    
    ; move disk from disk to tower
    ; ?d is the disk to move
    ; ?df is the disk under disk ?d
    ; ?t1 is the tower ?d is on
    ; ?t2 is the tower to move ?d to
    (:action move-d-to-t
        :parameters (?d ?df ?t1 ?t2)
        :precondition (and 
            (disk ?d)
            (disk ?df)
            (tower ?t1)
            (tower ?t2)
            (empty ?t2)
            (on-disk ?d ?df)
            (on-top ?d ?t1)
            )
        :effect (and 
            (on-top ?df ?t1)
            (not (empty ?t2))
            (not (on-disk ?d ?df))
            (on-tower ?d ?t2)
            (on-top ?d ?t2)
            (not (on-top ?d ?t1))
            )
    )
    
    ; move disk from disk to disk
    ; ?d is the disk to move
    ; ?df is the disk under disk ?d
    ; ?dt is the disk to move ?d to
    ; ?t1 is the tower ?d is on
    ; ?t2 is the tower ?dt is on
    (:action move-d-to-d
        :parameters (?d ?df ?dt ?t1 ?t2)
        :precondition (and 
            (disk ?d)
            (disk ?df)
            (disk ?dt)
            (on-top ?d ?t1)
            (on-top ?dt ?t2)
            (tower ?t1)
            (tower ?t2)
            (on-disk ?d ?df)
            (smaller ?d ?dt)
            )
        :effect (and 
            (on-top ?df ?t1)
            (not (on-top ?d ?t1))
            (on-top ?d ?t2)
            (on-disk ?d ?dt)
            (not (on-top ?dt ?t2))
            (not (on-disk ?d ?df))
            )
    )

    ; move disk from tower to tower
    ; ?d is the disk to move
    ; ?t1 is the tower ?d is on
    ; ?t2 is the tower to move ?d to
    (:action move-t-to-t
        :parameters (?d ?t1 ?t2)
        :precondition (and 
            (disk ?d)
            (tower ?t1)
            (tower ?t2)
            (empty ?t2)
            (on-tower ?d ?t1)
            (on-top ?d ?t1)
            )
        :effect (and
            (empty ?t1)
            (not (empty ?t2))
            (on-tower ?d ?t2)
            (not (on-tower ?d ?t1))
            (on-top ?d ?t2)
            (not (on-top ?d ?t1))
            )
    )

    ; move disk from tower to disk
    ; ?d is the disk to move
    ; ?dt is the disk to move ?d to
    ; ?t1 is the tower ?d is on
    ; ?t2 is the tower ?dt is on
    (:action move-t-to-d
        :parameters (?d ?dt ?t1 ?t2)
        :precondition (and 
            (disk ?d)
            (disk ?dt)
            (tower ?t1)
            (tower ?t2)
            (on-top ?d ?t1)
            (on-tower ?d ?t1)
            (on-top ?dt ?t2)
            (smaller ?d ?dt)
            )
        :effect (and
            (not (on-top ?d ?t1))
            (on-top ?d ?t2)
            (not (on-tower ?d ?t1))
            (empty ?t1)
            (on-disk ?d ?dt)
            (not (on-top ?dt ?t2))
        )
    )
)
    """)
    f.close()

# This function writes the PDDL problem file
# The number of disks is passed as an argument
def write_pddl_problem(n):
    f = open("hanoi-problem.pddl", "w")

    f.write("""(define (problem hanoi-problem) (:domain hanoi-domain)
    (:objects
        tower1 tower2 tower3
        """)

    for i in range(1, n+1):
        f.write("disk" + str(i) + " ")

    f.write("""
    )
    
    (:init
        (tower tower1)
        (tower tower2)
        (tower tower3)
        """)


    for i in range(1, n+1):
        f.write("(disk disk" + str(i) + """)
        """)
        if i != n:
            f.write("(on-disk disk" + str(i) + " disk" + str(i+1) + """)
        """)
        else:
            f.write("(on-tower disk" + str(i) + """ tower1)
        """)
        for j in range(i+1, n+1):
            f.write("(smaller disk" + str(i) + " disk" + str(j) + """)
        """)

    f.write("""(not (empty tower1))
        (empty tower2)
        (empty tower3)
        (on-top disk1 tower1)
    )
        
    (:goal (and
        (empty tower1)
        (empty tower2)
        (on-top disk1 tower3)
        """)

    for i in range(1, n+1):
        if i != n:
            f.write("(on-disk disk" + str(i) + " disk" + str(i+1) + """)
        """)
        else:
            f.write("(on-tower disk" + str(i) + """ tower3)
        """)

    f.write(""")
    )
)""")

    f.close()

# This function executes the PDDL file
def executePDDLFiles():
    os.system("./fast-downward.py hanoi-domain.pddl hanoi-problem.pddl --heuristic \"h=ff()\" --search \"astar(h)\"")

def main():
    write_pddl_domain()
    parser = argparse.ArgumentParser()
    parser.add_argument("--disks", help="number of disks, default=3", type=int)
    args = parser.parse_args()
    if args.disks is not None:
        if args.disks > 0:
            write_pddl_problem(args.disks)
        else:
            print("Invalid number of disks")
            sys.exit(1)
    else:
        write_pddl_problem(3)

    executePDDLFiles()

if __name__ == "__main__":
    main()