# MP42YUV
# 北京大学深圳研究生院2023年秋季学期数字图像基础第一次作业

##使用方法

使用命令行工具，输入以下命令：

```python mp4toyuv.py input_file width height fps --output_file output_file(optional)```

如：

```python mp4toyuv.py oceans.mp4 320 240 15```

即可将本仓库的oceans.mp4转换为YUV格式的视频，默认存储位置为当前文件夹

或者使用：

```python mp4toyuv.py oceans.mp4 320 240 15 --output_file ./output_file.yuv```

即可更改存储位置和文件名称

## 参考
本代码参考了WenhongZhang学长的代码，在此基础上对代码进行了些许优化，加快了处理速度；

添加了命令行解析器，方便代码使用。

参考代码仓库：https://github.com/WenhongZhang/video-rgb2yuv
