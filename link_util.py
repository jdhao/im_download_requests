import requests


def read_urls(txt_path):
    urls = []
    with open(txt_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            if line:
                urls.append(line)
    return urls



def main():
    fpath = "img_links.txt"

    urls = read_urls(fpath)

    for i, url in enumerate(urls):
        res = requests.get(url, timeout=5)
        print(f"{i+1}\t{res.status_code}")


if __name__ == "__main__":
    main()
