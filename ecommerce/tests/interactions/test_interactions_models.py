import pytest
from django.db import IntegrityError
from interactions.models import Rate,Comment


@pytest.mark.django_db
class TestRateModel:
    """
    test rate model
    """

    def test_rate_create(self, user, product):
        rate = Rate.objects.create(user = user, product = product,score=3)
        assert rate.user == user
        assert rate.product == product
        assert rate.score == 3

    #test unique
    def test_unique_together_constraint(self, user, product):
        Rate.objects.create(user=user, product=product, score=3)
        with pytest.raises(IntegrityError):
            Rate.objects.create(user=user, product=product, score=5)


@pytest.mark.django_db
class TestCommentModel:
    """
    test comment model
    """

    def test_comment_create(self, user, product):
        comment = Comment.objects.create(user = user, product = product, text = "this is a test comment")
        assert comment.user == user
        assert comment.product == product
        assert comment.text == "this is a test comment"
        assert comment.parent is None

    #test replay
    def test_create_replay_comment(self, user, product):
        parent_comment = Comment.objects.create(
            user = user,
            product = product,
            text = "this is a test comment"
        )
        replay_comment = Comment.objects.create(
            user = user,
            product = product,
            text = "this is a test comment",
            parent = parent_comment
        )
        assert replay_comment.parent == parent_comment
        assert replay_comment in parent_comment.replies.all()


