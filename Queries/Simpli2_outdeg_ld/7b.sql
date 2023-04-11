SELECT COUNT(*)
FROM movie_link AS ml
join link_type AS lt on (lt.link ='features' AND lt.id = ml.link_type_id ) 
join title AS t on (t.production_year BETWEEN 1980 AND 1984 AND ml.linked_movie_id = t.id ) 
join cast_info AS ci on (t.id = ci.movie_id AND ci.movie_id = ml.linked_movie_id ) 
join name AS n on (n.name_pcode_cf LIKE 'D%' AND n.gender='m' AND ci.person_id = n.id ) 
join aka_name AS an on (an.name LIKE '%a%' AND n.id = an.person_id AND an.person_id = ci.person_id ) 
join person_info AS pi on (pi.note ='Volker Boehm' AND n.id = pi.person_id AND pi.person_id = an.person_id AND pi.person_id = ci.person_id ) 
join info_type AS it on (it.info ='mini biography' AND it.id = pi.info_type_id );