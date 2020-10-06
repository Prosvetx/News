from django.http import JsonResponse
from ...models import New
import json


def likes_control(request):
    """Проверка авторизации и контроль количества лайков от одного пользователя (не более 1)"""
    post_id = dict(json.loads(request.body.decode()))['id']
    current_user = request.user
    post = New.objects.get(id=post_id)

    if post not in current_user.likes.all():
        post.like += 1
        post.save()
        current_user.likes.add(post)
        current_likes = post.like
        data = {'current_likes': current_likes, 'id': post_id}

    elif post in current_user.likes.all() and current_user in post.likes.all():
        post.like -= 1
        post.save()
        current_user.likes.remove(post)
        current_likes = post.like
        data = {'current_likes': current_likes, 'id': post_id}

    return JsonResponse(data, status=200)
