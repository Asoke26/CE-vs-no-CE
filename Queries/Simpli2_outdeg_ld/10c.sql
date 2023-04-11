SELECT COUNT(*)
FROM movie_companies AS mc
join company_type AS ct on (ct.id = mc.company_type_id ) 
join company_name AS cn on (cn.country_code = '[us]' AND cn.id = mc.company_id ) 
join title AS t on (t.production_year > 1990 AND t.id = mc.movie_id ) 
join cast_info AS ci on (ci.note LIKE '%(producer)%' AND t.id = ci.movie_id AND ci.movie_id = mc.movie_id ) 
join role_type AS rt on (rt.id = ci.role_id ) 
join char_name AS chn on (chn.id = ci.person_role_id );