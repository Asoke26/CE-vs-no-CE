SELECT COUNT(*)
FROM aka_name AS an
join name AS n on (n.gender ='f' AND n.name LIKE '%An%' AND an.person_id = n.id ) 
join cast_info AS ci on (ci.note IN ('(voice)', '(voice: Japanese version)',  '(voice) (uncredited)',  '(voice: English version)') AND n.id = ci.person_id AND an.person_id = ci.person_id ) 
join role_type AS rt on (rt.role_t ='actress' AND ci.role_id = rt.id ) 
join title AS t on (ci.movie_id = t.id ) 
join char_name AS chn on (chn.id = ci.person_role_id ) 
join movie_companies AS mc on (t.id = mc.movie_id AND ci.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id );