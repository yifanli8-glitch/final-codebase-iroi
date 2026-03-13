# P0: 门控实施完成 - 测试指南

## ✅ 已完成的修改

### 1. 新增功能（realtime_voice_assistant_rag.py）
- ✅ `record_audio()` - 录音功能
- ✅ `transcribe_audio()` - Whisper API 转录
- ✅ `text_to_speech()` - TTS 语音合成
- ✅ `play_audio()` - 音频播放
- ✅ `chat_with_rag()` - 已有门控功能

### 2. 修改的功能（robot_ui.py）
- ✅ `_start_qa_conversation_loop()` - 新的对话循环（替代 Realtime API）
- ✅ `set_mode()` - 更新 QA Chat 模式调用
- ✅ 添加 `import time`

## 🧪 测试步骤

### 前置条件

确保已安装依赖：
```bash
# 检查是否有 mpg123（播放 MP3）
which mpg123
# 如果没有，安装：
sudo apt install mpg123

# 检查 API key
echo $OPENAI_API_KEY
```

### 测试1：基础流程测试（5分钟）

```bash
cd /home/dogu/robot_workspace/DOOOGU
python3 robot_ui.py
```

**操作步骤：**
1. 按键盘 `9` 进入 Lab Select
2. 点击任意 Lab
3. 点击任意问题 → 进入 QA Chat 模式
4. 等待提示 "🎤 Listening..."
5. 说话（英文）
6. 等待回答

**预期结果：**
```
🎤 [Recording] Starting recording (max 10s)...
✅ [Recording] Saved to /tmp/recording_xxx.wav
📝 [Transcription] Transcribing...
✅ [Transcription] Result: How do I measure DC voltage?
```

### 测试2：门控测试 - 低置信度问题（关键！）

**操作步骤：**
进入 QA Chat 后，问一个**不在文档中**的问题：

**测试问题（应该被拦截）：**
- "How do I use MATLAB?"
- "What is the weather today?"
- "Tell me a joke"
- "How do I program in Python?"

**预期日志（重点看这些标记）：**
```
================================================================================
🚫🚫🚫 [GATE BLOCKED] FAIL-FAST: Confidence too low
================================================================================
   Query: How do I use MATLAB?
   Top-1 Score: 0.296 < Threshold: 0.35
   Decision: BLOCK LLM CALL
   ⚠️  LLM WILL NOT BE CALLED - returning fail-fast message
================================================================================

【关键：没有 🤖🤖🤖 [LLM ENTRY POINT] 标记】

Response: I can't find this in the lab knowledge base. Please rephrase or ask a different question.
```

**✅ 测试通过标准：**
- 听到机器人说："I can't find this in the lab knowledge base..."
- 日志中有 🚫🚫🚫 标记
- 日志中**没有** 🤖🤖🤖 标记

### 测试3：门控测试 - 高置信度问题

**测试问题（应该通过）：**
- "How do I measure DC voltage with a multimeter?"
- "What socket should I plug the red probe into?"
- "How do I calibrate oscilloscope probes?"
- "What is the maximum current the A socket can measure?"

**预期日志：**
```
================================================================================
✅✅✅ [GATE PASSED] High confidence - LLM will be called
================================================================================
   Query: How do I measure DC voltage?
   Top-1 Score: 0.856 >= Threshold: 0.35
   ✅ LLM WILL BE CALLED with retrieved context
================================================================================

================================================================================
🤖🤖🤖 [LLM ENTRY POINT] Calling OpenAI API
================================================================================
   ⚠️  LLM API CALL HAPPENING NOW
================================================================================

Response: To measure DC voltage with a multimeter, first plug...
```

**✅ 测试通过标准：**
- 听到正确的回答
- 日志中有 ✅✅✅ 标记
- 日志中有 🤖🤖🤖 标记

### 测试4：连续对话测试

**操作步骤：**
1. 问第一个问题（高置信度）
2. 等待回答完成
3. 立即问第二个问题（低置信度）
4. 验证门控是否生效

**预期结果：**
- 第一个问题：正常回答
- 第二个问题：被门控拦截

## 🐛 故障排查

### 问题1：录音失败

**症状：**
```
❌ [Recording] Error: ...
```

**解决：**
```bash
# 检查麦克风设备
arecord -l

# 测试录音
arecord -D hw:0,0 -f S16_LE -r 16000 -c 1 -d 5 test.wav
aplay test.wav
```

### 问题2：转录失败

**症状：**
```
❌ [Transcription] Error: ...
```

**解决：**
```bash
# 检查 API key
echo $OPENAI_API_KEY

# 检查网络
curl https://api.openai.com
```

### 问题3：播放失败

**症状：**
```
❌ [Playback] Error: ...
```

**解决：**
```bash
# 安装 mpg123
sudo apt install mpg123

# 测试播放
mpg123 --help
```

### 问题4：门控没有生效

**症状：**
低置信度问题仍然得到回答

**检查：**
1. 查看日志是否有 🚫🚫🚫 标记
2. 检查是否有 🤖🤖🤖 标记（不应该有）
3. 运行单独的门控测试：
```bash
python3 voice/prove_gating_works.py
```

## 📊 成功标准

### ✅ P0 完成标准

- [ ] 可以录音和转录
- [ ] 低置信度问题被拦截（听到 fail-fast 消息）
- [ ] 高置信度问题正常回答
- [ ] 日志清晰显示门控决策
- [ ] 语音输出正常

### ✅ 日志标记检查清单

**对于低置信度问题，必须看到：**
- [ ] 🚫🚫🚫 [GATE BLOCKED]
- [ ] Top-1 Score < 0.35
- [ ] Decision: BLOCK LLM CALL
- [ ] **没有** 🤖🤖🤖 [LLM ENTRY POINT]
- [ ] Response 是 fail-fast 消息

**对于高置信度问题，必须看到：**
- [ ] ✅✅✅ [GATE PASSED]
- [ ] Top-1 Score >= 0.35
- [ ] Decision: ALLOW LLM CALL
- [ ] 🤖🤖🤖 [LLM ENTRY POINT]
- [ ] Response 是实际答案

## 🎯 下一步

P0 完成后：
1. ✅ 验证幻觉问题已解决
2. ⏭️ 进入 P1：添加对话历史（支持追问）
3. ⏭️ 进入 P2：添加图片支持

## 📞 如果遇到问题

1. 检查日志中的错误信息
2. 运行独立测试：`python3 voice/prove_gating_works.py`
3. 检查 API key 和网络连接
4. 查看 `/tmp/` 目录是否有录音/音频文件

---

**P0 实施完成时间：** 2026-02-04
**预计测试时间：** 15-30分钟
**核心目标：** 解决幻觉问题，低置信度问题返回 "不知道"
