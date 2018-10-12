package main

import "fmt"

func produce(id int, ch chan<- int, done chan bool) {
	for i := 0; i < 100000; i++ {
		ch <- id
	}
	done <- true
}

func consume(id int, ch <-chan int, done chan bool) {
	for i := 0; i < 100000; i++ {
		<- ch
	}
	done <- true
}

func main() {
	fmt.Printf("BEGIN\n")

	buffer := make(chan int)

	done := make(chan bool, 100)
	for i := 0; i < 50; i++ {
		go produce(i, buffer, done)
	}
	for i := 0; i < 50; i++ {
		go consume(i, buffer, done)
	}

	for i := 0; i < 100; i++ {
		<-done
	}

	fmt.Printf("FINISHED\n")
}