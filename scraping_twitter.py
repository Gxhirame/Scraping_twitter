import tweepy, os
from dotenv import load_dotenv
from os.path import join, dirname

#パスの取得＆ロード（多分）
dotenv_path=join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#.env.sampleから各値を取得する。
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
    #入力によりツイートを抽出するアカウントのID取得。
    Account=input("Acount:@")
    num=0
    id_list=[]
    pages=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17]
    for page in pages:
        for tweet in api.user_timeline(Account, count=200, page=page):
            print('-----')
            print(tweet.created_at)
            print(tweet.text)
            num=num+1
    print(num,"ツイート表示しました。")
    

if __name__=='__main__':
    main()