package main

import "sync"
import "fmt"

type Process struct {
	id int
	clock int
	buffer chan *Message
	perceivedClocks map[int]int
	actions []*Action
}

func newProcess(id int) *Process{
	p := new(Process)
	p.id = id
	p.clock = 0
	p.buffer = make(chan *Message, 1)
	p.perceivedClocks = make(map[int]int)
	return p
}

func (from *Process) sendMessage(to *Process, payload string) {
	msg := new(Message)
	msg.from = from.id
	msg.clock = from.clock
	msg.payload = payload
	to.buffer <- msg
}

func (self *Process) processMessage() {
	msg := <- self.buffer
	self.perceivedClocks[msg.from] = msg.clock
	fmt.Printf("[%d] Processed message %s\n", self.id, msg.payload)
}

func (self *Process) addAction(action *Action) {
	self.actions = append(self.actions, action)
}

func (self *Process) performAction(a *Action, num int) {
	self.clock ++
	if(a.dependency != nil) {
		_, haskey := self.perceivedClocks[a.dependency.id]
		if(!haskey) {
			self.perceivedClocks[a.dependency.id] = 0
		}

		if(self.perceivedClocks[a.dependency.id] < a.dependency.clock) {
			for ;; {
				self.processMessage()
				if(self.perceivedClocks[a.dependency.id] >= a.dependency.clock) {
					break
				}
				
			}
		}
		fmt.Printf("[%d]%d can proceed past [%d]%d\n", self.id, num, a.dependency.id, a.dependency.clock)
		
	}

	if(a.action == SEND){
		self.sendMessage(a.to, a.content)
	} else if (a.action == RECEIVE) {
		//in a real situation, we would've stored the message we received to process it
		//in this simple example we needn't perform any action,
		//as no actions would manifest themselves to effect system state, only node state
	} else {
		//twiddle thumbs
	}

	fmt.Printf("[%d]%d Complete\n", self.id, num)
}

func (self *Process) run(wg *sync.WaitGroup) {
	go func() {
		for i := 0; i < len(self.actions); i++ {
			a := self.actions[i]
			self.performAction(a, i)
			
		}
		wg.Done()
	}()
}



type Message struct {
	from int
	clock int
	payload string
}

type Action struct {
	action ActionType
	to *Process
	content string
	dependency *Dependency
}

type ActionType int
const (
	SEND 	ActionType = 2
	RECEIVE ActionType = 1
	NONE	ActionType = 0
)

func newAction(t ActionType, to *Process, s string, d *Dependency) *Action {
	act := new(Action)
	act.action = t
	act.to = to
	act.content = s
	act.dependency = d
	return act
}

type Dependency struct {
	id int
	clock int
}

func newDependency(id int, clock int) *Dependency {
	d := new(Dependency)
	d.id = id
	d.clock = clock
	return d
}


func main() {

	wg := new(sync.WaitGroup)
	wg.Add(2)

	p0 := newProcess(0)
	p1 := newProcess(1)

	p0.addAction(newAction(NONE, p0, "start", nil))
	p0.addAction(newAction(NONE, p0, "twiddle", nil))
	p0.addAction(newAction(NONE, p0, "dee", nil))
	p0.addAction(newAction(NONE, p0, "start", nil))
	p0.addAction(newAction(SEND, p1, "hello", nil))

	p1.addAction(newAction(NONE, p1, "waitfor0", newDependency(0,2)))
	p1.addAction(newAction(NONE, p1, "happy", nil))

	p1.run(wg)
	p0.run(wg)

	wg.Wait()
}



