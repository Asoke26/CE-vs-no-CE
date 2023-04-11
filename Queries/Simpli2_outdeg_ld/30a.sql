SELECT COUNT(*)
FROM complete_cast AS cc
join comp_cast_type AS cct1 on (cct1.kind IN ('cast', 'crew') AND cct1.id = cc.subject_id ) 
join comp_cast_type AS cct2 on (cct2.kind ='complete+verified' AND cct2.id = cc.status_id ) 
join title AS t on (t.production_year > 2000 AND t.id = cc.movie_id ) 
join movie_info_idx AS mi_idx on (t.id = mi_idx.movie_id AND mi_idx.movie_id = cc.movie_id ) 
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mi_idx.movie_id = mk.movie_id AND mk.movie_id = cc.movie_id ) 
join keyword AS k on (k.keyword IN ('murder',  'violence',  'blood', 'gore', 'death',  'female-nudity',     'hospital') AND k.id = mk.keyword_id ) 
join movie_info AS mi on (mi.info IN ('Horror',   'Thriller') AND t.id = mi.movie_id AND mi.movie_id = mi_idx.movie_id AND mi.movie_id = mk.movie_id AND mi.movie_id = cc.movie_id ) 
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id ) 
join cast_info AS ci on (ci.note IN ('(writer)',  '(head writer)',  '(written by)',  '(story)',  '(story editor)') AND t.id = ci.movie_id AND ci.movie_id = mi.movie_id AND ci.movie_id = mi_idx.movie_id AND ci.movie_id = mk.movie_id AND ci.movie_id = cc.movie_id ) 
join name AS n on (n.gender = 'm' AND n.id = ci.person_id );