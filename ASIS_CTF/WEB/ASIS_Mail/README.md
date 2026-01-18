# ASIS CTF - ASIS_Mail Challenge

**Target:** http://91.107.143.167:8081/

## アーキテクチャ

Docker Composeで構成された複数のマイクロサービス：

### サービス構成

1. **db** (PostgreSQL)
   - ユーザー、メール、添付ファイル情報を保存
   - admin user: id=999, username='admin'

2. **sso** (Node.js/Express) - 認証サービス
   - ポート: 3001 (内部)
   - エンドポイント:
     - `POST /register` - ユーザー登録
     - `POST /login` - ログイン (tokenを返す)
     - `GET /auth` - トークン検証 (X-User-Id, X-User-Emailヘッダーを返す)
   - セッション管理: メモリ内にsessions = {}オブジェクト

3. **objectstore** (Python/Flask) - ファイルストレージ
   - ポート: 8082 (内部)
   - 認証: `X-User-Id` ヘッダー
   - **重要な脆弱性ポイント:**
     - `is_admin = user_id == "999"` でadmin判定
     - FLAGバケットへのアクセスはadminのみ許可
   - エンドポイント:
     - `GET/PUT/DELETE /<bucket>/<object_name>` - オブジェクト操作
     - `GET/POST /<bucket>` - バケット一覧/アップロード
     - `GET /public/<bucket>/<object_name>` - 公開ファイルアクセス (FLAGバケット除く)
     - `GET /public/<bucket>/<object_name>/hash` - ファイルハッシュ取得
   - flag.txt: ASIS{FAKE_FLAG} (ローカルのみ、本番は実際のflag)

4. **api** (Go バイナリ) - メールAPI
   - ポート: 不明 (内部)
   - エンドポイント (JSから推測):
     - `POST /compose` - メール送信 (XML + 添付ファイル)
     - `GET /inbox` - 受信箱
     - `GET /mail/:id` - メール詳細
   - XML処理とattachmentアップロードを実装
   - authMiddleware: SSOの/authを使ってユーザー認証

5. **frontend** (nginx + React)
   - ポート: 8081 (公開)
   - `/sso/*` → sso:3001
   - `/api/*` → api
   - `/objectstore/*` → objectstore:8082
   - 静的ファイル提供

## 既知の情報

### データベーススキーマ

```sql
-- users: id, username, password_hash, email
-- emails: id, user_id, from_addr, to_addr, subject, body, created_at
-- attachments: id, email_id, filename, object_url, object_key
-- admin user: id=999
```

### メール送信フロー

1. フロントエンドから `/api/compose` へPOST
2. XMLとファイルをmultipart/form-dataで送信
   ```xml
   <message>
     <to>recipient@asismail.local</to>
     <subject>Subject</subject>
     <body>Body</body>
   </message>
   ```
3. 添付ファイルは `uploadToObjectStore` 関数でobjectstoreへアップロード
4. メール情報とattachment URLをDBに保存

### 認証フロー

1. ユーザー登録: `/sso/register` → DBにユーザー作成
2. ログイン: `/sso/login` → セッショントークン発行
3. API呼び出し: `Authorization: Bearer <token>` ヘッダー
4. authMiddleware: `/sso/auth` を呼び出して `X-User-Id` を取得
5. objectstore呼び出し: `X-User-Id` ヘッダーで認証

## 攻撃可能性

### 1. XXE (XML External Entity) Injection
- `/api/compose` のXML処理でXXE脆弱性の可能性
- ファイル読み取りやSSRFが可能かも

### 2. Path Traversal
- objectstoreの `/<bucket>/<path:object_name>` でpath traversal
- しかし、Pythonの `pathlib.Path` は安全な実装

### 3. Admin User Impersonation
- **最も有望**: `X-User-Id: 999` ヘッダーを偽装できれば、FLAGバケットにアクセス可能
- 問題: SSOの `/auth` エンドポイントが正しい `X-User-Id` を返す
- 可能性: nginxの設定ミス、ヘッダーインジェクション、またはSSRF経由でobjectstoreに直接アクセス

