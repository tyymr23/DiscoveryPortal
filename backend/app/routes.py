
from io import BytesIO
from flask import Blueprint, jsonify, request
import mysql.connector
import logging
from .controllers import get_all_open_projects, get_project_by_semester, signup, login, create_user, get_all_users, add_project_to_user, remove_project_from_user, create_project, get_projects_by_username, get_project_data
from dotenv import load_dotenv
import os
import pymysql.cursors
import base64
import json
from .models import Project, Student, Admin, Semester, Client
import ast
from flask import Flask, send_from_directory, send_file
import docker
import redis
import zipfile
## NEW ROUTES FOR SEMESTER:
#      /semester/create
#      /semester/close
#      /semester/open
#      /semester/delete
#      /semesters

def bytes_to_base64_str(b):
    return base64.b64encode(b).decode('utf-8')

load_dotenv()


sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')
sql_port = int(os.getenv('MYSQL_PORT'))
upload_dir="/"

def get_db_connection():
    return pymysql.connect(
    host=sql_host,
    port=sql_port,
    user=sql_user,
    password=sql_password,
    database=sql_db,
    cursorclass=pymysql.cursors.DictCursor
)

main = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@main.route('/collection/edit', methods=['POST'])
def edit_project_route():
    project_name = request.args.get('project_name')
    if not project_name:
        return jsonify({'error': 'project_name is required'}), 400

    updated_project = request.json
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
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

        # Create a new dictionary with the correct column names
        project_data = {field_mapping[key]: value for key, value in updated_project.items() if key in field_mapping}

        semester = project_data['semester_id'].split(' ')
        project_data['semester_id'] = Semester.get_id(semester[1], semester[0])

        if type(project_data['keywords']) == list:
            project_data['keywords'] = json.dumps(project_data['keywords'])

        # Update the project in the database
        cursor.execute("""
            UPDATE projects
            SET project_name=%s, abstract=%s, description=%s, publisher=%s, deliverables=%s, impact=%s, skills=%s, project_type=%s, semester_id=%s, keywords=%s
            WHERE project_name=%s
        """, (
            project_data['project_name'], project_data['abstract'], project_data['description'], project_data['publisher'], 
            project_data['deliverables'], project_data['impact'], project_data['skills'], project_data['project_type'], 
            project_data['semester_id'], project_data['keywords'], project_name
        ))
        db.commit()

        if cursor.rowcount:
            cursor.close()
            return jsonify({'message': 'Project updated successfully'})
        else:
            cursor.close()
            return jsonify({'error': 'Project not found'}), 404
    except KeyError as key_error:
        logging.error('Missing key: %s', key_error)
        return jsonify({'error': f'Missing key: {key_error}'}), 400
    except Exception as error:
        logging.error('Error updating project:', exc_info=error)
        return jsonify({'error': 'Error updating project'}), 500

@main.route('/semester/create', methods=['POST'])
def semester_create_route():
    data = request.get_json()
    semester = Semester(data)
    semester.save()
    return jsonify({'message': f'Semester created'}), 200

@main.route('/semester/close', methods=['POST'])
def semester_close_route():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')
    sem = Semester.find_by_year_semester(year, semester)
    sem.status = 'close'
    sem.save()
    return jsonify({'message': f'Semester {semester} during {year} closed'}), 200

@main.route('/semester/open', methods=['POST'])
def semester_open_route():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')
    sem = Semester.find_by_year_semester(year, semester)
    sem.status = 'open'
    sem.save()
    return jsonify({'message': f'Semester {semester} during {year} opened'}), 200

@main.route('/semester/delete', methods=['DELETE'])
def semester_delete_route():
    data = request.get_json()
    year = data.get('year')
    semester = data.get('semester')
    sem = Semester.find_by_year_semester(year, semester)
    sem.delete()
    return jsonify({'message': f'Semester {data.semster} during {data.year} deleted'}), 200

@main.route('/semesters', methods=['GET'])
def semesters_route():
    return Semester.get_all_semesters()

@main.route('/opensemesters', methods=['GET'])
def open_semesters_route():
    return Semester.get_all_open_semesters()

