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


@app.route('/')
def main():
    return redirect('/index_Main')

def plotbokeh(nodename):
    conn=sqlite3.connect('misodata.db')
    npriceseries=pd.read_sql('SELECT DATE, PRICE FROM LMPdata WHERE NODE="%s" AND DATE>"2015-09-30"' %(nodename),conn)
    conn.close()
    return npriceseries
    
    

@app.route('/index_Main',methods=['GET','POST'])
def index_Main():
    if request.method =='GET':
        #conn=sqlite3.connect('misodata.db')
        #A=pd.read_sql('SELECT * FROM LMPdata LIMIT 5',conn)
        #conn.close()
        #B=A.loc[0]['NODE']
        return render_template('/Milestone_Main.html', Nodename="",node1n="",node1s="",node1t="")
    else:
        node=request.form['nodename']
        NODE_info=pd.read_csv('N_info.csv')
        node1=request.args.get("node1")
        #Hval2=Hval.loc[0]['NODE_NAME']
        #NODE_info=pd.DataFrame({'NODE':['AMIL.EDWARDS2','AMMO.LABADIE1'],'STATE':['IL','MO'],'TYPE':['GEN','GEN']})
        if any(NODE_info.NODE_NAME==node)==False:
            nodeout=node+' is not a Node name'
            return render_template('Milestone_Main.html', Nodename=nodeout, node1=node1)
        else:
            nodefind=NODE_info.loc[NODE_info['NODE_NAME']==node].index.tolist()[0]
            node1n=NODE_info.loc[nodefind]['NODE_NAME']
            node1s=NODE_info.loc[nodefind]['STATE']
            node1t=NODE_info.loc[nodefind]['TYPE']
            out1=1
            dfprice=plotbokeh(node1n)
            p1=figure(x_axis_type='datetime')
            Price_type=request.form['price_data']
            
            p1.line(dfprice['DATE'],dfprice['PRICE'])
            #np.array(
            #,dtype=np.datetime64)
            #p1.title = 'Stock Prices for ' + Stock_Symbol
            #p1.xaxis.axis_label = "Date"
            #p1.yaxis.axis_label = "Price"
            script, div = components(p1)
            #return render_template('/Milestone_Main.html',Nodename="",node1n=node1n,node1s=node1s,node1t=node1t)
            
            return render_template('Onenode_plot.html',node1n=node1n, out1=out1, script=script, div=div)

#@app.route('/Onenode_plot',methods=['GET','POST'])
#def Onenode_plot():
#    return render_template('Onenode_plot.html',node1n=node1n)

    

if __name__ == '__main__':
    app.run(port=33507)
