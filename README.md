# paraser_to_sms

1) Идем по ссылке: https://www.python.org/downloads/ и устанавливаем Python 3.7.9 под свою ось
2) Скачиваем этот репозиторий, или клоним
3) В скачанной/склоненной папке открываем консоль (Windows Win + X, в открытом окней выбираем PowerShell, Linux:  Ctrl+Alt+T) и выполняем pip (Если выдает ошибку, то использовать pip3) install -r requirement.txt

Для чистой сортировки, без скачивания:
   1) Заходим sms_settings.py
   2) Находим там PATH_TO_SAVE
   3) Меняем его на путь к папке в которой нужно отсортировать nsfw контент (Путь должен быть абсолютным, т.е. E:/папака_1/папка_2/)
   4) По желанию устанавливаем свою чувствительность нейронки (настройка NSFW_SENSITIVE) от 0.0 до 1.0 (0 - 100%)
   5) Запускаем через консоль python content_sort.py или python3 content_sort.py

Для скачивания и сортировки:
   1) Заходим в sms_settings.py
   2) По желанию меняем путь к папке в которою нужно сохранять контент, по стандарту, эта папка будет создаваться там, откуда запущен скрипт
   3) !!! Прокси, если есть прокси url / ip !!! Не тестил
   4) По желанию устанавливаем свою чувствительность нейронки для сортировки (настройка NSFW_SENSITIVE) от 0.0 до 1.0 (0 - 100%)
   5) Можно увеличить WORKERS_NUMBER, если позволяет мощности пекарни и интернета
   6) Запускаем через консоль python main.py или python3 main.py
