from flask import Flask, render_template, redirect, request
from bokeh.plotting import figure, show, output_file, vplot
from bokeh.embed import autoload_server, components
from bokeh.session import Session
from bokeh.document import Document

app=Flask(__name__)

import urllib2
import json
import pandas as pd
import numpy as np
import os
import sqlite3

api_key = 'cFuUY984Wxy1SpKr25zx'


@app.route('/')
def main():
    return redirect('/index_Main')

def quandl_search(query):
    url='https://www.quandl.com/api/v3/datasets/WIKI/' + query + '.json?auth_token=cFuUY984Wxy1SpKr25zx'
    json_obj = urllib2.urlopen(url)
    dataset=pd.read_json(json_obj)
    data=np.array(dataset['dataset']['data'])
    data_col=np.array(dataset['dataset']['column_names'])
    dout = pd.DataFrame({data_col[0]:data[:,0],data_col[1]:data[:,1],data_col[4]:data[:,4]})
    return dout


@app.route('/index_Main',methods=['GET','POST'])
def index_Main():
    if request.method =='GET':
        conn=sqlite3.connect('misodata.db')
        A=pd.read_sql('SELECT * FROM LMPdata LIMIT 5',conn)
        conn.close()
        B=A.loc[0]['NODE']
        return render_template('/Milestone_Main.html', Nodename="",node1n="",node1s="",node1t=B)
    else:
        node=request.form['nodename']
        NODE_info=pd.read_csv('N_info.csv')
        #Hval2=Hval.loc[0]['NODE_NAME']
        #NODE_info=pd.DataFrame({'NODE':['AMIL.EDWARDS2','AMMO.LABADIE1'],'STATE':['IL','MO'],'TYPE':['GEN','GEN']})
        if any(NODE_info.NODE_NAME==node)==False:
            nodeout=node+' is not a Node name'
            return render_template('Milestone_Main.html', Nodename=nodeout)
        else:
            nodefind=NODE_info.loc[NODE_info['NODE_NAME']==node].index.tolist()[0]
            #nodeout=NODE_info.loc[nodefind]['NODE_NAME']+", "+NODE_info.loc[nodefind]['STATE']+", "+NODE_info.loc[nodefind]['TYPE']+", "+str(NODE_info.loc[nodefind]['LAT'])+", "+str(NODE_info.loc[nodefind]['LONG'])
            node1n=NODE_info.loc[nodefind]['NODE_NAME']
            node1s=NODE_info.loc[nodefind]['STATE']
            node1t=NODE_info.loc[nodefind]['TYPE']
            return render_template('/Milestone_Main.html',Nodename="",node1n=node1n,node1s=node1s,node1t=node1t)


    

if __name__ == '__main__':
    app.run(port=33507)
