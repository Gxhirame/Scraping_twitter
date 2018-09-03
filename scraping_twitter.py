import tweepy, os, mysql.connector
from dotenv import load_dotenv
from os.path import join, dirname
from datetime import timedelta
from datetime import datetime as dt
import math
from math import pi
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.io import show
import pandas as pd


dotenv_path=join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#MySQLに接続する。
conn=mysql.connector.connect(
    host='localhost',
    port='3306',
    user='xxxxxxxxx',
    password='xxxxxxxxx',
    database='twitter_db',
    )
c=conn.cursor()

consumer_key=os.environ.get('CONSUMER_KEY')
consumer_secret=os.environ.get('CONSUMER_SECRET')
access_token=os.environ.get('ACCESS_TOKEN')
access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')

#認証情報を設定する
auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#APIインスタンスを作成
api=tweepy.API(auth)




def main():
    #アカ１
    Account=input("Acount:@")
    num=1
    pages=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17]
    c.execute('''CREATE TABLE IF NOT EXISTS tweets(id int AUTO_INCREMENT, DATEandTIME datetime, date date, time time, contents text, index(id))''')
    c.execute('''DELETE FROM tweets''')
    c.execute('''ALTER table tweets AUTO_INCREMENT=1''')
    for page in pages:
        tweets=api.user_timeline(Account, count=20, page=page)
        for tweet in tweets:
            tweet.created_at+=timedelta(hours=9)
            DT=tweet.created_at
            D=str(tweet.created_at.year) +"-" +str(tweet.created_at.month) +"-" +str(tweet.created_at.day)
            T=str(tweet.created_at.hour) +":" +str(tweet.created_at.minute)
            contents=tweet.text
            c.execute('''INSERT INTO tweets(DATEandTIME, date, time , contents) VALUES(%s,%s,%s,%s)''',(DT, D, T, contents))
            conn.commit()
            print('-----')
            print(DT)
            print(contents)
            print(num, 'ツイート目')
            num=num+1
    print("---------------------")
    print("合計で",num, "ツイートしました。")
    print("---------------------")
    xnum=1
    xlists=[]
    c.execute("SELECT date FROM tweets")
    while xnum<num:
        xsecs=c.fetchone()
        xnum+=1
        for xsec in xsecs:
            #print (xsec)
            xlists.append(str(xsec))
    print(xlists)
    
    print("---------------------")
    
    ynum=1
    ylists=[]
    c.execute("SELECT time FROM tweets")
    while ynum<num:
        ysecs=c.fetchone()
        ynum+=1
        for ysec in ysecs:
            #print(ysec)
            ylists.append(str(ysec))
    print(ylists)
    conn.close()
    
    """ここからBokeh"""
    #graph():
    num-=2
    # xlist,ylistを datetime型に変換
    xlist = [dt.strptime(d, '%Y-%m-%d') for d in xlists]
    ylist = [dt.strptime(d, '%H:%M:%S') for d in ylists]

    # データをプロット
    p = figure(x_axis_type='datetime',
               y_axis_type='datetime',
               tools="xpan, xwheel_pan,xwheel_zoom",
               x_range=(dt.strptime(xlists[num],'%Y-%m-%d'),
                        dt.strptime(xlists[0], '%Y-%m-%d')),
               y_range=(dt.strptime('00:00','%H:%M'),
                        dt.strptime('23:59','%H:%M')))
    p.circle(xlist, ylist,
             size=10,
            fill_alpha=0.5,)

    # X軸の設定
    x_format = "%m/%d"
    p.xaxis.formatter = DatetimeTickFormatter(
        seconds=[x_format],
        minutes=[x_format],
        hours=[x_format],
        days=[x_format],
        months=[x_format],
        years=[x_format]
    )
    p.xaxis.major_label_orientation = math.radians(90)

    # Y軸の設定
    y_format = "%H:%M"
    p.yaxis.formatter = DatetimeTickFormatter(
        seconds=[y_format],
        minutes=[y_format],
        hours=[y_format],
        days=[y_format],
        months=[y_format],
        years=[y_format]
        )
    
    #軸の角度
    p.xaxis.major_label_orientation=pi/4
    show(p)
    
    
    print(xlists[0])
    print(xlists[num])
    print(ylists[0])
    print(ylists[num])
    
    
if __name__=='__main__':
    main()