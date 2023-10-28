import io


from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class UserModel:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()


def encode():
    model_obj = UserModel('Amir', 'Zholdybaev', 'amir@mail.com')
    serializer = UserSerializer(model_obj)
    print(f'serializer.data: {serializer.data}', type(serializer.data), sep='\n')

    json = JSONRenderer().render(serializer.data)
    print(f'json: {json}')


"""
    Сериализатор принимает объект модели и конвертирует его в питоновский словарь с ключами и значениями.
    Далее возвращает объект сериализатора, внутри которого есть атрибут data, содержащий этот словарь.
    При конвертации занчения не валидируются, так как достаются из базы данных.

    model_obj = UserModel('Amir', 'Zholdybaev', 'amir@mail.com')
    serializer = UserSerializer(model_obj)
    serializer.data
    type - <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
    {'first_name': 'Amir', 'last_name': 'Zholdybaev', 'email': 'amir@mail.com'}


    Далее через метод render, объекта класса JSONRenderer, этот словарь конвертируется в байтовую json строку.
    После чего готов к отправке клиенту.

    b'{"first_name":"Amir","last_name":"Zholdybaev","email":"amir@mail.com"}'

    Если в сериализатор передается не один объект модели, а Queryset(список объектов), то при инициализации
    дополнительно нужно указывать параметр many=True

    serializer = UserSerializer(model_objects, many=True)
    В этом случае serializer.data содержит список упорядоченных словарей OrderedDict.
    Каждый OrderedDict представляет собой один объект модели
"""


def decode():
    stream = io.BytesIO(b'{"first_name":"Amir","last_name":"Zholdybaev","email":"amir@mail.com"}')
    data = JSONParser().parse(stream)
    print(f'data: {data}', type(data), sep='\n')

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        print(serializer.validated_data)


"""
    Пришедшая от клиента байтовая json строка переводится в объект класса io.BytesIO, который пердставляет
    собой поток байтов в памяти.

    stream = io.BytesIO(b'{"first_name":"Amir","last_name":"Zholdybaev","email":"amir@mail.com"}')


    Далее этот объект парсится методом parse, объекта класса JSONParser. Тем самым конвертируется в python
    словарь.

    data = JSONParser().parse(stream)
    type - <class 'dict'>
    {'first_name': 'Amir', 'last_name': 'Zholdybaev', 'email': 'amir@mail.com'}


    Теперь словарь передается сериализатору, через параметр data. Данные словаря валидируются.
    Класс сериализатора возвращает объект сериализатора.

    serializer = UserSerializer(data=data)


    Внутри этого объекта есть метод is_valid(), который возвращает True в случае валидности данных и False
    в обратном случае.
    У метода есть параметр rise_exception=True - is_valid(rise_exception=True).
    Если его указать, то клиенту вернется json строка, с указанием ошибок, в случае, если какие то данные
    не прошли валидацию.

    Если данные валидны, то атрибут validated_data должен содержать упорядоченный словарь с данными, иначе
    он должен быть пустым.
    В случае не валидности данных, можно получить доступ к атрибуту serializer.errors, который содержит
    словарь с сообщениями об ошибках для каждого невалидного поля

    if serializer.is_valid():
        serializer.validated_data

    OrderedDict([('first_name', 'Amir'), ('last_name', 'Zholdybaev'), ('email', 'amir@mail.com')])

    Этот Упорядоченный словарь можно конвертировать в объект модели, данные которого можно сохранить в базу
    данных.
"""
