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
    d) Number of threads. \
    
usages of this scripts can be found here [attach link]

## 3. Dataset and Queries
### 3.1 Internet Movie Data Base (IMDB)
The dataset that was used is Internet Movie Data Base (IMDB). The original data is publicly available (ftp://ftp.fu-berlin.de/pub/misc/movies/database/) in txt files, and open-source imdbpy package was used to transform txt files to CSV files. This 3.6GB snapshot is from May 2013. The dataset includes 21 CSV files i.e., 21 relations in total. 
### 3.2  Join Order Benchmark (JOB)
We used Join Order Benchmark (JOB) queries for our experiments. JOB consists of 113 queries in total, including 33 query families with equijoins, and each family's queries differ only in selection predicates. Join sizes 2-17, join predicates 4-28, and tables 2-17.

## 4. PostgreSQL
We use a modified version of PostgreSQL 14.2 which allows injecting estimates for subqueries during query runtime [[1](https://github.com/waltercai/pqo-opensource)]. We did below changes to optimize PostgreSQL performance. \
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
Last two variables only during thread experiements, for other experiments we kept values to default. Modified version of .conf file can be found in `scripts` folder.