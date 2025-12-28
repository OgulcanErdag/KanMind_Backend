from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound,ValidationError
from boards.models import Board
from tasks.models import Task, Comment


class IsPartOfBoard(BasePermission):

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        # try: 
        #     board_id = int(board_id)
        # except (ValidationError, ValueError):
        #     raise ValidationError("Board nicht gefunden")
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                raise NotFound("Board nicht gefunden")
        else:
            try:
                task:Task = Task.objects.get(pk=view.kwargs.get("task_id"))
                board = task.board
            except:
                raise NotFound("Board nicht gefunden")
        return (
            request.user == board.owner or
            board.members.filter(id=request.user.id).exists()
        )


    def has_object_permission(self, request, view, obj)->bool:
        task : Task = obj
        try:
            board = task.board
        except:
            return False
        
        if request.method == "DELETE":
            return bool(request.user == board.owner or request.user == task.creator)
        
        return bool(request.user == board.owner or request.user in board.members.all())
    
class IsCommentCreator(BasePermission):
    def has_permission(self, request, view)->bool:
        try:
            comment:Comment = Comment.objects.get(pk=view.kwargs.get('comment_id'))
        except Comment.DoesNotExist:
            raise NotFound("Kommentar nicht gefunden")
        if comment:
            return bool(request.user == comment.author)
    
    def has_object_permission(self, request, view, obj)->bool:
        comment:Comment = Comment.objects.get(pk=view.kwargs.get('comment_id'))
        if request.method == "DELETE":
            return bool(request.user == comment.author )
        
    
