# Vector Clocks

This simple vector clock implementation is written in Golang. It is comprised of the following primary components:

* `Process`, structs acting as objects which represent a line of computation
     * Processes communicate with each other by passing `Message`s
* `Message`, structs acting as objects which represent a message passed between processes. Messages contain content and metadata to allow processes to update their view of the (distributed) system state.
* `Action`, structs acting as objects which represent steps within a line of computation. Actions define what will be done by the process (*e.g.* `SEND`, or `RECEIVE`) as well as the `Dependency`s of that action.
* `Dependency`, structs acting as objects which represent an inter-process dependency. Processes block waiting to progress until they perceive the dependency is satisfied.

The application does not provide a testing framework (as most of that work would be in defining specification of processes, their actions, and dependencies) but does demonstrate its functionality in a somewhat simplistic manner in `main()`

Notably, this implementation is concurrent, but lacks other important capabilities which would allow it to be applicable in many useful (distributed) cases. Primarily, it does not provide any active method for processes to determine the state of peers, which would be critical for fault-tolerance in a system that can drop messages.
