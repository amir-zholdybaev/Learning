from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # path('api/v1/users/', UserViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # path('api/v1/users/<int:pk>', UserViewSet.as_view({
    #     'get': 'retrieve',
    #     'post': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),

    path('api/v1/', include(router.urls)),
]


"""
    При реализации апи с определенной моделью через VieSets, есть повторяющиеся моменты.
    А конкретно сочетания маршрутов(URL) и сопоставлений типов запросов с экшенами.

    Например:

    Если хотят реализовать получение списка объектов модели, то пишут:
    Маршрут 'api/v1/objects/' и сопоставление к нему {'get': 'list'}
    Если хотят реализовать создание объекта модели, то пишут:
    Такой же маршрут 'api/v1/objects/' и сопоставление {'post': 'create'}

    А точнее пишут один маршрут 'api/v1/objects/' и два сопоставления к нему:
    {
        'get': 'list',
        'post': 'create
    }

    Если хотят реализовать получение одного объекта, его полное и частичное изменение, а также удаление, то пишут:
    Маршрут 'api/v1/objects/<int:pk>/' и следующие сопоставления:
    {
        'get': 'retrieve',
        'post': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }

    То есть к маршруту 'api/v1/objects/' добавляют <int:pk>. Потому что для операций retrieve, update, partial_update и
    destroy нужен id объекта. А для получения списка объектов и для создания объекта id конкретного объекта указывать не
    нужно.

    В общем получается такое:
    urlpatterns = [
        path('api/v1/users/', ObjectViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
        path('api/v1/users/<int:pk>', ObjectViewSet.as_view({
            'get': 'retrieve',
            'post': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }))
    ]

    Все это довольно часто повторяющиеся паттерны, поэтому их автоматизировали через роутеры.

    Для этого у роутера нужно вызвать метод register и передать ему относительный путь, в данном случае 'objects' и
    ViewSet, например ObjectViewSet
    router.register(r'objects', ObjectViewSet)

    После этого у router формируется свойство urls, которое содержит список объектов класса Route, так называемые
    URLPatterns, которые содержат сгенерированные маршруты и их имена.
    
    [
        <URLPattern '^objects/$' [name='object-list']>,
        <URLPattern '^objects\.(?P<format>[a-z0-9]+)/?$' [name='object-list']>,
        <URLPattern '^objects/(?P<pk>[^/.]+)/$' [name='object-detail']>,
        <URLPattern '^objects/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='object-detail']>,
        <URLPattern '^$' [name='api-root']>,
        <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>
    ]

    Получается, что один URLPattern содержит маршрут, словарь сопоставлений, имя маршрута и прочие параметры.

    Префикс object, который прописан в именах маршрутов, берется из названия модели, скоторой работает ViewSet.
    Если мы хотим задать кастомный префикс отличающийся от названия модели, то в метод роутера register нам нужно
    передать параметр base_name, с нужным значением - router.register(r'objects', ObjectViewSet, base_name='users').
    Этот параметр обязателем, если во ViewSet не указан атрибут queryset.

    Роутер смотрит какие экшены есть во вьюсете и генерирует для них сопоставления.

    В общем роутер формирует маршруты(URL) и сопоставления для них. И при поступлении запроса на тот или иной маршрут,
    передает нужный словарь словарь сопоставлений во ViewSet.as_view().

    DefaultRouter отличается от SimpleRouter только тем, что у него есть маршрут, по которому возвращается список
    маршрутов роутера.

    
    Вот так можно сделать свой роутер:

    class MyCustomRouter(routers.SimpleRouter):
        routes = [
            routers.Route(
                url=r'^{prefix}/$',
                mapping={'get': 'list'},
                name='{basename}-list',
                detail=False,
                initkwargs={'suffix': 'List'}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/$',
                mapping={'get': 'retrieve'},
                name='{basename}-detail',
                detail=True,
                initkwargs={'suffix': 'Detail'}
            ),
        ]
"""