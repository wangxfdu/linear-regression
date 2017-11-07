# linear-regression

## 环境搭建(仅需一次)
* 下载 Anaconda https://repo.continuum.io/archive/Anaconda2-5.0.1-Windows-x86_64.exe or https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda2-5.0.1-Windows-x86_64.exe (国内镜像)
* 双击安装，安装路径可改
* 安装wxPython包
  * 在程序中找到"Anaconda Prompt"，点击运行
  * 输入conda install -c anaconda wxpython，回车。若有提示，输入y。（此步骤需要网络）
  * 安装成功，关闭退出
  * PS: 如果下载非常慢，请在执行conda install之前额外输入以下命令 (尚未亲测)
    * conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
    * conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    * conda config --set show_channel_urls yes
## 运行程序
* 下载本工程中的main.py，保存到本地，如c:\test1\test2 如果程序有更新，重新下载即可
* 在程序中找到"Anaconda Prompt"，点击运行
* cd c:\test1\test2
* python main.py
