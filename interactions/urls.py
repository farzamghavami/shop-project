from django.urls import path
from .views import (
    CommentListView,
    CommentDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    RateCreateView,
    RatingDetailView,
)

app_name = "interactions"

urlpatterns = [

    #this urls is for comment
    path("comments/", CommentListView.as_view(), name="comment-list"),
    path("comments/<int:pk>", CommentDetailView.as_view(), name="comment-detail"),
    path("comments/create", CommentCreateView.as_view(), name="comment-create"),
    path(
        "comments/update/<int:pk>", CommentUpdateView.as_view(), name="comment-update"
    ),
    path(
        "comments/delete/<int:pk>", CommentDeleteView.as_view(), name="comment-delete"
    ),

    #this urls is for rating
    path("rate/create", RateCreateView.as_view(), name="rate-create"),
    path("rate/<int:pk>", RatingDetailView.as_view(), name="rating-detail"),
]
