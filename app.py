from flask import Flask, request, render_template, redirect, jsonify, session
from waitress import serve
from connect_database import select_database, execute_database,check,delete_database
from datetime import date,datetime

app = Flask(__name__)


app.secret_key = 'jkht0201thjk'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/guide')
def guide():
    return "Add new employee, Add new job, create team and add employee into that team, display all employee, display a employee with job they take, display all job, display a job with who working on this job"
@app.route('/register')
def register():
        return render_template('register.html')
    
@app.route('/register_check', methods = ["POST","GET"])
def register_check():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        
        response_data = {}  
    
        if not username:
            response_data["error"] = "Username_empty"
            response_data["message"] = "Username must be input"
        elif check('select 1 from manager where user_name = ?',(username,)):
            response_data["error"] = "Username_had"
            response_data["message"] = "Username already exists"
        elif not password or not password_again:
            response_data["error"] = "Password_empty"
            response_data["message"] = "Password must be input"
        elif password != password_again:
            response_data["error"] = "Password_invalid"
            response_data["message"] = "Password and password again must be the same"
        else:
            response_data["success"] = "Registration_success"
            response_data["message"] = "Registration successful"
        return jsonify(response_data)
    

@app.route('/register_success', methods=['GET'])
def register_success():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
        sql = "insert into manager values (?, ?)"
        execute_database(sql,(username, password))
    return redirect('/')


@app.route('/success',methods=["POST"])
def success():
    username = request.form.get("username")
    password = request.form.get("password")
    sql = "select 1 from manager where user_name = ? and password = ? "
    mess = {}
    if check(sql,(username,password)):
        mess["success"] = "login_success"
        mess["message"] = "Login success"
        session['username'] = username  
    else:
        mess["failed"] = "login_failed"
        mess["message"] = "Your user name or password not right, please login again!"
    return jsonify(mess)

@app.route('/switch_account', methods=["POST"])
def switch_account():
    username = request.form.get("username")
    password = request.form.get("password")
    sql = "select 1 from manager where user_name = ? and password = ? "
    if check(sql,(username,password)):
        session['username'] = username
        return redirect('/home')
    return "Something wrong in system"

@app.route('/delete_account',methods=["POST"])
def delete_account():
    username = request.form.get("username")
    sql = "delete from manager where user_name = ?;"
    delete_database(sql,(username,))
    return redirect('/home')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect('/')

@app.route('/home')
def home():
    if 'username' in session:
        sql = "select * from manager where user_name not in ((?))"
        table_manager = select_database(sql,(session['username'],))
        return render_template('home.html',table_manager=table_manager)
    else:
        return redirect('/')
    
@app.route('/add_new_employee')
def add_new_employee():
    current_date = date.today()
    current_date_str = current_date.strftime('%Y-%m-%d')
    error = session.pop('error', None)
    success = session.pop('success', None)
    return render_template('add_new_employee.html',current_date = current_date_str, error = error,success=success)

@app.route('/loading_add_new_employee', methods=['POST'])
def loading_add_new_employee():
    employee_id = request.form.get("employee_id")
    employee_name = request.form.get("employee_name")
    employee_birthday = request.form.get("employee_birthday")
    employee_hometown = request.form.get("employee_hometown")
    if not (employee_id and employee_name and employee_birthday and employee_hometown):
        error = "Please fill in the complete information"
        session["error"] = error
        return redirect('/add_new_employee')
    elif check("select 1 from employee where employee_id = ? ",(employee_id,)):
        error = "Duplicate ID code"
        session["error"] = error
        return redirect('/add_new_employee')
    sql = "insert into employee values (?,?,?,?,?)"
    username_manager = session["username"]
    execute_database(sql,(employee_id,employee_name,employee_birthday,employee_hometown,username_manager))
    success = "Successfully added a new employee"
    session["success"] = success
    return redirect('/add_new_employee')

@app.route('/display_all_employee')
def display_all_employee():
    manager = session["username"]
    search_name = request.args.get('name') 
    if request.args.get('team_number'):
        team_number = request.args.get('team_number')
        sql = "select * from employee e join team_employee te on e.employee_id = te.employee_id where te.team_number = ? "
        if search_name:
            sql += "AND e.name LIKE ?"
            list_employees = select_database(sql, (team_number, f'%{search_name}%'))
        else:
            list_employees = select_database(sql, (team_number,))
        return render_template('display_all_employee.html', list_employees=list_employees,team_number=team_number)
    sql = "select * from employee where user_name_manager = ?"
    if search_name:
        sql += " AND name LIKE ?"
        list_employees = select_database(sql, (manager, f'%{search_name}%'))
    else:
        list_employees = select_database(sql, (manager,))
    return render_template('display_all_employee.html', list_employees=list_employees)

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    employee_id = request.form.get("employee_id")
    sql = "delete from employee where employee_id = ?"
    delete_database(sql,(employee_id,))
    if request.form.get('team_number'):
        team_number = request.form.get('team_number')
        return redirect(f'/display_all_employee?team_number={team_number}')
    return redirect('/display_all_employee')

@app.route('/view_employee')
def view_employee():
    employee_id = request.args.get('employee_id')
    sql = "select * from employee where employee_id = ? "
    detail_employee = select_database(sql,(employee_id,))
    if check("select 1 from team_employee where employee_id = ?",(employee_id,)):
        sql0 = "select t.* from team t join team_employee tm on t.team_number = tm.team_number where tm.employee_id = ?"
        team = select_database(sql0,(employee_id,))
        return render_template('view_employee.html',detail_employee=detail_employee,team=team)
    manager = session["username"]
    sql_team = "select * from team where user_name_manager = ?"
    all_team = select_database(sql_team,(manager,))
    return render_template('view_employee.html',detail_employee=detail_employee,all_team=all_team)

