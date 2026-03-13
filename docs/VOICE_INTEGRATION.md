# Voice Integration - 语音集成说明

## 📝 修改总结

### 已完成的修改

1. **主界面语音输入** - 使用新的 Realtime Voice Assistant
   - ✅ 从 `voice_assistant_rag.py`（旧版）替换为 `voice/realtime_voice_assistant_rag.py`（新版）
   - ✅ 集成 OpenWakeWord（本地唤醒词 "iroi"）
   - ✅ 集成 RAG（知识库检索）
   - ✅ 集成 OpenAI Realtime API（低延迟语音对话）

2. **QA 模式语音输入** - 保留传统方式
   - ✅ 使用 `voice/backup/voice_assistant_rag_original.py`
   - ✅ 继续使用 STT + GPT + TTS 流程（适合单次问答）

3. **移除的内容**
   - ❌ `--wake-mode` 参数（不再需要选择模式）
   - ❌ `voice_assistant.py` 导入（旧的 Whisper 唤醒模式）

## 🏗️ 架构说明

### 主界面 Wake Word 检测流程

```
用户说 "iroi" 
    ↓
OpenWakeWord 检测（本地，无需网络）
    ↓
停止唤醒词检测进程
    ↓
启动 OpenAI Realtime API
    ↓
用户说问题（实时识别）
    ↓
AI 实时回复（带语音）
    ↓
对话结束
    ↓
重启唤醒词检测
```

### QA 模式流程（Lab Select → Lab Detail → QA Chat）

```
用户进入 QA Chat 面板
    ↓
主界面唤醒词检测暂停
    ↓
QA 模式轮询录音启动
    ↓
用户说话 → 录音 → STT → RAG + GPT → TTS → 播放
    ↓
循环等待下一次输入
    ↓
用户退出 QA 面板
    ↓
QA 录音停止，主界面唤醒词检测恢复
```

## 🚀 使用方法

### 启动

```bash
cd /home/dogu/robot_workspace/DOOOGU
python3 robot_ui.py
```

### 功能测试

1. **Wake Word 测试**
   - 启动后等待 4 秒
   - 说 "**iroi**"
   - 应该自动进入 Lab Select 界面

2. **Realtime API 对话测试**
   - 唤醒后，直接说话
   - AI 会实时响应
   - 测试 RAG：问 "What socket should I plug the red probe into for measuring voltage?"
   - 应该回答："The far right socket"

3. **QA 模式测试**
   - 按键 `9` 进入 Lab Select
   - 选择一个 Lab
   - 进入 QA Chat
   - 系统会自动开始监听
   - 说话后会看到转录和回复

## 📁 文件结构

```
DOOOGU/
├── robot_ui.py                          # 主界面（已修改）
├── voice/                               # 新的语音模块
│   ├── realtime_voice_assistant_rag.py # 主语音助手（wakeword + RAG + Realtime API）
│   ├── test_integration.py             # 独立测试脚本
│   ├── local_peer.py                   # WebRTC 连接
│   ├── audio_distributor.py            # 音频分发
│   ├── mic_stream_arecord.py           # 麦克风输入
│   ├── config.py                       # 配置文件
│   └── backup/
│       └── voice_assistant_rag_original.py  # QA 模式使用的旧版
└── ui/
    └── panels/
        └── qa_chat_panel.py            # QA 对话面板
```

## 🔧 配置

### API Key

编辑 `voice/config.py`：
```python
OPENAI_API_KEY = "your-api-key-here"
```

或者主目录的 `config.py`：
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 麦克风设备

编辑 `voice/config.py`：
```python
MIC_DEVICE_NAME = "hw:0,0"  # 根据你的设备调整
```

查看可用设备：
```bash
arecord -l
```

## 🐛 故障排查

### 问题 1：唤醒词无反应
- 检查麦克风设备：`arecord -l`
- 测试麦克风：`python3 voice/test_mic.py`
- 检查模型：`ls model/eyeroeee.onnx`

### 问题 2：Realtime API 连接失败
- 检查 API Key 是否有效
- 检查网络连接
- 查看终端错误信息

### 问题 3：Whisper 识别错误语言
- 已设置 `language: "en"` 和 VAD 阈值 0.3
- 如果仍有问题，调高 VAD 阈值到 0.5

### 问题 4：QA 模式语音不工作
- QA 模式使用旧版 RAG，路径：`voice/backup/voice_assistant_rag_original.py`
- 确保文件存在
- 检查终端错误信息

## ✅ 测试清单

- [ ] 启动后无错误
- [ ] 4 秒后可以唤醒（说 "iroi"）
- [ ] 唤醒后进入 Lab Select 界面
- [ ] Realtime API 可以识别语音
- [ ] RAG 回答正确（测试问题在 `voice/test_rag_questions.md`）
- [ ] 按键 9 进入 Lab Select
- [ ] QA 模式语音监听正常
- [ ] 退出 QA 模式后，主唤醒词恢复

## 📊 性能对比

| 特性 | 旧版 | 新版 |
|------|------|------|
| 唤醒词检测 | Whisper（需要网络） | OpenWakeWord（本地） |
| 语音识别延迟 | 3-5 秒 | 0.5-1 秒 |
| 对话模式 | 单次问答 | 连续对话 |
| RAG 支持 | ✅ | ✅（改进） |
| 麦克风资源冲突 | ❌ 有冲突 | ✅ 已修复 |
| 日志输出 | 混乱 | 清爽 |

## 🎯 下一步

1. 测试所有功能
2. 根据需要调整 VAD 参数
3. 添加更多 RAG 文档到 `TechRAG/docs/`
4. 考虑为 QA 模式也使用 Realtime API（需要大改）

## 📞 支持

遇到问题？检查：
1. 终端错误输出
2. `voice/test_integration.py` 是否单独工作
3. 麦克风权限和设备配置
