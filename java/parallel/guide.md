# Parallel Programming

## Background

Parallel Programming consists of dividing a problem into subproblems, solving those subproblems simultaneously (in parallel, with each subproblem running in a separate thread), and then combining the results of the solutions to the subproblems.

## Overview

Theree are two main approaches to parallel programming:

- **Task Parallelism**: The program is divided into a set of tasks that are executed concurrently. Each task is a unit of work that performs a specific action and that operates on data stored in one or more data structures. The tasks communicate with each other by using synchronization mechanisms such as locks. The tasks can execute on a single processor or on multiple processors in a multiprocessor system.

- **Data Parallelism**: The program is divided into segments of code that operate on different parts of the same data structure. The compiler or run-time system distributes the code and data across multiple processors in a multiprocessor system, and the tasks operate on the data in parallel. The tasks can execute on a single processor or on multiple processors in a multiprocessor system.
