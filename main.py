#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: alex-merge
# @version: 1.0

import subprocess
import os
import time
import argparse

arg_parser = argparse.ArgumentParser(description='Nvidia GPU temperature watcher')
arg_parser.add_argument(
    "--chatid",
    "-c",
    dest = "chatid",
    required = True,
    type = str,
    help = "Telegram ChatID")
arg_parser.add_argument(
    "--botid",
    "-b",
    dest = "botid",
    required = True,
    type = str,
    help = "Telegram BotID")
arg_parser.add_argument(
    "--threshold",
    "-t",
    dest = "threshold",
    default = 70,
    required = False,
    type = int,
    help = "Temperature threshold")
arg_parser.add_argument(
    "--interval",
    "-i",
    dest = "interval",
    default = 600,
    required = False,
    type = int,
    help = "Time interval between checks")
args = arg_parser.parse_args()

while True:
    p1 = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE)
    p2 = subprocess.check_output(['grep', '-oe', '[0-9][0-9]C'],
                                 stdin = p1.stdout)
    
    current_temp = int(p2[:2]) 
    print(current_temp)
    
    if current_temp >= args.threshold:    
        subprocess.run([
            'curl',
            '-H',
            'Content-Type: application/json',
            '-d',
            f'{{"chat_id":"{args.chatid}","text":"GPU temp exceeds thermal limits ! ({current_temp}/{args.threshold}C)"}}',
            f'https://api.telegram.org/bot{args.botid}/sendMessage',
            ],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
    
    time.sleep(args.interval)
