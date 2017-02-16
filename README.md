# 顔認識 API
<hr />

## Endpoint

https://mf7k96zs89.execute-api.us-west-2.amazonaws.com/dev/

## 認証

HTTPヘッダーに、`x-api-key`という名前でAPIキーを入れる必要があります。
三軒家に言ってもらえれば発行します。

<hr />

## 使い方
### 1. 動画IDを取得する

`GET /movie`を実行し、対象の動画IDを取得します。

#### 例

リクエストの例：
```shell
prompt %> curl --header "x-api-key: ${API_KEY}" "https://mf7k96zs89.execute-api.us-west-2.amazonaws.com/dev/movie/"
```

レスポンスの例：
```javascript
{
  "body": [
    {
      "capture_finish_at": null,
      "movie_id": "a06f449e9b83a9d473348d775d40a4e31487192288.51",
      "categorize_finish_at": "2017-02-16 12:24:36.124159",
      "object_key": "kaze_oke.mp4"
    },
    {
      "capture_finish_at": null,
      "movie_id": "a06f449e9b83a9d473348d775d40a4e31487191980.58",
      "categorize_finish_at": null,
      "object_key": "kaze_oke.mp4"
    },
    {
      "capture_finish_at": "2017-02-16 10:29:17.104173",
      "movie_id": "97bc47503d1ed6d302dc9198f2a323081487240915.31",
      "categorize_finish_at": "2017-02-16 11:29:13.924396",
      "object_key": "redcarpet_short.mp4"
    }
  ]
  "headers": {},
  "statusCode": 200
}
```

### 2. 動画IDから人物tagを取得する

`GET /movie/{movie_id}/tags`を実行し、人物tagの情報を取得します。

#### 例

リクエストの例：
```shell
curl --header "x-api-key: ${API_KEY}" "https://mf7k96zs89.execute-api.us-west-2.amazonaws.com/dev/movie/97bc47503d1ed6d302dc9198f2a323081487240915.31/tags"
```

レスポンスの例：
```javascript
{
  "body": {
    "24": [
      1,
      2,
      5
    ],
    "25": [
      2,
      1,
      5
    ],
    "26": [
      2,
      1,
      5
    ],
    "27": [
      2,
      5,
      1
    ]
  },
  "headers": {},
  "statusCode": 200
}
```


<hr />

## 各APIのドキュメント

### GET /movie

アップロードされている動画の一覧を取得するAPIです。

以下のようなレスポンスが返ってきます。

```javascript
{
  "body": [
    {
      "capture_finish_at": null,
      "movie_id": "a06f449e9b83a9d473348d775d40a4e31487192288.51",
      "categorize_finish_at": null,
      "object_key": "kaze_oke.mp4"
    },
    {
      "capture_finish_at": "2017-02-16 10:29:17.104173",
      "movie_id": "97bc47503d1ed6d302dc9198f2a323081487240915.31",
      "categorize_finish_at": "2017-02-16 11:29:13.924396",
      "object_key": "redcarpet_short.mp4"
    }
  ],
  "headers": {},
  "statusCode": 200
}
```

`body`プロパティがレスポンスの内容です。リストに含まれるHashがそれぞれ一つの動画を表しています。

- `capture_finish_at`と`categorize_finish_at`の両方が`null`でない動画についてのみ、顔認識情報を取得できます。
    - `capture_finish_at`が`null`の動画については、動画をアップロードしなおす必要があります。
    - `categorize_finish_at`が`null`の動画は、後述の`POST /movie/{movie_id}/tags`を実行して、顔の分類を行う必要があります

### POST /movie/{movie\_id}/tags

顔認識が完了した動画の、顔の分類を実行するAPIです。
後述の`GET /movie/{movie_id}/tags`を実行するために、事前に実行しておく必要があります。

以下のようなレスポンスが返ってきます。

```javascript
{
  "body": {
    "message": "success"
  },
  "headers": {
    "Content-Type": "application/json"
  },
  "statusCode": 200
}
```

### GET /movie/{movie\_id}/tags

顔の分類が完了した動画の、人物の出現時刻を取得するAPIです。

以下のようなレスポンスが返ってきます。

```javascript
{
  "body": {
    "1": [
      8
    ],
    "2": [
      8
    ],
    "3": [
      8
    ],
    "4": [
      8
    ],
    "5": [
      2,
      1
    ]
  },
  "headers": {},
  "statusCode": 200
}
```

`body`プロパティがレスポンスの内容です。

- このHashのkeyは動画開始からの時刻（秒）を表し、Hashのvalueはその時刻に動画に写っている人物のIDを表します。
    - 上記のレスポンスの例は、時刻00:01の時点では８番の人物だけが写っており、時刻00:05の時点では１番と２番の人物だけが写っている、という意味です。
- その秒数のときに動画に誰も写っていないときは、Hashのvalueは空リストになります。
