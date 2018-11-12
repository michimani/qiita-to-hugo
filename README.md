## About
Qitia の投稿を Hugo 用に出力します。

## Usage
1. clone

```
$ git clone https://github.com/michimani/qiita-to-hugo.git
$ cd qiita-to-hugo.git
```

2. config setting

```
$ cp config.ini.sample config.ini
```

Qiita のマイページから作成したアクセストークンを記述します。

```diff
 [qiita]
- access_token = your_qiita_access_token
+ access_token = 1234567890abcdefghijklmnopqrstuvwxyz
```

3. run

```
$ python qth.py
```

## Detail
- Markdown は`content/posts` 以下に生成されます。
- Markdown のファイル名は、 Qiita の記事タイトルをファイル名に使用できる形で加工したものになります。
- Qiita 記事内の画像は `static/images` 以下に保存されます。
- 記事内の画像リンクは、 `/images/*` の形に置き換えられます。
- 記事内の画像の alt 属性は、該当ファイルのファイル名に置き換えられます。

## Note
- このスクリプトは、対象の Qiita の記事が 100 記事以内を想定しています。