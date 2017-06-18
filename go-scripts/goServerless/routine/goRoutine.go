package main

import (
	"fmt"
	"time"
)

func f(n int) {
	for i := 0; i < n; i++ {
		fmt.Println(n, ":", i)
		//amt := time.Duration(rand.Intn(250))
		//time.Sleep(time.Millisecond * amt)
	}
}

func pinger(c chan string) {
	for i := 0; ; i++ {
		c <- "."
	}
}
func printer(c chan string) {
	for {
		msg := <-c
		fmt.Print(msg)
		time.Sleep(time.Second * 1)
	}
}

//======================
func main() {
	var input int

	var c chan string = make(chan string)
	go pinger(c)
	go printer(c)

	fmt.Scanln(&input)

	go f(input - 5)
	for i := 0; i < input; i++ {
		fmt.Println(input, ":", i)
	}

}
