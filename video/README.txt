## 编解码原理(流程)
@Td


## 程序分层与输入输出

### 总入口

需求, 便利性决定总入口的输入输出.

davi.py: 图片序列 <-> 视频格式

`python3 davi.py encode images/ xxx`
生成视频 `xxx.davi`

`python3 davi.py decode xxx images/`
解析视频, 得到图片序列

### 分层

编解码原理, 决定了分层输入输出.
包括: 图片集合, 预测帧数据, 视频格式.

pred  一个场景的图片序列 <-> 预测帧数据
video 预测帧数据 <-> 视频格式

`python3 pred.py encode 1.png 2.png vblock_dir/ diff_dir/`
产出预测帧数据 `2.vblock` 和 `2.diff.png`

`python3 pred.py decode 1.png 2.vblock 2.diff.png 2.png`
还原出图片`2.png`

`python3 video.py encode 1.png vblock/ diff/ xxx`
产出`xxx.davi`

`python3 video.py decode xxx vblock/ diff/`
在指定路径解析出 预测帧数据


## davi视频规格说明

Header
	identifier:: 4s		// 'davi', 4bytes
	version:: 4s 		// '1.0\n'
	frames:: B			// 1bytes
	width::  H 			// 2bytes
	height:: H 			// 2bytes

Diff[]
	size1:: I			// 4bytes
	diff1:: bytes

VBlock[], 图块长度8, 每帧的图块数量 = (width/8) * (heigth/8)
	x:: 	H 			// 2bytes
	y:: 	H 			// 2bytes
