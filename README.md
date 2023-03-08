# Format HaifuData
## 概要
天鳳牌譜ビューア形式の牌譜データをjsonl形式に変換するPythonプログラムです. 

## Usage
### 変換元データ
天鳳牌譜ビューアβ形式のIFRAME記述.  
[sample_haifudata.xml](test/sample_haifudata.xml)
### 実行
```
python3 reformat_haifudata.py --filepath "test/sample_haifudata.xml" --savedir "test" --detail
```
### 出力
jsonl形式の牌譜データ.  
[sample_output.json](test/created_haifudata.jsonl)

### 詳細
"--detail"で詳細な牌譜経過をコマンドラインに表示


## 実行環境
Python 3.10

