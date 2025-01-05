

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models
from django.contrib.auth.decorators import login_required
import json
from .models import Task


@method_decorator(csrf_exempt, name='dispatch')
class UserAuthView(View):
    def post(self, request, action):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if action == 'register':
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Missing username or password'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'User already exists'}, status=400)
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User registered successfully', 'user_id': user.id}, status=201)

        elif action == 'login':
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        elif action == 'logout':
            logout(request)
            return JsonResponse({'message': 'Logout successful'})

        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class TaskView(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        task_list = [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]
        return JsonResponse({'tasks': task_list}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        title = data.get('title')
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        task = Task.objects.create(user=request.user, title=title)
        return JsonResponse({'message': 'Task created', 'task_id': task.id}, status=201)

    def put(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        task_id = data.get('id')
        completed = data.get('completed')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.completed = completed
            task.save()
            return JsonResponse({'message': 'Task updated'}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

    def delete(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        task_id = data.get('id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'message': 'Task deleted'}, status=204)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)