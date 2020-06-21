from functools import partial
import concurrent.futures
import random
import time

import requests


def read_urls(txt_path):
    urls = []
    with open(txt_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            if line:
                urls.append(line)
    return urls


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


sess1 = requests.Session()
sess2 = requests.Session()
get_im_partial = partial(get_img, session=sess1)
get_im_partial2 = partial(get_img2, session=sess2)

def get_img_multithread(urls, func):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # result will be a generator, not plain list.
        res = executor.map(func, urls)
    return res


def main():
    num_run = 20
    im_num = 20

    url_file = "img_links.txt"
    im_urls = read_urls(url_file)
    print(f"URL num: {len(im_urls)}")

    total_time1 = 0
    total_time2 = 0
    total_time3 = 0
    total_time4 = 0
    for i in range(num_run):
        print(f"run {i+1}/{num_run}")
        urls = random.choices(im_urls, k=im_num)

        start = time.time()
        res = get_img_multithread(urls, get_im_partial)
        elapse = time.time() - start
        total_time1 += elapse

        start = time.time()
        res = get_img_multithread(urls, get_im_partial2)
        elapse = time.time() - start
        total_time2 += elapse

        start = time.time()
        res = get_img_multithread(urls, get_img3)
        elapse = time.time() - start
        total_time3 += elapse

        start = time.time()
        res = get_img_multithread(urls, get_img4)
        elapse = time.time() - start
        total_time4 += elapse

    print(f"avg time (r.raw with session): {total_time1/num_run}")
    print(f"avg time (r.content with session): {total_time2/num_run}")
    print(f"avg time (r.raw no session): {total_time3/num_run}")
    print(f"avg time (r.content no session): {total_time4/num_run}")


if __name__ == "__main__":
    main()