@main.route('/clients', methods=['GET'])
def all_clients_route():
    return Client.get_all()


@main.route('/signup', methods=['POST'])
def signup_route():
    logging.info('Signup route accessed')
    return signup()

@main.route('/login', methods=['POST'])
def login_route():
    logging.info('Login route accessed')
    return login()

@main.route('/create-user', methods=['POST'])
def create_user_route():
    logging.info('Create user route accessed')
    return create_user()

@main.route('/users', methods=['GET'])
def get_all_users_route():
    logging.info('Get all users route accessed')
    return get_all_users()

@main.route('/users/<username>/add-project', methods=['PUT'])
def add_project_to_user_route(username):
    logging.info('Add project to user route accessed')
    data = request.get_json()
    return add_project_to_user(username, data.get('projectT<username>itle'))

@main.route('/users/remove-project', methods=['GET', 'PUT'])
def remove_project_from_user_route():
    data = request.get_json()
    username = data.get('username')
    userProject = data.get('projectName')
    logging.info('Remove project from user route accessed')
    print(username)
    print(userProject)
    return remove_project_from_user(username, userProject)

@main.route('/project', methods=['POST'])
def create_project_route():
    data = request.get_json()
    return create_project(data)

# New routes for projects
# Have the search route now go through the collections api
# Either send a user, project_name, semester, or nothing
@main.route('/collections', methods=['GET', 'POST'])
def get_projects_route():
    username = request.args.get('username')
    project = request.args.get('project')
    semester = request.args.get('semester')
    try:
        if username:
            return get_projects_by_username(username)
        elif project:
            return get_project_data(project)
        elif semester:
            return get_project_by_semester(semester)
        else:
            return get_all_open_projects()
    except pymysql.MySQLError as e:
        logging.error(f'Error fetching rows: {e}')
        return jsonify({'error': 'Database error occurred'}), 500
    except ValueError as ve:
        logging.error(f'ValueError: {ve}')
        return jsonify({'error': str(ve)}), 500


@main.route('/projects', methods=['POST'])
def add_project():
    new_project = request.json
    print(new_project)
    logging.info(f'Adding new project: {new_project}')
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO projects (project_name, Abstract, Authors, Date, Keywords, Publisher)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (new_project['project_name'], new_project['Abstract'], new_project['Authors'], new_project['Date'], new_project['Keywords'], new_project['Publisher']))
        db.commit()
        cursor.close()
        return jsonify({'_id': cursor.lastrowid})
    except Exception as error:
        cursor.close()
        logging.error('Error adding project:', exc_info=error)
        return jsonify({'error': 'Error adding project'}), 500

@main.route('/collections/<project_name>/remove-author', methods=['DELETE'])
def leave_project(project_name):
    try:
        return jsonify({"message": "Author removed successfully"})
    except Exception as error:
        logging.error('Error removing author from project:', error)
        return jsonify({'error': 'Error removing author from project'}), 500
    
@main.route('/users/add-project', methods=['POST'])
def join_project():
    data = request.get_json()
    username = data.get('username')
    project = data.get('project')
    logging.info(f'Adding user to project: {project}')
    db = get_db_connection()
    cursor = db.cursor()
    try:
        add_project_to_user(username, project)
        return jsonify({"success": True, "message": f"Project {project} added to user {username}."})
    except Exception as error:
        logging.error('Error adding project to user:', error)
        return jsonify({'error': 'Error adding project to user'}), 500
    finally:
        cursor.close()

@main.route('/collections/<collection_name>/add-author', methods=['PUT'])
def add_author_to_collection(collection_name):
    data = request.get_json()
    author = data.get('author')
    print(f'Adding author {author} to collection {collection_name}')  # Debugging log
    try:
        return jsonify({'message': f'Author {author} added to project {collection_name}'}), 200
    except Exception as error:
        logging.error('Error adding author to project:', error)
        return jsonify({'error': 'Error adding author to project'}), 500
    
