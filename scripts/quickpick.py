import sys,os
import random
from datetime import datetime

QUERY_PATH = "/home/postgres/Simpli2-EXP-new/Queries/implicit/"

files = ['13d']

def Random_Generate(_no_of_edges):
	random.seed(None)
	x = random.randint(0,sys.maxsize)
	h = random.randint(0,sys.maxsize)

	return (x ^ ((h & 1) << 31))%_no_of_edges

# Connect Postgres
def get_explain(_query) :
	connection = psycopg2.connect(host=host, database=db, user=usr, password=pwd)
	cursor = connection.cursor()
	cursor.execute("set from_collapse_limit = 1;")
	cursor.execute("set join_collapse_limit = 1;")

	# collect the plan



	connection.close()

wF = open("/home/postgres/Simpli2-EXP-new/plans/13d.txt", 'w')
for file in files:
	print("####################### Query # ",file," ########################################")

	query = open(QUERY_PATH+file+".sql",'r').read()
	
	FROM = query.split("WHERE")[0].split("FROM")[1]
	FROM = FROM.split(',')
	AS_MAPPING = dict()
	for tbl_as in FROM:
	    tbl = tbl_as.split("AS")[0].strip()
	    as_ = tbl_as.split("AS")[1].strip()
	    AS_MAPPING[as_] = tbl


## Step 1 : Find all the edges
	query_lines = open(QUERY_PATH+file+".sql",'r').readlines()

	whr_flag = False
	EDGES = []
	JOIN_GRAPH = dict()

	for key in AS_MAPPING.keys():
		JOIN_GRAPH[key] = list()

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
				continue
			left = predicate.split('=')[0].strip()
			right = predicate.split('=')[1].strip()
			if '.' in left and '.' in right and 'id' in predicate:
				left_key = left.split('.')[0]
				right_key = right.split('.')[0]
				JOIN_GRAPH[left_key].append(predicate)
				JOIN_GRAPH[right_key].append(predicate)
				EDGES.append(predicate)


## Step 2 : Quickpick algorithm
	# 1 - Initialize cost buffer
	# 2 - Iterate over edges
		## If not first edge then check if current edge any connection with existing edges
			### If yes, then add it to already visited list or move to next iteration
		## Check if all the edges are visited

	valid_JOINS = []
	visited_cache = []
	planNo = 0
	print(len(EDGES))
	for i in range(10000):
		EDGES_copy = list()
		EDGES_copy = EDGES.copy()
		
		
		c = 0
		while 1:
			c += 1
			edge_no = Random_Generate(len(EDGES_copy))
			
			random_edge = EDGES_copy[edge_no]
			left_tbl = random_edge.strip().split('=')[0].strip().split('.')[0]
			right_tbl = random_edge.strip().split('=')[1].strip().split('.')[0]

			if left_tbl in visited_cache or right_tbl in visited_cache or len(visited_cache) == 0:
				if left_tbl not in visited_cache:
					visited_cache.append(left_tbl)
				if right_tbl not in visited_cache:
					visited_cache.append(right_tbl)
				EDGES_copy.remove(random_edge)
			else: continue

			if len(visited_cache) == len(AS_MAPPING.keys()):
				print(visited_cache)
				plan = ' '.join(visited_cache)
				id_plan = str(planNo) + ' : ' + plan
				# if plan not in valid_JOINS:
				valid_JOINS.append(plan)
				wF.write(id_plan + '\n')
				planNo += 1
				visited_cache.clear()
				break
wF.close()



