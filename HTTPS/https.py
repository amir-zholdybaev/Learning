"""
    Итак, какова функция протокола HTTPS?

    1 Шифрование. Информация передаётся в зашифрованном виде. По причине этого злоумышленники не могут украсть информацию,
    которой обмениваются посетители сайта, а также отследить их действия на других страницах.
    2 Аутентификация. Посетители уверены, что переходят на официальный сайт компании, а не на дубликат, сделанный
    злоумышленником.
    3 Сохранение данных. Протокол фиксирует все изменения данных. Если злоумышленник всё-таки пытался взломать защиту,
    об этом можно узнать из сохранённых данных.


    Для примера возьмём ситуацию: пользователь хочет перейти на сайт Рег.ру, который работает по безопасному протоколу HTTPS.

    1 Браузер пользователя просит предоставить SSL-сертификат.
    2 Сайт на HTTPS отправляет сертификат.
    3 Браузер проверяет подлинность сертификата в центре сертификации.
    4 Браузер и сайт договариваются о симметричном ключе при помощи асимметричного шифрования.
    5 Браузер и сайт передают зашифрованную информацию.
"""
