import os
import utils



# utils.runQueriesCost('8', '8', "off", "on", "off", "900000", True, "Pessimistic", "imdb", "implicit", False)

############++++++++++++++++++++++++++++ Cost Experiments +++++++++++++++++++++++++++++++++######################

# #runQueriesCost(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder)

# # No Index setting - HJ only setting
# utils.runQueriesCost('8', '8', "off", "on", "off", "900000", True, "TrueCard", "imdb", "implicit", False)
# utils.runQueriesCost('8', '8', "off", "on", "off", "900000", False, "TrueCard", "imdb", "implicit", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "Simpli2", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "Simpli2_pd", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "alg1", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "alg2_pd", False)

# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "alg2_pd", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "Simpli2", False)
# utils.runQueriesCost('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "Simpli2_pd", False)


# # # FK settings
# utils.runQueriesCost('8', '8', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "implicit", False)
# utils.runQueriesCost('8', '8', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "implicit", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", False)
# utils.runQueriesCost('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", False)
# utils.runQueriesCost('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "alg1", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)
# utils.runQueriesCost('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)

# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", False)
# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)

# utils.runQueriesCost('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "test", False)

# ############++++++++++++++++++++++++++++ Execution Time Experiments +++++++++++++++++++++++++++++++++######################

# #runQueriesTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index):

# # No Index
# utils.runQueriesTime('8', '8', "off", "on", "off", "900000", True, "TrueCard", "imdb", "implicit", False)
# utils.runQueriesTime('8', '8', "off", "on", "off", "900000", False, "TrueCard", "imdb", "implicit", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "Simpli2", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "Simpli2_pd", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "alg1", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", "alg2_pd", False)

# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "Simpli2", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "Simpli2_pd", False)
# utils.runQueriesTime('1', '1', "off", "on", "off", "900000", True, "TrueCard", "imdb", "alg2_pd", False)



# # Indexed Setting
# utils.runQueriesTime('8', '8', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "implicit", True)
# utils.runQueriesTime('8', '8', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "implicit", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", True)
# utils.runQueriesTime('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", True)
# utils.runQueriesTime('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "alg1", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)
# utils.runQueriesTime('1', '1', "on", "off", "off", "900000", False, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)

# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "Simpli2_outdeg_pd_ld", True)
# utils.runQueriesTime('1', '1', "on", "on", "off", "900000", True, "TrueCard", "imdb_fk", "alg2_outdegree_pd_ld", True)


# Merge cost and time files for noindex and fk index setting
# cost_dir = "/home/postgres/Simpli2-EXP-new/cost_experiments/costs/no_index/"
# cost_dir_fk = "/home/postgres/Simpli2-EXP-new/cost_experiments/costs/fk/"
# time_dir = "/home/postgres/Simpli2-EXP-new/cost_experiments/execTime/no_index"
# time_dir_fk = "/home/postgres/Simpli2-EXP-new/cost_experiments/execTime/fk/"

# utils.merge_cost_files(cost_dir)
# utils.merge_cost_files(cost_dir_fk)
# utils.merge_time_files(time_dir)
# utils.merge_time_files(time_dir_fk)


# def runQueriesCostTime(_fromLimit, _joinLimit, _nlFlag, _hjFlag, _mjFlag, _timeOut, _estFlag, _estFolder, _db, _inFolder, _index, files):
# utils.runQueriesCostTime('8', '8', 'off', 'on', 'off', '300000', True, "TrueCard_Yesta", "imdby", "FIXED_ORDER_JOB_GREEDY_OPT", False)

#non-indexed
non_indexed_inputs = ["Simpli2"]
indexed_inputs = ["implicit", "Simpli2_outdeg_ld"]

# for input_folder in non_indexed_inputs:
#     if input_folder == "implicit":
#         estimateFlgs = [True, False]
#         for est_Flag in estimateFlgs:
#             for i in range(0,5):
#                 utils.runQueriesTime('8', '8', "off", "on", "off", "900000", est_Flag, "TrueCard", "imdb", input_folder, False, i)
#     # Simpli2
#     else:
#         for i in range(1,5):
#                     utils.runQueriesTime('1', '1', "off", "on", "off", "900000", False, "TrueCard", "imdb", input_folder, False, i)

#indexed
# for input_folder in indexed_inputs:
#     if input_folder == "implicit":
#         estimateFlgs = [True, False]
#         for est_Flag in estimateFlgs:
#             for i in range(0,5):
#                 utils.runQueriesTime('8', '8', "on", "on", "off", "900000", est_Flag, "TrueCard", "imdb_fk", input_folder, False, i)
#     # Simpli2
#     else:
#         for i in range(0,5):
#                     utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", input_folder, False, i)

utils.runQueriesTime('1', '1', "on", "on", "off", "900000", False, "TrueCard", "imdb_fk", "Simpli2_outdeg_ld", False, 16)