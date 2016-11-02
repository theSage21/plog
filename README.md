Plog
====

Quick and dirty logging for parallel tasks.

Usage
-----

1. Run `python plog.py report.csv`. We call this the `logging` process.
2. Run your program which spawns processes/threads which need to report to some
   kind of a log. We call this the `supplier` process.
3. Wait for the supplier to stop running.
3. `Ctrl+C` the logging process to flush any logs in memory to disk.

In your `supplier` process, the worker function is the one which needs to call
the `addlog` function from `plog.py` to add a log.

For example a sample `supplier` program may do this:

```python
from plog import addlog
from multiprocessing import Pool

def worker(i):
    string = '{},{}'.format(i, i**2)
    addlog(string)


with Pool() as pool:
    pool.map(worker, range(10000))
```
