from django.shortcuts import render
from django.db.models import Q
from todo.models import Task
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Display the home page with tasks"""
    try:
        # Get search query if any
        search_query = request.GET.get('search', '').strip()
        
        # Base querysets
        tasks_queryset = Task.objects.filter(is_completed=False)
        completed_tasks_queryset = Task.objects.filter(is_completed=True)
        
        # Apply search filter if provided
        if search_query:
            tasks_queryset = tasks_queryset.filter(task__icontains=search_query)
            completed_tasks_queryset = completed_tasks_queryset.filter(task__icontains=search_query)
        
        # Order tasks
        tasks = tasks_queryset.order_by('-updated_at')
        completed_tasks = completed_tasks_queryset.order_by('-updated_at')
        
        context = {
            'tasks': tasks,
            'completed_tasks': completed_tasks,
            'search_query': search_query,
        }
        
        return render(request, 'home.html', context)
    
    except Exception as e:
        logger.error(f'Error loading home page: {e}')
        # Return empty context in case of error
        context = {
            'tasks': [],
            'completed_tasks': [],
            'search_query': '',
        }
        return render(request, 'home.html', context)