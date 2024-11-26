import time
import os

from os import system, name
from datetime import datetime

import CONFIG

def Clear():
    if name == 'nt': # Windows & DOS powered
        _ = system('cls')
    else:            # 'posix' - UNIX powered (Mac & Linux)
        _ = system('clear')

def Log(_tag, _msg):
    # ERR handling - SYS_TAG length check
    if len(_tag) >= 16:
        _tag = "SYS_TAG_ERR     "

    # SYS_TAG formatting
    while (len(_tag) < 16):
        _tag = _tag + " "

    print(f"{_tag}| {_msg}")

def SectionHeader(caller, header):
    Log(caller, '==================================================')
    Log(caller, header)
    Log(caller, '==================================================')


def Home(tick=None, latency=None):
    Clear()

    # Header
    SectionHeader('SYSTEM', f'{CONFIG.VERSION_ID} | Iteration: {tick} | {datetime.now().time()}')
    print(f"SYSTEM          | Last Tick length: {latency}")


def RenderProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """        
    if len(prefix) >= 16:
        prefix = "SYS_TAG_ERR     "

    # SYS_TAG formatting
    while (len(prefix) < 16):
        prefix = prefix + " "
    
    prefix += '| '

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    # Print New Line on Complete
    if iteration == total: 
        print()

def Delay(delay_time):
    # Initial call to print 0% progress
    RenderProgressBar(iteration=0, 
                            total=60, 
                            prefix='TICK DELAY',
                            length=65)

    for i in range (0, 60):
        time.sleep(min([delay_time/60, 0.2]))
        # Update Progress Bar
        RenderProgressBar(iteration=i + 1, total=60, length = 65, prefix='TICK DELAY')


def OutputTokenTicker(token, df):
    string = f"{token} | ASK-{round(float(df['ASK PRICE'].iloc[-1]), 2)} / BID-{round(float(df['BID PRICE'].iloc[-1]), 2)} | RSI: {df['RSI'].iloc[-1]} | T-{df['TIMESTAMP'].iloc[-1]}"
    Log("EXCHANGE", string)


