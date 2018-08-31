#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 21:22:04 2018

@author: yumi.zhang
"""

import time, sys, cherrypy, os
from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf
 
def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("movie_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
    sc = SparkContext(conf=conf, pyFiles=['movie_engine.py', 'app.py'])
 
    return sc
    
def run_server(app):
 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
    
 
if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    dataset_path = 'file:///Users/yumi.zhang/Desktop/recommendation/datasets/ml-latest-small'
    app = create_app(sc, dataset_path)
 
    # start web server
    run_server(app)