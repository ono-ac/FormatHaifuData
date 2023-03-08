# Format HaifuData
## 概要
天鳳牌譜ビューア形式の牌譜データをjsonl形式に変換するPythonプログラムです. 

## Usage
### 変換元データ
天鳳牌譜ビューアβ形式の埋め込み用IFRAME記述.  
[sample_haifudata.xml](test/sample_haifudata.xml)
### 実行
```
python3 reformat_haifudata.py --filepath "test/sample_haifudata.xml" --savedir "test" --detail
```
### 出力
jsonl形式の牌譜データ.  
[sample_output.json](test/created_haifudata.jsonl)

### 詳細
--detailで詳細な牌譜経過をコマンドラインに表示
```
-------------------------------------------------------------
0
START HAND
(0p) 黒沢 : 3m 6m 9m 1p 4p 7p 7p 1s 7s 8s 9s 1j 2j
(1p) 丸山 : 3m 5m 7m 1p 9p 3s 4s 8s 9s 3j 4j 6j 6j
(2p) 多井 : 1m 2m 7m 9m 3p 3p 6p 8p 9p 1s 3s 6s 6s
(3p) 沢崎 : 1m 3m 3m 5m 2p 3p 5p 8p 4s 1j 7j 7j R5p
-------------------------------------------------------------
1
	(0p) 黒沢   tumo : 6j
[3m 6m 9m 1p 4p 7p 7p 1s 7s 8s 9s 1j 2j]
 -> [3m 6m 9m 1p 4p 7p 7p 1s 7s 8s 9s 1j 2j 6j]

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2
	(0p) 黒沢   dahai : tumogiri
 -> [3m 6m 9m 1p 4p 7p 7p 1s 7s 8s 9s 1j 2j]

-------------------------------------------------------------
3
	(1p) 丸山   tumo : 8p
[3m 5m 7m 1p 9p 3s 4s 8s 9s 3j 4j 6j 6j]
 -> [3m 5m 7m 1p 8p 9p 3s 4s 8s 9s 3j 4j 6j 6j]

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
4
	(1p) 丸山   dahai : 1p
 -> [3m 5m 7m 8p 9p 3s 4s 8s 9s 3j 4j 6j 6j]

-------------------------------------------------------------
5
	(2p) 多井   tumo : 5p
[1m 2m 7m 9m 3p 3p 6p 8p 9p 1s 3s 6s 6s]
 -> [1m 2m 7m 9m 3p 3p 5p 6p 8p 9p 1s 3s 6s 6s]

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
6
	(2p) 多井   dahai : 9p
 -> [1m 2m 7m 9m 3p 3p 5p 6p 8p 1s 3s 6s 6s]

-------------------------------------------------------------
7
...

```


## 実行環境
Python 3.10

