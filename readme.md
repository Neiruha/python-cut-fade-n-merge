# Python Cut-Fade-n-Merge
Скрипт на Python для обрезки, плавного перехода и объединения двух видео с использованием FFmpeg.

## Задача
Скрипт позволяет:

- Обрезать конец первого видео с добавлением фейдаута.
- Обрезать начало второго видео с добавлением фейдина.
- Объединить два видео в один файл с плавным переходом.

## Требования
- Python 3.7+
- FFmpeg установлен и доступен через PATH.
- [Скачать FFmpeg](https://ffmpeg.org/)

## Установка
Клонируйте репозиторий:

```bash
git clone https://github.com/Neiruha/python-cut-fade-n-merge.git
cd python-cut-fade-n-merge
```

Убедитесь, что FFmpeg установлен:

```bash
ffmpeg -version
```

## Использование
Запустите скрипт с аргументами:

```bash
python video_merge.py <video1> <video2> <cut1> <cut2> <output>
```

Аргументы:
- `<video1>` — путь к первому видеофайлу.
- `<video2>` — путь ко второму видеофайлу.
- `<cut1>` — время (в секундах), до которого обрезается первое видео.
- `<cut2>` — время (в секундах), с которого начинается второе видео.
- `<output>` — имя выходного файла.

Пример:

```bash
python video_merge.py video1.mp4 video2.mp4 3 3 merged_video.mp4
```

### Опция --help:
Вы можете получить подсказку по использованию скрипта:

```bash
python video_merge.py --help
```

Вывод:

```bash
usage: video_merge.py [-h] video1 video2 cut1 cut2 output

Склеивание двух видео с плавным переходом.

positional arguments:
  video1      Путь к первому видеофайлу.
  video2      Путь ко второму видеофайлу.
  cut1        Секунды, до которых обрезать первое видео.
  cut2        Секунды, с которых начать второе видео.
  output      Имя выходного файла.

optional arguments:
  -h, --help  Показывает это сообщение и завершает выполнение.
```

## Что делает скрипт
- Обрезает первое видео до указанного времени, добавляя фейдаут.
- Обрезает второе видео, начиная с указанного времени, добавляя фейдин.
- Создаёт текстовый файл (file_list.txt) для объединения видео через FFmpeg.
- Логирует весь процесс в process.log и выводит диагностику файлов.

## Пример структуры файлов
```
python-cut-fade-n-merge/
│
├── video_merge.py        # Основной скрипт
├── README.md             # Описание проекта
├── .gitignore            # Игнорируемые файлы
└── examples/             # Папка для примеров (опционально)
    ├── video1.mp4        # Пример входного видео 1
    ├── video2.mp4        # Пример входного видео 2
    └── result.mp4        # Результат объединения
```

## Логирование
Все шаги и ошибки записываются в файл process.log. Если что-то пошло не так, проверьте его содержимое.

## Требования к видео
- Видео должны быть в одном формате (например, MP4).
- Должны совпадать кодеки, разрешение и частота кадров.

## Примечания
- Значения времени (cut1 и cut2) задаются в секундах.
- Фейды рассчитаны на 5 кадров (0.2 секунды при 25 FPS).

## Автор
Этот скрипт был создан Нейрухой, вашим AI-помощником, для решения задач любой сложности.

Присоединяйтесь к нашему [Нейруха Бизнес Кафе](https://t.me/neiruha_business_cafe), чтобы найти ещё больше идей и инструментов для автоматизации!