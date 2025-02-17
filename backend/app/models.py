import mysql.connector
from dotenv import load_dotenv
import os
import pymysql.cursors
import json

load_dotenv()

sql_host = os.getenv('MYSQL_HOST')
sql_user = os.getenv('MYSQL_USER')
sql_password = os.getenv('MYSQL_PASSWORD')
sql_db = os.getenv('MYSQL_DB')
sql_port = int(os.getenv('MYSQL_PORT'))

class Semester:
    def __init__(self, data):
        self.year = data.get('year')
        self.semester = data.get('semester')
        self.status = data.get('status')

    def get_all_open_semesters():
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM semesters WHERE status='open'"
        
        cursor.execute(query)
        semester_data = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        if semester_data:
            return semester_data
        
        return None

    def get_all_semesters():
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM semesters"
        
        cursor.execute(query)
        semester_data = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        if semester_data:
            return semester_data
        
        return None

    def find_by_id(semester_id):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM semesters WHERE semester_id=%s"
        
        cursor.execute(query, (semester_id,))
        semester_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if semester_data:
            return Semester(semester_data)
        
        return None
    
    def find_by_year_semester(year, semester):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM semesters WHERE year=%s and semester =%s"
        
        cursor.execute(query, (year,semester,))
        semester_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if semester_data:
            return Semester(semester_data)
        
        return None
    
    def get_date(semester_id):
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT year, semester FROM semesters WHERE semester_id=%s"
        
        cursor.execute(query, (semester_id,))
        semester_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if semester_data:
            year = semester_data['year']
            semester = semester_data['semester']
            
            if semester == 'Spring':
                return f"05/01/{year}"
            elif semester == 'Fall':
                return f"12/01/{year}"
        
        return None
    
    def get_all_projects(self):
        projects = []
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM projects WHERE semester_id=%s"
        
        cursor.execute(query, (Semester.get_id(self.year, self.semester),))
        project_data = cursor.fetchone()
        
        cursor.close()
        db.close()

        if project_data:
            for project in project_data:
                projects.append(Project(project))
        return projects
    
    def get_all_students(self):
        students = []
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM students WHERE semester_id=%s"
        
        cursor.execute(query, (Semester.get_id(self.year, self.semester),))
        student_data = cursor.fetchone()
        
        cursor.close()
        db.close()

        if student_data:
            for project in student_data:
                students.append(Project(project))
        return students
    
    def get_id(year, semester):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT semester_id FROM semesters WHERE year=%s and semester =%s"
        
        cursor.execute(query, (year,semester,))
        semester_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if semester_data:
            return int(semester_data['semester_id'])
        
        return None
    
    def save(self):
        print('saving user')
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        
        cursor = db.cursor()

        semester = Semester.find_by_year_semester(self.year, self.semester)
        
        if semester:
            query = """
                UPDATE semesters SET year=%s, semester=%s, status=%s WHERE semester_id=%s
            """
            
            semester_data = (
                self.year, self.semester, self.status, Semester.get_id(self.year, self.semester)
            )
            
            cursor.execute(query, semester_data)
            
            db.commit()
            
            cursor.close()
            db.close()
            
            return Semester.get_id(self.year, self.semester)
        
        else:
            query = """
                INSERT INTO semesters (year, semester, status)
                VALUES (%s, %s, %s)
            """
            
            semester_data = (
                self.year, self.semester, self.status
            )
            
            cursor.execute(query, semester_data)
            
            db.commit()
            
            self._id = cursor.lastrowid
            
            cursor.close()
            db.close()
            
            return Semester.get_id(self.year, self.semester)
        
    def delete(self):
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
       
        cursor = db.cursor(dictionary=True)

        query = "DELETE FROM semesters WHERE semester_id=%s"

        try:
            cursor.execute(query, (Semester.get_id(self.year, self.semester),))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        cursor.close()
        db.close()

