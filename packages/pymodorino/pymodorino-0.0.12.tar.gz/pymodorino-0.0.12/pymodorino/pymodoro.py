#!/usr/bin/env python3

import argparse
import time
import sys
import os
import warnings
from blessed import Terminal
from notifypy import Notify
from utils import getFormattedTime, minutesToSeconds, printMessage, InputBuffer

DEBUG = False
if not DEBUG:
    warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('-w', type=float, default=25, help='Focus/work minutes. (default: 25m)')
parser.add_argument('-b', type=float, default=5, help='Break minutes. (default: 5m)')
parser.add_argument('-s', help='Wav file to use for the notifications. (default: ./oi.wav)')

args = parser.parse_args()
t = Terminal()

total_work_time = 0
total_break_time = 0

notification = Notify(
    default_notification_title="Pymodorino timer",
    default_notification_application_name="Pymodorino",
    default_notification_icon= "./pymodorino/pomodorino.png",
    default_notification_audio= "./pymodorino/oi.wav"
)

def sendNotification(message):
    notification.message = message
    notification.send()

def quitPomodoro():
    printMessage(
        t.center("Good job"),
        f"Total work time: {getFormattedTime(total_work_time)}",
        f"Total break time: {getFormattedTime(total_break_time)}",
        terminal=t, withLocation=False)
    sys.exit()

def askForConfirmation(message):
    answer = ""
    while answer != "y" and answer != "n":
        printMessage(f"{message}(y/n): ", terminal=t)
        answer = t.inkey().lower()
        if answer == "q":
            quitPomodoro()

    return answer == "y"

class Timer():
    WORK_M = 0
    BREAK_M = 0
    isBreak = False
    timeLeft = -1
    running = False

    def __init__(self, work_m, break_m):
        self.WORK_M = work_m
        self.BREAK_M = break_m
        self.timeLeft = minutesToSeconds(args.w)

    def stop(self):
        self.running = False

    def start(self):
        global total_work_time, total_break_time

        self.running = True
        msgPrefix = "BREAK" if self.isBreak else "WORKING"

        while self.timeLeft >= 0 and self.running:
            printMessage(f"[{msgPrefix}]: Time remaining: {t.bold + getFormattedTime(self.timeLeft) + t.normal}", terminal=t)
            self.timeLeft -= 1
            if self.isBreak:
                total_break_time += 1
            else:
                total_work_time += 1
            time.sleep(1)

        if not self.running:
            return
        if self.isBreak:
            sendNotification("Break time is up. Get to work!")
            if askForConfirmation("Start working again?"):
                self.isBreak = False
                self.timeLeft = minutesToSeconds(self.WORK_M) 
                self.start()
        else:
            sendNotification("Good work, you may take a break!")
            if askForConfirmation("Time is up. Start break?"):
                self.isBreak = True
                self.timeLeft = minutesToSeconds(self.BREAK_M) 
                self.start()

def main():
    # Make space for the output. Without this hackfix the t.withLocation context 
    # can malfunction on some terminals
    print('\n'*10 + t.move_up(10))

    timer = Timer(args.w, args.b)

    def onPressQuit(char):
        if char.lower() == 'q':
            timer.stop()
            quitPomodoro()

    inputBuffer = InputBuffer(terminal=t, callback=onPressQuit)
    inputBuffer.daemon = True
    inputBuffer.start()

    with t.cbreak(), t.hidden_cursor():
        try:
            timer.start()
        except (KeyboardInterrupt, Exception):
            quitPomodoro()

if __name__ == "__main__":
    main()