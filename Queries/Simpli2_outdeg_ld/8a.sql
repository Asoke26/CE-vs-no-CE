SELECT COUNT(*)
FROM aka_name AS an1
join name AS n1 on (n1.name LIKE '%Yo%' AND n1.name NOT LIKE '%Yu%' AND an1.person_id = n1.id ) 
join cast_info AS ci on (ci.note ='(voice: English version)' AND n1.id = ci.person_id AND an1.person_id = ci.person_id ) 
join role_type AS rt on (rt.role_t ='actress' AND ci.role_id = rt.id ) 
join title AS t on (ci.movie_id = t.id ) 
join movie_companies AS mc on (mc.note LIKE '%(Japan)%' AND mc.note NOT LIKE '%(USA)%' AND t.id = mc.movie_id AND ci.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.country_code ='[jp]' AND mc.company_id = cn.id );