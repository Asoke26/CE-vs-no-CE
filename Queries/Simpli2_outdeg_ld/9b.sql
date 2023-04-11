SELECT COUNT(*)
FROM aka_name AS an
join name AS n on (n.gender ='f' AND n.name LIKE '%Angel%' AND an.person_id = n.id ) 
join cast_info AS ci on (ci.note = '(voice)' AND n.id = ci.person_id AND an.person_id = ci.person_id ) 
join role_type AS rt on (rt.role_t ='actress' AND ci.role_id = rt.id ) 
join title AS t on (t.production_year BETWEEN 2007 AND 2010 AND ci.movie_id = t.id ) 
join char_name AS chn on (chn.id = ci.person_role_id ) 
join movie_companies AS mc on (mc.note LIKE '%(200%)%' AND (mc.note LIKE '%(USA)%'  OR mc.note LIKE '%(worldwide)%') AND t.id = mc.movie_id AND ci.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id );