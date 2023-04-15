# Good Plans Despite Bad/No Cardinalities?

## 1. Experimental Setup

Experimental was conducted in the following environment:

- Machine: 2x Intel(R) Xeon(R) CPU E5-2660 v4 (28 CPU cores and 256GB memory, and HDD storage ). 
- OS: Ubuntu 22.04 LTS, Python 3.10.6.
- Docker v20.10.12 .
- RStudio 2022.12.0 .


## 2. Dataset and Queries
### 2.1 Internet Movie Data Base (IMDB)
We used the Internet Movie Data Base (IMDB) dataset. The original data is publicly available in txt files (ftp://ftp.fu-berlin.de/pub/misc/movies/database/), and we utilized the open-source imdbpy package to convert the txt files to CSV files. The 3.6GB snapshot is from May 2013, and the dataset contains 21 CSV files, i.e., 21 relations in total.


### 2.2  Join Order Benchmark (JOB)
Our experiments used Join Order Benchmark (JOB) queries. JOB includes 113 queries in total, comprising 33 query families with equijoins. The queries within each family differ only in selection predicates. The join sizes range from 2 to 17, join predicates from 4 to 28, and tables from 2 to 17.

## 3. PostgreSQL
We employed a modified version of PostgreSQL 14.2(https://github.com/waltercai/pqo-opensource) that allows injecting estimates for subqueries during query runtime [[2](https://github.com/waltercai/pqo-opensource)]. To optimize PostgreSQL performance, we made the following changes:

```
shared_buffers = 128GB
work_mem = 128GB
max_wal_size = 128GB
effective_cache_size = 128GB
geqo_threshold = 18
from_collapse_limit = 1 (default 8, to disable subquery reordering)
join_collapse_limit = 1	(default 8, to disable join reordering)
max_parallel_workers_per_gather = 0-5 (default 2)
max_parallel_workers = 0-5 (default 8)
```
The last two variables were only adjusted during thread experiments. For other experiments, we kept the default values. The modified version of the `postgresql.conf` file can be found in scripts folder.


## 4. Scripts
We provide python scripts to replicate - 
1. $Simpli^2$ join ordering algorithm.
2. Scripts for generating query from join order.
3. QuickPick algorithm.
4. Cost calculation using Leis et al. in-memory cost function.
5. Runtime collection for different settings. Includes - \
    a) Indexed/ non-indexed.\
    b) Join operator selection.\
    c) Estimate selection.\
    d) Number of threads.
    
usages of this scripts is below
### 4.1. $Simpli^2$ join order and query generation
- non-indexed

```
python3 Simpli2/Simpli2.py
```
- indexed

```
python3 Simpli2/Simpli2_idx.py
```

Above two scripts will help to generate join orders for $Simpli^2$ in both non-indexed and indexed settings. Below script will take those join order as input and generate sql queries.

```
python3 sql_generator.py
```

### 4.2. Cost and Runtime collection

Below script will collect cost and runtime.
```
python3 pg_cost_calc.py
```

This script has configurable parameters which are described below -
```
_fromLimit = from collapse limit (1/8)
_joinLimit = join collapse limit (1/8)
_nlFlag = nested loop join (on/off)
_hjFlag = hash join (on/off)
_mjFlag = marge join (on/off)
_timeOut = query timeout (in seconds)
_estFlag = estimates availability (True/False)
_estFolder = location of estimates (folder location)
_db = database name
_inFolder = query location
_index = index availability (True/ False)
_threads = number of threads (0 - 4)

Functions : 
# cost
def runQueriesCost(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)

# runtime
def runQueriesTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)

# runtime and cost
def runQueriesCostTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)
```
