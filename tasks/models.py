from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import User
from boards.models import Board

STATUS_STATES=(
    ('to-do','To Do'),
    ('in-progress','In Progress'),
    ('review','Review'),
    ('done','Done')
)

PRIORITY_STATES=(
    ('low','Low'),
    ('medium','Medium'),
    ('high','High')
)

def one_week_from_now():
    return date.today() + timedelta(weeks=1)
    

class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE ,related_name='tasks')
    creator = models.ForeignKey(User, related_name="created_task", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=500, default="")
    status = models.CharField(max_length = 20 , choices=STATUS_STATES, default='to-do')
    priority = models.CharField(max_length = 20 , choices=PRIORITY_STATES, default='medium')
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_reviews')
    due_date = models.DateField(editable=True, default=one_week_from_now)
    comments_count = models.IntegerField(default=0)
    
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
