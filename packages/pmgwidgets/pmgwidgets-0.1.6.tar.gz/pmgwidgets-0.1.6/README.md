# pmgwidgets常用控件介绍
``` python
from pmgwidgets import {控件名}
```
用以上语句即可导入相应的控件。
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
 ### 
 