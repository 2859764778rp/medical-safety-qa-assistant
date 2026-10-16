# 医疗用药安全问答助手

基于 **Qwen2.5-7B-Instruct** 的医疗领域 LoRA 微调 + vLLM 私有化部署项目：将通用大模型微调为专注日常用药咨询的助手（不做诊断，回答用法用量与药物相互作用等），并完成「数据清洗 → 微调 → 模型合并 → 部署 → 公网对话」完整闭环，验证 LoRA + vLLM 低成本私有化落地路径。

> 说明：本项目仅作为技术实践展示；模型不做诊断，涉及具体用药请咨询医生或药师。

## 实现链路

```
Huatuo-26M 医疗问答数据
  → 清洗 + alpaca 三字段格式转换
  → 8:1:1 划分（训练 8000 / 验证 1000 / 测试 1000）
  → LLAMA-Factory LoRA 微调（rank=8、3 epochs、bf16，可训练参数约 2018 万 / 0.265%）
  → 模型合并
  → vLLM 部署（fp16、max_model_len=1024、gpu_memory_utilization=0.3）OpenAI 兼容推理服务
  → Flask 多线程封装 → 公网展示平台
```

## 评估结果

- **训练收敛性**：验证集（1000 条）`eval_loss` 收敛至 1.6915
- **推理性能**：实测单请求生成速率 13–30 tokens/s，前缀缓存命中率最高 68%
- **对比测试**：同环境同参数下 25 条用药安全问答对比显示，微调后回答的结构性与风险提示完整度提升（禁忌症、药物相互作用等场景主动警示更完整）；事实正确性由知识库/检索兜底

## 目录结构

```
├── 01-code-logs/
│   └── server.py          # 部署服务入口（Flask 封装 vLLM 推理）
├── A4实战全流程.pdf        # 实战流程文档
├── 基于 Qwen2.5-7B 的医疗领域 LoRA 微调.pdf
├── models/                # 微调后模型权重（不入库）
└── output/                # LoRA 训练产物（不入库）
```

## 运行方式

```bash
# 1. 安装依赖（vLLM、transformers、LLaMA-Factory）
pip install vllm transformers

# 2. 启动推理服务（OpenAI 兼容）
python 01-code-logs/server.py
# 默认端口与模型路径见 server.py 配置
```

微调与评估详细步骤见仓库内两份 PDF 文档。
