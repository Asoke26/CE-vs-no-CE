### 1. $Simpli^2$ join order and query generation
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

### 2. Cost and Runtime collection

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
# To collect cost
def runQueriesCost(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)

# To collect runtime
def runQueriesTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)

# To collect runtime and cost
def runQueriesCostTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads)
```