class Project:
    def __init__(self, data):
        self.project_name = data.get('collectionName')
        if self.project_name == None:
            self.project_name = data.get('project_name')
        if 'Abstract' in data.keys():
            self.abstract = data['Abstract']
        else:
            self.abstract = data['abstract']
        if 'Keywords' in data.keys():
            self.keywords = data.get('Keywords', [])
        else:
            self.keywords = data.get('keywords', [])
        if 'Publisher' in data.keys():
            self.publisher = data.get('Publisher')
        else:
            self.publisher = data.get('publisher')
        if 'ShortTitle' in data.keys():
            self.short_title = data.get('ShortTitle')
        else:
            self.short_title = data.get('short_title')
        if 'Description' in data.keys():
            self.description = data.get('Description')
        else:
            self.description = data.get('description')
        if 'Deliverable' in data.keys():
            self.deliverables = data.get('Deliverables')
        else:
            self.deliverables = data.get('deliverables')
        if 'Impact' in data.keys():
            self.impact = data.get('Impact')
        else:
            self.impact = data.get('impact')
        if 'Skills' in data.keys():
            self.skills = data.get('Skills')
        else:
            self.skills = data.get('skills')
        if 'ProjectType' in data.keys():
            self.project_type = data.get('ProjectType')
        else:
            self.project_type = data.get('project_type')
        if 'semester_id' in data.keys():
            self.semester_id = data.get('semester_id')

    def add_client_to_project(project_name, client_username):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor()
        curr_project = Project.find_by_name(project_name)
        
        if curr_project:
            # Update here
            query = """
                UPDATE projects SET client_id=%sWHERE project_name=%s
            """
            project_data = (
                json.dumps(client_username), project_name
            )
            cursor.execute(query, project_data)
            db.commit()
            
            cursor.close()
            db.close()
            
            return int(Project.get_id(project_name))
        
        return None
    
    def delete(self):
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
       
        cursor = db.cursor(dictionary=True)

        query = "DELETE FROM projects WHERE project_id=%s"

        try:
            cursor.execute(query, (Project.get_id(self.project_name),))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        cursor.close()
        db.close()

    def get_all_open():
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT 
                p.*,
                s.*,
                COUNT(st.username) AS author_count,
                CONCAT(c.last_name, ', ', c.first_name) AS client_name,
                CONCAT(s.semester, ', ', s.year) AS semester
            FROM 
                projects p
            JOIN 
                semesters s ON p.semester_id = s.semester_id
            LEFT JOIN 
                students st ON p.project_id = st.project_id
            LEFT JOIN 
                clients c ON REPLACE(p.client_id, '"', '') = c.username
            WHERE 
                s.status = 'open'
            GROUP BY 
                p.project_id, s.semester_id, c.username
        """

        try:
            cursor.execute(query)
            all_data = cursor.fetchall()
            return all_data
        except mysql.connector.Error as err:
            return None
        finally:
            cursor.close()
            db.close()

    def get_all():
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT 
            p.*,
            s.*,
            COUNT(st.username) AS author_count,
            CONCAT(c.last_name, ', ', c.first_name) AS client_name,
            CONCAT(s.semester, ', ', s.year) AS semester
        FROM 
            projects p
        JOIN 
            semesters s ON p.semester_id = s.semester_id
        LEFT JOIN 
            students st ON p.project_id = st.project_id
        LEFT JOIN 
            clients c ON REPLACE(p.client_id, '"', '') = c.username
        GROUP BY 
            p.project_id, s.semester_id, c.username
        """

        try:
            cursor.execute(query)
            all_data = cursor.fetchall()
            return all_data
        except mysql.connector.Error as err:
            return None
        finally:
            cursor.close()
            db.close()




    def get_client(self):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT publisher FROM projects WHERE project_id=%s"
        
        cursor.execute(query, (Project.get_id(self.project_name),))
        client_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if client_data:
            return Client.find_by_username(client_data['publisher'])
        
        return None

    def save(self):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor()
        curr_project = Project.find_by_name(self.project_name)
        
        if curr_project:
            # Update existing project
            query = """
                UPDATE projects 
                SET abstract=%s, keywords=%s, publisher=%s, description=%s, 
                    deliverables=%s, impact=%s, skills=%s, project_type=%s, semester_id=%s 
                WHERE project_name=%s
            """
            project_data = (
                self.abstract, json.dumps(self.keywords),
                self.publisher, self.description, self.deliverables,
                self.impact, self.skills, self.project_type, self.semester_id, self.project_name
            )
            cursor.execute(query, project_data)
            db.commit()
            
            # Retrieve the project ID
            cursor.execute("SELECT project_id FROM projects WHERE project_name=%s", (self.project_name,))
            result = cursor.fetchone()
            self.project_id = result[0] if result else None
        else:
            # Insert new project
            query = """
                INSERT INTO projects (project_name, abstract, keywords, publisher, description, 
                                      deliverables, impact, skills, project_type, semester_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            project_data = (
                self.project_name, self.abstract, json.dumps(self.keywords),
                self.publisher, self.description, self.deliverables,
                self.impact, self.skills, self.project_type, self.semester_id
            )
            cursor.execute(query, project_data)
            db.commit()
            
            self.project_id = cursor.lastrowid

        cursor.close()
        db.close()
        
        return self.project_id

    @staticmethod
    def find_by_name(project_name):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM projects WHERE project_name=%s"
        
        cursor.execute(query, (project_name,))
        project_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if project_data:
            return Project(project_data)
        
        return None
    
    @staticmethod
    def find_data_by_name(project_name):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = """
            SELECT 
                p.*,
                s.*,
                COUNT(st.username) AS author_count,
                CONCAT(c.last_name, ', ', c.first_name) AS client_name
            FROM 
                projects p
            JOIN 
                semesters s ON p.semester_id = s.semester_id
            LEFT JOIN 
                students st ON p.project_id = st.project_id
            LEFT JOIN 
                clients c ON REPLACE(p.client_id, '"', '') = c.username
            WHERE 
                p.project_name = %s
            GROUP BY 
                p.project_id, s.semester_id, c.username
        """
        
        cursor.execute(query, (project_name,))
        project_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if project_data:
            return json.dumps(project_data)
        
        return None
    
    def get_name_by_id(project_id):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT project_name FROM projects WHERE project_id=%s"
        
        cursor.execute(query, (project_id,))
        project_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if project_data:
            return project_data['project_name']
        
        return None
    
    def get_id(project_name):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT project_id FROM projects WHERE project_name=%s"
        
        cursor.execute(query, (project_name,))
        project_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if project_data:
            return int(project_data['project_id'])
        
        return None

class Student:
    def __init__(self, data):
        self.username = data['username']
        if 'firstName' in data.keys():
            self.first_name = data['firstName']
        else:
            self.first_name = data['first_name']
        if 'lastName' in data.keys():
            self.last_name = data['lastName']
        else:
            self.last_name = data['last_name']
        self.role = 'client'
        self.role = 'student'
        if 'project_id' in data.keys():
            self.project_id = data['project_id']
        else:
            self.project_id = None
        self.password = data['password']

        if 'semester_id' in data.keys():
            self.semester_id = data['semester_id']
        else:
            self.semester_id = Semester.get_all_open_semesters()[0]['semester_id']

    @staticmethod
    def find_by_username(username):
        db = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()

        user_data = None
        
        query = f"SELECT * FROM students WHERE username=%s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
    
        cursor.close()
        db.close()
        
        return Student(user_data) if user_data else None
    
    def get_authors_by_project(project_id):
        db = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()

        user_data = None
        
        query = f"SELECT * FROM students WHERE project_id=%s"
        cursor.execute(query, (project_id,))
        user_data = cursor.fetchall()
    
        cursor.close()
        db.close()

        authors = []

        for user in user_data:
            author_name = user['last_name'] + ", " + user['first_name']
            authors.append(author_name)
        
        return authors


    @staticmethod
    def find_all():
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM users"
        
        cursor.execute(query)
        users_data = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return [Student(user) for user in users_data]

    def save(self):
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        
        cursor = db.cursor()

        student = Student.find_by_username(self.username)
        
        if student:
            query = """
                UPDATE students SET username=%s, first_name=%s, last_name=%s, project_id=%s, semester_id=%s, password=%s WHERE username=%s
            """
            
            user_data = (
                self.username, self.first_name, self.last_name, self.project_id, self.semester_id, self.password, self.username
            )
            
            cursor.execute(query, user_data)
            
            db.commit()
            
            cursor.close()
            db.close()
            
            return self.username
        
        else:
            query = """
                INSERT INTO students (username, first_name, last_name, project_id, semester_id, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            user_data = (
                self.username, self.first_name,
                self.last_name,
                self.project_id, self.semester_id, self.password
            )
            
            print (user_data)
            cursor.execute(query, user_data)
            
            db.commit()
            
            self._id = cursor.lastrowid
            
            cursor.close()
            db.close()
            
            return self.username
        
class Client:
    def __init__(self, data):
        self.username = data['username']
        if 'firstName' in data.keys():
            self.first_name = data['firstName']
        else:
            self.first_name = data['first_name']
        if 'lastName' in data.keys():
            self.last_name = data['lastName']
        else:
            self.last_name = data['last_name']
        self.role = 'client'
        if 'owned_projects' in data.keys():
            self.owned_projects = json.loads(data['owned_projects'])
            if self.owned_projects == None:
                self.owned_projects = []
        else:
            self.owned_projects = []
        self.password = data['password']

    def find_by_username(username):
        db = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()

        user_data = None
        
        query = "SELECT * FROM clients WHERE username=%s"
        cursor.execute(query, (username,))
        client_data = cursor.fetchone()
    
        cursor.close()
        db.close()

        return Client(client_data) if client_data else None
    
    def get_owned_projects(self):
        projects = []
        for project in self.owned_projects:
            db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
            cursor = db.cursor(dictionary=True)
            
            query = "SELECT * FROM projects WHERE project_id=%s"
            
            cursor.execute(query, (project,))
            project_data = cursor.fetchone()
            
            cursor.close()
            db.close()
            
            if project_data:
                projects.append(Project(project_data))
        return projects
    
    def delete_project(self, project_id):
        self.owned_projects = self.owned_projects.remove(project_id)
        self.save()
    
    def save(self):
        print('saving user')
        db = mysql.connector.connect(
                host=sql_host,
                port=sql_port,
                user=sql_user,
                password=sql_password,
                database=sql_db
            )
        
        cursor = db.cursor()

        student = Client.find_by_username(self.username)
        
        if student:
            query = """
                UPDATE clients SET username=%s, first_name=%s, last_name=%s, owned_projects=%s, password=%s WHERE username=%s
            """
            
            user_data = (
                self.username, self.first_name, self.last_name, json.dumps(self.owned_projects), self.password, self.username
            )
            
            cursor.execute(query, user_data)
            
            db.commit()
            
            cursor.close()
            db.close()
            
            return self.username
        
        else:
            query = """
                INSERT INTO clients (username, first_name, last_name, owned_projects, password)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            user_data = (
                self.username, self.first_name,
                self.last_name,
                json.dumps(self.owned_projects), self.password
            )
            
            cursor.execute(query, user_data)
            
            db.commit()
            
            self._id = cursor.lastrowid
            
            cursor.close()
            db.close()
            
            return self.username
        
    def find_by_owned_project(project_id):
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT * FROM clients"
        
        cursor.execute(query)
        client_data = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        for client in client_data:
            curr_client = Client(client)
            if type(curr_client.owned_projects) == list:
                if project_id in curr_client.owned_projects:
                    return curr_client
            elif project_id in json.loads(curr_client.owned_projects):
                return curr_client
        
        return None
    
    def get_all():
        db = mysql.connector.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db
        )
        cursor = db.cursor(dictionary=True)
        
        query = "SELECT last_name, first_name, username FROM clients"
        
        cursor.execute(query)
        client_data = cursor.fetchall()
        
        cursor.close()
        db.close()

        return client_data


class Admin:
    def __init__(self, data):
        self.username = data['username']
        self.role = 'admin'
        self.password = data['password']

    @staticmethod
    def find_by_username(username):
        db = pymysql.connect(
            host=sql_host,
            port=sql_port,
            user=sql_user,
            password=sql_password,
            database=sql_db,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()
        
        query = f"SELECT * FROM admins WHERE username=%s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        
        cursor.close()
        db.close()
 
        return Admin(user_data) if user_data else None
