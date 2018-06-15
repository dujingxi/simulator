#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Filename: 
# Description: 

# Copyright: (C) 2018 dujingxi

# Author: Dujingxi <dujingxi@streamocean.com>
# License: Streamocean
# Last-Updated: 2018/

import os.path
import time
from ctypes import *
from config import config
from flask import Flask, request, abort, render_template, jsonify, redirect, url_for


state_func = {
        'init': {
            'logon': 'online'
            },
        'online': {
            'logon': 'online', 
            'addmt':'inmt', 
            'reset': 'init'
            },
        'inmt': {
            'raise': 'inmt', 
            'select': 'inmt', 
            'bye': 'online', 
            'reset': 'init'
            },
        'err': {
            'reset': 'init'
            }
    }


class BaseFsm:

    def __init__(self, name, uid_list):
        self.__uid_list = uid_list
        self.name = name

    def add_uid(self, ulist):
        self.__uid_list = self.__uid_list + ulist
        return ulist

    def sub_uid(self, ulist):
        uid_list_set = set(self.__uid_list)
        ret_set = uid_list_set - set(ulist)
        self.__uid_list = list(ret_set)
        return ulist

    @property
    def get_uid_list(self):
        return self.__uid_list

    def run(self, state):
        pass


class meeting:

    def __init__(self, mttype, uid_list):
        self.mttype = mttype
        self.uid_list = uid_list

    def add_uid(self, ulist):
        self.uid_list += ulist
        return ulist
    
    def sub_uid(self, ulist):
        self.uid_list -= ulist

init = BaseFsm('init', [])
online = BaseFsm('online', [])
inmt = BaseFsm('inmt', [])
err = BaseFsm('err', [])
states_ins = [init, online, inmt, err]
# global 
G_CUR_STATE = dict()

def refresh_var():
    for state in states_ins:
        state_uid_list = state.get_uid_list
        state_uid_len = len(state_uid_list)
        global G_CUR_STATE
        G_CUR_STATE[state.name] = {"count": state_uid_len, "content": state_uid_list}

# refresh_var(); print(g_cur_state)

def action_logon(name):
    var = "hello world, {0}.".format(name)
    return var

# print(action_logon('zhangsan'))

def action_addmt():
    pass

def action_raise():
    pass

def action_select():
    pass

def action_bye():
    pass

def action_reset():
    pass





















app = Flask(__name__)

G_PRE = False

@app.route('/prepare/', methods=['GET', 'POST'])
def prepare():
    if request.method == 'POST':
        global G_PRE
        G_PRE = True
        with open('userlist', 'r') as fp:
            init.add_uid(fp.readlines())
        return redirect('/index/')
    else:
        return render_template('prepare.html')

@app.route('/')
@app.route('/index/')
def index():
    refresh_var()
    return render_template("index.html")


@app.route('/test/')
def test():
    refresh_var()
    return render_template("base.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")