@app.route('/join_team',methods=["POST"])
def join_team():
    team_number = request.form.get('team_number')
    employee_id = request.form.get('employee_id')
    sql = "insert into team_employee values (?,?)"
    execute_database(sql,(team_number,employee_id))
    return redirect(f'/view_employee?employee_id={employee_id}')

@app.route('/remove_team',methods=["POST"])
def remove_team():
    team_number = request.form.get('team_number')
    employee_id = request.form.get('employee_id')
    sql = "delete from team_employee where team_number = ? and employee_id = ? "
    delete_database(sql,(team_number,employee_id))
    return redirect(f'/view_employee?employee_id={employee_id}')

@app.route('/add_new_job')
def add_new_job():
    current_date = date.today()
    current_date_str = current_date.strftime('%Y-%m-%d')
    error = session.pop('error', None)
    success = session.pop('success', None)
    return render_template("add_new_job.html",current_date=current_date_str,error=error,success=success)

@app.route('/loading_add_new_job', methods = ["POST"])
def loading_add_new_job():
    job_id = request.form.get("job_id")
    job_name = request.form.get("job_name")
    job_start = request.form.get("job_start")
    job_end = request.form.get("job_end")
    if not (job_id and job_name and job_start and job_end):
        error = "Please fill in the complete information"
        session["error"] = error
        return redirect('/add_new_job')
    elif check("select 1 from job where job_id = ? ",(job_id,)):
        error = "Duplicate ID code"
        session["error"] = error
        return redirect('/add_new_job')
    elif datetime.strptime(job_start, "%Y-%m-%d") > datetime.strptime(job_end, "%Y-%m-%d"):
        error = "Start date must be before or equal to end date"
        session["error"] = error
        return redirect('/add_new_job')
    
    manager = session["username"]
    sql = "insert into job values(?,?,?,?,?)"
    execute_database(sql,(job_id,job_name,job_start,job_end,manager))
    success = "Successfully added a new job"
    session['success'] = success
    return redirect('/add_new_job')

@app.route('/display_all_jobs')
def display_all_jobs():
    manager = session["username"]
    sql = "select * from job where user_name_manager = ? "
    list_jobs = select_database(sql,(manager,))
    return render_template("display_all_job.html",list_jobs=list_jobs)

@app.route('/delete_job', methods=["POST"])
def delete_job():
    job_id = request.form.get("job_id")
    sql = "delete from job where job_id = ? "
    delete_database(sql,(job_id,))
    return redirect("/display_all_jobs")

@app.route('/add_new_team', methods =['GET'])
def add_new_team():
    manager = session["username"]
    sql = "select * from team where user_name_manager = ? "
    teams = select_database(sql,(manager,))
    error = session.pop('error', None)
    success = session.pop('success', None)
    return render_template('add_new_team.html',teams=teams, error=error, success=success)
    
    
@app.route('/loading_add_new_team', methods=['POST'])
def loading_add_new_team():
    team_number= request.form.get("team_number")
    team_name = request.form.get("team_name")
    describe = request.form.get("describe")
    manager = session["username"]
    if not (team_number and team_name and describe):
        error = "Please fill in the complete information"
        session['error'] = error
        return redirect('/add_new_team')
    elif check("select 1 from team where team_number = ?",(team_number,)):
        error = "Duplicate ID code"
        session['error'] = error
        return redirect('/add_new_team')
    sql = "insert into team values(?,?,?,?)"
    execute_database(sql,(team_number,team_name,describe,manager))
    success = "Successfully added a new team"
    session['success'] = success
    return redirect('/add_new_team')

@app.route('/delete_team', methods=["POST"])
def delete_team():
    team_number = request.form.get("team_number")
    sql = "delete from team where team_number = ? "
    delete_database(sql,(team_number,))
    return redirect('/add_new_team')

@app.route('/view_team')
def view_team():
    team_number = request.args.get('team_number')
    sql = "select * from team where team_number = ? "
    detail_team = select_database(sql,(team_number,))
    # hiển thị job chưa nhận và job nhận rồi
    sql1 = "select job_id,job_name from job where job_id not in (select job_id from team_job)"
    group_no_job = select_database(sql1)
    sql2="select job.job_id, job.job_name from job inner join team_job on job.job_id = team_job.job_id where team_job.team_number = ? "
    group_job= select_database(sql2,(team_number,))
    return render_template('view_team.html',detail_team = detail_team,group_no_job=group_no_job,group_job=group_job)

@app.route('/add_new_job_to_team', methods = ['POST'])
def add_new_job_to_team():
    job_id = request.form.get("job_id")
    team_number = request.form.get('team_number')
    sql = "insert into team_job values(?,?)"
    execute_database(sql,(team_number,job_id))
    return redirect(f'/view_team?team_number={team_number}')

@app.route('/delete_job_from_team', methods=['POST'])
def delete_job_from_team():
    job_id = request.form.get("job_id")
    team_number = request.form.get('team_number')
    sql = "delete from team_job where team_number= ? and job_id = ? "
    delete_database(sql,(team_number,job_id))
    return redirect(f'/view_team?team_number={team_number}')


mode = 'dev'
if __name__ == '__main__':
    if mode == 'dev':
        app.run(host= '0.0.0.0', port = 50100, debug = True)
    else:
        serve(app,host= '0.0.0.0', port = 50100, Threads = 2)