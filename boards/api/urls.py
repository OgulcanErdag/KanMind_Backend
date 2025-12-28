from django.urls import path
from .views import BoardListCreateView,BoardSingleView

urlpatterns = [
    path('', BoardListCreateView.as_view()),
    path('<int:id>/', BoardSingleView.as_view(),name='single_board')
]
