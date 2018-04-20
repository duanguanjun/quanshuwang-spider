#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:gjduan time:2018/4/13

import os
from multiprocessing import Process


def run_proc(name):
    print('child process %s (%s) running...' % (name, os.getpid()))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    for i in range(5):
        p = Process(target=run_proc, args=(str(i),))
        print('Process will start.')
        p.start()
    p.join()
    print('Process end.')
