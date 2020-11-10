#!/usr/bin/env python3
from django.urls import path
from . import views


urlpatterns = [
    path("questions/", views.QuestionViewSet.as_view()),
    path("questions/<int:pk>", views.QuestionDetailViewSet.as_view()),
    path("questions/<int:pk>/vote", views.VoteViewSet.as_view({"post": "create"})),
]
