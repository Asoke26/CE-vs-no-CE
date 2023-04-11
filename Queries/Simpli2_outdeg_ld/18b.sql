SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it2 on (mi_idx.info > '8.0' AND it2.info = 'rating' AND it2.id = mi_idx.info_type_id ) 
join title AS t on (t.production_year BETWEEN 2008 AND 2014 AND t.id = mi_idx.movie_id ) 
join movie_info AS mi on (mi.info IN ('Horror',  'Thriller') AND mi.note IS NULL AND t.id = mi.movie_id AND mi.movie_id = mi_idx.movie_id ) 
join info_type AS it1 on (it1.info = 'genres' AND it1.id = mi.info_type_id ) 
join cast_info AS ci on (ci.note IN ('(writer)',    '(head writer)',   '(written by)',  '(story)',  '(story editor)') AND t.id = ci.movie_id AND ci.movie_id = mi.movie_id AND ci.movie_id = mi_idx.movie_id ) 
join name AS n on (n.gender != '' AND n.gender = 'f' AND n.id = ci.person_id );