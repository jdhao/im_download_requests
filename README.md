# Introduction

There are different ways to download images using
[requests](https://requests.readthedocs.io/en/master/). This repo provides a
script to benchmark the speed of parallel image downloads with requests.

# How to run?

Make sure you have requests package installed, and simply run the following
command:

```bash
python compare.py
```

You may change the variable `im_num` to benchmark the download speed for
different numbers of images.
