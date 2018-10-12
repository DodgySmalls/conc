package main

import "fmt"
import "time"

//UnboundedFifoMutex
type FifoMutex struct {
	queue chan chan bool
}

func newFifoMutex() *FifoMutex {
	b := new(FifoMutex)
	b.queue = make(chan chan bool)	//unbuffered channels are FIFO according to spec: https://golang.org/ref/spec#Channel_types
	b.unlock()						//	see also test provided in producerconsumer repo
	return b
}

func (b FifoMutex) lock() {
	ch := make(chan bool, 1)
	b.queue <- ch
	<- ch
}

func (b FifoMutex) unlock() {
	go func() {
		next := <- b.queue 
		next <- true
	}()
}

func exampleOp(id int, mutex *FifoMutex, done chan bool ) {
	mutex.lock()
	fmt.Printf("(%d) Entering critical\n", id)
	time.Sleep(time.Duration(100)*time.Millisecond)
	fmt.Printf("(%d) Exiting critical\n", id)
	mutex.unlock()
	done <- true
}

func main() {
	fmt.Printf("BEGIN\n")

	var b *FifoMutex = newFifoMutex()

	done := make(chan bool, 50)
	for i := 0; i < 50; i++ {
		go exampleOp(i, b, done)
	}

	for i := 0; i < 50; i++ {
		<-done
	}

	fmt.Printf("FINISHED\n")
}