SELECT COUNT(*)
FROM movie_keyword AS mk
join keyword AS k on (k.keyword = 'marvel-cinematic-universe' AND k.id = mk.keyword_id ) 
join title AS t on (t.production_year > 2010 AND t.id = mk.movie_id ) 
join cast_info AS ci on (t.id = ci.movie_id AND ci.movie_id = mk.movie_id ) 
join name AS n on (n.name LIKE '%Downey%Robert%' AND n.id = ci.person_id );