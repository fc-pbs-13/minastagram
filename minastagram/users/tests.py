from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User, Relation


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        # pip install model-bakery
        self.users = baker.make('users.User', _quantity=3)

        self.user = User(username='mina', password='1234')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_list(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=test_user)
        response = self.client.get('/users/')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for user_response, user in zip(response.data, self.users):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_create(self):
        data = {
            "username": "mina010@hanmail.net",
            "password": "1234"
        }
        response = self.client.post('/users/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_retrieve(self):
        instance = self.users[0]
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/users/{self.users[0].pk}/')

        self.assertEqual(instance.username, response.data['username'])

    def test_partial_update(self):
        user = self.user
        self.client.force_authenticate(user=user)
        data = {'username': 'kanggg'}

        response = self.client.patch(f'/users/{user.id}/', data=data)

        self.assertEqual(data['username'], response.data['username'])
        self.assertNotEqual(user.username, response.data['username'])

    def test_destroy(self):
        user = self.user
        self.client.force_authenticate(user=user)

        response = self.client.delete(f'/users/{user.pk}/')
        print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data)
        pk = User.objects.filter(id=user.id).count()
        print('pkpkpk:', pk)
        self.assertEqual(pk, 0)

    def test_should_login(self):
        data = {
            'username': 'mina',
            'password': '1234'
        }
        response = self.client.post('/users/login/', data=data)
        print('loginnn', response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token'])

    def test_should_logout(self):
        token = Token.objects.create(user=self.user)
        response = self.client.delete('/users/logout/', HTTP_AUTHORIZATION='Token ' + token.key)


class ProfileTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('users.User', _quantity=3)

        self.user = User(username='mina', password='1234')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_profile_create(self):
        data = {
            'username': 'mina',
            'password': '1234'
        }
        login_response = self.client.post('/users/login/', data=data)
        # print('ddddddddddd', login_response)

        response = self.client.get(f'/profile/{self.user.pk}/')
        # print('pppppppppp:', response)

        self.assertEqual(data['username'], response.data['user'])

    def test_profile_partial_update(self):
        user = self.user
        self.client.force_authenticate(user=user)
        data = {
            'introduce': 'aaaaaaa'
        }
        response = self.client.patch(f'/profile/{user.pk}/', data=data)

        self.assertEqual(response.data['introduce'], data['introduce'])


class RelationTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testUser',
            password='1111'
        )
        self.user1 = User.objects.create_user(
            username='testUser2',
            password='1111'
        )

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = {
            'from_user': self.user.id,
            'to_user': self.user1.id,
            'related_type': 'f'
        }
        response = self.client.post(f'/relation/', data=data)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)

    def test_destroy(self):
        self.client.force_authenticate(self.user)
        data = {
            'from_user': self.user.id,
            'to_user': self.user1.id,
            'related_type': 'f'
        }
        response_post = self.client.post(f'/relation/', data=data)
        self.assertTrue(response_post.status_code, status.HTTP_201_CREATED)
        a = response_post.data['id']
        # print('dadaadada', a)

        response = self.client.delete(f'/relation/{a}/')
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        user2 = User.objects.create_user(
            username='testUser3',
            password='1111'
        )
        # data = {
        #     'from_user': self.user.id,
        #     'to_user': user2.id,
        #     'related_type': 'b'
        # }
        # response = self.client.post(f'/users/{user2.id}/relation/', data=data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print('Relation:', response.data)
        relation = baker.make('users.Relation', from_user=self.user, to_user=user2, related_type='b')

        data2 = {
            'related_type': 'f'
        }
        response = self.client.patch(f'/relation/{relation.id}/', data=data2)
        # print('rerererererere', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow(self):
        from_user = baker.make('users.User')
        to_user_size = 2
        to_users = baker.make('users.User', _quantity=to_user_size)
        for to_user in to_users:
            baker.make('users.Relation', from_user=from_user, to_user=to_user, related_type='f')

        request_user = self.user
        self.client.force_authenticate(user=request_user)
        response = self.client.get(f'/users/{from_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), to_user_size)

        for response_to_user, to_user in zip(response.data, to_users):
            self.assertEqual(response_to_user['id'], to_user.id)
            self.assertEqual(response_to_user['username'], to_user.username)

    def test_follower(self):
        to_user = baker.make('users.User')
        from_user_size = 2
        from_users = baker.make('users.User', _quantity=from_user_size)
        for from_user in from_users:
            baker.make('users.Relation', from_user=from_user, to_user=to_user, related_type='f')

        request_user = self.user
        self.client.force_authenticate(user=request_user)

        response = self.client.get(f'/users/{to_user.id}/follower/')
        print('ewewewewewewe', response)

        self.assertEqual(len(response.data), from_user_size)


    # def test_block(self):
    #     self.client.force_authenticate(user=self.user)
    #     to_user = baker.make('users.User')
    #     relation = baker.make('users.Relation', from_user=self.user, to_user=to_user, related_type='b')
    #
    #     response = self.client.delete(f'/relation/{relation.id}/')
    #     print('232323232323323', relation)
    #
    #     self.fail()