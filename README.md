# NewsPortal
## Учебный проект "Новостной портал"
### В рамках итогового задания D14 реализовано:
- Перевод портала на английский и русский
- Возможность переключения языков - у пользователя есть возможность выбора языка из англмйского м русского
- Локализация по времени - у пользователя есть возможность переключать свой часовой пояс
- С 19 до 7 автоматически включается темная тема оформления портала
- Добавлена  возможность добавления статей на двух языках не только через панель администратора
### В рамках итогового задания D13 реализовано: 
- произведена настройка логирования
### В рамках итогового задания D8 реализовано:
- Кэширование меню приложения до изменения
- Кэширование правой колонки 15 минут
- Кэширование страниц приложения 5 минут
- Кэширование статей - до момeнта изменения
#### Дополнительно:
- Добавлено поле изображения в статью и загрузка картинок
- Парсинг статей из 10 категорий сайта https://naked-science.ru - каждые сутки парсится последняя опубликованная статья в 10 категориях и добавляется в приложение (у четом проверки на дублирование)
- Релизована подписка и отписка от рассылки новостей категории как внизу каждой статьи, так и в каждом разделе категорий
- Возможность оцениать статью (лайк/дизлайк)
- Возможность оценивать комментарии (лайк/дизлайк)
- при изменении рейтинга статьи или комментариев - перерачет рейтинга автора 
### В рамках итогового задания D7 реализовано:
- Добавлен Celery и настроен для работы с Redis
- Отправка писем при добалении статьи, по сигналу перенесена в Celery - добавляется задание после добавления поста
- Отправка еженедельной рассылки перенесена из APScheduler в Celery - настроена расссылка на 8:00, каждый понедельник
- Дополнительно добавлена возможность настройки отправки почты через SMTP mail.ru и gmail.com
### В рамках итогового задания D6 реализовано:
- Отправка приветсвенного письма при регистрации
- Отправка письма с подтверждением email
- Подписка на категории новостей (форма под статьей)
- Отправка письма при оформлении подписки на категорию
- Отправка персоанализированных писем каждому подписчику при добавлении новости в категории
- Ограничение публикации больше 3 постов в сутки (релизовано в get_context_data модели PostCreate) отключение формы для добавления поста
- Добавлен APScheduler и добавлены задания по расписанию
- Отправка персоанализированных писем каждому подписчику с еженедельным дайджестом новостей
