# Bài 11: Concurrency & Parallelism

## 🎯 Mục tiêu
- Threading, processes, async
- Locks, deadlocks, race conditions
- Concurrent data structures
- Python GIL & workarounds

---

## 1. Concurrency vs Parallelism

```
Concurrency: multiple tasks progress (interleaved on 1 core)
  → I/O-bound tasks: web requests, file I/O, DB queries
  → Tools: asyncio, threading

Parallelism: multiple tasks run simultaneously (multi-core)
  → CPU-bound tasks: computation, data processing
  → Tools: multiprocessing, ProcessPoolExecutor
```

---

## 2. Python Threading

```python
import threading

# Race condition example
counter = 0
def increment():
    global counter
    for _ in range(100000):
        counter += 1  # NOT atomic! Read-modify-write

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # Expected 200000, actual < 200000!

# Fix with Lock
lock = threading.Lock()
counter = 0
def safe_increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1  # Atomic now

# Producer-Consumer pattern
from queue import Queue

def producer(q, items):
    for item in items:
        q.put(item)
    q.put(None)  # sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None: break
        process(item)

q = Queue(maxsize=100)  # bounded buffer
```

---

## 3. Asyncio (Cooperative Concurrency)

```python
import asyncio
import aiohttp

# 100 HTTP requests concurrently
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Sequential: 100 × 200ms = 20s
# Async:      max(200ms) ≈ 200ms
```

---

## 4. Multiprocessing (True Parallelism)

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

# CPU-bound task
def compute(n):
    return sum(i*i for i in range(n))

# Parallel with ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
    results = list(executor.map(compute, [10**7]*8))
```

---

## 5. Common Concurrency Patterns

```python
# Semaphore — limit concurrent access
sem = threading.Semaphore(5)  # max 5 concurrent
def limited_task():
    with sem:
        do_work()

# Read-Write Lock
class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()
        self.write_lock = threading.Lock()
    
    def acquire_read(self):
        with self.lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire()
    
    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()
```

---

## Python GIL (Global Interpreter Lock)
```
GIL: chỉ 1 thread chạy Python bytecode tại 1 thời điểm
→ Threading KHÔNG parallel cho CPU-bound tasks trong Python

Workarounds:
  1. multiprocessing (mỗi process có GIL riêng)
  2. C extensions (NumPy releases GIL)
  3. asyncio cho I/O-bound
  4. Python 3.13+ free-threaded mode (experimental)
```

---

## 📝 Bài tập
1. Implement thread-safe bounded queue
2. Web scraper: 1000 URLs bằng asyncio + aiohttp
3. Parallel data processing: multiprocessing vs threading benchmark
4. Implement Read-Write Lock, test with concurrent readers/writers

## 🎯 LeetCode Practice List (Concurrency)

- #1114 Print in Order (Easy)
- #1115 Print FooBar Alternately (Medium)
- #1116 Print Zero Even Odd (Medium)
- #1117 Building H2O (Medium)
- #1188 Design Bounded Blocking Queue (Medium)
- #1226 The Dining Philosophers (Medium)
- #1195 Fizz Buzz Multithreaded (Medium)

> Nhóm bài Concurrency trên LeetCode ít, focus vào hands-on projects ở mục Bài tập.

## 📚 Tài liệu
- *Python Concurrency with asyncio* — Matthew Fowler
- *Java Concurrency in Practice* — Brian Goetz
