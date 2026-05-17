# API организационной структуры

REST API для управления иерархической структурой подразделений и сотрудников компании.

## 🚀 Технологии

- **FastAPI** - современный веб-фреймворк
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy ORM** - объектно-реляционное отображение
- **Alembic** - миграции базы данных
- **Docker** - контейнеризация
- **Pydantic** - валидация данных

## 📋 Функциональность

- ✅ Создание, чтение, обновление, удаление подразделений
- ✅ Создание сотрудников в подразделениях
- ✅ Древовидная структура подразделений (до глубины 5 уровней)
- ✅ Каскадное удаление или переназначение сотрудников
- ✅ Валидация данных (уникальность названий, защита от циклов)
- ✅ Автоматическая документация API (Swagger/ReDoc)

# 🚀 Запуск проекта
+ Клонируйте репозиторий и перейдите в папку проекта
```
git clone https://github.com/GGGamzat/UnitStaff.git
cd UnitStaff
```

+ Соберите и запустите с помощью Docker
```
docker-compose up --build
```

# 📡 API Эндпоинты

1. Создать корневое подразделение
```
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "IT Department",
    "parent_id": null
  }'
```

2. Создать дочернее подразделение
```
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend Team",
    "parent_id": 1
  }'
```

3. Создать несколько подразделений для теста
```
# IT отдел
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{"name": "IT Department", "parent_id": null}'

# HR отдел
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{"name": "HR Department", "parent_id": null}'

# Frontend команда (дочерняя IT)
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Frontend Team", "parent_id": 1}'

# DevOps команда (дочерняя IT)
curl -X POST "http://localhost:8000/departments/" \
  -H "Content-Type: application/json" \
  -d '{"name": "DevOps Team", "parent_id": 1}'
```

4. Создать сотрудника в конкретном отделе
```
curl -X POST "http://localhost:8000/departments/1/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Иван Иванов",
    "position": "Senior Developer",
    "hired_at": "2024-01-15"
  }'
```

5. Получить подразделение (глубина 1, с сотрудниками)
```
curl "http://localhost:8000/departments/1?depth=1&include_employees=true"
```

6. Получить подразделение без сотрудников
```
curl "http://localhost:8000/departments/1?depth=2&include_employees=false"
```

7. Получить подразделение с максимальной глубиной
```
curl "http://localhost:8000/departments/1?depth=5&include_employees=true"
```

8. Получить всю структуру организации
```
curl "http://localhost:8000/departments/1?depth=3&include_employees=true"
```

9. Переименовать подразделение
```
curl -X PATCH "http://localhost:8000/departments/2" \
  -H "Content-Type: application/json" \
  -d '{"name": "Backend Development Team"}'
```

10. Переместить подразделение в другой отдел
```
# Переместить отдел с ID=3 в отдел с ID=2
curl -X PATCH "http://localhost:8000/departments/3" \
  -H "Content-Type: application/json" \
  -d '{"parent_id": 2}'
```

11. Сделать подразделение корневым
```
# Установить parent_id = null
curl -X PATCH "http://localhost:8000/departments/4" \
  -H "Content-Type: application/json" \
  -d '{"parent_id": null}'
```

12. Каскадное удаление (удалить отдел и всё его содержимое)
```
curl -X DELETE "http://localhost:8000/departments/3?mode=cascade"
```

13. Удаление с переназначением сотрудников
```
# Сотрудники отдела 4 перейдут в отдел 2
curl -X DELETE "http://localhost:8000/departments/4?mode=reassign&reassign_to_department_id=2"
```

14. даление корневого отдела с переназначением
```
curl -X DELETE "http://localhost:8000/departments/1?mode=reassign&reassign_to_department_id=2"
```