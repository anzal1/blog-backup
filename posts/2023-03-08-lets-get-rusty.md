---
title: "Let's Get Rusty"
slug: "lets-get-rusty"
date: "2023-03-08T15:48:36+00:00"
author: "Anzal Husain Abidi"
description: "What the heck is rust ? Rust is a programming language that was initially developed by Mozilla and released to the public in 2010. It was designed to be a fast, efficient, and safe alternative to other system programming languages like C++ and C. Rus..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1678290018820/c5bd3e21-0607-49bc-ba9e-f74c8e4ad86e.webp"
tags:
  - "Rust"
  - "Programming Blogs"
  - "coding"
  - "technology"
  - "Web Development"
canonical_url: "https://anzal.hashnode.dev/lets-get-rusty"
source: "hashnode"
---

![Let's Get Rusty](https://cdn.hashnode.com/res/hashnode/image/upload/v1678290018820/c5bd3e21-0607-49bc-ba9e-f74c8e4ad86e.webp)

### What the heck is rust ?

Rust is a programming language that was initially developed by Mozilla and released to the public in 2010. It was designed to be a fast, efficient, and safe alternative to other system programming languages like C++ and C. Rust's popularity has been increasing rapidly in recent years, and for good reason. In this blog, we'll dive deep into Rust and explore its advantages over other languages.

1. Memory safety and thread safety One of the most significant advantages of Rust is its strong emphasis on memory safety and thread safety. Rust's ownership and borrowing system ensures that memory is managed safely and efficiently, which can help prevent common bugs like null pointers, buffer overflows, and use-after-free errors. The language's type system also helps ensure that code is thread-safe, meaning that it can be run concurrently without data races.
2. High performance Rust is designed to be a high-performance language, which makes it an excellent choice for system-level programming. Its syntax and semantics are designed to optimize code, and it provides direct access to hardware resources, making it faster than many other languages. Rust is also designed to work well with multi-core processors, making it ideal for high-performance computing and parallel processing.
3. Easy to learn Despite its advanced features, Rust is surprisingly easy to learn. Its syntax is clean and easy to understand, and its compiler provides helpful error messages that can make it easier to fix issues in code. Rust also has an active community of developers who are eager to help new users, making it a welcoming language for beginners.
4. Cross-platform support Rust is a cross-platform language, meaning that it can be used to develop software for a wide range of platforms, including Windows, macOS, Linux, and even embedded systems. This makes it an ideal choice for developers who need to build applications that can run on multiple platforms.
5. Large and growing community Rust has a large and growing community of developers who are working on a wide range of projects. This community provides a wealth of resources, including libraries, frameworks, and tools, making it easier for developers to get started with Rust and build complex applications.

In conclusion, Rust is a powerful programming language that offers a range of benefits over other languages. Its emphasis on memory and thread safety, high performance, ease of use, cross-platform support, and growing community make it an excellent choice for system-level programming, high-performance computing, and more. If you're looking for a modern, efficient, and safe programming language, Rust is definitely worth considering.

![](https://doc.rust-lang.org/book/img/ferris/does_not_compile.svg)

### Too much theory show me some code :

1. Memory safety and thread safety Rust's ownership and borrowing system allows for safe memory management, which can prevent common bugs like null pointers, buffer overflows, and use-after-free errors. Here's an example of how Rust's ownership system works:

```rust
fn main() {
    let mut s = String::from("hello");

    let len = calculate_length(&s);

    println!("The length of '{}' is {}.", s, len);

    change(&mut s);

    let len = calculate_length(&s);

    println!("The length of '{}' is {}.", s, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

In this example, we create a string `s` and pass a reference to it to the `calculate_length` function, which returns the length of the string. We then pass a mutable reference to the `change` function, which appends `", world"` to the string. Finally, we call `calculate_length` again to get the new length of the string. Because Rust's ownership system ensures that there is only one mutable reference to the string at a time, this code is safe and will not cause any memory or thread-related issues.

1. High performance Rust is designed to be a high-performance language, which makes it an excellent choice for system-level programming. Here's an example of how Rust's performance compares to that of Python:

```rust
rust:
fn main() {
    let mut sum = 0;

    for i in 0..1000000000 {
        sum += i;
    }

    println!("{}", sum);
}
```

```python
python
sum = 0
for i in range(1000000000):
    sum += i
print(sum)
```

In this example, we calculate the sum of the first billion integers in both Rust and Python. When we run the Rust code, it completes in just a few seconds, whereas the Python code takes several minutes to complete. This illustrates Rust's performance advantage over interpreted languages like Python.

1. Easy to learn Despite its advanced features, Rust is surprisingly easy to learn. Here's an example of how Rust's syntax is clean and easy to understand:

```rust
fn main() {
    let x = 5;
    let y = {
        let x = 3;
        x + 1
    };
    println!("The value of x is {}.", x);
    println!("The value of y is {}.", y);
}
```

In this example, we create a variable `x` and set it to `5`. We then create another variable `y` and set it to the result of a block of code that adds 1 to `x`. Because Rust uses a block expression for the calculation of `y`, we don't need to use the `return` keyword, which makes the code more concise and easier to read.

1. Cross-platform support Rust is a cross-platform language, meaning that it can be used to develop software for a wide range of platforms, including Windows, macOS, Linux, and even embedded systems. Here's an example of how Rust can be used to develop an application that runs on multiple platforms:

```rust
fn main() {
    println!("Hello, world!");
}
```

This simple "Hello, world!" program can be compiled and run on any platform that supports Rust, without any modifications to the code. This illustrates Rust's cross-platform compatibility, which can save developers time and effort when developing software for multiple platforms.

1. Large and growing community:

```rust
use std::thread;

fn main() {
    let mut handles = vec![];

    for i in 0..10 {
        handles.push(thread::spawn(move || {
            println!("Thread {} started.", i);
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
```

In this example, we create 10 threads that print a message to the console. We use Rust's standard library to create and manage the threads, which makes the code more concise and easier to understand. If we have any questions or issues with this code, we can turn to Rust's community for help, either through forums, chat rooms, or online resources.

In comparison to other languages like C++, Rust provides advantages in terms of safety, performance, ease of learning, cross-platform support, and community. These features make Rust an excellent choice for system-level programming, game development, web development, and more.

### Rust as a server side language , are you serious ?

There are several reasons why Rust is a good choice for server-side programming:

1. Memory safety: Rust's ownership and borrowing system prevents common memory errors like null pointers, buffer overflows, and use-after-free errors, which can lead to security vulnerabilities and crashes. This makes Rust a safe choice for server-side programming, where security and reliability are critical.
2. High performance: Rust is designed to be a high-performance language, which makes it a good choice for server-side programming where performance is important. Rust's performance is comparable to that of C and C++, but with safer memory management.
3. Asynchronous programming: Rust has excellent support for asynchronous programming, which is essential for server-side programming. Rust's async/await syntax and futures library make it easy to write efficient and scalable asynchronous code.
4. Web frameworks: Rust has several excellent web frameworks, including Actix, Rocket, and Warp. These frameworks make it easy to write efficient and secure web applications in Rust, with features like middleware, routing, and authentication.
5. Cross-platform support: Rust is a cross-platform language, meaning that it can be used to develop server-side applications for a wide range of platforms, including Windows, Linux, and macOS.
6. Community: Rust has a large and growing community of developers.
