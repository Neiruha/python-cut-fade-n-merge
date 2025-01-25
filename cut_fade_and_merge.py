import subprocess
import os
import argparse

def execute_command(command):
    """Выполняет системную команду и обрабатывает ошибки."""
    try:
        print(f"Выполняю: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Ошибка: {result.stderr}")
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        print(f"Исключение: {e}")
        return False, str(e)

def create_concat_list(file1, file2, concat_file):
    """Создаёт текстовый файл для ffmpeg concat."""
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write(f"file '{file1}'\n")
        f.write(f"file '{file2}'\n")

def diagnose_video(file_path):
    """Проверяет информацию о видеофайле с помощью ffprobe."""
    info_cmd = f'ffprobe -v error -show_entries stream=codec_name,width,height,avg_frame_rate,duration -of json "{file_path}"'
    success, output = execute_command(info_cmd)
    if success:
        print(f"Информация о файле {file_path}:\n{output}")
        return output
    else:
        print(f"Ошибка диагностики файла {file_path}: {output}")
        return None

def process_videos(video1, video2, cut1, cut2, output_file, log_file="process.log"):
    """Основной процесс обработки видео."""
    trimmed_video1 = "trimmed_video1.mp4"
    trimmed_video2 = "trimmed_video2.mp4"
    concat_list = "file_list.txt"

    # Обрезаем и добавляем fade для video1
    trim_video1_cmd = (
        f'ffmpeg -i {video1} -vf "fade=out:{int(cut1 * 25)}:5" -t {cut1} '
        f'-c:v libx264 -crf 18 -preset fast -c:a copy {trimmed_video1}'
    )

    # Обрезаем и добавляем fade для video2
    trim_video2_cmd = (
        f'ffmpeg -i {video2} -vf "fade=in:0:5" -ss {cut2} '
        f'-c:v libx264 -crf 18 -preset fast -c:a copy {trimmed_video2}'
    )

    # Лог файл
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("Начинаю процесс обработки видео...\n")
        
        # Обрезка первого видео
        success, _ = execute_command(trim_video1_cmd)
        if success:
            log.write("Первое видео обработано успешно.\n")
            diagnose_video(trimmed_video1)
        else:
            log.write("Ошибка обработки первого видео.\n")

        # Обрезка второго видео
        success, _ = execute_command(trim_video2_cmd)
        if success:
            log.write("Второе видео обработано успешно.\n")
            diagnose_video(trimmed_video2)
        else:
            log.write("Ошибка обработки второго видео.\n")

        # Создание файла списка для склейки
        if os.path.exists(trimmed_video1) and os.path.exists(trimmed_video2):
            create_concat_list(trimmed_video1, trimmed_video2, concat_list)
            log.write("Файл списка для склейки создан.\n")
        else:
            log.write("Ошибка: промежуточные файлы для склейки не найдены.\n")

        # Склейка видео
        merge_cmd = f'ffmpeg -f concat -safe 0 -i {concat_list} -c copy {output_file}'
        success, _ = execute_command(merge_cmd)
        if success:
            log.write("Видео успешно объединены.\n")
            merged_info = diagnose_video(output_file)
            if merged_info:
                log.write(f"Диагностика объединённого видео:\n{merged_info}\n")
        else:
            log.write("Ошибка объединения видео.\n")

    print(f"Процесс завершён. Проверь результаты: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Склеивание двух видео с плавным переходом.")
    parser.add_argument("video1", help="Путь к первому видеофайлу.")
    parser.add_argument("video2", help="Путь ко второму видеофайлу.")
    parser.add_argument("cut1", type=float, help="Секунды, откуда обрезать первое видео.")
    parser.add_argument("cut2", type=float, help="Секунды, откуда обрезать второе видео.")
    parser.add_argument("output", help="Имя выходного файла.")
    args = parser.parse_args()

    process_videos(args.video1, args.video2, args.cut1, args.cut2, args.output)
