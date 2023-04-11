import os,sys
from termcolor import colored
from operator import itemgetter
from collections import OrderedDict
import copy
import psycopg2




# qry_reader reads a query and runturs selection conditions
def qry_reader_select(file):
  PATH = "/home/postgres/Simpli2-EXP-new/Queries/implicit/"
  query = open(PATH+file+".sql",'r').read()
  AS_MAPPING = dict()
  FROM = query.split("WHERE")[0].split("FROM")[1]
  FROM = FROM.split(',')

  for tbl_as in FROM:
      tbl = tbl_as.split("AS")[0].strip()
      as_ = tbl_as.split("AS")[1].strip()
      AS_MAPPING[as_] = tbl

  query_lines = open(PATH+file+".sql",'r').readlines()
  SELECT_MAPPING = dict()
  JOIN_MAPPING = dict()
  for key in AS_MAPPING.keys():
    SELECT_MAPPING[key] = list()
    JOIN_MAPPING[key] = list()

  whr_flag = False
  for predicate in query_lines:
    if ';' in predicate:
      predicate = predicate.replace(';','')
    if not predicate.strip():
      continue
    if "WHERE" in predicate:
      whr_flag = True
    if whr_flag == True:
      if "WHERE" in predicate:
        predicate = predicate.replace("WHERE","",1).strip()
      elif "AND" in predicate:
        predicate = predicate.replace("AND","",1).strip()

      if '=' not in predicate:
        key1 = predicate.split('.')[0].replace('(','')
        SELECT_MAPPING[key1].append(predicate)
        continue
      left = predicate.split('=')[0].strip()
      right = predicate.split('=')[1].strip()
      if '.' in left and '.' in right and 'id' in predicate:
        left_key = left.split('.')[0]
        right_key = right.split('.')[0]
        JOIN_MAPPING[left_key].append(predicate)
        JOIN_MAPPING[right_key].append(predicate)
      else:
        key2 = predicate.split('.')[0]
        if '(' in key2:
          key2 = key2.replace('(','')
        SELECT_MAPPING[key2].append(predicate)


  for key,val in AS_MAPPING.items():
    if len(SELECT_MAPPING[key]) > 0:
      stmt = "SELECT count(*) FROM "+val+" AS "+key+" WHERE "

      for pred in SELECT_MAPPING[key]:
        stmt += pred + " AND "
      SELECT_MAPPING[key] = stmt[:-4]+';'
  return SELECT_MAPPING




# qry_reader reads a query and runturs selection conditions, as, join conditions
def qry_reader_all(file):
	PATH = "/home/postgres/Simpli2-EXP-new/Queries/implicit/"
	query = open(PATH+file+".sql",'r').read()
	AS_MAPPING = dict()
	FROM = query.split("WHERE")[0].split("FROM")[1]
	FROM = FROM.split(',')

	for tbl_as in FROM:
		tbl = tbl_as.split("AS")[0].strip()
		as_ = tbl_as.split("AS")[1].strip()
		AS_MAPPING[as_] = tbl

	query_lines = open(PATH+file+".sql",'r').readlines()
	SELECT_MAPPING = dict()
	JOIN_MAPPING = dict()
	for key in AS_MAPPING.keys():
		SELECT_MAPPING[key] = list()
		JOIN_MAPPING[key] = list()

	whr_flag = False
	for predicate in query_lines:
		if ';' in predicate:
			predicate = predicate.replace(';','')
		if not predicate.strip():
			continue
		if "WHERE" in predicate:
			whr_flag = True
		if whr_flag == True:
			if "WHERE" in predicate:
				predicate = predicate.replace("WHERE","",1).strip()
			elif "AND" in predicate:
				predicate = predicate.replace("AND","",1).strip()

			if '=' not in predicate:
				key1 = predicate.split('.')[0].replace('(','')
				SELECT_MAPPING[key1].append(predicate)
				continue
			left = predicate.split('=')[0].strip()
			right = predicate.split('=')[1].strip()
			if '.' in left and '.' in right and 'id' in predicate:
				left_key = left.split('.')[0]
				right_key = right.split('.')[0]
				JOIN_MAPPING[left_key].append(predicate)
				JOIN_MAPPING[right_key].append(predicate)
			else:
				key2 = predicate.split('.')[0]
				if '(' in key2:
					key2 = key2.replace('(','')
				SELECT_MAPPING[key2].append(predicate)

	return AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING




