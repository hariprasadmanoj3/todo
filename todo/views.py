from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Task
import logging

logger = logging.getLogger(__name__)

def addTask(request):
    """Add a new task"""
    try:
        if request.method == 'POST':
            task_content = request.POST.get('task', '').strip()
            
            # Basic validation
            if not task_content:
                messages.error(request, 'Task cannot be empty.')
                return redirect('home')
            
            if len(task_content) > 200:
                messages.error(request, 'Task is too long. Maximum 200 characters allowed.')
                return redirect('home')
            
            # Create the task
            Task.objects.create(task=task_content)
            messages.success(request, 'Task added successfully!')
        
    except Exception as e:
        logger.error(f'Error adding task: {e}')
        messages.error(request, 'An error occurred while adding the task.')
    
    return redirect('home')

def mark_as_done(request, pk):
    """Mark a task as completed"""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = True
        task.save()
        messages.success(request, f'Task marked as completed!')
        
    except Exception as e:
        logger.error(f'Error marking task as done: {e}')
        messages.error(request, 'An error occurred while updating the task.')
    
    return redirect('home')

def mark_as_undone(request, pk):
    """Mark a task as not completed"""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = False
        task.save()
        messages.success(request, f'Task marked as active!')
        
    except Exception as e:
        logger.error(f'Error marking task as undone: {e}')
        messages.error(request, 'An error occurred while updating the task.')
    
    return redirect('home')

def edit_task(request, pk):
    """Edit an existing task"""
    try:
        get_task = get_object_or_404(Task, pk=pk)
        
        if request.method == 'POST':
            new_task = request.POST.get('task', '').strip()
            
            # Basic validation
            if not new_task:
                messages.error(request, 'Task cannot be empty.')
                return render(request, 'edit_task.html', {'get_task': get_task})
            
            if len(new_task) > 200:
                messages.error(request, 'Task is too long. Maximum 200 characters allowed.')
                return render(request, 'edit_task.html', {'get_task': get_task})
            
            # Update the task
            get_task.task = new_task
            get_task.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('home')
        
        else:
            context = {'get_task': get_task}
            return render(request, 'edit_task.html', context)
    
    except Exception as e:
        logger.error(f'Error editing task: {e}')
        messages.error(request, 'An error occurred while editing the task.')
        return redirect('home')

def delete_task(request, pk):
    """Delete a task"""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        
    except Exception as e:
        logger.error(f'Error deleting task: {e}')
        messages.error(request, 'An error occurred while deleting the task.')
    
    return redirect('home')