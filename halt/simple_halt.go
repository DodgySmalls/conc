package main

import "fmt"
import "time"


func operation(id int, ch chan<- int, cancel chan bool, done chan bool) {
	
	defer func() { done <- true }()
	
	for i := 0; i < 500; i++ {
		
		//once per second produce an item
		time.Sleep(time.Duration(1000)*time.Millisecond)
		ch <- i
		fmt.Printf("(%d) is operating\n", id)

		select {
			case <- cancel:
				return
			default:
				continue
		}
	}
}


func main() {
	fmt.Printf("BEGIN\n")

	buffer := make(chan int, 1000)
	done := make(chan bool)
	cancel := make(chan bool, 1)
	
	go operation(1, buffer, cancel, done)

	go 	func() {
			time.Sleep(time.Duration(5500)*time.Millisecond)
			cancel <- true
		}()

	<-done

	fmt.Printf("FINISHED\n")
}