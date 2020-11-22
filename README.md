# paraser_to_sms
## FAQ

### ENG:
+ 1) Goes to the link: https://www.python.org/downloads/ and install Python 3.7.9 (Chose to your OS)
+ 2) Download or clone this repository
+ 3) In download and unarchived / cloned repo opent a terminal (On Windows using Win + X hotkeys, or Ctrl+Alt+T on Linux) and execute command pip (If it throwing errors, use pip3) install -r requirements.txt 

#### For only sorting, without downloading content:
   + 1) Open sms_settings.py
   + 2) Finding there PATH_TO_SAVE
   + 3) Changing to path of the directory to sort
   + 4) Optional!!! change NSFW sensitive by NSFW_SENSITIVE parameter (from 0.0 (0%) to 1.0 (100%))
   + 5) Run command from console python content_sort.py / python3 content_sort.py
   
#### For downloading content and sorting:
   + 1) Open sms_settings.py
   + 2) Optional!! changing path to save directory, by default save directory creating where you running script
   + 3) !!! Proxy, if you have ip or url !!! Not tested (HTTP proxy)
   + 4) Optional!!! change NSFW sensitive by NSFW_SENSITIVE parameter (from 0.0 (0%) to 1.0 (100%))
   + 5) You can increase number of workers by WORKERS_NUMBER parameter in sms_settings.py
   + 6) Run commnad from console python main.py or python3 main.py
   
#### For ignoring unnecessary, repetitive pictures you can add, this pictures to ignored directory in directory output
P.S: If errors occurred while executing command pip install -r requirements.txt, open requirements.txt, and find there name of erroring module and deleting all symbols after module name

#### RU:
+ 1) Идем по ссылке: https://www.python.org/downloads/ и устанавливаем Python 3.7.9 под свою ось
+ 2) Скачиваем этот репозиторий, или клоним
+ 3) В скачанной/склоненной папке открываем консоль (Windows Win + X, в открытом окней выбираем PowerShell, Linux:  Ctrl+Alt+T) и выполняем pip (Если выдает ошибку, то использовать pip3) install -r requirements.txt

#### Для чистой сортировки, без скачивания:
   + 1) Заходим sms_settings.py
   + 2) Находим там PATH_TO_SAVE
   + 3) Меняем его на путь к папке в которой нужно отсортировать nsfw контент (Путь должен быть абсолютным, т.е. E:/папака_1/папка_2/)
   + 4) По желанию устанавливаем свою чувствительность нейронки (настройка NSFW_SENSITIVE) от 0.0 до 1.0 (0 - 100%)
   + 5) Запускаем через консоль python content_sort.py или python3 content_sort.py

#### Для скачивания и сортировки:
   + 1) Заходим в sms_settings.py
   + 2) По желанию меняем путь к папке в которою нужно сохранять контент, по стандарту, эта папка будет создаваться там, откуда запущен скрипт
   + 3) !!! Прокси, если есть прокси url / ip !!! Не тестил
   + 4) По желанию устанавливаем свою чувствительность нейронки для сортировки (настройка NSFW_SENSITIVE) от 0.0 до 1.0 (0 - 100%)
   + 5) Можно увеличить WORKERS_NUMBER, если позволяет мощности пекарни и интернета
   + 6) Запускаем через консоль python main.py или python3 main.py
   
Для игнорирования некоторых пикч, положить их в папку ignored в папке output


P.S.: Если выбивает ошибки на этапе pip install -r requirements.txt, то, берем из ошибки имя модуля, заходим в requirements.txt, находим имя этого модуля и оставляем на этой строке только его имя (без == и чисел после этих знаков)
