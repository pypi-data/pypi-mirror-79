
# relpath

!!! このドキュメントは書きかけです。
!!! This document is a work in progress.

下の方に日本語・●・●の説明があります

## 概要 (日本語)
このパッケージでできること:
1. 直感的な相対パス参照ができる
	- pythonのパス参照の仕様は直感に反する
2. モジュールの相対importに使える
	- フォルダが多重で複雑なプロジェクトにも対応できる

## 使い方1: 基本的な例

下記は、pythonファイル自身の場所(ディレクトリ)を取得する例です。

```python
import relpath as rp
print(rp.rel2abs("./"))	# -> "(このpythonファイルが存在するディレクトリ)"
```

## 使い方2: 実用的な例

このツールは、下記のような場合に真価を発揮します。

```
.
`-- project_folder
    |-- parts
    |   |-- data.txt
    |   `-- script_B.py
    `-- script_A.py
```

上記のように、複数のpythonファイルからなるプロジェクトを考えます。
`script_A.py`の中では下記のように、`script_B.py`を利用します。

```python
# script_A.py

# load script_B.py
from parts.script_B import get_data

print(get_data())
```

この場合に、下記のコード例のように、
`script_B.py`から"./data.txt"を相対的に読み込もうとすると失敗します。[^1]

[^1]: 厳密には、`script_A.py`からの相対パス指定をすれば読み込めますが、呼び出し元が別の場所に変更された場合、正常に動作しなくなるので、メンテナンス性が悪くなります。これを回避するため、`relpath`パッケージの利用を推奨します。

```python
# script_B.py

def get_data():
    with open("./data.txt", "r") as f:  # -> FileNotFoundError: [Errno 2] No such file or directory: './data.txt'
        return f.read()
```

そこで、`relpath`パッケージを使って下記のように書くと、
"./data.txt"を相対的に読み込めるようになります。[^2]

```python
# script_B.py

from relpath import rel2abs

def get_data():
    with open(rel2abs("./data.txt"), "r") as f:  # -> NO ERROR!!
        return f.read()
```

[^2]: 相対パスに関するpythonの仕様は、必ずしも間違いというわけではありません。pythonの仕様(相対パスの指定が、記述するファイルの場所に関わらず、常に最初の呼び出し元を基準として解釈される仕様)には、プログラムを開発する中でもしファイル読み込み等の命令を記述する場所(ファイル)が変更になった場合でも、パス指定方法の変更が不要になるという利点があります。`relpath`パッケージは、pythonの仕様の他に、プログラマーにもう一つの選択肢を与える手段に過ぎないので、状況に応じて利用の要否を検討することを推奨します。

## 使い方3: 相対importとしての利用

`relpath`パッケージを利用すると、下記の例のように、
モジュールの直感的な相対importを実現できます。

```python
from relpath import add_import_path
add_import_path("../")

from my_module import some_function

some_function()
```

上記の例を見ると、単に`sys.path.append("../")`としても動作するように思われます。
しかし、プロジェクトフォルダの階層構造が複雑で、1つのモジュールが別々の場所から使われるような場合には、`sys.path.append("../")`では対応できないことがあります。
そのため、相対importを実現したいときは、常に`relpath`パッケージの`add_import_path`を利用することを推奨します。

なお、`add_import_path("../")`
は、内部的には`sys.path.append(rel2abs("../"))`と等価です。
