from flask import Flask, request
def default():
    return request.args