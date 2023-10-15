import sqlite3

conn = sqlite3.connect('job_management.db')

# conn.execute('''
#     create table manager(
#         user_name varchar(20) primary key,
#         password varchar(20)
#     );
# ''')



# conn.execute('''
#     create table employee(
#         employee_id varchar primary key,
#         employee_user_name varchar,
#         employee_birthday datetime,
#         employee_hometown varchar,
#         user_name_manager varchar,
#         FOREIGN KEY (user_name_manager) REFERENCES manager(user_name) ON DELETE CASCADE
#     );
# ''')

# conn.execute('''
#     create table job(
#         job_id varchar primary key,
#         job_name varchar,
#         job_start datetime,
#         job_end datetime,
#         user_name_manager varchar,
#         FOREIGN KEY (user_name_manager) REFERENCES manager(user_name) ON DELETE CASCADE
#     );
# ''')

# conn.execute('''
#         create table team(
#              team_number varchar primary key,
#              team_name varchar,
#              describe varchar,
#              user_name_manager varchar,
#               FOREIGN KEY (user_name_manager) REFERENCES manager(user_name) ON DELETE CASCADE
#         )
#              ''')

# conn.execute('''
#     create table team_employee(
#         team_number varchar,
#         employee_id varchar,
#         FOREIGN KEY (team_number) REFERENCES team(team_number) ON DELETE CASCADE,
#         FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
#     )
# ''')

# conn.execute('''
#     create table team_job(
#         team_number varchar,
#         job_id varchar,
#         FOREIGN KEY (team_number) REFERENCES team(team_number) ON DELETE CASCADE,
#         FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE
#     );
# ''')


# conn.execute("""
#     insert into manager values ('manager','123456789TxTaaaV')
# """)


# a = conn.execute("select * from job where user_name_manager like 'ngocanh' ")
# b = a.fetchall()
# print(b)

# conn.execute("drop table team")

a =  conn.execute("delete from manager")
b = a.fetchall()
print(b)

conn.commit()
conn.close()