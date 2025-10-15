How to run

Clone the repository:

git clone <your_github_repo_url>
cd <repository_folder>


Make sure Python 3 is installed:

python --version


Run the program:

python scheduler.py


Example usage in Python:

from scheduler import Scheduler

s = Scheduler()
s.create_queue("Mobile", 2)
s.create_queue("WalkIns", 2)

s.enqueue("Mobile", "latte")
s.enqueue("WalkIns", "americano")

logs = s.run(quantum=1, steps=2)
print("\n".join(logs))

How to run tests locally

Install pytest if not already installed:

pip install pytest


Run all tests:

python -m pytest -q


. indicates a passed test

F indicates a failed test

Complexity Notes
Queue Design

Each queue is implemented using a Python list for storing tasks.

Auto-incremented task IDs ensure unique identification per queue.

Round-robin scheduling iterates over queues in order.

Skip functionality allows a queue to be skipped for one turn without losing tasks.

Time Complexity

Enqueue: O(1) amortized (append to list)

Dequeue / Run: O(#turns + total_minutes_worked), iterates only over the number of steps specified

Mark Skip: O(1), implemented with a set for quick lookup

Space Complexity

O(N) for storing N tasks across all queues

Additional space for task metadata, logs, and skip tracking