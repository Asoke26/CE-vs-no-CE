SELECT COUNT(*)
FROM movie_companies AS mc
join company_name AS cn on (mc.note != '' AND (mc.note LIKE '%(USA)%' OR mc.note LIKE '%(worldwide)%') AND cn.country_code ='[us]' AND cn.id = mc.company_id ) 
join title AS t on (t.production_year BETWEEN 2005 AND 2009 AND t.id = mc.movie_id ) 
join cast_info AS ci on (ci.note IN ('(voice)', '(voice: Japanese version)', '(voice) (uncredited)', '(voice: English version)') AND t.id = ci.movie_id AND mc.movie_id = ci.movie_id ) 
join role_type AS rt on (rt.role_t ='actress' AND rt.id = ci.role_id ) 
join char_name AS chn on (chn.id = ci.person_role_id ) 
join name AS n on (n.gender ='f' AND n.name LIKE '%Ang%' AND n.id = ci.person_id ) 
join aka_name AS an on (n.id = an.person_id AND ci.person_id = an.person_id ) 
join movie_info AS mi on (mi.info != '' AND (mi.info LIKE 'Japan:%200%' OR mi.info LIKE 'USA:%200%') AND t.id = mi.movie_id AND mc.movie_id = mi.movie_id AND mi.movie_id = ci.movie_id ) 
join info_type AS it on (it.info = 'release dates' AND it.id = mi.info_type_id );