#!/user/bin/env python
# coding: utf-8

import os
import sys
import subprocess

class shell:
    def value(cmd):
        try:
            os.system(f'{cmd}')
        except:
            os.system(f'pip3 install --upgrade pip')
            os.system(f'{cmd}')
        a = subprocess.check_output(cmd, shell=True)
        return_value = a.decode('EUC-KR', 'backslashreplace')
        return return_value
    def install(module):
        cmd = f'pip3 install {module}'
        try:
            a = os.system(cmd)
        except:
            os.system('pip3 install --upgrade pip')
            a = os.system(cmd)
        if a == 0:
            print('OK to install!')
        else:
            print('error!')
