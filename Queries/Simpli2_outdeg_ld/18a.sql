SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id ) 
join title AS t on (t.id = mi_idx.movie_id ) 
join movie_info AS mi on (t.id = mi.movie_id AND mi.movie_id = mi_idx.movie_id ) 
join info_type AS it1 on (it1.info = 'budget' AND it1.id = mi.info_type_id ) 
join cast_info AS ci on (ci.note IN ('(producer)',  '(executive producer)') AND t.id = ci.movie_id AND ci.movie_id = mi.movie_id AND ci.movie_id = mi_idx.movie_id ) 
join name AS n on (n.gender = 'm' AND n.name LIKE '%Tim%' AND n.id = ci.person_id );