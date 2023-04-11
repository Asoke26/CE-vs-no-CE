SELECT COUNT(*)
FROM movie_companies AS mc
join company_type AS ct on (mc.note NOT LIKE '%(VHS)%' AND mc.note LIKE '%(USA)%' AND mc.note NOT LIKE '%(1994)%' AND ct.kind = 'production companies' AND ct.id = mc.company_type_id ) 
join title AS t on (t.production_year > 2010 AND t.id = mc.movie_id ) 
join movie_info AS mi on (mi.info IN ('USA','America') AND t.id = mi.movie_id AND mc.movie_id = mi.movie_id ) 
join info_type AS it on (it.id = mi.info_type_id );