SELECT COUNT(*)
FROM aka_name AS an
join name AS n on (n.name LIKE '%Yo%' AND n.name NOT LIKE '%Yu%' AND an.person_id = n.id ) 
join cast_info AS ci on (ci.note ='(voice: English version)' AND n.id = ci.person_id AND an.person_id = ci.person_id ) 
join role_type AS rt on (rt.role_t ='actress' AND ci.role_id = rt.id ) 
join title AS t on (t.production_year BETWEEN 2006 AND 2007 AND (t.title LIKE 'One Piece%'  OR t.title LIKE 'Dragon Ball Z%') AND ci.movie_id = t.id ) 
join movie_companies AS mc on (mc.note LIKE '%(Japan)%' AND mc.note NOT LIKE '%(USA)%' AND (mc.note LIKE '%(2006)%'  OR mc.note LIKE '%(2007)%') AND t.id = mc.movie_id AND ci.movie_id = mc.movie_id ) 
join company_name AS cn on (cn.country_code ='[jp]' AND mc.company_id = cn.id );