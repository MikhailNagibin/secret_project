# pre-professional-Olympiad

# Содержание 
- [Краткое описание](#краткое-описание)
- [Инструкция по развертыванию](#интсрукция-по-установке)
- [Ссылка на видеоролик](#ссылка-на-видеоролик)

# Краткое описание
## Цель проекта
Создать сервис для эффективного учета, контроля и распределения спортивного 
инвентаря для улучшения спортивной деятельности учащихся.
## Технологии
- Python
  - Flask
  - psycopg2
- БД
  - PostgreSQL
- HTML/CSS
## Возможности продукта 
1. Для администратора
   - Авторизация
   - Просмотр существующего инвентаря
   - Редактирование/добавление инвенторя
   - Выдача инвентаря пользователям 
   - Создание отчетов по использованию инвентаря
   - Планирование закупки нового инвентаря
2. Для пользователя
   - Авторизация/регистрация
   - Просмотр существующего инвентаря
   - Запрос на получение инвентаря и отслеживание статуса запроса
   - Создание заявки о ремонте или замене инвентаря
3. Возможности для улучшения проекта
    - Добавление новых ролей
    - Поддержка интеграции с внешними системами для автоматизации закупок
    - Создание статистики по использованию инвентаря пользователями

## База данных
При создании веб приложения  была создана бд, ер-диаграмма  которой представлена ниже
![Здесь должна быть Ер-диаграмма, но что-то пошло не так](./for_readme/img.png)
# Интсрукция по установке

Для упрощения развертывания веб-приложения был использован докер. Достаточно установить на целевой машине докер, без питона, 
среды разработки и PostgreSQL. Далее нужно скопировать 
[этот файл](docker-compose.yml) 
и положить его в папку. В той же директории нужно создать папку db и в ней ещё две папки: data  и init. Во вторую папку нужно положить [файл с инициализацией базы данных](./db/init)
Вот как должна выглядеть файловая структура:
```
/project
├──/db
|  ├──/data
|  └──/init
|     └── init.sql
└── docker-compose.yml
```
Потом открыть Docker Desktop и командную строку. В командной строке нужно войти в папку с файлом docker-compose.yml и написать следующую 
команду 
```
docker-compose -p project_name up --build 
```
После этого произойдет скачивание необходимых  образов и создание контейнера. Все изменения в базе данных будут храниться в папке ./db/data. В случае, если понадобиться удалить контейнер, все данные из базы данных остануться на машине пользователя.
*Важно!* При первом запуске приложение не сразу подключиться к бд, нужно подождать

# Ссылка на видеоролик 
Перейдя по [ссылке](https://vk.com/video886864837_456239017) можно ознакомиться с демонстрацией работы веб-приложения
