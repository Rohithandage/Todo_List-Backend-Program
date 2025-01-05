Here’s how to run your Django application and test the APIs for user authentication and task management 

Run the Code
1. Set Up Your Django Project: If you don’t already have a Django project, create one:
   django-admin startproject task_manager
   cd task_manager 
2. Create a Django App: Create an app where the Task model and views will live:
   python manage.py startapp tasks
3. Migrate the Database: Run the following commands to apply migrations:
   python manage.py makemigrations
   python manage.py migrate
4. Run the Server: Start the development server:
   python manage.py runserver

API Testing
You can use tools like Postman, cURL, or httpie to test the API.

1. Register a User
Endpoint: POST /api/auth/register/
Body (JSON):
{
  "username": "Rohit",
  "password": "Rohit123"
}
Expected Response:
{
  "message": "User registered successfully",
  "user_id": 1
}
2.  Login
Endpoint: POST /api/auth/login/
Body (JSON):
{
  "username": "testuser",
  "password": "testpassword"
}
Expected Response:
{
  "message": "Login successful"
}
3. Create a Task
Endpoint: POST /api/tasks/
Headers: Include a session cookie (Postman handles this automatically after login).
Body (JSON):
{
  "title": "My First Task 1"
}
Expected Response:
{
  "message": "Task created",
  "task_id": 1
}
4. Get All Tasks
Endpoint: GET /api/tasks/
Headers: Include the session cookie.
Expected Response:
{
  "tasks": [
{
"id":    1,
      "title": "My First Task 1",
      "completed": false
    }
  ]
}
5. Update a Task
Endpoint: PUT /api/tasks/
Headers: Include the session cookie.
Body (JSON):
{
  "id": 1,
  "completed": true
}
Expected Response:
{
  "message": "Task updated"
}
6.Delete a Task
Endpoint: DELETE /api/tasks/
Headers: Include the session cookie.
Body (JSON):
{
  "id": 1
}
Expected Response:
{
  "message": "Task deleted"
}



