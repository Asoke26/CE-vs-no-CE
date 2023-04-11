SELECT COUNT(*)
FROM movie_companies AS mc
join company_type AS ct on (ct.kind ='production companies' AND ct.id = mc.company_type_id ) 
join company_name AS cn on (cn.country_code ='[de]' AND cn.id = mc.company_id ) 
join title AS t on (mc.movie_id = t.id ) 
join kind_type AS kt on (kt.kind ='movie' AND kt.id = t.kind_id ) 
join movie_info_idx AS miidx on (miidx.movie_id = t.id AND miidx.movie_id = mc.movie_id ) 
join info_type AS it on (it.info ='rating' AND it.id = miidx.info_type_id ) 
join movie_info AS mi on (mi.movie_id = t.id AND mi.movie_id = miidx.movie_id AND mi.movie_id = mc.movie_id ) 
join info_type AS it2 on (it2.info ='release dates' AND it2.id = mi.info_type_id );