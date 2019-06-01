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

usernames = ["kacper"]
hosts = ["10.182.29.234"]

colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
          Fore.MAGENTA, Fore.CYAN]

open_gedit_test = "gedit ~/test.txt"
run_tabu = "~/aiir-workspace/main 200 300 ~/aiir-workspace/ftv47.atsp wynik.txt 5 13"
give_credits = "chmod a+x ~/aiir-workspace/*"
compile_cpp = "gcc -w main.cpp -lstdc++ -o main"
mk_workspace = "mkdir aiir-workspace"
ls = "ls ~/wynik.txt"

prefix = "########## "

def get_username_for_host(host):
  i = 0
  for h in hosts:
    if h == host:
      return usernames[i]
    i += 1
  return ""

def connect_to_host(host):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect('%s' % host, username=get_username_for_host(host),key_filename="/home/michal/.ssh/id_rsa")

  _execute_on_remote(client, mk_workspace,random.choice(colors))
  _copy_files(client, host, random.choice(colors), "ftv47.atsp")
  _copy_files(client, host, random.choice(colors), "main")
  _execute_on_remote(client, give_credits, random.choice(colors))
  _execute_on_remote(client, run_tabu, random.choice(colors))
  
  while(True):
    if _execute_on_remote(client, ls, random.choice(colors)):
      break
  print("========================================")
  _copy_files_from_remote(client, host, random.choice(colors), "wynik.txt")
  
  client.close()


def _copy_files(client, host, color, filename):
  print(color + prefix + "copying file to " + host)
  sftp = client.open_sftp()
  print(get_username_for_host(host))

  filename_from = os.getcwd() + "/data/" + filename
  filename_to = "/home/" + get_username_for_host(host) +  "/aiir-workspace/" + filename
  print(filename_to)
  sftp.put(filename_from, filename_to)
  sftp.close()
  print(color + prefix + "copying to :" + host + "done" + Style.RESET_ALL)


def _copy_files_from_remote(client, host, color, filename):
  print(color + prefix + "copying file to " + host)
  sftp = client.open_sftp()

  filename_from = "/home/" + get_username_for_host(host) + "/" + filename
  print(filename_from)
  filename_to = os.getcwd() + "/data/" + filename
  sftp.get(filename_from, filename_to)
  sftp.close()
  print(color + prefix + "copying to :" + host + "done" + Style.RESET_ALL)


def _execute_on_remote(client, bash, color):
  print(color + prefix + "executing: " + bash)
  stdin,stdout,stderr = client.exec_command(bash)
  print(prefix + "done" + Style.RESET_ALL)
  return stdout.readlines()


if __name__ == '__main__':
#  save_docker_to_file()
  with Pool(processes=len(hosts)) as pool:
    pool.map(connect_to_host, hosts)
