SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it on (mi_idx.info > '2.0' AND it.info ='rating' AND it.id = mi_idx.info_type_id ) 
join title AS t on (t.production_year > 1990 AND t.id = mi_idx.movie_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mk.movie_id = mi_idx.movie_id ) 
join keyword AS k on (k.keyword LIKE '%sequel%' AND k.id = mk.keyword_id );