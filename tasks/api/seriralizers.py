from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Task,Comment
from authentication.api.serializers import SimpleUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_full_name(user):
    return f'{user.username} {user.last_name}'.strip()


class TaskListCreateSerializer(serializers.ModelSerializer):
    # Serializer get's used to display the needed data only
    assignee = SimpleUserSerializer(read_only=True)
    reviewer = SimpleUserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(  # need id for corresponding model-relation (PK) and disable required to allow Null
        queryset=User.objects.all(), source='assignee', write_only=True, required=False)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'comments_count', 'board', 'assignee', 'reviewer', 'assignee_id',
                  'reviewer_id', 'due_date', 'creator']


class TaskCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['comments_count']


class CommentListCreateSerializer(serializers.ModelSerializer):
    
    author = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        return get_user_full_name(obj.author)
