from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .seriralizers import TaskListCreateSerializer, CommentListCreateSerializer
from ..models import Task, Comment
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPartOfBoard,IsCommentCreator


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListCreateSerializer
    permission_classes = [IsPartOfBoard , IsAuthenticated]


class TaskListAssignedView(ListAPIView):
    serializer_class = TaskListCreateSerializer

    def get_queryset(self):
        user: User = self.request.user
        return Task.objects.filter(assignee=user)


class TaskListReviewerView(ListAPIView):
    serializer_class = TaskListCreateSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'
    serializer_class = TaskListCreateSerializer
    permission_classes = [IsPartOfBoard]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskCommentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'comment_id'
    permission_classes = [IsCommentCreator]

    def get_object(self) -> Comment:
        task_id: int = int(self.kwargs.get('task_id'))
        comment_id: int = int(self.kwargs.get('comment_id'))
        return Comment.objects.get(pk=comment_id, task__id=task_id)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskCommentsListCreateView(ListCreateAPIView):
    serializer_class = CommentListCreateSerializer
    permission_classes = [IsPartOfBoard]

    def perform_create(self, serializer: CommentListCreateSerializer):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)
        
    def get_queryset(self):
        return Comment.objects.filter(task__id=self.kwargs.get("task_id"))
