import io
from PIL import Image
from django.template.context_processors import media
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker
from posts.models import Post, Comment
from users.models import User


class PostTestCase(APITestCase):
    PHOTO_FILE_EXTENSION = 'png'

    def photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(1, 1), color=(0, 0, 0))
        image.save(file, 'png')
        file.name = f'test_test.{self.PHOTO_FILE_EXTENSION}'
        file.seek(0)
        return file

    def setUp(self) -> None:
        self.user = User(username='testUser', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

        self.data = {
            'image': self.photo_file(),
            'text': 'hello mina',
        }

        self.multi_data = {
            'image': [self.photo_file(), self.photo_file()],
            'text': 'hello mina',
        }

        self.posts = baker.make(Post, _quantity=3)

    def test_post_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/posts/', self.data, format='multipart')
        print('rrrr:', response)

        # self.assertEqual(response.data['image'], self.data['image'])
        self.assertTrue(response.data['image'].startswith('http') and
                        response.data['image'].endswith(self.PHOTO_FILE_EXTENSION))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_list(self):
        user = self.user
        self.client.force_authenticate(user=user)
        response = self.client.get('/posts/')
        print('list:', response)

        for response_data, posts_data in zip(response.data, self.posts):
            self.assertEqual(response_data['text'], posts_data.text)
            # self.assertEqual(response_data['image'], posts_data.image)

    def test_post_retrieve(self):
        user = self.user
        self.client.force_authenticate(user=user)
        make_post = self.posts[0]
        response = self.client.get(f'/posts/{make_post.pk}/')
        print('eee;', response)

        # self.assertEqual(make_post.image, response.data['image'])
        self.assertEqual(make_post.text, response.data['text'])

    def test_post_update(self):
        user = self.user
        self.client.force_authenticate(user=user)
        make_post = self.posts[0]
        data = {
            'text': 'kkkkkkkk'
        }
        response = self.client.patch(f'/posts/{make_post.pk}/', data=data)
        self.assertEqual(response.data['text'], data['text'])

    def test_post_destroy(self):
        user = self.user
        self.client.force_authenticate(user=user)
        make_post = self.posts[0]

        response = self.client.delete(f'/posts/{make_post.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data)
        pk = Post.objects.count()
        print('pkpkpk:', pk)
        self.assertEqual(pk, 2)

    def test_like(self):
        user = self.user
        self.client.force_authenticate(user=user)
        make_post = self.posts[0]
        response = self.client.post(f'/posts/{make_post.pk}/like_toggle/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(f'/posts/{make_post.pk}/like_toggle/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTestCode(APITestCase):
    def setUp(self) -> None:
        self.user = User(username='mina', password='1234')
        self.user.set_password(self.user.password)
        self.user.save()

        self.posts = baker.make(Post, _quantity=3)
        self.post = Post(image='kekeke', text='222222', owner=self.user)
        self.post.save()

        self.comments = baker.make(Comment, _quantity=3)
        self.comment = Comment(text='7777', post=self.post, author=self.user)
        self.comment.save()

        self.queryset = Comment.objects.all()

    def test_comment_crate(self):
        user = self.user
        self.client.force_authenticate(user=user)
        post = self.post
        data = {

            "text": "tttttttt"
        }
        response = self.client.post(f'/posts/{post.pk}/comments/', data=data)

        print('tttttttt', response.data)

        # response = self.client.post(f'/comments/{self.comment.pk}/reply/', data=data)

        self.assertEqual(response.data['text'], data['text'])

    def test_comment_list(self):
        user = self.user
        self.client.force_authenticate(user=user)

        response = self.client.get(f'/posts/{self.post.pk}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for a, b in zip(response.data, self.queryset):
            self.assertEqual(a['text'], b.text)
            self.assertEqual(a['author'], b.author_id)

    def test_comment_destroy(self):
        user = self.user
        self.client.force_authenticate(user=user)

        response = self.client.delete(f'/posts/{self.post.pk}/comments/{self.comment.pk}/')
        print('ㅇㅇㅇㅇㅇㅇㅇ', response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data)


class ReplyTestCode(APITestCase):

    def setUp(self):
        self.user = User(username='mina', password='1234',)
        self.user.set_password(self.user.password)
        self.user.save()

        self.post = Post(image='kekeke', text='222222', owner=self.user)
        self.post.save()

        self.comment = Comment(text='7777', post=self.post, author=self.user)
        self.comment.save()

    def test_reply_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            # 'parent': self.comment.pk,
            # 'author': self.user.author_id,
            'text': 'RRRRRRRR',
        }

        response = self.client.post(f'/comments/{self.comment.pk}/reply/', data=data)
