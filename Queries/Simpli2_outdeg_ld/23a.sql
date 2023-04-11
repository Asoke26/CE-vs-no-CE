SELECT COUNT(*)
FROM complete_cast AS cc
join comp_cast_type AS cct1 on (cct1.kind = 'complete+verified' AND cct1.id = cc.status_id ) 
join title AS t on (t.production_year > 2000 AND t.id = cc.movie_id ) 
join kind_type AS kt on (kt.kind IN ('movie') AND kt.id = t.kind_id ) 
join movie_companies AS mc on (t.id = mc.movie_id AND mc.movie_id = cc.movie_id ) 
join company_type AS ct on (ct.id = mc.company_type_id ) 
join company_name AS cn on (cn.country_code = '[us]' AND cn.id = mc.company_id ) 
join movie_keyword AS mk on (t.id = mk.movie_id AND mk.movie_id = mc.movie_id AND mk.movie_id = cc.movie_id ) 
join keyword AS k on (k.id = mk.keyword_id ) 
join movie_info AS mi on (mi.note LIKE '%internet%' AND mi.info != '' AND (mi.info LIKE 'USA:% 199%'  OR mi.info LIKE 'USA:% 200%') AND t.id = mi.movie_id AND mk.movie_id = mi.movie_id AND mi.movie_id = mc.movie_id AND mi.movie_id = cc.movie_id ) 
join info_type AS it1 on (it1.info = 'release dates' AND it1.id = mi.info_type_id );