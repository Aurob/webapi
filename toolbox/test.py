from lib.private import private
from lib.verify import *
from flask import Flask, request
import inspect
import sys

def a():
    valid = validate()
    if valid:
        return valid
    return False

def b():
    # return data
    # return request.form
    return alt_validate()

def default(data):
    # print all methods of the current module
    # return list(sys.modules[__name__].request.headers)
    return list(request.headers)
    