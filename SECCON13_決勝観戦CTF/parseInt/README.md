## parseInt

a < b && parseInt(a) > parseInt(b) となるような a, b を見つけてください🐟
```
const rl = require("node:readline").createInterface({
    input: process.stdin,
    output: process.stdout,
});

rl.question("Input a,b: ", input => {
    const [a, b] = input.toString().trim().split(",").map(Number);
    if (a < b && parseInt(a) > parseInt(b))
        console.log(process.env.FLAG);
    else
        console.log(":(");
    rl.close();
});
```
## solve
`if (a < b && parseInt(a) > parseInt(b))`
- a < b :文字列比較
- parseInt() は文字列を整数として解釈します。文字列に数字が続いていても、数値として解釈できる部分だけが使われ、残りは無視される

大きい数値いれれば行けそう
```
$ nc 34.170.146.252 45996
Input a,b: 100000000000000000000,1000000000000000000000
100000000000000000000,1000000000000000000000
Alpaca{..ww.w....<')))><.~~~}
```

### flag
`Alpaca{..ww.w....<')))><.~~~}`
100000000000000000,100000000000000000000