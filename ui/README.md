# UI 模块说明

这个目录包含从 `robot_ui.py` 重构出来的所有 UI 组件。

## 📁 目录结构

```
ui/
├── widgets/          # 可复用的小组件
│   ├── status_item.py      # 状态显示项（图标+标签+值）
│   ├── lab_button.py       # 实验室按钮（圆角蓝色）
│   └── back_button.py      # 返回按钮（◀ 圆形）
│
└── panels/           # 各个显示面板
    ├── status_panel.py     # 系统状态面板（时间、电池等）
    ├── camera_panel.py     # 摄像头面板（含流线程）
    ├── lab_select_panel.py # 实验室选择界面
    ├── lab_detail_panel.py # 实验室详情界面
    └── qa_chat_panel.py    # 问答对话面板
```

## 📦 使用方式

### 导入 Widgets
```python
from ui.widgets import StatusItem, LabButton, BackButton

# 创建状态项
battery_item = StatusItem("🔋", "BATTERY", "85%")

# 创建按钮
lab_btn = LabButton("LAB 1")
back_btn = BackButton()
```

### 导入 Panels
```python
from ui.panels import (
    StatusPanel,      # 系统状态
    CameraPanel,      # 摄像头
    LabSelectPanel,   # 实验室选择
    LabDetailPanel,   # 实验室详情
    QAChatPanel       # 问答对话
)

# 创建面板
status = StatusPanel()
camera = CameraPanel(stream_url="http://...")
```

### 导入线程类
```python
from ui.panels import MJPEGStreamThread, LocalCameraThread

# 创建流线程
stream_thread = MJPEGStreamThread("http://192.168.1.100:8080/video_feed")
```

## 🎯 设计原则

1. **单一职责**：每个文件只负责一个组件
2. **清晰依赖**：widgets 不依赖 panels，panels 可以依赖 widgets
3. **易于测试**：每个组件可以单独测试
4. **可复用性**：组件可以在其他项目使用

## 📝 与 robot_ui.py 的关系

`robot_ui.py` 导入这些组件并组装成完整界面：

```python
# robot_ui.py
from ui.widgets import StatusItem, LabButton, BackButton
from ui.panels import StatusPanel, CameraPanel, ...

class RobotContent(QWidget):
    def init_ui(self):
        # 使用这些组件创建界面
        self.status_panel = StatusPanel(self)
        self.camera_panel = CameraPanel(self)
        ...
```

## 🧪 测试

运行测试验证所有组件：
```bash
python3 test_full_refactor.py
```

---

*最后更新: 2026-01-26*
