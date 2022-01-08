from functools import partial
import concurrent.futures
import random
import time

import requests

from link_util import read_urls


num_run = 10
im_num = 20

url_file = "img_links.txt"
im_urls = read_urls(url_file)
print(f"URL num: {len(im_urls)}")
selected_urls = random.choices(im_urls, k=im_num)

sess1 = requests.Session()
sess2 = requests.Session()


def get_img(url, session=None):
    r = session.get(url, timeout=5, stream=True)
    # https://requests.readthedocs.io/en/master/user/quickstart/#raw-response-content
    r.raw.decode_content = True
    return r.raw.read()

def get_img2(url, session=None):
    r = session.get(url, timeout=5)
    return r.content


def get_img3(url):
    r = requests.get(url, stream=True, timeout=5)
    r.raw.decode_content = True
    return r.raw.read()


def get_img4(url):
    r = requests.get(url, timeout=5)
    return r.content


def get_img_multithread(urls, func):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # result will be a generator, not plain list.
        res = executor.map(func, urls)
    return res


def get_running_time(func):
    start = time.time()
    get_img_multithread(selected_urls, func)

    return time.time() - start


get_im_partial = partial(get_img, session=sess1)
get_im_partial2 = partial(get_img2, session=sess2)


def main():
    total_time1 = 0
    total_time2 = 0
    total_time3 = 0
    total_time4 = 0

    for i in range(num_run):
        print(f"run {i+1}/{num_run}")

        elapse = get_running_time(get_im_partial)
        total_time1 += elapse

        elapse = get_running_time(get_im_partial2)
        total_time2 += elapse

        elapse = get_running_time(get_img3)
        total_time3 += elapse

        elapse = get_running_time(get_img4)
        total_time4 += elapse

    print(f"avg time (r.raw with session): {total_time1/num_run}")
    print(f"avg time (r.content with session): {total_time2/num_run}")
    print(f"avg time (r.raw no session): {total_time3/num_run}")
    print(f"avg time (r.content no session): {total_time4/num_run}")


if __name__ == "__main__":
    main()
