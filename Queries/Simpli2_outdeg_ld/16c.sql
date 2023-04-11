SELECT COUNT(*)
FROM movie_companies AS mc
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id ) 
join title AS t on (t.episode_nr < 100 AND t.id = mc.movie_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mc.movie_id = mk.movie_id ) 
join keyword AS k on (k.keyword ='character-name-in-title' AND mk.keyword_id = k.id ) 
join cast_info AS ci on (ci.movie_id = t.id AND ci.movie_id = mc.movie_id AND ci.movie_id = mk.movie_id ) 
join name AS n on (n.id = ci.person_id ) 
join aka_name AS an on (an.person_id = n.id AND an.person_id = ci.person_id );