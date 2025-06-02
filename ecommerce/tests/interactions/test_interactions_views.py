import pytest
from django.urls import reverse
from rest_framework import status

from interactions.models import Comment, Rate
from tests.conftest import comment, regular_user


@pytest.mark.django_db
class TestCommentCreateView:
    """
    test comment create
    """
    @pytest.fixture
    def url(self):
        return reverse ("interactions:comment-create")

    #test authenticated user can create comment with no parent
    def test_authenticate_user_can_create_no_parent_comment(self, token_regular_user_client, url,product):
        data = {
            "product": product.id,
            "text" : "this is a test comment",
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "this is a test comment"
        assert response.data

    #test authenticated user can replay to comment with parent
    def test_authenticate_user_can_replay_comment_with_parent(self, token_regular_user_client, url,product,another_user):
        parent = Comment.objects.create(product=product, text="this is a test comment",user = another_user)
        data = {
            "product": product.id,
            "text" : "this is a test comment",
            "parent": parent.id,
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "this is a test comment"
        assert response.data

    #test unauthenticated user cant create comment
    def test_unauthenticated_user_cant_create_comment(self, client, url,product):
        data = {
            "product": product.id,
            "text" : "this is a test comment",
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #test cant replay to comment with no id
    def test_invalid_parent_comment_id(self, token_regular_user_client, url, product):
        data = {
            "text": "Trying to reply to non-existent comment",
            "product": product.id,
            "parent": 9999,  #no comment with this id
        }
        response = token_regular_user_client.post(url, data=data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

@pytest.mark.django_db
class TestCommentListView:
    """
    test comment list
    """
    @pytest.fixture
    def url(self):
        return reverse ("interactions:comment-list")

    #test authenticated user can see lists of the comment
    def test_authenticate_user_can_see_list__comment(self, token_regular_user_client, url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    #tset unauthenticated user cant see
    def test_unauthenticated_user_cant_list_comment(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestCommentDetailView:
    """
    test comment detail
    """
    @pytest.fixture
    def url(self,comment):
        return reverse ("interactions:comment-detail",kwargs={"pk": comment.id})

    #test authenticated user can see comment detail
    def test_authenticate_user_can_see_detail__comment(self, token_regular_user_client, url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data

    #test unauthenticated user cant see comment detail
    def test_unauthenticated_user_cant_get_detail_comment(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestCommentUpdateView:
    """
    test comment update
    """

    @pytest.fixture
    def url(self,comment):
        return reverse ("interactions:comment-update",kwargs={"pk":comment.id})

    #test user can update his own comment
    def test_user_can_update_his_own_comment(self, token_regular_user_client, url):
        data = {
            "text": "this is a test comment2",
        }
        response = token_regular_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

    #test user cant update another one comment
    def test_another_user_cant_update_regular_user_comment(self,token_another_user_client,url):
        data = {
            "text": "this is a test comment2",
        }
        response = token_another_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    #test admin can update users comment
    def test_admin_can_update_regular_user_comment(self,token_admin_client,url):
        data = {
            "text": "this is a test comment2",
        }
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestCommentDeleteView:
    """
    test comment delete
    """

    @pytest.fixture
    def url(self,comment):
        return reverse ("interactions:comment-delete",kwargs={"pk":comment.id})

    #test user can delete his comment
    def test_user_can_delete_his_own_comment(self, token_regular_user_client, url):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    #test user cant delete other comments
    def test_another_user_cant_delete_regular_user_comment(self,token_another_user_client,url):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    #test admin can delete everyone comment
    def test_admin_cant_delete_regular_user_comment(self,token_admin_client,url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestRateCreateView:
    """
    test rate create
    """

    @pytest.fixture
    def url(self):
        return reverse ("interactions:rate-create")

    #test authenticated user can rate
    def test_authenticate_user_can_rete_product(self,url,token_regular_user_client,product):
        data = {
            "product": product.id,
            "score": 4
        }
        response = token_regular_user_client.post(url, data= data)
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    #test unauthenticated user cant rate
    def test_unauthenticated_user_cant_create_rate(self,client,url):
        response = client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #test authenticated user cant rate product with no pk
    def test_invalid_product_id(self, url, token_regular_user_client):
        data = {"product": 9999, "score": 3}
        response = token_regular_user_client.post(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

