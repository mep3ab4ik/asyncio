from time import time

import requests

from asyn.part1.sites import sites

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 ' \
             'Safari/537.36 OPR/86.0.4363.64 '


def elapsed_time(function):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = function(*args, **kwargs)

        func_name = function.__name__
        result_str = f'({result})' if result else ''
        url = f'[{args[0]}]' if args else ''
        print(f'[{func_name}]{url} Time elapsed: {time() - start_time:.2f} seconds. {result_str}')
        return result

    return wrapper


def send_request(url):
    start_time = time()
    response = requests.get(url, headers={'User-Agent': user_agent})
    # print(f'[{url}] Time elapsed: {time() - start_time:.2f}s. ({response.status_code})')
    return response.status_code


def main():
    start_time = time()

    for site in sites:
        send_request(site)

    print(f'Total time: {time() - start_time:.2f}s')


if __name__ == '__main__':
    main()
