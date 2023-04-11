SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id ) 
join title AS t on (t.id = mi_idx.movie_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mi_idx.movie_id = mk.movie_id ) 
join keyword AS k on (k.keyword IN ('murder', 'blood',   'gore',   'death',  'female-nudity') AND k.id = mk.keyword_id ) 
join movie_info AS mi on (mi.info = 'Horror' AND t.id = mi.movie_id AND mi.movie_id = mi_idx.movie_id AND mi.movie_id = mk.movie_id ) 
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id ) 
join cast_info AS ci on (ci.note IN ('(writer)', '(head writer)', '(written by)', '(story)',  '(story editor)') AND t.id = ci.movie_id AND ci.movie_id = mi.movie_id AND ci.movie_id = mi_idx.movie_id AND ci.movie_id = mk.movie_id ) 
join name AS n on (n.gender = 'm' AND n.id = ci.person_id );