# pg_con connects with PostgreSQL and update base table cardinalities
def pg_con(_SELECT_MAPPING,_rel_dict):
  host= "localhost"#input("host: ")
  db = "imdb"#input("database: ")
  usr = "postgres"#input("user: ")
  pwd = "postgres"#input("password: ")

  connection = psycopg2.connect(host=host, database=db, user=usr, password=pwd)
  
  rel_dict = _rel_dict
  cursor = connection.cursor()
  for key,val in _SELECT_MAPPING.items():
    if len(val) > 0:
      stm = val
      cursor.execute(stm)
      rel_dict[key] = cursor.fetchone()[0]

  connection.close()
  return rel_dict


# pg_con connects with PostgreSQL and returns the cardinality
def exec_qry(_qry):
  host= "localhost"#input("host: ")
  db = "imdb_fk"#input("database: ")
  usr = "postgres"#input("user: ")
  pwd = "postgres"#input("password: ")

  connection = psycopg2.connect(host=host, database=db, user=usr, password=pwd)
  cursor = connection.cursor()
  cursor.execute(_qry)
  card = cursor.fetchone()[0]

  connection.close()
  return card



# Sort a list based on Total number tuples
def TT_sort(_tbls,_AS_mapping,_order,rel_dict):
  tbl_tuples = dict()
  for tbl in _tbls:
    tbl_tuples[tbl] = rel_dict[tbl] 
    
  tbl_tuples_sorted = OrderedDict(sorted(tbl_tuples.items(), key=itemgetter(1) , reverse= _order))
  return list(tbl_tuples_sorted.keys())





# Sort a list based on Total number tuples and Join graph
def TT_sort_g(_tbls,_AS_mapping,_order,_FK_join_graph,rel_dict):
  tbl_tuples = dict()
  for tbl in _tbls:
    tbl_tuples[tbl] = rel_dict[tbl]

  tbl_tuples_sorted = OrderedDict(sorted(tbl_tuples.items(), key=itemgetter(1) , reverse= _order)) 
  final_order = []
  already_joined = []
  not_joined_yet = list(tbl_tuples_sorted.keys())
  cand = not_joined_yet[0]
  already_joined.append(cand)
  final_order.append(cand)
  not_joined_yet.remove(cand)

  i = 0
  connected = 0
  while(len(not_joined_yet)!=0):
    cand = not_joined_yet[i]
    for tbl in already_joined:
      if cand in _FK_join_graph[tbl]:
        already_joined.append(cand)
        final_order.append(cand)
        not_joined_yet.remove(cand)
        i = 0
        connected = 1
        break
      else:
        connected = 0
    if connected == 0:
      i+=1

  return final_order


# Sort a list based on Total number tuples / 2 ** outdegree and Join graph
def TT_sort_outdeg(_tbls,_AS_mapping,_order,_FK_join_graph,rel_dict):
  tbl_tuples = dict()
  for tbl in _tbls:
    tbl_tuples[tbl] = rel_dict[tbl] / 2**len(_FK_join_graph[tbl])

  tbl_tuples_sorted = OrderedDict(sorted(tbl_tuples.items(), key=itemgetter(1) , reverse= _order)) 
  final_order = []
  already_joined = []
  not_joined_yet = list(tbl_tuples_sorted.keys())
  cand = not_joined_yet[0]
  already_joined.append(cand)
  final_order.append(cand)
  not_joined_yet.remove(cand)

  i = 0
  connected = 0
  while(len(not_joined_yet)!=0):
    cand = not_joined_yet[i]
    for tbl in already_joined:
      if cand in _FK_join_graph[tbl]:
        already_joined.append(cand)
        final_order.append(cand)
        not_joined_yet.remove(cand)
        i = 0
        connected = 1
        break
      else:
        connected = 0
    if connected == 0:
      i+=1

  return final_order



