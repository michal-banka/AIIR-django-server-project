#!/usr/bin/env python3
import os
import paramiko
import random
from colorama import Fore, Style
from multiprocessing import Pool


import warnings
########### hiding bug in paramiko
warnings.filterwarnings(action='ignore', module='.*paramiko.*')
###########

hosts = ["10.182.36.207"]

colors = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
          Fore.MAGENTA, Fore.CYAN]

open_gedit_test = "gedit ~/test.txt"
run_tabu = "~/aiir-workspace/main 200 300 ~/aiir-workspace/ftv47.atsp wynik.txt 5 13"
give_credits = "chmod a+x ~/aiir-workspace/*"
compile_cpp = "gcc -w main.cpp -lstdc++ -o main"
mk_workspace = "mkdir aiir-workspace"

prefix = "########## "


def connect_to_host(host):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect('%s' % host, username='ooo', password='oooo')

  _execute_on_remote(client, mk_workspace,random.choice(colors))
  _copy_files(client, host, random.choice(colors), "ftv47.atsp")
  _copy_files(client, host, random.choice(colors), "main")
  _execute_on_remote(client, give_credits, random.choice(colors))
  _execute_on_remote(client, run_tabu, random.choice(colors))
  
  client.close()


def _copy_files(client, host, color, filename):
  print(color + prefix + "copying file to " + host)
  sftp = client.open_sftp()
  filename_from = "/home/kacper/AIIR_PROJEKT/AIIR/tests/data/" + filename
  filename_to = "/home/michal/aiir-workspace/" + filename
  sftp.put(filename_from, filename_to)
  sftp.close()
  print(color + prefix + "copying to :" + host + "done" + Style.RESET_ALL)


def _execute_on_remote(client, bash, color):
  print(color + prefix + "executing: " + bash)
  stdin,stdout,stderr = client.exec_command(bash)
  print(stdout.readlines())
  print(stderr.readlines())

  print(prefix + "done" + Style.RESET_ALL)


if __name__ == '__main__':
#  save_docker_to_file()
  with Pool(processes=len(hosts)) as pool:
    pool.map(connect_to_host, hosts)
