SELECT COUNT(*)
FROM movie_companies AS mc
join company_name AS cn on (cn.country_code ='[us]' AND cn.id = mc.company_id ) 
join title AS t on (mc.movie_id = t.id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mc.movie_id = mk.movie_id ) 
join keyword AS k on (k.keyword ='character-name-in-title' AND mk.keyword_id = k.id );