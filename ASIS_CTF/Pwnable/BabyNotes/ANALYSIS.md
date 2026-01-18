# BabyNotes - ASIS CTF Pwnable

**Target:** nc 65.109.211.136 13373

**Original Message:** Welcome to BabyNotes! Your notes, our responsibility ;)

## Binary Info

- **Type:** ELF 64-bit LSB PIE executable
- **Architecture:** x86-64
- **Protections:** PIE enabled, likely has stack canary
- **Stripped:** Yes
- **File:** babynotes

## Functionality

BabyNotesは以下の機能を持つノート管理プログラム：

1. **Add** - ノートを追加
   - サイズを指定
   - データを入力
   - `/tmp/.n%04d` 形式のファイルとして保存される可能性
   
2. **Edit** - ノートを編集
   - インデックスを指定
   - 新しいコンテンツを入力
   
3. **View** - ノートを表示
   - インデックスを指定
   - 内容を表示（ただし、テストでは表示されず）
   
4. **Delete** - ノートを削除
   - インデックスを指定
   - ノートを削除

5. **Exit** - プログラム終了

## 発見された文字列

```
/tmp/.n%04d        # 一時ファイルのパターン
[-] Full           # ノートが満杯
[-] Invalid        # 無効な入力
[-] Failed         # 失敗
[+] Note %d        # ノート追加成功
[-] Error          # エラー
[+] Done           # 完了
[+] Deleted        # 削除成功
[!] Time's up!     # タイムアウト
```

## 解析のポイント

1. **一時ファイルの使用**
   - `/tmp/.n%04d` パターンでファイルを作成
   - ファイルディスクリプタの管理
   - open()とfstat()の呼び出しが確認できる
   
2. **グローバル配列**
   - `0x40a0` あたりにノートポインタの配列がありそう
   - malloc()でヒープメモリを確保
   - 16バイト単位 (shl rax, 0x4 = << 4)
   
3. **可能な脆弱性**
   - Use-After-Free (UAF)
   - Double Free
   - Heap Overflow
   - File descriptor confusion
   - Race condition (一時ファイル)
   - Integer overflow (サイズ指定)

## テスト結果

```bash
# 基本動作テスト
$ echo -e "1\n32\nAAAAAAAA\n3\n0\n4\n0\n5" | ./babynotes
- Add成功: [+] Note 0
- View: 出力なし (?)
- Delete成功: [+] Deleted
```

## 次のステップ

- [ ] Ghidra/IDAで詳細な逆アセンブル
- [ ] Heap構造の確認
- [ ] Use-After-Free の有無をテスト
- [ ] ファイルディスクリプタ操作の悪用
- [ ] Libc leak とROP chain構築
- [ ] リモートサーバーでテスト
