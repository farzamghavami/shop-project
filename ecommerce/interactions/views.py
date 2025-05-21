from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Comment, Rate
from .serializers import CommentSerializer, RateSerializer
from core.permissions import IsSellerOrAdmin, IsOwnerOrAdmin
from accounts.views import get_current_user_from_token
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["comments"])
class CommentCreateView(APIView):
    """
    create a new comment
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        current_user = get_current_user_from_token(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["comments"])
class CommentListView(APIView):
    """
    all comments
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all()
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["comments"])
class CommentDetailView(APIView):
    """
    read one comment
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, pk):
        comment = get_object_or_404(parent=None, pk=pk)
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["comments"])
class CommentUpdateView(APIView):
    """
    update one comment
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, parent=None)
        self.check_object_permissions(comment, request.user)
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["comments"])
class CommentDeleteView(APIView):
    """
    delete one comment
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(comment, request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["rating"])
class RatingDetailView(APIView):
    """
    get one rating
    """

    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer

    def get(self, request, pk):
        comment = get_object_or_404(Comment, parent=None, pk=pk)
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["rating"])
class RateCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer

    def post(self, request):
        user = request.user
        product_id = request.data.get("product")
        score = request.data.get("score")

        # بررسی مقدارهای ورودی
        if not product_id or not score:
            return Response({"detail": "فیلدهای محصول و امتیاز الزامی هستند."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
            score = int(score)
        except ValueError:
            return Response({"detail": "مقادیر نامعتبر هستند."}, status=400)

        # جلوگیری از ثبت تکراری
        if Rate.objects.filter(user=user, product_id=product_id).exists():
            return Response({"detail": "شما قبلاً به این محصول امتیاز داده‌اید."}, status=400)

        # ذخیره امتیاز
        data = {
            "user": user.id,
            "product": product_id,
            "score": score
        }
        srz_data = self.serializer_class(data=data)
        if srz_data.is_valid():
            srz_data.save(user=user)  # کاربر رو دستی پاس می‌دیم چون read_only هست
            return Response(srz_data.data, status=201)
        return Response(srz_data.errors, status=400)