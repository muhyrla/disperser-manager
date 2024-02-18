import os
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3


def generate_key():
    private_key = os.urandom(32)
    private_key_hex = private_key.hex()
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'))

    return private_key_hex+";"+w3.eth.account.from_key(private_key_hex).address


def save_keys_to_file(key, index):
    with open(f'private_keys.txt', 'a') as file:
        file.write(key+'\n')


def save_keys_and_number_to_file(keys, number):
    with open('disperser.txt', 'w') as file:
        for key in keys:
            address = key.split(';')[-1]
            file.write(f'{address},{number}\n')


def main():
    mode = int(input("Введите режим работы (1 или 2): "))

    if mode == 1:
        num_keys = int(input("Введите количество ключей: "))

        with ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(num_keys):
                key = executor.submit(generate_key)
                save_keys_to_file(key.result(), i)

        print(f"{num_keys} приватных ключей было сгенерировано и сохранено в файл 'private_keys.txt'.")

    elif mode == 2:
        filename = input("Введите название файла: ")
        number = input("Введите число: ")

        with open(filename, 'r') as file:
            keys = [line.strip() for line in file]

        save_keys_and_number_to_file(keys, number)

        print(f"Приватные ключи и число были сохранены в файл {filename}.")

    else:
        print("Неверный режим работы. Введите 1 или 2.")


main()
