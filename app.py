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
import datetime

NODE_info=pd.read_csv('N_info.csv')
NODE_front=[NODE_info['NODE_NAME'][x].split(".")[0] for x in range(len(NODE_info))]

@app.route('/')
def main():
    return redirect('/index_Main')

def plotbokeh(nodename,start_date,end_date):
    conn=sqlite3.connect('misodata.db')
    npriceseries=pd.read_sql('SELECT DATE, PRICE FROM LMPdata WHERE NODE="%s" AND DATE>"%s" AND DATE<"%s"' %(nodename,start_date,end_date),conn)
    conn.close()
    return npriceseries

def plotbokehcomp(node1, node2, start_date,end_date):
    conn=sqlite3.connect('misodata.db')
    datestart, datefinish = start_date, end_date
    comppriceseries=pd.read_sql('SELECT DATE, SUM(CASE WHEN NODE = "%s" THEN PRICE ELSE -1.0 * PRICE END) As DIFF_COST FROM LMPdata WHERE (NODE="%s" OR NODE="%s") AND (DATE>"%s" AND DATE<"%s") GROUP BY DATE' %(node1, node1, node2,datestart,datefinish),conn)
    conn.close()
    return comppriceseries
    
    

@app.route('/index_Main',methods=['GET','POST'])
def index_Main():
    if request.method =='GET':
        #conn=sqlite3.connect('misodata.db')
        #A=pd.read_sql('SELECT * FROM LMPdata LIMIT 5',conn)
        #conn.close()
        #B=A.loc[0]['NODE']
        return render_template('/Milestone_Main.html', Nodename="",node1n="",node1s="",node1t="",nodes=['AMMO.UE.AZ','AMIL.EDWARDS2'])
    else:
        node=request.form['nodename']
        start_date=datetime.datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date=datetime.datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        node=node.upper()
        #node1=request.args.get("node1")
        #Hval2=Hval.loc[0]['NODE_NAME']
        #NODE_info=pd.DataFrame({'NODE':['AMIL.EDWARDS2','AMMO.LABADIE1'],'STATE':['IL','MO'],'TYPE':['GEN','GEN']})
        if any(NODE_info.NODE_NAME==node)==False:
            if node.split(".")[0] in NODE_front:
                Poss_others=", ".join(NODE_info[NODE_info['NODE_NAME'].str.contains(node.split(".")[0])]['NODE_NAME'].tolist())
                nodeout=node.split(".")[1]+ " is not a proper extension for "+node.split(".")[0]+". Did you mean "+Poss_others
            
            else:
                nodeout=node+' is not a Node name'
            return render_template('Milestone_Main.html', Nodename=nodeout)
        #elif end_date < start_date==True:
        #    nodeout="Problem with Dates. Choose new dates."
        else:
            nodefind=NODE_info.loc[NODE_info['NODE_NAME']==node].index.tolist()[0]
            node1n=NODE_info.loc[nodefind]['NODE_NAME']
            node1s=NODE_info.loc[nodefind]['STATE']
            node1t=NODE_info.loc[nodefind]['TYPE']
            #if nodenum=='1nodes':
            nodenum=request.form['nodenum']
            if nodenum=='1nodes':
                
                dfprice=plotbokeh(node1n,start_date,end_date)
                bdate=np.array(dfprice['DATE'], dtype=np.datetime64)
                bprice=np.array(dfprice['PRICE'])
                p1=figure(x_axis_type='datetime')
                p1.line(bdate,bprice)
                #np.array(
                #,dtype=np.datetime64)
                p1.title = ' Energy Prices for ' + node1n
                p1.xaxis.axis_label = "Date"
                p1.yaxis.axis_label = "Price/MWh"
                script, div = components(p1)
                cout="Can add some text in here"
                return render_template('Onenode_plot.html',node1n=node1n, script=script, div=div,cout=cout)
            else:
                node2=request.form['nodename2']
                node2=node2.upper()
                if any(NODE_info.NODE_NAME==node2)==False:
                    if node2.split(".")[0] in NODE_front:
                        Poss_others=", ".join(NODE_info[NODE_info['NODE_NAME'].str.contains(node2.split(".")[0])]['NODE_NAME'].tolist())
                        nodeout=node2.split(".")[1]+ " is not a proper extension for "+node2.split(".")[0]+". Did you mean "+Poss_others
                    else:
                        nodeout=node2+' is not a Node name'
                    return render_template('Milestone_Main.html', Nodename=nodeout)
                else:
                    
                    dfprice=plotbokehcomp(node1n,node2, start_date, end_date)
                    bdate=np.array(dfprice['DATE'], dtype=np.datetime64)
                    bprice=np.array(dfprice['DIFF_COST'])
                    p1=figure(x_axis_type='datetime')
                    p1.line(bdate,bprice)
                    p1.title = "Temporal Energy Price Differences"
                    p1.xaxis.axis_label = "Date"
                    p1.yaxis.axis_label = "Price/MWh (+Node1,-Node2)"
                    script, div = components(p1)
                    Total_Charge=dfprice['DIFF_COST'].sum(axis=0)
                    cout= "The total charge was $"+str(Total_Charge)+" per MWh for transmitting energy from "+node1n+" to "+node2+"."
                    #cout2= "This charge is for the time range "+start_date+" to "+end_date+"."
                    #script=bdate
                    #div=bprice
                    #return render_template('/Milestone_Main.html',Nodename="",node1n=node1n,node1s=node1s,node1t=node1t)
                #else:
                #    script='empty'
                #    div='empty'
                    return render_template('Onenode_plot.html',node1n=node1n, script=script, div=div,cout=cout)

#@app.route('/Onenode_plot',methods=['GET','POST'])
#def Onenode_plot():
#    return render_template('Onenode_plot.html',node1n=node1n)

    

if __name__ == '__main__':
    app.run(port=33507)
