# 📦 Ручная публикация на PyPI - Инструкция

## ❌ Проблема

При попытке загрузки на PyPI возникает ошибка:
```
ConnectionResetError: [WinError 10054] Удаленный хост принудительно разорвал существующее подключение
```

Это проблема с вашим интернет-провайдером или файрволом, который блокирует загрузку больших файлов на PyPI.

## ✅ Решения

### Вариант 1: GitHub Actions (РЕКОМЕНДУЕТСЯ) 🎯

Это обойдет проблемы с вашей сетью, так как загрузка будет с серверов GitHub.

#### Шаг 1: Добавить PyPI токен в GitHub

1. Откройте: https://github.com/f1sherFM/My_1st_library_python/settings/secrets/actions

2. Нажмите **"New repository secret"**

3. Заполните:
   - **Name:** `PYPI_API_TOKEN`
   - **Secret:** Ваш PyPI API токен (начинается с `pypi-`)
   
4. Нажмите **"Add secret"**

#### Шаг 2: Создать GitHub Release

1. Откройте: https://github.com/f1sherFM/My_1st_library_python/releases/new

2. Заполните форму:
   - **Choose a tag:** Выберите `v0.4.5` из списка
   - **Release title:** `v0.4.5 - Critical Bug Fixes`
   - **Description:** Скопируйте текст из файла `RELEASE_NOTES_v0.4.5.md`

3. Нажмите **"Publish release"**

4. **Готово!** GitHub Actions автоматически:
   - Соберет пакет
   - Проверит его
   - Загрузит на PyPI

5. Проверьте статус:
   - Откройте: https://github.com/f1sherFM/My_1st_library_python/actions
   - Найдите workflow "Publish Python Package to PyPI"
   - Дождитесь зеленой галочки ✅

6. Проверьте на PyPI:
   - https://pypi.org/project/fishertools/

---

### Вариант 2: Использовать VPN

Если у вас есть VPN:

1. Подключитесь к VPN (желательно к серверу в США или Европе)

2. Запустите команду:
```bash
python -m twine upload dist/fishertools-0.4.5*
```

3. Введите ваш PyPI API токен когда попросит

---

### Вариант 3: Использовать другую сеть

Попробуйте загрузить с другой сети:

1. Мобильный интернет (раздача с телефона)
2. Другой Wi-Fi
3. Интернет на работе/в университете

Команда:
```bash
python -m twine upload dist/fishertools-0.4.5*
```

---

### Вариант 4: Использовать TestPyPI сначала

Проверьте, работает ли загрузка на TestPyPI:

```bash
python -m twine upload --repository testpypi dist/fishertools-0.4.5*
```

Если это работает, значит проблема специфична для основного PyPI.

---

## 🎯 Рекомендация

**Используйте Вариант 1 (GitHub Actions)** - это самый надежный способ:

1. ✅ Не зависит от вашей сети
2. ✅ Автоматизирован
3. ✅ Работает для всех будущих релизов
4. ✅ Логи доступны в GitHub Actions

Просто добавьте токен в Secrets и создайте Release - все остальное сделает GitHub!

---

## 📞 Если ничего не помогает

Напишите в поддержку PyPI: https://pypi.org/help/

Опишите проблему:
- Ошибка: ConnectionResetError (WinError 10054)
- Версия Python: 3.13
- Версия twine: (проверьте: `pip show twine`)
- Страна/провайдер

Они могут помочь с настройкой или предложить альтернативные методы загрузки.
