SELECT COUNT(*)
FROM movie_link AS ml
join link_type AS lt on (lt.id = ml.link_type_id ) 
join title AS t on (t.production_year > 1950 AND ml.movie_id = t.id ) 
join movie_companies AS mc on (mc.note != '' AND t.id = mc.movie_id AND ml.movie_id = mc.movie_id ) 
join company_type AS ct on (ct.kind != 'production companies' AND ct.kind != '' AND mc.company_type_id = ct.id ) 
join company_name AS cn on (cn.country_code !='[pl]' AND mc.company_id = cn.id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND ml.movie_id = mk.movie_id AND mk.movie_id = mc.movie_id ) 
join keyword AS k on (k.keyword IN ('sequel',  'revenge', 'based-on-novel') AND mk.keyword_id = k.id );