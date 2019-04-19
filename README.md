# Maltose


一个使用Django编写的静态博客生成器，当然你可以选择不使用生成器功能，而作为一个单纯的Django博客部署到主机上。

--------

## 安装

由于作者精力有限，目前只提供由源码生成方法

```bash
git clone https://github.com/maltoseeditor/maltose.git
```

--------

## 快速开始


#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 修改配置

在运行服务之前，你需要在`./matlose/settings.py`做好相关配置，示例如下：

```python
HOMEPAGE = 'https://abersheeran.com' # 主页
```

需要注意的是，`HOMEPAGE`参数应严格遵循 **协议://域名** 的形式，其余参数如无必要无需更改。

#### 3. 加入环境变量

将`maltose.py`的路径加入Windows环境变量，或在Linux中软链接到`/usr/bin/maltose.py`。

#### 4. 初始化服务

将工作目录切换到你的Blog文件夹，此目录下必须要有`templates`文件夹，包含自己的模板文件以及静态文件。

```bash
python maltose.py migrate

python maltose.py createsuperuser
```

#### 5. 运行服务

现在你可以愉快地在本地运行matlose了。

```
python maltose.py runserver
```

--------

## 编写第一篇博客

如果上述过程没有发生意外，当你打开浏览器输入`127.0.0.1:8000`时，你就可以看到一个崭新的个人博客了，现在你可以进入`127.0.0.1:8000/editor/`开始编写你的第一篇博客。

![](./example.png)
