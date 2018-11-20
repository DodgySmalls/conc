# Byzantine Generals Oral-Message

This repository is a solution to the Byzantine Generals problem using oral message passing (as opposed to signatures).

Lamport et al. [1] state the problem from the perspective of a global recursive algorithm. However, in a real system the problem is inherently only useful when peers are communicating under the specified protocol. This makes it necessary to design a message passing system such that communications can occur between nodes with the knowledge of which message within the algorithm the payload represents. I've used a similar scheme to what is defined by Mark Nelson[2], where messages are 'tagged' with a path that denotes where the payload sits w.r.t. the complete algorithm.

This distinctly separates the algorithm proposed by Lamport et al. into two phases (defined in steps 2 and 3 of the OM(m) algorithm [1]), one of message passing, and one of inference about those messages. These distinctions are disguised by the format of the algorithms specification which is written from an omniscient (*i.e.* system) perspective, rather than a peer perspective.
* The Message-Passing stage is handled by `General.forwardMessage()` and `General.receiveMessage()`, where the OM(0) algorithm is expected to be handled manually (see `byzantine.py` `main`, or `Scenario.run()`
* The inference stage automatically occurs as results are populated to a `General`'s inference tree in `General.infer()`

### Testing Framework
`Scenario.py` defines a scenario class which runs all permutations of traitorous generals for the given number of traitors. Its output will not be useful if it is given an unsolvable scenario (*i.e.* too little recursion or too many traitors within the ranks). It outputs nothing when results are successful (consensus among generals is reached), but denotes errors when generals do not come to consensus in a solvable scenario.

If, rather than testing, you would like to observe operation, you can run the sample code in `byzantine.py main`

### Notable flaws:
* I have not provided a CLI or File interface for this library. The testing framework demonstrates how to use the library which is quite simple and conforms to the assignment spec, and since it runs every possible scenario under a given definition there should be no need to manually run scenarios.
* The algorithm is imperfect, and is currently experiencing some failures at larger scales (4/240 tests fail for a single general at 10 general 3 traitor scale). I believe this is not due to message passing, but to an error in the inference algorithm relating to resolving majorities from an inference tree.


### References

[1] [Lamport et al., The Byzantine Generals Problem](https://dl.acm.org/citation.cfm?id=357176)

[2] [Mark Nelson, The Byzantine Generals](http://www.cs.kzoo.edu/cs480/homework/MarkNelsonBG.pdf)
