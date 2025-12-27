from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Board
from .permissions import IsOwnerOrAuthenticated
from .serializers import BoardSerializer, SingleBoardSerializer


class BoardListCreateView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        boards: QuerySet[Board] = Board.objects.filter(
            members=user) | Board.objects.filter(owner=user)

        return boards.distinct()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # if not queryset.exists():
        #     return Response(
        #         [{"Nichts zu tun": "Du bist noch kein Mitglied auf einem Board"}],
        #         status=status.HTTP_200_OK
        #     )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BoardSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = SingleBoardSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrAuthenticated]
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
