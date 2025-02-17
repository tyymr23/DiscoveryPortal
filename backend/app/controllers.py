import mysql.connector
from flask import request, jsonify, make_response
from .models import Project, Student, Admin, Client
from .utils import create_secret_token
import bcrypt
from dotenv import load_dotenv
import os
import pymysql.cursors
import ast
import json
import pymysql.cursors
from .models import Project, Student, Admin, Semester, Client

load_dotenv()


sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')
sql_port = int(os.getenv('MYSQL_PORT'))

def get_db_connection():
    return pymysql.connect(
    host=sql_host,
    port=sql_port,
    user=sql_user,
    password=sql_password,
    database=sql_db,
    cursorclass=pymysql.cursors.DictCursor
)

load_dotenv()

sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')

def signup():
    data = request.get_json()
    role = data['role']
    if role == 'student':
        existing_student = Student.find_by_username(data['username'])
        existing_client = Client.find_by_username(data['username'])
        existing_admin = Admin.find_by_username(data['username'])
        if existing_student or existing_client or existing_admin:
            return jsonify({'message': 'User already exists'}), 409

        # Hash the password before saving the user
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')

        user = Student(data)
        user_id = user.save()
        token = create_secret_token(user_id)
        print(f'User saved with ID: {user_id}')  # Debugging log
        response = make_response(jsonify({
            'message': 'User signed up successfully',
            'success': True,
            'user': {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'project': user.project_id
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response
    elif role == 'client':
        existing_student = Client.find_by_username(data['username'])
        if existing_student:
            return jsonify({'message': 'Client already exists'}), 409

        # Hash the password before saving the user
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')

        user = Client(data)
        user_id = user.save()
        token = create_secret_token(user_id)
        print(f'User saved with ID: {user_id}')  # Debugging log
        response = make_response(jsonify({
            'message': 'User signed up successfully',
            'success': True,
            'user': {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'project': user.owned_projects
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response

def login():
    print('Login endpoint reached')  # Debugging log
    data = request.get_json()
    user = Student.find_by_username(data['username'])
    client = Client.find_by_username(data['username'])
    admin = Admin.find_by_username(data['username'])
    
    if user:
        # Log the hashed password from the database and the entered password
        print('Stored hashed password:', user.password.encode('utf8'))  # Debugging log
        print('Entered password:', bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))  # Debugging log

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf8')):
            print('Password does not match')  # Debugging log
            return jsonify({'message': 'Incorrect username or password'}), 401
        
        id = user.save()

        token = create_secret_token(id)
        response = make_response(jsonify({
            'message': 'User logged in successfully',
            'success': True,
            'user': {
                'id': str(id),
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'project': user.project_id,
                'semester': user.semester_id
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response
    
    elif client:
        # Log the hashed password from the database and the entered password
        print('Stored hashed password:', client.password.encode('utf8'))  # Debugging log
        print('Entered password:', bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))  # Debugging log

        if not bcrypt.checkpw(data['password'].encode('utf-8'), client.password.encode('utf8')):
            print('Password does not match')  # Debugging log
            return jsonify({'message': 'Incorrect username or password'}), 401

        token = create_secret_token(client.username)
        response = make_response(jsonify({
            'message': 'User logged in successfully',
            'success': True,
            'user': {
                'username': client.username,
                'firstName': client.first_name,
                'lastName': client.last_name,
                'role': client.role,
                'project': client.owned_projects
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response
    
    elif admin:
        # Log the hashed password from the database and the entered password
        print('Stored hashed password:', admin.password.encode('utf8'))  # Debugging log
        print('Entered password:', bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))  # Debugging log

        if not bcrypt.checkpw(data['password'].encode('utf-8'), admin.password.encode('utf8')):
            print('Password does not match')  # Debugging log
            return jsonify({'message': 'Incorrect username or password'}), 401

        token = create_secret_token(admin.username)
        response = make_response(jsonify({
            'message': 'User logged in successfully',
            'success': True,
            'user': {
                'username': admin.username,
                'role': admin.role,
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response
    
    return jsonify({'message': 'No user found with the provided username'}), 404


def create_user():
    data = request.get_json()
    role = data['role']
    if role == 'student':
        existing_student = Student.find_by_username(data['username'])
        existing_client = Client.find_by_username(data['username'])
        existing_admin = Admin.find_by_username(data['username'])
        if existing_student or existing_client or existing_admin:
            return jsonify({'message': 'User already exists'}), 409

        # Hash the password before saving the user
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')

        user = Student(data)
        user_id = user.save()
        token = create_secret_token(user_id)
        print(f'User saved with ID: {user_id}')  # Debugging log
        response = make_response(jsonify({
            'message': 'User signed up successfully',
            'success': True,
            'user': {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'project': user.project_id
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response
    elif role == 'client':
        existing_student = Client.find_by_username(data['username'])
        if existing_student:
            return jsonify({'message': 'Client already exists'}), 409

        # Hash the password before saving the user
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')

        user = Client(data)
        user_id = user.save()
        token = create_secret_token(user_id)
        print(f'User saved with ID: {user_id}')  # Debugging log
        response = make_response(jsonify({
            'message': 'User successfully created',
            'success': True,
            'user': {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'project': user.owned_projects
            }
        }), 201)
        response.set_cookie('token', token, httponly=False)
        return response

def get_all_users():
    print("Accessing get_all_users")  # Debugging log
    users = Student.find_all()
    return jsonify({'success': True, 'users': [user.__dict__ for user in users]}), 200


def get_projects_by_username(username):
    student = Student.find_by_username(username)
    client = Client.find_by_username(username)
    admin = Admin.find_by_username(username)
    if student:
        p_data = Project.find_data_by_name(Project.get_name_by_id(student.project_id))
        if p_data:
            student.__dict__['projects'] = [p_data]
        else:
            student.__dict__['projects'] = []
        return jsonify({'success': True, 'user': student.__dict__}), 200
    
    if client:
        project_data = []
        if client.owned_projects:
            for project_id in client.owned_projects:
                project_data.append(Project.find_data_by_name(Project.get_name_by_id(project_id)))
        client.__dict__['projects'] = project_data
        return jsonify({'success': True, 'user': client.__dict__}), 200

    if admin:
        rows = Project.get_all()
        return jsonify({'success': True, 'projects': rows})
    
    return jsonify({'message': 'User not found'}), 404

def get_project_data(project):
    db = get_db_connection()
    cursor = db.cursor()  # Ensure you have a valid connection method
    if cursor is None:
        raise ValueError("Failed to establish a database connection.")
    cursor.execute("SELECT * FROM projects WHERE project_name = %s", (project,))
    row = cursor.fetchone()
    if row:
        client = Client.find_by_owned_project(row['project_id'])
        semester = Semester.find_by_id(row['semester_id'])
        # Parse JSON fields
        authors = Student.get_authors_by_project(row['project_id'])
        if authors:
            row['authors'] = json.dumps(authors)
        else:
            row['authors'] = "[]"
        row['date'] = Semester.get_date(row['semester_id'])
        row['keywords'] = row['keywords'].split(', ') if row['keywords'] else []
        if client:
            row['client'] = client.last_name + ", " + client.first_name
        row['semester'] = semester.semester
        row['year'] = semester.year
        return jsonify(row)
    
def get_project_by_semester(semester):
    return Semester.find_by_year_semester(semester.semester, semester.year).get_all_projects()

def get_all_open_projects():
    rows = Project.get_all_open()
    if rows:
        return jsonify(rows)
    else:
        return []
    
def add_project_to_user(username, project_title):
    print("Accessing add_project_to_user")  # Debugging log
    print("Here is the project title:", project_title)
    try:
        student = Student.find_by_username(username)
        client = Client.find_by_username(username)

        if student:
            student.project_id = Project.get_id(project_title)
            student.save()
            return jsonify({'success': True, 'message': 'Project added successfully', 'user': student.__dict__}), 200
        if client:
            if client.owned_projects:
                client.owned_projects.append(Project.add_client_to_project(project_title, client.username))
            else:
                client.owned_projects = [Project.add_client_to_project(project_title, client.username)]

            client.save()
            return jsonify({'success': True, 'message': 'Project added successfully', 'user': client.__dict__}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as error:
        print('Error adding project to user:', error)
        return jsonify({'message': str(error)}), 500


def remove_project_from_user(username, userProject):
    print("Accessing remove_project_from_user")  # Debugging log
    data = request.get_json()
    student = Student.find_by_username(username)
    client = Client.find_by_username(username)
    admin = Admin.find_by_username(username)

    if student:
        
        student.project_id = None
        
        student.save()
        
        return jsonify({'success': True, 'message': 'Project removed successfully', 'user': student.__dict__}), 200
    elif client:
        if client.owned_projects == None:
            client.owned_projects = []
        else:
            try:
                client.owned_projects.remove(Project.get_id(userProject))
            except:
                pass
        client.save()
        return jsonify({'success': True, 'message': 'Project removed successfully', 'user': client.__dict__}), 200
    elif admin:
        return jsonify({'success': True, 'message': 'Project removed successfully', 'user': admin.__dict__}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

def create_project(data):
    try:
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400

        # Mapping from incoming data keys to database column names
        field_mapping = {
            'longTitle': 'project_name',
            'abstract': 'abstract',
            'description': 'description',
            'publisher': 'publisher', 
            'deliverables': 'deliverables',
            'impact': 'impact',
            'skills': 'skills',
            'projectType': 'project_type',
            'semester': 'semester_id',
            'keywords': 'keywords'
        }

        # Validate required fields
        required_fields = ['longTitle', 'abstract', 'description', 'publisher', 'deliverables', 'impact', 'skills', 'projectType', 'semester']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        if type(data['publisher']) == dict:
            data['publisher'] = data['publisher']['client']

        print(data)

        # Create a new dictionary with the correct column names
        project_data = {field_mapping[key]: value for key, value in data.items() if key in field_mapping}

        # Create and save the project
        project = Project(project_data)
        project_id = project.save()

        # Find the client and add the project to their owned_projects
        client = Client.find_by_username(data['publisher'])
        if not client:
            return jsonify({'error': 'Client not found'}), 404

        if not hasattr(client, 'owned_projects'):
            client.owned_projects = []
        client.owned_projects.append(project_id)
        client.save()

        return jsonify({'id': project_id, 'message': 'Project created successfully and added to client', **project_data}), 201
    except KeyError as key_error:
        return jsonify({'error': f'Missing key: {key_error}'}), 400
    except Exception as error:
        print("this was the error: ", error)
        return jsonify({'error': str(error)}), 500


