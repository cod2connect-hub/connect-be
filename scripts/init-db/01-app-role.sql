create role app_runtime with login password 'CHANGE_ME' noinherit;
create role app_migrator with login password 'CHANGE_ME' noinherit;

grant select, insert, update, delete on all tables in schema public to app_runtime;
alter default privileges in schema public
  grant select, insert, update, delete on tables to app_runtime;
