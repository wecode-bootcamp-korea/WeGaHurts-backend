from django.urls import path
from .views import CommentView

urlpatterns = [
	path('',CommentView.as_view()),
]
