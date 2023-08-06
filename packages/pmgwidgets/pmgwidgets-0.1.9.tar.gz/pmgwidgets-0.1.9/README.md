# pmgwidgets常用控件介绍
``` python
from pmgwidgets import {控件名}
```
用以上语句即可导入相应的控件。
控件的有关示例见pmgwidgets/tests文件夹。
## 设置控件SettingsPanel
查看示例即可。在tests/settings_panel中,运行示例即可得到以下界面：

![](pmgwidgets/doc_figures/settings_panel.png)
创建这个界面只需要一个json式的数据结构，如下所示：
```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150)),
         ('number', 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
         ('bool', 'sport', 'do you like sport', True),
         ('choose_box', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
          ['f22战斗机', 'f18战斗轰炸机', 'j20战斗机', 'su57战斗机']),
         ('color', 'color', 'Which color do u like?', (0, 200, 0))]
```
这些数据的格式为：
数据类型；数据名称；提示信息；初始值。第四位之后的其他数据为修饰信息，比如单位、范围等。

| 返回值类型                               | 1:选择器名称 | 2:数据名称 | 3：提示信息 | 4：初始值                  | 5        | 6               |
| ---------------------------------------- | ------------ | ---------- | ----------- | -------------------------- | -------- | --------------- |
| 字符串型（str）                          | 'line_edit'  | str        | str         | 初始值：str                | /        | /               |
| 整型或者浮点（int/float）字符串型（str） | 'number'     | 名称:str   | str         | int/float初始值：str       | 单位str  | 范围（min,max） |
| 布尔型（bool）                           | 'bool'       | str        | str         | bool                       | /        | /               |
| 任意类型，多选一（str）                  | 'choose_box' | str        | str         | object（任意类型）*        | 选项列表 | 选项文本列表    |
| 颜色（返回形如'#a0b89d'的颜色字符串）    |              | 'color'    | str         | tupleRGB,每位为0~255的整数 | /        |                 |
*:注意，任意类型，多选一的下拉列表中，列表可以填入任意类型。但是你所输入的初始值，必须在选项列表中存在，否则会抛出异常。

## 文件树控件
class PMGFilesTreeview(QTreeView):
### 如何插入界面
def __init__(self, initial_dir: str = '', parent=None):
initial_dir:str,初始时的路径。
parent:父控件，可以为None。
### 信号：
 - new_file_signal = pyqtSignal(str)
 新建文件信号，返回一个参数，是新建文件的绝对路径
 - new_folder_signal = pyqtSignal(str)
 新建文件夹信号，返回一个参数，是新建文件夹的绝对路径
 - delete_file_signal = pyqtSignal(str)
 删除文件或者文件夹信号，返回一个参数，是文件夹的绝对路径。
 - rename_file_signal = pyqtSignal(str, str)
 文件重命名的信号，返回两个参数，分别是重命名之前的绝对路径和重命名之后的绝对路径。

 注意：以上信号都是只有操作成功才会被触发的。**如果操作不成功（比如重命名时存在相同文件、删除文件时权限不够），那么就不会触发。**。


# 容器控件
## 流式布局控件PMFlowArea

流式布局控件为PMFlowArea，示例见tests文件夹的flow_layout_widget.py。

运行这个例子可以发现以下效果：
![](pmgwidgets/doc_figures/pmflowarea_1.png)
![](pmgwidgets/doc_figures/pmflowarea_2.png)
可以看到，布局在界面左右拖拽的时候，按钮会自动重排。
问题：控件库的按钮自动重排之前，似乎不是从0,0开始添加按钮的。
## 选项卡控件PMGTabWidget
(这里名字不对！需要改过来！！)
是选项卡控件。
选项卡控件的特点是，它的setup_ui方法中，会调用子界面的setup_ui方法。同理也适用于bind_events。
## 可停靠控件PMGDockWidget
额外定义了raise_into_view的方法，调用这方法时可以保证此控件提升到窗口最顶端。
[TODO]:需要考虑将窗口也增设进来！

# 相关函数和方法
## 文件操作
### rename_file(prev_absolute_path:str, new_absolute_path:str)->bool
重命名文件或者文件夹
prev_absolute_path:之前的绝对路径
new_absolute_path:新的绝对路径
返回值：True为操作成功，False为不成功（比如已有文件或者文件夹与新的名称重名）
### move_to_trash（path:str）->bool
path:要移到回收站的文件夹的绝对路径。
返回值：True为操作成功，False为不成功。
