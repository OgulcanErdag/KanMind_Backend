from rest_framework import serializers
from ..models import Board
from tasks.api.seriralizers import TaskListCreateSerializer
from django.contrib.auth.models import User
from authentication.api.serializers import SimpleUserSerializer
from rest_framework.request import Request

class MembersField(serializers.Field):
    
    def to_representation(self, value:User):
        return SimpleUserSerializer(value.all(), many=True).data
    
    def to_internal_value(self, data):
        users=[]
        for pk in data:
            try:
                
                user = User.objects.get(pk=pk)
                users.append(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"Ein oder meherere User nicht vorhanden")
        return users
    

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    members = MembersField()
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'members',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        ]

    def get_member_count(self, instance):
        return instance.members.count()
    
    def get_ticket_count(self, instance):
        return instance.tasks.count()
    
    def get_tasks_to_do_count(self, instance):
        return instance.tasks.filter(status="to-do").count()
    
    def get_tasks_high_prio_count(self, instance):
        return instance.tasks.filter(priority="high").count()

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        request = self.context.get("request")
        owner = request.user if request else None

        board = Board.objects.create(owner=owner, **validated_data)

        board.members.set(members)
        return board
    
class SingleBoardSerializer(BoardSerializer):
    tasks = TaskListCreateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'tasks',
            'members'
        ]
        write_only_fields = ['members']
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request:Request = self.context.get('request')
        
        if request.method == "PATCH":
            rep['owner_data']= SimpleUserSerializer(instance.owner).data
            rep['members_data'] = SimpleUserSerializer(instance.members.all(), many=True).data
            rep.pop('members',None)
        else:
           rep['owner_id']=instance.owner_id 
           rep['members'] = SimpleUserSerializer(instance.members.all(), many=True).data
        return rep