package main

import (
	"fmt"
)

// fib returns a function that returns
// successive Fibonacci numbers.
func fib() func() int {
	a, b := 0, 1
	return func() int {
		a, b = b, a+b
		return a
	}
}

func factorial(x int64) int64 {
	if x == 0 {
		return 1
	}
	return x * factorial(x-1)
}

func main() {
	f := fib()
	var x string = "Hello"
	y := "World"
	fmt.Println(x + " " + y)
	fmt.Println(len(x), len(y), len(x)+len(y), len(x+y))
	fmt.Println(x[1])
	fmt.Println("Hello " + "World")
	fmt.Println(f(), f(), f(), f(), f())

	fmt.Print("Enter a number: ")
	var input int64
	fmt.Scanf("%d", &input)
	fmt.Println("The number was", input)

	fmt.Println(`
	struct
	qsdq
	s
	dq
	sd
	sdqqs
	`)

	var tab [10]int
	for i := 0; i < len(tab); i++ {
		tab[i] = i
		if i%2 == 0 {
			fmt.Println(i, "is even")
		} else {
			fmt.Println(i, "is odd")
		}
	}

	for i := 0; i < len(tab); i++ {
		fmt.Printf("\n%d", tab[i])
	}
	fmt.Println()

	tab2 := make([]int, 10)
	for i := 0; i < len(tab2); i++ {
		tab2[i] = tab[i]
	}
	fmt.Println(tab2)

	dict := make(map[string]int)
	dict["one"] = 1
	dict["two"] = 2
	fmt.Println(dict)

	fmt.Println("Factorial of", input, "is", factorial(input))

	defer func() {
		str := recover()
		fmt.Println(str)
	}()
	panic("PANIC")
}
