

# Пионячий клиент для пользования сервисом логгера

Клинет работает на python 3.8+ либах requests и requests-futures.
Логи отпарвляются на сервер асинхронно, 
ответа это не жди, или обработай асинхронный ответ.

## Использование 

Логгирование функции делается с использование декоратора `log_function`.
Логируется имя функции, затраченное врмея, входящие и исходящие параметры.

### Создание обычного лога
В аргументы передается название логгера    
    
    msg: str - любая строка
    data: dict - словарь с данными
    
    Остальные данные  *args, **kwargs будут добавленны под соответсвующие ключи в словарь data

Примеры:

    serv_log = ServLogger("my log") 
    
    def my_func():
        serv_log.info(
            msg="Fuck you Tony!", 
            instance=YourMom
            data={"special":"There is a fireplace!"}
        )
        serv_log.info(
            msg="Fuck you Eizekiel", 
            data={"tags":["tag1", "tag2", "tag3"], "wish":"Best Regards!"}
        )
        
### Логирующий декоратор
    
    @log_function
    def function_to_be_logged()
        ...

Для логирования метода класса с первым аргументом инстансом или моделью. как в джанге. 
Можно использовтаь флаг `is_class_method`. По умолчанию он `False`.

    class MyClass(models.Model)
        ...
        @log_function(is_class_method=True)
        def save(self, *args, **kwargs):
            ... 

Декоратор также принимает аргументы `level: str = "info"`,  `msg="Log func"`
Если при выполнении функции поломается - логу будет иметь `lvl` `error`, 
запишет ошибку и поднимет ее все равно. 

### Дополнительно

Для лучшей практики и кастомизации логов приглашаю ознакомиться 
с функциями `get_changed_values_data`, `get_jsonable_arg` в файле` utils.py` 


## Первый старт 

### Установка
 
    pip install -e git+https://github.com/mlnagents/logger_serv_py_cli.git#egg=logger_serv_py_cli

### Переменные окружения

Не забудь установить переменные или на сервис отправляться логи не будут

    LOGGER_SERV_LINK - ссылка на сервер логов
    LOGGER_AUTH_TOKEN - токен проекта, получается на сервисе логов. 
        Используется обозначение проекта и его использование (dev, battle, test, stage)
    
    
