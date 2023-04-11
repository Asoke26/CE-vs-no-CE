SELECT COUNT(*)
FROM aka_name AS a1
join name AS n1 on (a1.person_id = n1.id ) 
join cast_info AS ci on (n1.id = ci.person_id AND a1.person_id = ci.person_id ) 
join role_type AS rt on (rt.role_t ='writer' AND ci.role_id = rt.id ) 
join title AS t on (ci.movie_id = t.id ) 
join movie_companies AS mc on (t.id = mc.movie_id AND ci.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.country_code ='[us]' AND mc.company_id = cn.id );