import os,sys
from termcolor import colored
from operator import itemgetter
from collections import OrderedDict
import copy
import utils
import time

# Number of Total Tuples 
TT_dict = {"aka_name":901343,"aka_title":361472,"cast_info":36244344,"char_name":3140339,"company_name":234997, \
	"company_type":4,"comp_cast_type":4,"complete_cast":135086,"info_type":113,"keyword":134170,"kind_type":7, \
	"link_type":18,"movie_companies":2609129,"movie_info_idx":1380035,"movie_keyword":4523930,"movie_link":29997, \
	"name":4167491,"role_type":12,"title":2528312,"movie_info":14835720,"person_info":2963664}


PATH = "Queries/implicit/"
files = [     
         '1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6b','6c','6d','6e','6f', \
         '7a','7b','7c','8a','8b','8c','8d','9a','9b','9c','9d','10a','10b','10c','11a','11b','11c','11d','12a','12b','12c', \
         '13a','13b','13c','13d','14a','14b','14c','15a','15b','15c','15d','16a','16b','16c','16d','17a','17b','17c','17d', \
         '17e','17f','18a','18b','18c','19a','19b','19c','19d','20a','20b','20c','21a','21b','21c','22a','22b','22c','22d', \
         '23a','23b','23c','24a','24b','25a','25b','25c','26a','26b','26c','27a','27b','27c','28a','28b','28c','29a','29b', \
         '29c','30a','30b','30c','31a','31b','31c','32a','32b','33a','33b','33c'
        ]


