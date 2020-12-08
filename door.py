import sys
import threading

this = sys.modules[__name__]
this._opened = False

def close():
    this._opened = False

this._timer = threading.Timer(3, close)

def open(name):
    """
    Closes the door three seconds after the last call to this function
    """
    this._opened = True
    this._unlocker = name
    this._timer.cancel()
    this._timer = threading.Timer(3, close)
    this._timer.start()

def unlocker():
    return this._unlocker

def isOpened():
    return this._opened