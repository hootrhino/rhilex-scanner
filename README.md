# rhino-scanner
![1700120284351](image/README/1700120284351.png)

设备扫描器, 这个软件是Chatgpt帮忙写的！注意IP范围和子网掩码不要输错了。

## 下载
这里已经打包好了一个exe：https://github.com/hootrhino/rhilex-scanner/tree/master/release 。其他系统没试过，应该是可以跨平台的。

## 搭建环境
开发环境用python3.11，注意环境安装正确。
```sh
python -m venv venv
cd ./venv/Scripts
./Activate.ps1
pip install pyinstaller
pip install -r required.txt
```
## Build
```sh
pyinstaller --noconsole --onefile --name RhilexScanner rhilex-scanner.py
```
编译好的在 `dits` 目录下。