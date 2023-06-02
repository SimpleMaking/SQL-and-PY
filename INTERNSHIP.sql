Вывести список сотрудников, получающих заработную плату большую чем у непосредственного руководителя
1. SELECT * FROM "EMPLOYEE" AS "OUTER" WHERE "OUTER"."SALARY" > (SELECT "SALARY" FROM "EMPLOYEE" AS "INNER" WHERE "OUTER"."CHIEF_ID" = "INNER"."ID")

Вывести список сотрудников, получающих максимальную заработную плату в своём отделе
2. SELECT * FROM "EMPLOYEE" AS "OUTER" WHERE "OUTER"."SALARY" = (SELECT MAX("SALARY") FROM "EMPLOYEE" AS "INNER" WHERE "OUTER"."DEPARTMENT_ID"="INNER"."DEPARTMENT_ID")

Вывести список ID отделов, количество сотрудников в которых не превышает 3 человек
3. SELECT "OUTER"."ID" FROM "DEPARTMENT" AS "OUTER" WHERE (SELECT COUNT(*) FROM "EMPLOYEE" AS "INNER" WHERE "OUTER"."ID"="INNER"."DEPARTMENT_ID") <= 3

Вывести список сотрудников, не имеющих назначенного руководителя, работающего в том-же отделе
4. SELECT * FROM "EMPLOYEE" AS "OUTER" WHERE "OUTER"."DEPARTMENT_ID" != (SELECT "INNER"."DEPARTMENT_ID" FROM "EMPLOYEE" AS "INNER" WHERE "OUTER"."CHIEF_ID"="INNER"."ID")

Найти список ID отделов с максимальной суммарной зарплатой сотрудников
5. CREATE VIEW "SALARY_BY_DEPARTMENT" AS (SELECT "DEPARTMENT_ID", SUM("SALARY") AS "SALARY" FROM "EMPLOYEE" GROUP BY "DEPARTMENT_ID");
SELECT "DEPARTMENT_ID" FROM "SALARY_BY_DEPARTMENT" WHERE "SALARY_BY_DEPARTMENT"."SALARY" = (SELECT MAX("SALARY") FROM "SALARY_BY_DEPARTMENT")