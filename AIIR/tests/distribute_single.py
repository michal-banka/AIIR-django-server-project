#!/usr/bin/env python3
import os
import paramiko
import random
import sys
from colorama import Fore, Style
from multiprocessing import Pool


import warnings
########### hiding bug in paramiko
warnings.filterwarnings(action='ignore', module='.*paramiko.*')
###########

#PARAMS
tabu_length = sys.argv[1]
iterations_without_improvement = sys.argv[2]
matrix_filename = sys.argv[3]
result_filename = sys.argv[4]
iterations = sys.argv[5]
node_id = sys.argv[6]
parts_of_matrix = sys.argv[7]
task_id = sys.argv[8]
single_host = sys.argv[9]


usernames = ["kacper", "witoldini"]
hosts = ["10.182.29.234", "10.182.62.254"]

colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
          Fore.MAGENTA, Fore.CYAN]

def get_cmd_run_tabu():
  return "main" + tabu_length + " " + iterations_without_improvement + " ~/aiir-workspace/" + matrix_filename + " " + result_filename + " " + iterations + " " + node_id + " " + parts_of_matrix

open_gedit_test = "gedit ~/test.txt"
run_tabu = "~/aiir-workspace/" + get_cmd_run_tabu()
give_credits = "chmod a+x ~/aiir-workspace/*"
compile_cpp = "gcc -w main.cpp -lstdc++ -o main"
mk_workspace = "mkdir aiir-workspace"
ls = "ls ~/wynik.txt"
rm_data_dir = "rm -r ~/aiir-workspace"
rm_wynik = "rm ~/" + result_filename

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

  _execute_on_remote(client, mk_workspace, random.choice(colors))
  _copy_files(client, host, random.choice(colors), matrix_filename)
  _copy_files(client, host, random.choice(colors), "main")
  _execute_on_remote(client, give_credits, random.choice(colors))
  _execute_on_remote(client, run_tabu, random.choice(colors))
  
  while(True):
    if _execute_on_remote(client, ls, random.choice(colors)):
      break

  _copy_files_from_remote(client, host, random.choice(colors), result_filename)
  _execute_on_remote(client, rm_data_dir, random.choice(colors))
  _execute_on_remote(client, rm_wynik, random.choice(colors))
  client.close()


def _copy_files(client, host, color, filename):
  sftp = client.open_sftp()

  filename_from = os.getcwd() + "/tests/data/" + filename
  filename_to = "/home/" + get_username_for_host(host) +  "/aiir-workspace/" + filename
  sftp.put(filename_from, filename_to)
  sftp.close()
  print(color + prefix + "copying to :" + host + "done" + Style.RESET_ALL)


def _copy_files_from_remote(client, host, color, filename):
  print(color + prefix + "copying file to " + host)
  sftp = client.open_sftp()

  filename_from = "/home/" + get_username_for_host(host) + "/" + filename
  print(filename_from)
  filename_to = os.getcwd() + "/data/results/" + task_id + "_" + node_id + " " + get_username_for_host(host) + "_" + result_filename
  sftp.get(filename_from, filename_to)
  sftp.close()
  print(color + prefix + "copying to :" + host + "done" + Style.RESET_ALL)


def _execute_on_remote(client, bash, color):
  print(color + prefix + "executing: " + bash)
  stdin,stdout,stderr = client.exec_command(bash)
  print(prefix + "done" + Style.RESET_ALL)
  return stdout.readlines()


# if __name__ == '__main__':
#   with Pool(processes=len(hosts)) as pool:
#     pool.map(connect_to_host, hosts)
connect_to_host(single_host)
