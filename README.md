# NewsPortal
## Учебный проект "Новостной портал"
### В рамках итогового задания D6 реализовано:
- Отправка приветсвенного письма при регистрации
- Отправка письма с подтверждением email
- Подписка на категории новостей (форма под статьей)
- Отправка письма при оформлении подписки на категорию
- Отравка персоанализированных писем каждому подписчику при добавлении новости в категории
- Ограничение публикации больше 3 постов в сутки (релизовано в get_context_data модели PostCreate) отключение формы для добавления поста
- Добавлен APScheduler и добавлены задания по расписанию
- Отравка персоанализированных писем каждому подписчику с еженедельным дайджестом новостей