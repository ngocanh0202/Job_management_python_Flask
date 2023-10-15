from sqlite3 import connect

def select_database(sql,li=""):
    conn = connect("job_management.db")
    pointer = conn.cursor()
    if not li:
        pointer.execute(sql)
        list_array = pointer.fetchall()
    else:
        pointer.execute(sql,li)
        list_array = pointer.fetchall()
    conn.commit()
    conn.close()
    return list_array

def delete_database(sql,dic=""):
    conn = connect("job_management.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    if not dic:
        cursor.execute(sql)
    else:
        cursor.execute(sql,dic)
    conn.commit()

def execute_database(sql,dic=""):
    conn = connect("job_management.db")
    pointer = conn.cursor()
    if not dic:
        pointer.execute(sql)
    else:
        pointer.execute(sql,dic)
    conn.commit()
    conn.close()

def check(sql,dic=""):
    conn = connect("job_management.db") 
    cursor = conn.cursor()
    cursor.execute(sql,dic)
    result = cursor.fetchone()
    conn.close()
    return result is not None