# For Windows 11 run guide

You must have Line Develpoer's account :
https://developers.line.biz/en/
(Set your account first)

Download repostory
```
git clone https://github.com/Steve900125/FengShuiLineChatBot.git
```

Install requirements package
```
pip install -r requirements.txt
```



### Initial 
In .en file add these
```
LINE_BOT_API_KEY = ""
SQL_URL = "External Database URL"
PYTHON_VERSION = 3.8.18
TAVILY_API_KEY = ""
OPENAI_API_KEY = ""
CHANNEL_SECRECT_KEY = ""
```
Create database and table columns ...
```
conda install psycopg2
python initial\initial_all.py
```

### AWS upload image by S3

```
aws configure
```

IAM can get Access Key and Secret 


```
AWS Access Key ID [None]: AKIA*******WHQ4R
AWS Secret Access Key [None]: MJem************mdt5ZK4T5
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

S3 bucket fschatbot is bucket name
Bucket policy
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicReadAccess",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::fschatbot/*"
    }
  ]
}
```

Click "ngroke.exe"

Set your ngrok 
```
ngrok config add-authtoken xxYour-Tokenxxx
```

Open your port on 5000 (flask default)
```
ngrok http --domain=big-rattler-certainly.ngrok-free.app 5000
```

Set your call back route on MessagesAPI Webhook URL

![alt text](image.png)

Run the code
```
python main.py
```

