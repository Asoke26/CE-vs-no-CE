from socket import timeout
import sys, os
import psycopg2
import time
import statistics
import csv
import json
import logging as log

tau = 0.2
lamb = 2
PATH = "../Queries/"
PATH_Est = "../Estimates/"
OUTPUT = "../results/"
infoFile = "../pqo-opensource/output/info.txt" 

files = [     
         '1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6b','6c','6d','6e','6f', \
         '7a','7b','7c','8a','8b','8c','8d','9a','9b','9c','9d','10a','10b','10c','11a','11b','11c','11d','12a','12b','12c', \
         '13a','13b','13c','13d','14a','14b','14c','15a','15b','15c','15d','16a','16b','16c','16d','17a','17b','17c','17d', \
         '17e','17f','18a','18b','18c','19a','19b','19c','19d','20a','20b','20c','21a','21b','21c','22a','22b','22c','22d', \
         '23a','23b','23c','24a','24b','25a','25b','25c','26a','26b','26c','27a','27b','27c','28a','28b','28c','29a','29b', \
         '29c','30a','30b','30c','31a','31b','31c','32a','32b','33a','33b','33c'
        ]

# files = [ '1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6b','6c','6d','6e','6f', \
#         '7a','7b','7c','8a','8b','8c','8d','9a','9b','9c','9d','10a','10b','10c','11a','11b','11c','11d','12a','12b','12c', \
#          '13a','13b','13c','13d','14a','14b','14c','15a','15b','15c','15d','16a','16b','16c','16d','17a','17b','17c','17d', \
#          '17e','17f']

def recursive_trav(node):

    children = node.get('Plans', [])
    if children == []:
        if 'Scan' in node['Node Type']:
            tuples = node['Actual Rows']
            tuples  = tuples + node.get('Rows Removed by Filter', 0)
            tuples = tuples * node['Actual Loops']
            cost = tuples * tau

            if node.get('Relation Name', []) != []:
                print("Cost", node['Node Type'], "(", node['Relation Name'], ")= ", cost)
            elif node.get('Index Name', []) != []:
                print("Cost", node['Node Type'], "(", node['Index Name'], ")= ", cost)
            else:
                print('Unknown Scan Node!!!')

            return cost
    else:
        cost = 0

        # this is for Index Nested Loop Join
        if 'Nested Loop' == node['Node Type']:
            # find the child that has a single child itself and contains an INDEX node below
            found = False
            PT = children[0]
            while True:
                if 'Index' in PT['Node Type'] and PT.get('Index Cond', []) != []:
                    T1 = children[1]
                    T2 = PT
                    found = True
                    break

                if len(PT.get('Plans', [])) != 1:
                    break

                PT = PT.get('Plans', [])[0]


            if False == found:
                PT = children[1]
                while True:
                    if 'Index' in PT['Node Type'] and PT.get('Index Cond', []) != []:
                        T1 = children[0]
                        T2 = PT
                        found = True
                        break

                    if len(PT.get('Plans', [])) != 1:
                        break

                    PT = PT.get('Plans', [])[0]

            if True == found:
                isIndexNL = T2.get('Index Cond', [])
                if isIndexNL != []:
                    cost = recursive_trav(T1)

                    T1_c = T1['Actual Rows'] * node['Actual Loops']
                    if T1_c == 0: T1_c = 1

                    J_c = node['Actual Rows'] * node['Actual Loops']
                    if J_c/T1_c > 1:
                        cost = cost + lamb * T1_c * (J_c/T1_c)
                    else:
                        cost = cost + lamb * T1_c

                    print("Cost Index Nested Loop Join(", T2['Index Cond'], ")= ", cost)

            else:
                T1 = children[0]
                T2 = children[1]
                cost = recursive_trav(T1) + recursive_trav(T2)

                cost = cost + (
                    T1['Actual Rows'] * node['Actual Loops'] *
                    T2['Actual Rows'] * node['Actual Loops'])

                cart_product = node.get('Join Filter', [])
                if cart_product == []:
                    print("Cost Product Join(A x B)= ", cost)
                else:
                    print("Cost Nested Loop Join(", node['Join Filter'], ")= ", cost)

        else:
            # print(type(children))
            for c in children:
                cost = cost + recursive_trav(c)

            if 'Hash' == node['Node Type'] or 'Hash Join' == node['Node Type']:
                cost = cost + node['Actual Rows'] * node['Actual Loops']

            if 'Hash' == node['Node Type']:
                print("Cost Hash(", node['Actual Rows'], ")= ", cost)

            if 'Hash Join' == node['Node Type']:
                print("Cost HashJoin(", node['Hash Cond'], ")= ", cost)

        return cost

    return 0



def reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _threads):
    # Setting postgres internal parameters
    fromLimitQry = "SET from_collapse_limit = " + _fromLimit + ";"
    joinLimitQry = "SET join_collapse_limit = " + _joinLimit + ";"
    nextLoopQry = "SET enable_nestloop = " + _nlFlag + ";"
    hashJoinQry = "SET enable_hashjoin = " + _hjFlag + ";"
    mergeJoinQry =  "SET enable_mergejoin = " + _mjFlag + ";"
    timeOutQry = "SET statement_timeout = " + _timeOut + ";"
    workerGeather = "SET max_parallel_workers_per_gather = " + _threads + ";"
    workerParallel = "SET max_parallel_workers = " + _threads + ";"

    cursor.execute(fromLimitQry)
    cursor.execute(joinLimitQry)
    cursor.execute(nextLoopQry)
    cursor.execute(hashJoinQry)
    cursor.execute(mergeJoinQry)
    cursor.execute(timeOutQry)
    cursor.execute(workerGeather)
    cursor.execute(workerParallel)


    cursor.execute("show from_collapse_limit;")
    fromLimit = cursor.fetchone()
    cursor.execute("show join_collapse_limit;")
    joinLimit = cursor.fetchone()
    cursor.execute("show enable_nestloop;")
    nlFlag = cursor.fetchone()
    cursor.execute("show enable_hashjoin;")
    hjFlag = cursor.fetchone()
    cursor.execute("show enable_mergejoin;")
    mjFlag = cursor.fetchone()
    cursor.execute("show statement_timeout;")
    timeOut = cursor.fetchall()
    cursor.execute("show max_parallel_workers_per_gather;")
    maxp_gather = cursor.fetchall()
    cursor.execute("show max_parallel_maintenance_workers;")
    maxp_maintenance_workers = cursor.fetchall()
    cursor.execute("show max_worker_processes;")
    maxw_process = cursor.fetchall()
    cursor.execute("show max_parallel_workers;")
    maxp_workers = cursor.fetchall()


    print("from_collapse_limit - ", fromLimit)
    print("join_collapse_limit - ", joinLimit)
    print("enable_nestloop - ", nlFlag)
    print("enable_hashjoin - ", hjFlag)
    print("enable_mergejoin - ", mjFlag)
    print("statement_timeout(ms) - ", timeOut)
    print("max_parallel_workers_per_gather - ", maxp_gather)
    print("max_parallel_maintenance_workers - ", maxp_maintenance_workers)
    print("max_worker_processes - ", maxw_process)
    print("max_parallel_workers - ", maxp_workers)
    


def runQueriesCost(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads):
    connection = psycopg2.connect(host = "localhost", database = _db, user = "postgres", password = "postgres")
    cursor = connection.cursor()
    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _threads)
    print("Estimation Flag # ", _estFlag)
    print("Estimation Folder # ", _estFolder)
    print("Database # ", _db)
    print("Input Folder # ", _inFolder)

    queryFiles = PATH + _inFolder + '/'
    estFiles = PATH_Est + _estFolder + '/'

    outFfile = ""
    if _estFlag == True and "implicit" in _inFolder:
        outFfile = _estFolder
    elif _estFlag == False and "implicit" in _inFolder:
        outFfile = "PostgreSQL"
    else:
        outFfile = _inFolder
    if _estFlag == True and "implicit" not in _inFolder:
        outFfile += '_true'

    outFolder = "fk" if _db == "imdb_fk" else "no_index"
    outFfile = outFfile + '_nl' if _hjFlag == "off" else outFfile

    outPATH = OUTPUT + "costs/" + outFolder + '/'
    if False == os.path.exists(outPATH):
        os.makedirs(outPATH)

    jsonPATH = OUTPUT + "json/" + outFolder + '/' + outFfile + '/' if _index == False else OUTPUT + "json/" + outFolder + '/' + outFfile + '/'

    if False == os.path.exists(jsonPATH):
        os.makedirs(jsonPATH)

    print("\n\n\n\n\n+++++++++++++++++++++++++ ",outFolder, outFfile," +++++++++++++++++++++++++\n\n\n\n\n")

    for file in files:
        print("------------------Query # ",file,"["+ outFolder +"] -------------------------")
        query = open(queryFiles + file + ".sql", 'r').read().strip()

        if True == _estFlag:
            estimates = open(estFiles + file + ".sql.txt", "r").read().strip()
        else:
            estimates = ''
        w_f = open(infoFile,'w')
        w_f.write(estimates)
        w_f.close()

        for i in range(1):
            qry = "EXPLAIN (ANALYZE, BUFFERS,FORMAT JSON) " + query
            e = open(infoFile, 'r').read()
            if e != estimates:
                print("ERROR ! Estimation statistics doesn't match!!\n")

            try:
                card = cursor.execute(qry)
                plan = cursor.fetchall()

                with open(jsonPATH + '/' + file + '.json', 'w', encoding='utf-8') as f:
                    json.dump(plan, f, ensure_ascii=False, indent=2)

                plan_cost = recursive_trav(plan[0][0][0]['Plan'])
            except psycopg2.Error as e:
                log.error(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
                plan_cost = -99
                if connection: 
                    connection.rollback()
                    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut)
            line_w = file + ',' + str(plan_cost) + '\n'

        write_cost = open(outPATH + outFfile + '.csv', 'a') # -- 9
        write_cost.writelines(line_w)
        write_cost.close()

        print("---- Plan cost - ",file," ## ",plan_cost,"\n\n")

    connection.close()



def runQueriesTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads):
    connection = psycopg2.connect(host = "localhost", database = _db, user = "postgres", password = "postgres")
    cursor = connection.cursor()
    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, str(_threads))
    print("Estimation Flag # ", _estFlag)
    print("Estimation Folder # ", _estFolder)
    print("Database # ", _db)
    print("Input Folder # ", _inFolder)

    queryFiles = PATH + _inFolder + '/'
    estFiles = PATH_Est + _estFolder + '/'

    outFfile = ""
    
    if _estFlag == True and "implicit" in _inFolder:
        outFfile = _estFolder
    elif _estFlag == False and "implicit" in _inFolder:
        outFfile = "PostgreSQL"
    else:
        outFfile = _inFolder
    if _estFlag == True and "implicit" not in _inFolder:
        outFfile += '_true'
    
    outFolder = "fk" if _db == "imdb_fk" else "no_index"
    outFfile = outFfile + '_nl' if _hjFlag == "off" else outFfile
    outFfile = outFfile + '_' + str(_threads + 1)

    outPATH = OUTPUT + "threadExp/" + outFolder + '/'
    if False == os.path.exists(outPATH):
        os.makedirs(outPATH)

    print("\n\n\n\n\n+++++++++++++++++++++++++ ",outFolder, outFfile," +++++++++++++++++++++++++\n\n\n\n\n")

    for file in files:
        print("------------------Query # ",file,"["+ outFolder +"] -------------------------")
        query = open(queryFiles + file + ".sql", 'r').read().strip()

        if True == _estFlag:
            estimates = open(estFiles + file + ".sql.txt", "r").read().strip()
        else:
            estimates = ''
        w_f = open(infoFile,'w')
        w_f.write(estimates)
        w_f.close()

        runTimes = []
        for i in range(11):
            qry = "EXPLAIN (ANALYZE, BUFFERS,FORMAT JSON) " + query
            e = open(infoFile, 'r').read()
            if e != estimates:
                print("ERROR ! Estimation statistics doesn't match!!\n")

            try:
                cursor.execute(qry)
                plan = cursor.fetchall()
                plan_time = float(plan[0][0][0]["Planning Time"])
                exec_time = float(plan[0][0][0]["Execution Time"])
            
            except psycopg2.Error as e:
                log.error(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
                runTime = _timeOut
            
                if connection: 
                    connection.rollback()
                    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut)

            print("Planning Time - ",plan_time," | Execution Time - ",exec_time)
            runTimes.append(plan_time)
            runTimes.append(exec_time)
            if plan_time + exec_time >= float(_timeOut):
                break
        
        runTimes = [str(i) for i in runTimes]
        print(runTimes)
        line_w = ','.join(runTimes)
        line_w = file + ',' + line_w + '\n'
        print(line_w)
        write_cost = open( outPATH + outFfile + '.csv', 'a') # -- 9
        write_cost.writelines(line_w)
        write_cost.close()

        print(runTimes,"\n\n")

    connection.close()



def runQueriesCostTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, _threads):
    connection = psycopg2.connect(host = "localhost", database = _db, user = "postgres", password = "postgres")
    cursor = connection.cursor()
    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _threads)
    print("Estimation Flag # ", _estFlag)
    print("Estimation Folder # ", _estFolder)
    print("Database # ", _db)
    print("Input Folder # ", _inFolder)

    queryFiles = PATH + _inFolder + '/'
    estFiles = PATH_Est + _estFolder + '/'

    outFfile = ""
    
    if _estFlag == True and "implicit" in _inFolder:
        outFfile = _estFolder
    elif _estFlag == False and "implicit" in _inFolder:
        outFfile = "PostgreSQL"
    else:
        outFfile = _inFolder
    if _estFlag == True and "implicit" not in _inFolder:
        outFfile += '_true'
    
    outFolder = "fk" if _db == "imdb_fk" else "no_index"
    outFfile = outFfile + '_nl' if _hjFlag == "off" else outFfile

    outPATH = OUTPUT + "costTime/" + outFolder + '/'
    if False == os.path.exists(outPATH):
        os.makedirs(outPATH)

    print("\n\n\n\n\n+++++++++++++++++++++++++ ",outFolder, outFfile," +++++++++++++++++++++++++\n\n\n\n\n")

    for file in files:
        print("------------------Query # ",file,"["+ outFolder +"] -------------------------")
        query = open(queryFiles + file + ".sql", 'r').read().strip()

        if True == _estFlag:
            estimates = open(estFiles + file + ".sql.txt", "r").read().strip()
        else:
            estimates = ''
        w_f = open(infoFile,'w')
        w_f.write(estimates)
        w_f.close()

        runTimes = []
        for i in range(5):
            qry = "EXPLAIN (ANALYZE, BUFFERS,FORMAT JSON) " + query
            e = open(infoFile, 'r').read()
            if e != estimates:
                print("ERROR ! Estimation statistics doesn't match!!\n")

            try:
                cursor.execute(qry)
                plan = cursor.fetchall()
                plan_time = float(plan[0][0][0]["Planning Time"])
                exec_time = float(plan[0][0][0]["Execution Time"])
                plan_cost = recursive_trav(plan[0][0][0]['Plan'])

            except psycopg2.Error as e:
                log.error(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
                runTime = _timeOut
            
                if connection: 
                    connection.rollback()
                    reset_db_parameters(cursor, _fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut)

            print("Planning Time - ",plan_time," | Execution Time - ",exec_time)
            runTimes.append(plan_time)
            runTimes.append(exec_time)
            runTimes.append(plan_cost)
            if plan_time + exec_time >= float(_timeOut):
                break
        
        runTimes = [str(i) for i in runTimes]
        print(runTimes)
        line_w = ','.join(runTimes)
        line_w = file + ',' + line_w + '\n'
        print(line_w)
        write_cost = open( outPATH + outFfile + '.csv', 'a') # -- 9
        write_cost.writelines(line_w)
        write_cost.close()

        print(runTimes,"\n\n")

    connection.close()




def merge_cost_files(_dir):
    merged_dict = {}
    csv_files = os.listdir(_dir)
    for file in files:
        merged_dict[file] = ""
    merged_dict["qry_no"] = ""

    for file in csv_files:
        header = file.split('.')[0]
        merged_dict["qry_no"] += ',' + header

        for line in open(_dir + file, 'r').readlines():
            data = line.strip().split(',')
            qry = data[0]
            cost = data[1]
            merged_dict[qry] += (',' + cost)
    
    w_f = open(_dir + "merged_cost_files.csv", 'w')
    w_f.write("qry_no " + merged_dict['qry_no'] + '\n')
    
    for key, val in merged_dict.items():
        if key != 'qry_no':
            w_f.write(key + val + '\n')
    w_f.close()

def merge_time_files(_dir):
    merged_dict, pg_plantime_dict = {}, {}
    csv_files = os.listdir(_dir)
    for file in files:
        merged_dict[file] = ""
    merged_dict["qry_no"] = ""
    pg_plantime_dict["qry_no"] = []

    for file in csv_files:
        if "TrueCard" in file: continue
        elif 'true' in file: continue

        header = file.split('.')[0]
        merged_dict["qry_no"] += ',' + header
        
        for line in open(_dir + file, 'r').readlines():
            data = line.strip().split(',')
            qry = data[0]
            runTimes = []

            for i in range(5):
                plan_time = float(data[2*i + 1])
                exec_time = float(data[2*i + 2])
                runTimes.append(plan_time + exec_time)

                if "PostgreSQL" in file:
                    if qry not in pg_plantime_dict: pg_plantime_dict[qry] = []
                    pg_plantime_dict[qry].append(plan_time)

            median_time = statistics.median(runTimes)
            merged_dict[qry] += (',' + str(median_time))

    ## True card planning time overhead due to data reading is removed
    for file in csv_files:
        if "TrueCard" not in file : 
            if 'true' not in file : continue

        header = file.split('.')[0]
        merged_dict["qry_no"] += ',' + header
        
        for line in open(_dir + file, 'r').readlines():
            data = line.strip().split(',')
            qry = data[0]
            runTimes = []

            for i in range(5):
                plan_time = statistics.median(pg_plantime_dict[qry])
                exec_time = float(data[2*i + 2])
                runTimes.append(plan_time + exec_time)

            median_time = statistics.median(runTimes)
            merged_dict[qry] += (',' + str(median_time))
    
    w_f = open(_dir + "merged_time_files.csv", 'w')
    w_f.write("qry_no " + merged_dict['qry_no'] + '\n')
    
    for key, val in merged_dict.items():
        if key != 'qry_no':
            w_f.write(key + val + '\n')
    w_f.close()