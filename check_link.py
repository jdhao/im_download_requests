import requests


from compare import read_urls


def main():
    fpath = "img_links.txt"

    urls = read_urls(fpath)

    for i, url in enumerate(urls):
        res = requests.get(url, timeout=5)
        print(f"{i+1}\t{res.status_code}")


if __name__ == "__main__":
    main()
