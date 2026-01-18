## TexyC



① PDFを人間可読にする（最優先）
qpdf --qdf --object-streams=disable texyc.pdf out.pdf


これで：

FlateDecode が剥がれる

オブジェクトが平文になる

TeXが仕込んだゴミも全部見える

--

PDF解析 → TeX展開 → ハッシュ逆算

「PDFに何か隠れてる？」という直感は正解

しかし 本丸はLaTeXコード

crypto + reversing の中間問題

アルゴリズムの正体（重要）

このコード、見た目は複雑ですが正体は：

16bit × 2（ASIS@H, ASIS@L）

初期値：0xFFFF, 0xFFFF

多項式：

poly@H = 60856 (0xEDB8)

poly@L = 33568 (0x8320)

GF(2) 上のシフト＋条件付き XOR

つまり CRC系（カスタムCRC32もどき）

しかも致命的に：

ソルトなし・秘密なし・4文字固定長

CTF作者の優しさが滲み出ています。

攻撃方針（最短ルート）
方針は一択

4文字 → ハッシュ
なので
ハッシュ → 4文字 を総当たり

です。

ASCII printable（例えば flag{} 含む）なら：

95⁴ ≒ 81M（やや多い）

でも実際は：

flag{...} 形式

英数字 + _{}

実質数万〜数十万

しかも 8個しかない。