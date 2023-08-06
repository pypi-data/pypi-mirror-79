import threading
import os
from importlib.resources import path


def minutesToSeconds(minutes):
    return int(minutes * 60)


def getFormattedTime(seconds):
    minutes = seconds // 60
    return f"{minutes}m {seconds - minutes * 60}s"


def printMessage(*argv, terminal, withLocation=True):
    t = terminal
    def sendFormatted():
        print('\n\n')
        print(t.white + t.center("", fillchar="@"))
        print("@" + t.move_right(t.width) + "@")
        for arg in argv:
            print(t.center(f"{t.red + arg + t.white}"))
        print("@" + t.move_right(t.width) + "@")
        print(t.center("", fillchar="@"))
    if withLocation:
        with t.location():
            sendFormatted()
    else:
        sendFormatted()


def from_package(fileName):
    with path(__package__, fileName) as filePath:
        return str(filePath)


class InputBuffer(threading.Thread):
    '''
        Input buffer class.
        Takes in a terminal object (blessed)

        Used to check the input stream every second as a separate thread.
    '''
    currChar = None
    __running = True

    def __init__(self, callback, terminal, debug):
        self.terminal = terminal
        self.callback = callback
        self.debug = debug
        threading.Thread.__init__(self)
    
    def run(self):
        # Gets input buffer char every second
        while self.__running:
            self.currChar = self.terminal.inkey(timeout=1)
            self.callback(self.currChar)
            if self.debug:
                print(self.currChar)
    def getChar(self):
        return self.currChar

    def stop(self):
        self.__running = False
        if self.debug:
            print("Stopped InputBuffer")