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

api_key = 'cFuUY984Wxy1SpKr25zx'
NODE_info=pd.DataFrame({'NODE':['AMIL.EDWARDS2','AMMO.LABADIE1'],'STATE':['IL','MO'],'TYPE':['GEN','GEN']})

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
        return render_template('/Milestone_Main.html', Nodename="")
    else:
        node=request.form['nodename']
        nodefind=NODE_info.loc[NODE_info['NODE']==node]
        nodeout=nodefins.loc[0]['NODE']+", "+nodefind.loc[0]['STATE']+", "+nodefind.loc[0]['TYPE']
        
#        Stock_Symbol =request.form['stock_symbol']
#        dout= quandl_search(Stock_Symbol)
#        
#        
#        p1=figure(x_axis_type='datetime')
#        Price_type=request.form['price_data']
#
        return render_template('/Milestone_Main.html',Nodename=nodeout)
    

if __name__ == '__main__':
    app.run(port=33507)
