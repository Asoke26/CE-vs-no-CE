SELECT COUNT(*)
FROM movie_info_idx AS mi_idx
join info_type AS it2 on (mi_idx.info < '8.5' AND it2.info = 'rating' AND it2.id = mi_idx.info_type_id ) 
join title AS t on (t.production_year > 2005 AND t.id = mi_idx.movie_id ) 
join kind_type AS kt on (kt.kind IN ('movie',  'episode') AND kt.id = t.kind_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mk.movie_id = mi_idx.movie_id ) 
join keyword AS k on (k.keyword != '' AND k.keyword IN ('murder',  'murder-in-title',  'blood',  'violence') AND k.id = mk.keyword_id ) 
join movie_info AS mi on (mi.info IN ('Sweden',  'Norway',  'Germany',  'Denmark',  'Swedish',  'Danish', 'Norwegian',  'German', 'USA',  'American') AND t.id = mi.movie_id AND mk.movie_id = mi.movie_id AND mi.movie_id = mi_idx.movie_id ) 
join info_type AS it1 on (it1.info = 'countries' AND it1.id = mi.info_type_id );