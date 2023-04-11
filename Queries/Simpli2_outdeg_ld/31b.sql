SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it2 on (it2.info = 'votes' AND it2.id = mi_idx.info_type_id ) 
join title AS t on (t.production_year > 2000 AND (t.title LIKE '%Freddy%'  OR t.title LIKE '%Jason%'  OR t.title LIKE 'Saw%') AND t.id = mi_idx.movie_id ) 
join movie_companies AS mc on (mc.note LIKE '%(Blu-ray)%' AND t.id = mc.movie_id AND mi_idx.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.name LIKE 'Lionsgate%' AND cn.id = mc.company_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mi_idx.movie_id = mk.movie_id AND mk.movie_id = mc.movie_id ) 
join keyword AS k on (k.keyword IN ('murder',   'violence',  'blood',  'gore',  'death', 'female-nudity',   'hospital') AND k.id = mk.keyword_id ) 
join movie_info AS mi on (mi.info IN ('Horror',  'Thriller') AND t.id = mi.movie_id AND mi.movie_id = mi_idx.movie_id AND mi.movie_id = mk.movie_id AND mi.movie_id = mc.movie_id ) 
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id ) 
join cast_info AS ci on (ci.note IN ('(writer)', '(head writer)',  '(written by)',  '(story)', '(story editor)') AND t.id = ci.movie_id AND ci.movie_id = mi.movie_id AND ci.movie_id = mi_idx.movie_id AND ci.movie_id = mk.movie_id AND ci.movie_id = mc.movie_id ) 
join name AS n on (n.gender = 'm' AND n.id = ci.person_id );