drop extension if exists "pg_net";

alter table "public"."experience_analysis" add column "experience_rating_facet_a" integer;

alter table "public"."experience_analysis" add column "experience_rating_facet_b" integer;

alter table "public"."experience_analysis" add column "experience_rating_facet_c" integer;

alter table "public"."experience_analysis" add column "experience_rating_facet_d" integer;

alter table "public"."experience_analysis" drop column if exists "experience_rating";


