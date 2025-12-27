from django.urls import path
from .views import TaskListCreateView,TaskUpdateDeleteView,TaskListAssignedView,TaskListReviewerView,TaskCommentsListCreateView,TaskCommentUpdateDeleteView

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('<int:task_id>/', TaskUpdateDeleteView.as_view(), name='update_task'),
    path('<int:task_id>/comments/', TaskCommentsListCreateView.as_view(), name='comments'),
    path('<int:task_id>/comments/<int:comment_id>/', TaskCommentUpdateDeleteView.as_view(), name='delete_comments'),
    path('assigned-to-me/', TaskListAssignedView.as_view(), name='assigned_task'),
    path('reviewing/', TaskListReviewerView.as_view(), name='to_review_task'),
]