no_tbls = 0
for file in files:
  startTime = time.time()
  query = open(PATH + file + '.sql').read()
  join_predicates = []
  AS_mapping = dict()
  FROM = query.split("WHERE")[0].split("FROM")[1]
  FROM = FROM.split(',')

  for tbl_as in FROM:
    tbl = tbl_as.split("AS")[0].strip()
    as_ = tbl_as.split("AS")[1].strip()
    AS_mapping[as_] = tbl

  where = query.split("WHERE")[1]
  predicates = where.split("AND")

  for predicate in predicates:
    if '=' not in predicate:
      continue
    left = predicate.split('=')[0].strip()
    right = predicate.split('=')[1].strip()
    if '.' in left and '.' in right and 'id' in predicate:
      join_predicates.append(predicate.strip())

  no_tbls = len(AS_mapping)
  FK_FK = set()   # Get FK-FK joins and join graphs for FK keys
  FK_join_graph = dict()
  complete_join_graph = dict()

  for key in AS_mapping.keys():
    complete_join_graph[key] = []

  for join_pred in join_predicates:
    left = join_pred.split('=')[0]
    right = join_pred.split('=')[1]
    left_tbl = left.split('.')[0].strip()
    right_tbl = right.split('.')[0].strip()
    left_attr = left.split('.')[1].strip()
    right_attr = right.split('.')[1].strip()
    if left_attr != 'id' and right_attr != 'id' :
      FK_FK.add(left_tbl)
      FK_FK.add(right_tbl)
      complete_join_graph[left_tbl].append(right_tbl)
      complete_join_graph[right_tbl].append(left_tbl)
    else:
      complete_join_graph[left_tbl].append(right_tbl)
      complete_join_graph[right_tbl].append(left_tbl)

  SELECT_MAPPING = utils.qry_reader_select(file)

  rel_dict = dict()
  for key,val in AS_mapping.items(): 
    rel_dict[key] = TT_dict[val]
  # rel_dict = utils.pg_con(SELECT_MAPPING,rel_dict) # Process for push down


  # Case 1 : If no FK-FK join exists
  all_FK_join_cands = []
  if not FK_FK:
    join_graph = dict()
    visited_tbl = dict()
    tables = AS_mapping.keys()
    tables = utils.TT_sort(tables,AS_mapping,True,rel_dict)
    for tbl in tables:
      join_graph[tbl] = []
      visited_tbl[tbl] = False

    for join_pred in join_predicates:
      left = join_pred.split('=')[0]
      right = join_pred.split('=')[1]
      left_tbl = left.split('.')[0].strip()
      right_tbl = right.split('.')[0].strip()
      join_graph[left_tbl].append(right_tbl)
      join_graph[right_tbl].append(left_tbl)

    join_order = [tables[0]]
    join_candidates_2 = []
    cur_candidate = join_order[0]

    while(cur_candidate != None):
      visited_tbl[cur_candidate] = True
      for tbl in join_graph[cur_candidate]:
        if visited_tbl[tbl] == False:
          join_candidates_2.append(tbl)
      join_candidates_2 = utils.TT_sort(join_candidates_2,AS_mapping,False,rel_dict)
      if not join_candidates_2:
        cur_candidate = None
        break
      cur_candidate = join_candidates_2[0]
      join_candidates_2.remove(cur_candidate)
      join_order.append(cur_candidate)

    str1 = file+" , "+' '.join(join_order)
    endTime = time.time()
    print(str1, ',',(endTime - startTime) * 1000)

  else: # Case 2 : When FK-FK join exists
    FK_FK = list(set(FK_FK))
    for fk in FK_FK:
      FK_join_graph[fk] = []

    for join_pred in join_predicates:
      left = join_pred.split('=')[0]
      right = join_pred.split('=')[1]
      left_tbl = left.split('.')[0].strip()
      right_tbl = right.split('.')[0].strip()
      if left_tbl in FK_FK:
        FK_join_graph[left_tbl].append(right_tbl)
      if right_tbl in FK_FK:
        FK_join_graph[right_tbl].append(left_tbl)

    FK_FK = utils.TT_sort_outdeg(FK_FK,AS_mapping,False,FK_join_graph,rel_dict) # Sort FK-FK based on total tuples order desc.
    for key,val in FK_join_graph.items():
      all_FK_join_cands.extend(val)

    for key,val in FK_join_graph.items():
      FK_join_graph[key] = utils.TT_sort(val,AS_mapping,False,rel_dict)

    #  Enumerate over FK-FK :
    #   a) sort FK key graph on total tuples order asce. {ci : {t,n,mk},mk:{k,t,ci}}
    #   b) Enumerate over FK key graph:

    join_order = str(FK_FK[0])
    visited = dict()
    subqry_flag = False
    for key,val in AS_mapping.items():
      visited[key] = False

    for _tbl in FK_FK:  # Removing FK join candidates
      FK_join_graph = utils.update_join_graph(_tbl,FK_join_graph)

    for FK in FK_FK:  # Enumerate over FK key graph:
      visited[FK] = True
      join_candidates = FK_join_graph[FK].copy() 
      if not join_candidates:
        join_order += ' '+str(FK)+" "
        continue
      if FK != FK_FK[0]:
        join_order += " ("+str(FK)
        subqry_flag = True
      i = 0
      if subqry_flag == True:
        for tbl in join_candidates:
          if tbl not in FK_FK and visited[tbl] == False:
            visited[tbl] = True
            FK_join_graph = utils.update_join_graph(tbl, FK_join_graph)
            join_order += " " + str(tbl) + utils.lonely_tbl(complete_join_graph[tbl], all_FK_join_cands)+' '
        join_order = join_order[:-1]+')'
        subqry_flag = False
      else:
        for tbl in join_candidates:
          if tbl not in FK_FK and visited[tbl] == False:
            visited[tbl] = True
            FK_join_graph = utils.update_join_graph(tbl, FK_join_graph)
            join_order += " "+str(tbl) + utils.lonely_tbl(complete_join_graph[tbl],all_FK_join_cands)+" "

    join_order = join_order.replace('  ',' ').replace(")(",") (")
    join_order_c = copy.copy(join_order)
    join_order = file+" , "+join_order
    endTime = time.time()
    print(colored(join_order, 'green'), ',',(endTime - startTime) * 1000)
