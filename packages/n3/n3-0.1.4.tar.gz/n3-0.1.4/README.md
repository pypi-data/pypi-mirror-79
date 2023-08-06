# N3: Neural Network Notation

[![travis-ci](https://api.travis-ci.com/kerryeon/n3.svg?token=EwDa73MhCmpxV2ZhCUmb&branch=master)](https://travis-ci.com/github/kerryeon/n3)
[![Coverage Status](https://coveralls.io/repos/github/kerryeon/n3/badge.svg?branch=master&t=bHgSyR)](https://coveralls.io/github/kerryeon/n3?branch=master)

[![PyPI version shields.io](https://img.shields.io/pypi/v/n3.svg)](https://pypi.python.org/pypi/n3/)
[![PyPI license](https://img.shields.io/pypi/l/n3.svg)](https://pypi.python.org/pypi/n3/)

This project is in construction. Please be aware of using it.

```
node LeNet5:
    let K: kernel size = int 5

    let C: input channels = dim
    let W: width = dim
    let H: height = dim

    with Conv2D:
        set kernel size = K
        set padding = K / 2
        set stride = 2

    node MyConv:
        1. Conv2D
        2. Relu

    0. Input                    =  C, W  , H
    1. MyConv                   = 32, W/2, H/2
    2. MyConv                   = 64, W/4, H/4
    3. Transform                = 64* W/4* H/4
    4. Linear + Relu + Dropout  = 1024
    5. Linear                   = 10
```

## Usage
* Training
    ```bash
    $ n3 train image-classification --model LeNet5 --data Mnist --devices cuda:0 cpu
    ```
* Evaluating
    ```bash
    $ n3 eval image-classification --model LeNet5 --data Mnist --devices cuda:0 cpu
    ```
* Publish
    ```bash
    $ n3 publish image-classification --model LeNet5 --data Mnist --target android:java
    ```
    * android: java, flutter
    * ios: flutter
    * universal: c++, python
* Monitoring using Tensorboard
    ```bash
    $ n3 run tensorboard  # and, browse http://localhost::xxxx/
    ```
* Clustering with `n3-clu`
    ```bash
    $ n3 eval image-classification --model LeNet5 --data Mnist --devices w:180:cuda:0 w:192.168.0.181 cpu
    ```
    * "w:180:cuda:0": the "cuda:0" device in "xxx.xxx.xxx.180" (local)
    * "w:192.168.0.181": automatically choose devices in "192.168.0.181"
    * These can be defined as environment variables (N3_DEVICES)