@main.route('/collections/delete/<collection_name>', methods=['DELETE'])
def delete_project(collection_name):
    try:
        project = Project.find_by_name(collection_name)
        client = project.get_client()
        project_id = Project.get_id(collection_name)
        project.delete()
        client.delete_project(project_id)
        return jsonify({'message': f'Deleted project {collection_name}'}), 200
    except Exception as error:
        logging.error('Error deleting project:', error)
        return jsonify({'error': 'Error deleting project'}), 500

@main.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    updated_project = request.json
    logging.info(f'Updating project with ID: {project_id} with data: {updated_project}')
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE projects
            SET project_name=%s, Abstract=%s, Authors=%s, Date=%s, Keywords=%s, Publisher=%s
            WHERE id=%s
        """, (updated_project['project_name'], updated_project['Abstract'], updated_project['Authors'], updated_project['Date'], updated_project['Keywords'], updated_project['Publisher'], project_id))
        db.commit()
        if cursor.rowcount:
            cursor.close()
            return jsonify({'message': 'Project updated successfully'})
        else:
            cursor.close()
            return jsonify({'error': 'Project not found'}), 404
    except Exception as error:
        cursor.close()
        logging.error('Error updating project:', exc_info=error)
        return jsonify({'error': 'Error updating project'}), 500


# Endpoint to fetch files for a specific project
@main.route('/projects/<project_name>', methods=['GET'])
def get_files(project_name):
    logging.info(f'Fetching files for project: {project_name}')
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT f.file_name
            FROM project_files f
            JOIN projects p ON f.project_id = p.project_id
            WHERE p.project_name = %s
        """, (project_name,))
        files = cursor.fetchall()
        
        if not files:
            logging.error(f'No files found for project: {project_name}')
            return jsonify([]), 200  # Return an empty list with a 200 status code
        
        # Map each file name to a URL
        file_urls = [
            f"{request.scheme}://{request.host}/projects/{project_name}/{file['file_name']}"
            for file in files
        ]
        
        cursor.close()
        db.close()
        
        return jsonify(file_urls)  # Send file URLs as response
    except pymysql.MySQLError as e:
        logging.error('Database error:', exc_info=e)
        return jsonify([]), 200  # Return an empty list with a 200 status code
    except Exception as e:
        logging.error('Error fetching files:', exc_info=e)
        return jsonify({'error': 'Error fetching files'}), 500

