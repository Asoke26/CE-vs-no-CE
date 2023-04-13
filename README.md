# CE-vs-no-CE

## 1. Experimental Setup

Experimental was conducted in the following environment:

- Machine: 2x Intel(R) Xeon(R) CPU E5-2660 v4 (28 CPU cores and 256GB memory, and HDD storage ). 
- OS: Ubuntu 22.04 LTS, Python 3.10.6.
- Docker v20.10.12 .
- RStudio 2022.12.0 .

## 2. Scripts
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
    
usages of this scripts can be found here [[1](https://github.com/Asoke26/CE-vs-no-CE/tree/main/scripts)]

## 3. Dataset and Queries
### 3.1 Internet Movie Data Base (IMDB)
We used the Internet Movie Data Base (IMDB) dataset. The original data is publicly available in txt files (ftp://ftp.fu-berlin.de/pub/misc/movies/database/), and we utilized the open-source imdbpy package to convert the txt files to CSV files. The 3.6GB snapshot is from May 2013, and the dataset contains 21 CSV files, i.e., 21 relations in total.


### 3.2  Join Order Benchmark (JOB)
Our experiments used Join Order Benchmark (JOB) queries. JOB includes 113 queries in total, comprising 33 query families with equijoins. The queries within each family differ only in selection predicates. The join sizes range from 2 to 17, join predicates from 4 to 28, and tables from 2 to 17.

## 4. PostgreSQL
We employed a modified version of PostgreSQL 14.2 that allows injecting estimates for subqueries during query runtime [[2](https://github.com/waltercai/pqo-opensource)]. To optimize PostgreSQL performance, we made the following changes:

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
The last two variables were only adjusted during thread experiments. For other experiments, we kept the default values. The modified version of the `postgresql.conf` file can be found [here](https://github.com/Asoke26/CE-vs-no-CE/blob/main/scripts/postgresql.conf).