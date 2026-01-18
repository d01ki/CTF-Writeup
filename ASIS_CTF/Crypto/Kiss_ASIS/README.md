Kiss ASIS — 分析まとめ

**概要**

このチャレンジはカスタムキー生成を行う RSA 問題です。サーバーに接続して公開パラメータを取得し、暗号文を復号できればフラグを取得できます。

接続先:
- `nc 65.109.214.93 13137`

含まれるファイル:
- `kiss_asis.py` — サーバー側のスクリプト（添付済み）
- `solve.py` / `offline_solve.py` / `solve_pwn.py` — 作業用スクリプト（ワークスペース内）

発見事項（取得済みパラメータ）:
- N: 1020 ビット (取得済み)
- e: 約2048 ビット (取得済み)
- enc: 暗号文（取得済み）

脆弱性のポイント
- `genkey` の実装: d を小さく作っている（dbit = int(nbit * D) + 1、D は 0.9990～0.9999）
- `phi` の計算が通常と異なる: `phi = (p**k - 1) * (q**k - 1)`（k は 1..6 のランダム）
- `e` は `inverse(phi + (-1)**r * d, phi)` として計算され、結果として `e*d ≡ ±1 (mod phi)` の関係が成り立つ

試した攻撃と結果
- Wiener's attack（小さい d を狙う連分数攻撃）を実装して試行しましたが、標準的な Wiener の条件では復号まで至りませんでした（`offline_solve.py` 使用）。
- 複数のスクリプトでサーバー応答をキャプチャし、`N`、`e`、`enc` は取得済みです（出力は `raw_data.txt` / スクリプトで再現可能）。

残りの方針（推奨）
- 高速因数分解（ECM / msieve / yafu）で `N` を分解する（現実的かつ最も直接的）。ローカルで msieve/ECM を実行できます。
- Boneh–Durfee / 改良型小 d 攻撃を試す（実装は複雑で時間がかかる可能性あり）。
- サーバーへ複数回接続して別インスタンスの鍵や暗号文を収集し、鍵再利用や統計的弱点を探す。

再現手順（ローカル）

1. サーバーへ接続してパラメータを取得:
```bash
python3 Kiss_ASIS/test_connection.py
# または
nc 65.109.214.93 13137
# -> メニューで 'p' と 'e' を選択して N, e, enc を取得
```

2. 取得した `N`, `e`, `enc` を `offline_solve.py` に貼り付けて Wiener's 攻撃を試す:
```bash
python3 Kiss_ASIS/offline_solve.py
```

3. 因数分解を試す（例: msieve/ECM）:
```bash
# msieve の利用例
msieve -v -d N_value
# または ECM (gmp-ecm)
gmp-ecm -q N_value
```

次の提案
- まずは ECM/msieve 等で `N` を分解してみるのが最短ルートです。私が代行して試す場合は、どの方法（msieve / yafu / gmp-ecm）を優先するか指示ください。

付録: 既存スクリプト
- `Kiss_ASIS/solve.py` — インタラクティブに接続して自動で攻撃を試みるスクリプト（途中デバッグあり）
- `Kiss_ASIS/solve_pwn.py` — `pwntools` 版（環境に pwntools が必要）
- `Kiss_ASIS/offline_solve.py` — 取得したパラメータでローカル解析用スクリプト

―― まとめ終わり ――