@main.route('/projects/<project_name>/<file_name>', methods=['GET'])
def serve_file(project_name, file_name):
    logging.info(f'Serving file: {file_name} from project: {project_name}')
    
    try:
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT f.project_file
            FROM project_files f
            JOIN projects p ON f.project_id = p.project_id
            WHERE p.project_name = %s AND f.file_name = %s
        """, (project_name, file_name))
        result = cursor.fetchone()
        
        if result is None:
            logging.error(f'File does not exist in database: {file_name}')
            return jsonify({'error': 'File does not exist'}), 404
        
        file_data = result['project_file']
        
        cursor.close()
        db.close()
        
        return send_file(BytesIO(file_data), download_name=file_name, as_attachment=True)
    except pymysql.MySQLError as e:
        logging.error('Database error:', exc_info=e)
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logging.error('Error serving file:', exc_info=e)
        return jsonify({'error': 'Error serving file'}), 500




# Endpoint to upload a file to a specific project
@main.route('/upload/<project_name>', methods=['POST'])
def upload_file(project_name):
    logging.info(f'Uploading files to project: {project_name}')
    if 'files' not in request.files:
        logging.error('No files part in the request')
        return jsonify({'error': 'No files part in the request'}), 400
    
    files = request.files.getlist('files')
    
    if not files or all(file.filename == '' for file in files):
        logging.error('No selected files')
        return jsonify({'error': 'No selected files'}), 400
    
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("SELECT project_id FROM projects WHERE project_name = %s", (project_name,))
        project_id = cursor.fetchone()
        
        if not project_id:
            logging.error('Project not found')
            return jsonify({'error': 'Project not found'}), 404
        
        project_id = project_id['project_id']
        
        file_urls = []
        
        for file in files:
            cursor.execute(
                "INSERT INTO project_files (project_id, file_name, project_file) VALUES (%s, %s, %s)",
                (project_id, file.filename, file.read())
            )
            file_urls.append(f"{request.scheme}://{request.host}/projects/{project_name}/{file.filename}")
        
        db.commit()
        
        logging.info(f'Files uploaded to project {project_name}')
        
        cursor.close()
        db.close()
        
        return jsonify({'message': 'Files uploaded successfully.', 'fileUrls': file_urls}), 201
    except pymysql.MySQLError as e:
        logging.error('Database error:', exc_info=e)
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logging.error('Error uploading files:', exc_info=e)
        return jsonify({'error': 'Error uploading files'}), 500


client=docker.from_env()

redis_client=redis.Redis(host=sql_host, port=6379, db=0)

# build a docker image
@main.route('/projects/<project_name>/image', methods=['GET','POST'])
def create_docker_image(project_name):
    if request.method=='POST':
        if 'zipFile' not in request.files or "volumes" not in request.form or "frontendPort" not in request.form or "dockerfilePath" not in request.form:
            return jsonify({'error': 'Data missing in request'}), 400

        zip_file=request.files['zipFile']
        image_data=request.form


        if not zip_file.filename:
            return jsonify({'error': 'No selected file'}), 400

        if not zip_file.filename.lower().endswith('.zip'):
            return jsonify({'error': 'Not a zip file'}), 400

        image_name=project_name.strip().lower().replace(" ","_")
        project_path=os.path.join(upload_dir, image_name)
        os.makedirs(project_path, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_file, 'r') as zf:
                zf.extractall(project_path)
        except:
            return jsonify({'error': 'Invalid zip file'}), 400
        
        try:
            client.images.build(
                path=os.path.join(project_path,image_data["dockerfilePath"]),
                tag=image_name,
                rm=True
            )
        except:
            return jsonify({'error': 'Error building image'}), 500

        redis_client.set(project_name,json.dumps(dict(image_data)))

        return jsonify({"message": "Form data saved uploaded"}), 200
    else:
       return "" # implement later

# get container if running
def get_running_container(project_name):
    container_name=project_name.strip().lower().replace(" ","_")
    try:
        container=client.containers.get(container_name)
        if container.status=='running':
            return container
    except:
        return None

# start  container
def start_container(project_name):
    container_data=redis_client.get(project_name)
    image_name=project_name.strip().lower().replace(" ","_")
    if container_data:
        container_data=json.loads(container_data.decode('utf-8'))
    else:
        return None

    port=container_data["frontendPort"]
    volumes={os.path.join(upload_dir,k):{"bind":v,"mode":"rw"} for k,v in json.loads(container_data["volumes"]).items() if k and v}
    
    try:
        container=client.containers.run(
            image=image_name,
            name=image_name,
            ports={port:None},
            volumes=volumes,
            remove=True,
            detach=True
        )
        return container
    except:
        return None


def get_frontend_port(container,project_name):
    container.reload()
    container_data=redis_client.get(project_name)
    if container_data:
        container_data=json.loads(container_data.decode('utf-8'))
    else:
         return None
    try:
        port=container_data["frontendPort"]
        return container.ports[port+'/tcp'][0]['HostPort']
    except:
        return None
    
# start a container
@main.route('/projects/<project_name>/run', methods=['GET'])
def run_project(project_name):
    container=get_running_container(project_name)
    if not container:
        container=start_container(project_name)
        if not container: return jsonify({'error':'Could not start container'}),400
    host_port=get_frontend_port(container,project_name)
    if not host_port: return jsonify({'error':'Error getting frontend port'}),400
    redis_client.incr(f'{project_name}-active_users')
    url=f'{sql_host}:{host_port}'
    return jsonify({'url': url})


@main.route('/projects/<project_name>/stop', methods=['POST'])
def stop_project(project_name):
    active_users=redis_client.get(f'project:{project_name}-active_users')
    if active_users is None or int(active_users)==0:
        container=get_running_container(project_name)
        if container:
            container.stop()
    else:
        redis_client.decr(f'{project_name}-active_users')
    return 200