### 4. SSRF (Server-Side Request Forgery)
- `/api/compose` からobjectstoreへの内部リクエスト
- XXEを使ってSSRFを発動し、objectstoreに直接 `X-User-Id: 999` でアクセス

### 5. Session Hijacking
- adminのセッショントークンを取得
- しかしadminは通常ログインしていない

## 次のステップ

1. [ ] `/api/compose` のXML処理を詳しく調査
2. [ ] XXE payloadをテスト
3. [ ] nginx設定を推測 (ヘッダーフィルタリング)
4. [ ] objectstoreへの直接アクセスを試行
5. [ ] `/public/<bucket>/<object_name>/hash` エンドポイントを悪用

## テスト済み

- ユーザー登録・ログイン: 成功 (ctfuser作成)
- トークン取得: 成功
- 正しいAPIエンドポイント: `/api/inbox`, `/api/mail/:id`, `/api/compose`
- objectstore FLAG直接アクセス: nginxで404 (フィルタリング)

### XXE/SSRF攻撃テスト結果

1. **基本的なXXE (file:// プロトコル)**: 
   - 送信成功 (200 OK)
   - しかしメールbodyにエンティティが展開されない
   - GoのXMLパーサーが安全にパース (エンティティ無効化)

2. **SSRF to objectstore**:
   - `<!ENTITY ssrf SYSTEM "http://objectstore:8082/FLAG">` 送信成功
   - しかしレスポンスに内容が反映されない
   - XMLパーサーがexternal entityを無効化している可能性

3. **Parameter Entity**:
   - テスト実施、送信成功
   - しかし効果なし

4. **CDATA & Numeric Character Reference**:
   - テスト実施、通常の動作

5. **添付ファイルアップロード with Path Traversal**:
   - ファイル名 `../../FLAG/flag.txt` でアップロード試行
   - 送信成功したが、実際のパスは不明

## メモ

- objectstore.pyの `/public/<bucket>/<object_name>/hash` エンドポイントは**FLAGバケットのチェックなし**
  - これを使ってFLAGファイルの内容ハッシュを取得可能
  - しかし、ハッシュからflagを復元するのは困難
  
- Go APIバイナリにstrings検索で `/compose`, `/inbox`, `/mail/` が見つかった
  - ソースパス: `/home/x1/dev/ctf/2025/ASIS/Final/WEB/asis-mail-build/api/main.go`

## 攻略方針

### 現在の状況
- **XXE攻撃は無効**: GoのXMLパーサーがexternal entityを展開していない
- **SSRF経由のアクセス**: 送信は成功するが、レスポンスが得られない
- **nginx前段フィルタ**: `/objectstore/public/FLAG/*` へのアクセスをブロック

### 次の試行候補

1. **Blind XXE / OOB (Out-of-Band)**
   - 外部サーバーへのコールバックでデータを抽出
   - しかし、ネットワーク制限がある可能性

2. **objectstore APIの別の脆弱性**
   - `/public/<bucket>/<object_name>/hash` エンドポイントにFLAGチェックなし
   - しかしnginxでブロックされている
   - 内部からのアクセスが必要（SSRF経由）

3. **添付ファイル機能の悪用**
   - `uploadToObjectStore` 関数の実装を推測
   - objectstoreへのアップロード時に `X-User-Id` ヘッダーを設定
   - ヘッダーインジェクションやRace Conditionの可能性

4. **Go API バイナリの解析**
   - stringsで見つかったパス: `/home/x1/dev/ctf/2025/ASIS/Final/WEB/asis-mail-build/api/main.go`
   - バイナリを逆コンパイルして詳細な実装を確認

5. **nginx設定の推測とバイパス**
   - リバースプロキシの設定ミス
   - パスの正規化の違い（`//`, `./`, URL encoding等）

### 推奨アクション
1. Go APIバイナリをGhidraなどで解析
2. nginxのパス正規化バイパスを試す（例: `/objectstore//public/FLAG/flag.txt/hash`）
3. Blind XXEでSSRF経由のデータ抽出を試す
4. 添付ファイルアップロードの内部実装を詳しく調査