def build_join_graph(join_predicates, FK_join_graph, FK_FK):
  for join_pred in join_predicates:
    left = join_pred.split('=')[0]
    right = join_pred.split('=')[1]
    left_tbl = left.split('.')[0].strip()
    right_tbl = right.split('.')[0].strip()
    
    if left_tbl in FK_FK:
      FK_join_graph[left_tbl].append(right_tbl)

    if right_tbl in FK_FK:
      FK_join_graph[right_tbl].append(left_tbl)

  return join_graph




def update_join_graph(_tbl,_FK_join_graph):
  for key,val in _FK_join_graph.items():
    if _tbl in val:
      val.remove(_tbl)
      _FK_join_graph[key] = val

  return _FK_join_graph




def lonely_tbl(cur_join_cands,all_FK_join_cands):
  tbl_list = " "
  for tbl in cur_join_cands:
    if tbl not in all_FK_join_cands:
      tbl_list += tbl+" "
  if tbl_list.isspace():
    return ""
  else:
    return tbl_list[:-1]




def common_item(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True 
    else:
        return False




def plan_validation(plan,complete_join_graph):
  plan_copy = plan
  plan = plan.split(' ')
  subquery_dict = dict()
  subquery = []
  subquery_str = ""
  s = 1
  subq_f = 0
  for tbl in plan:
    if '(' in tbl:
      subquery_str += tbl+" "
      tbl = tbl.replace('(','')
      subquery.append(tbl)
      subq_f = 1
    elif ')' in tbl:
      subquery_str += tbl
      tbl = tbl.replace(')','')
      subquery.append(tbl)
      subquery_dict['S'+str(s)] = subquery.copy()
      plan_copy = plan_copy.replace(subquery_str,'S'+str(s))
      subquery.clear()
      subquery_str = ""
      s += 1
      subq_f = 0
    elif subq_f == 1:
      subquery_str += tbl + " "
      subquery.append(tbl)

  visited = []
  plan_copy = plan_copy.replace("  "," ")
  not_visited = plan_copy.strip().split(' ')
  visited.append(not_visited[0])
  not_visited.remove(visited[0])
  connections = []
  order = visited.copy()
  i = 0
  while (len(not_visited) != 0):
    cur = not_visited[0]
    if 'S' in cur:
      for candS in subquery_dict[cur]:
        connections.extend(complete_join_graph[candS])
    else:
      connections.extend(complete_join_graph[cur])

    if common_item(visited,connections) == True:
      if 'S' in cur:
        for candS in subquery_dict[cur]:
          visited.append(candS)
        order.append(cur)
      else:
        visited.append(cur)
        order.append(cur)
      not_visited.remove(cur)
      connections.clear()
    else:
      s = i + 1
      while s < len(not_visited):
        connections.clear()
        cand = not_visited[s]
        if 'S' in cand:
          for candS in subquery_dict[cur]:
            connections.extend(complete_join_graph[candS])
        else:
          connections.extend(complete_join_graph[cand])
        if common_item(visited,connections) == True:
          if 'S' in cur:
            for candS in subquery_dict[cur]:
              visited.append(candS)
            order.append(cand)
          else:
            visited.append(cand)
            order.append(cand)
          not_visited.remove(cand)
          connections.clear()
          break
        else:
          s += 1
  order = ' '.join(order)
  for key,val in subquery_dict.items():
    sub = '('
    for tbl in val:
      sub += tbl+' '
    sub = sub[:-1]+')'
    order = order.replace(key,sub)
  return order


def expose_columns(_tbls,sub_no,JOIN_MAPPING):
	columns_visited = []
	subquery_col_map = dict()
	select_stmt = ""
	for tbl in _tbls:
		for pred in JOIN_MAPPING[tbl]:
			left = pred.split('=')[0].strip()
			right = pred.split('=')[1].strip()
			left_tbl = left.split('.')[0].strip()
			right_tbl = right.split('.')[0].strip()
			left_attr = left.split('.')[1].strip()
			right_attr = right.split('.')[1].strip()

			if left_tbl == tbl and left not in columns_visited and right_tbl not in _tbls:
				select_stmt += left+' AS '+left_tbl+'_'+left_attr+','
				columns_visited.append(left)
				subquery_col_map[left] = sub_no+'.'+left_tbl+'_'+left_attr
			elif right_tbl == tbl and right not in columns_visited and left_tbl not in _tbls:
				select_stmt += right+' AS '+right_tbl+'_'+right_attr+','
				columns_visited.append(right)
				subquery_col_map[right] = sub_no+'.'+right_tbl+'_'+right_attr
	return select_stmt,subquery_col_map



def update_join_map(_tbls,sub_no,_JOIN_MAPPING,subquery_col_map):
  JOIN_MAPPING = _JOIN_MAPPING
  for tbl in _tbls:
    for pred in JOIN_MAPPING[tbl]:
      left = pred.split('=')[0].strip()
      right = pred.split('=')[1].strip()
      left_tbl = left.split('.')[0].strip()
      right_tbl = right.split('.')[0].strip()
      if left_tbl in _tbls and right_tbl in _tbls:
        JOIN_MAPPING[right_tbl].remove(pred)
        JOIN_MAPPING[left_tbl].remove(pred)

  for tbl in _tbls:
    for pred in JOIN_MAPPING[tbl]:
      pred_copy = pred
      left = pred.split('=')[0].strip()
      right = pred.split('=')[1].strip()
      if left in subquery_col_map.keys():
        pred = pred.replace(left,subquery_col_map[left])
        right_tbl = right.split('.')[0]
        JOIN_MAPPING[right_tbl].remove(pred_copy)
        JOIN_MAPPING[right_tbl].append(pred)
        JOIN_MAPPING[sub_no].append(pred)
      elif right in subquery_col_map.keys():
        pred = pred.replace(right,subquery_col_map[right])
        left_tbl = left.split('.')[0]
        JOIN_MAPPING[left_tbl].remove(pred_copy)
        JOIN_MAPPING[left_tbl].append(pred)
        JOIN_MAPPING[sub_no].append(pred)
    del JOIN_MAPPING[tbl]
  return JOIN_MAPPING




def build_subquery(_tbls,sub_no,AS_MAPPING,SELECT_MAPPING,JOIN_MAPPING):
	visited = []
	not_visited = _tbls.copy()
	visited.append(not_visited[0])
	not_visited.remove(visited[0])
	i = 0
	first_tbl_flag = True
	sql_stmt = " FROM "+AS_MAPPING[visited[0]]+" AS "+visited[0]+"\n"
	while(len(not_visited) != 0):
		tbl = not_visited[i]
		sql_stmt += ' join '
		sql_stmt += AS_MAPPING[tbl]+' AS '+tbl +' on ('
		if first_tbl_flag == True:
			for pred in SELECT_MAPPING[visited[0]]:
				sql_stmt += pred+' AND '
			first_tbl_flag = False	
		for pred in SELECT_MAPPING[tbl]:
			sql_stmt += pred+' AND '

		for pred in JOIN_MAPPING[tbl]:
			pred = pred.strip()
			left = pred.split('=')[0].strip()
			right = pred.split('=')[1].strip()
			left_tbl = left.split('.')[0].strip()
			right_tbl = right.split('.')[0].strip()
			if left_tbl in visited or right_tbl in visited:
				sql_stmt += pred+' AND '
		sql_stmt = sql_stmt[:-4]+')'
		visited.append(tbl)
		not_visited.remove(tbl)

	columns,subquery_col_map = expose_columns(_tbls,sub_no,JOIN_MAPPING)
	columns = columns[:-1]
	# Create sub-query statement
	subquery_stmt = "(SELECT "+columns+sql_stmt+')'+sub_no
	JOIN_MAPPING = update_join_map(_tbls,sub_no,JOIN_MAPPING,subquery_col_map)
	return JOIN_MAPPING, subquery_stmt





def subQry_loader(_qry):
  path = "/home/postgres/Simpli2-EXP-new/Estimates/TrueCard_1/"
  query = open(path + _qry + '.sql.txt', 'r').readlines()
  subQryDict = {}

  for sq in query:
    # print(sq)
    key = sq.split(',:')[0]
    val = sq.split(',:')[1]
    subQryDict[key] = val
  
  return subQryDict
  
# Load all two way cardinality from file
def loadCard(_qry):
  path = "/home/postgres/Simpli2-EXP-new/Estimates/TrueCard/"
  query = open(path + _qry + '.sql.txt', 'r').readlines()
  cardDict = {}

  for sq in query:
    key = sq.split(',:')[0]
    tbls = key.split(',')
    if len(tbls) == 2:
      val = sq.split(',:')[1]
      cardDict[key.strip()] = int(val.strip())
  
  return cardDict

def updateDict( _tbl, _canDict, _cardDict, _joinOrder):
  newDict = _canDict
  for key,val in _cardDict.items():
    keys = key.split(',')
    if keys[0] in _joinOrder and keys[1] in _joinOrder:
      continue
    if _tbl in keys and key not in newDict:
      newDict[key] = val
  newDict = dict(sorted(newDict.items(), key=lambda item: item[1]))
  return newDict

# start with lowest join size
def alg1(_cardDict):
  cardDict = _cardDict
  cardDict = dict(sorted(cardDict.items(), key=lambda item: item[1]))
  joinOrder = []
  candDict = {}

  start = list(cardDict.keys())[0]
  joinOrder.extend(start.split(','))    # Adding first join in join order
  # print("start # ", start, " Join Order $ ",joinOrder)
  candDict = updateDict(joinOrder[0], candDict, cardDict, joinOrder)
  candDict = updateDict(joinOrder[1], candDict, cardDict, joinOrder)

  while candDict:
    firstKey = list(candDict.keys())[0]
    keys = firstKey.split(',')

    if keys[0] not in joinOrder or keys[1] not in joinOrder:
      cand = keys[0] if keys[0] not in joinOrder else keys[1]
      joinOrder.append(cand)
      candDict = updateDict(cand, candDict, cardDict, joinOrder)

    del candDict[firstKey]
  
  return joinOrder

# Sort FK and its join candidates based on true join cardinalities
def trueSort(_fkKey, _joinCands, _cardDict):
  pred_card_dict = {}
  order_list = []

  for joinCand in _joinCands:
    cand1 = _fkKey + ',' + joinCand
    cand2 = joinCand + ',' + _fkKey
    if cand1 in _cardDict: pred_card_dict[cand1] = _cardDict[cand1]
    elif cand2 in _cardDict: pred_card_dict[cand2] = _cardDict[cand2]
  
  pred_card_dict = dict(sorted(pred_card_dict.items(), key=lambda item: item[1]))
  # print(pred_card_dict)

  for key, val in pred_card_dict.items():
    keys = key.strip().split(',')
    cand = keys[0] if keys[0] != _fkKey else keys[1]
    order_list.append(cand)
  # print(order_list)
  return order_list




def num_of_joinCands(_key, _fk_join_graph, _fks, _join_order):
  cnt = 0

  for cand in _fk_join_graph[_key]:
    if cand not in _fks and cand not in _join_order:
      cnt += 1
  
  return cnt