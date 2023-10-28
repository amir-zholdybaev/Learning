from rest_framework import generics, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
    ViewSets:

    Вьюсеты введены для того, чтобы сократить код из множества Generic Views.

    Основное их отличие от Generic Views заключается в том, что внутри них нет реализации методов get, post, put, patch
    и delete

    Вместо этого они внутри себя сразу вызывают экшены(actions).
    Actions - Это методы миксинов(ModelMixins) create, list, retrieve, update, partial_update и destroy.

    Как же они понимают какой экшен вызывать при поступлении того или иного типа запроса(get, post и т.д.)?

    Дело в том, что в метод as_view() вьюсетов нужно передавать словарь, в котором сопоставляются типы запросов и экшены.
    В этих словарях ключами являются типы запросов, а значениями названия экшенов.

    urlpatterns = [
        path('api/v1/users/', UserViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
        path('api/v1/users/<int:pk>', UserViewSet.as_view({
            'get': 'retrieve',
            'post': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })),
    ]


    ViewSets в отличии от Generic Views, наследуются не от ModelMixins и GenericAPIView, а от ModelMixins и GenericViewSet.
    GenericViewSet в свою очередь наследуется от ViewSetMixin и GenericAPIView.

    ViewSetMixin добавляет тот самый функционал сопоставления типов запроса от клиента и экшенов.
    У ViewSetMixin есть метод as_view(), который как раз принимает словарь сопоставлений. После чего вьюха понимает,
    какой экшен ей вызывать при поступлении того или иного типа запроса. Этот метод переопределяет метод as_view()
    класса GenericAPIView, который наследуется им от APIView.

    Получается, что ViewSets наследуются от того же что и Generic Views(ModelMixins и GenericAPIView), плюс ViewSetMixin.
    В итоге ViewSets наследуются от ModelMixins, GenericAPIView и ViewSetMixin. Почему GenericAPIView и ViewSetMixin
    объеденены в GenericViewSet, я не знаю.

"""
