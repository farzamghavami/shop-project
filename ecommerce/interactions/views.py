from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Comment, Rate
from .serializers import CommentSerializer, RateSerializer
from core.permissions import IsSellerOrAdmin,IsOwnerOrAdmin
from accounts.views import get_current_user_from_token

class CommentCreateView(APIView):
    """
    create a new comment
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    def post(self, request):
        current_user = get_current_user_from_token(request)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    """
    all comments
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDetailView(APIView):
    """
    read one comment
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, pk):
        comment = get_object_or_404(parent=None, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentUpdateView(APIView):
    """
    update one comment
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer

    def put(self, request, pk):
        comment = get_object_or_404(parent=None, pk=pk)
        self.check_object_permissions(comment, request.user)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(APIView):
    """
    delete one comment
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer
    def delete(self, request, pk):
        comment = get_object_or_404(parent=None, pk=pk)
        self.check_object_permissions(comment, request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class RatingDetailView(APIView):
    """
    get one rating
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer
    def get(self, request, pk):
        comment = get_object_or_404(parent=None, pk=pk)
        serializer = RateSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RatingCreateView(APIView):
    """
    create one rating
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer
    def post(self, request):
        current_user = get_current_user_from_token(request)
        srz_data = RateSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=current_user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
