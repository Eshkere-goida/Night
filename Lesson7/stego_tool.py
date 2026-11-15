import argparse

def setup_cli():
    parser = argparse.ArgumentParser(
        description="Консольная LSB-стеганографическая утилита"
    )

    parser.add_argument(
        "mode",
        choices=['inject', 'extract'],
        help="Режим работы: inject (внедрение) или extract (извлечение)",
    )

    parser.add_argument(
        "-i",
        "--image",
        required=True,
        help='Путь к изображению',
    )

    parser.add_argument(
        "-s",
        "--secret",
        help='Путь к секретному сообщению, которое нужно зашифровать',
    )

    parser.add_argument (
        "-o",
        "--output",
        help='Путь, по которому сохраняется выходное изображение',
    )

    parser.add_argument (
        "-t",
        "--threshold",
        type=int,
        default=12,
        help='Порог шифрования пикселей',
    )

    parser.add_argument (
        "-k",
        "--key",
        default="",
        help="Ключ для XOR шифрования",
    )


    return parser.parse_args()

import os
from Module1.Lesson5.smart_injector import smart_inject

def handle_inject(output_path: str, secret_path: str, image_path: str, threshold: int):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл контейнера '{image_path}' не найден!")
    if not os.path.exists(secret_path):
        raise FileNotFoundError(f"Файл секретного сообщения '{secret_path}' не найден!")

    with open(secret_path, "r", encoding="utf-8") as f:
        secret_text = f.read().strip()

    if not secret_text: 
        raise ValueError("Файл с секретом пуст!")

    smart_inject(
        container_path=image_path,
        secret_text=secret_text,
        output_path=output_path,
        threshold=threshold,
    )

    print(f'Инъекция прошла(не факт что правильно), сохранено в {output_path}')

from Module1.Lesson6.smart_extractor import smart_extract

def handle_exract(image_path: str, threshold: int) -> None:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл изображения '{image_path}' не найден!")

    extracted_text = smart_extract(
        stego_path=image_path,
        threshold=threshold
    )

    print(f"Скрытое сообщение извлечено: {extracted_text}")


def main():
    args = setup_cli()
    try:
        if args.mode == 'inject':
            if not args.output or not args.secret:
                print("Ошибка, для режима inject обязательно ввести 2 дополонительных аргумента:")
                print("-o/--output  Путь к файлу для сохранения результата")
                print("-s/--secret  Путь к файлу с секретным текстом")
                return

            handle_inject(args.output, args.secret, args.image, args.threshold)

        elif args.mode == 'extract':
            handle_exract(args.image, args.threshold)
    except (ValueError, UnicodeDecodeError, FileNotFoundError) as err:
        print(f"Ошибка при выполнении операции: {err}")

if __name__ == "__main__":
    main()
            
# if __name__ == "__main__":
#     args = setup_cli()

#     print("Полученные аргументы:")
#     print(f"Режим: {args.mode}")
#     print(f"Путь к изображению: {args.image}")
#     if args.secret:
#         print(f"Путь к секретному сообщению: {args.secret}")
#     if args.output:
#         print(f"Путь к результату внедрения: {args.output}")


