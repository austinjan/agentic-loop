# Example 08: Flow Monitor Agent — Implementation Plan

> Base commit: `cee9702`

## 目標
建立一個液體流速監控 agent，使用模擬 sensor 資料，以 Bernoulli 方程式即時驗證，異常時呼叫 LLM agent 分析原因。

## 架構

```
[模擬 Sensor] → [即時監控 Loop] → 異常 → [Agent 分析 + 建議]
  P1, v1, P2, v2    Bernoulli 驗證        Gemini LLM
                     每秒一次              含 compaction
```

## 檔案

- `examples/08_flow_monitor.py` — 主程式（單一檔案）
- `examples/08_flow_monitor.md` — 說明文件

## 管路假設參數

| 參數 | 值 | 說明 |
|------|-----|------|
| ρ | 1000 kg/m³ | 水的密度 |
| A1 | 0.01 m² | 上游管截面積 |
| A2 | 0.005 m² | 下游管截面積（縮管） |
| 容差 | ±5% | 超過視為異常 |
| Polling | 1 秒 | 每秒讀取一次 |

## Bernoulli 公式

```
P1 + ½ρv1² = P2 + ½ρv2²
```

驗證方式：計算左右兩邊的差值，若偏差超過 5% 則視為異常。

```python
left = P1 + 0.5 * rho * v1**2
right = P2 + 0.5 * rho * v2**2
error = abs(left - right) / left
if error > 0.05:  # 異常
```

## 模擬 Sensor 設計

### 正常資料產生
1. 設定基準 P1, v1
2. 由連續方程式算 v2：`v2 = (A1 / A2) * v1`
3. 由 Bernoulli 算 P2：`P2 = P1 + ½ρ(v1² - v2²)`
4. 加入小幅隨機雜訊（±1%）模擬 sensor 誤差

### 異常注入（隨機，約每 10 次觸發 1 次）
| 異常類型 | 模擬方式 |
|----------|----------|
| 洩漏 (leak) | P2 驟降 20-30% |
| 堵塞 (blockage) | v2 驟降 30-50% |
| Sensor 故障 | P1 或 v1 跳到離譜值 |

## 程式結構

```python
# --- 常數與設定 ---
RHO, A1, A2, TOLERANCE, POLL_INTERVAL

# --- 模擬 Sensor ---
def simulate_sensor() -> dict:
    """回傳 {P1, v1, P2, v2, anomaly_type}"""

# --- Bernoulli 驗證 ---
def check_bernoulli(P1, v1, P2, v2) -> tuple[bool, float]:
    """回傳 (is_ok, error_percentage)"""

# --- Agent 分析（LLM）---
# Tools:
#   - get_recent_readings: 取得最近 N 筆 sensor 資料
#   - get_pipe_params: 取得管路參數
#
# System prompt: 你是流體力學專家，分析異常原因並建議處置
#
# Compaction: 沿用 07 的機制，長時間監控不爆 context

# --- 主程式 ---
def main():
    contents = []  # agent 對話歷史
    readings = []  # sensor 資料歷史

    while True:
        data = simulate_sensor()
        readings.append(data)

        ok, error = check_bernoulli(data)
        print(f"[Monitor] P1={data['P1']:.0f} v1={data['v1']:.1f} "
              f"P2={data['P2']:.0f} v2={data['v2']:.1f} "
              f"error={error:.1%} {'✓' if ok else '✗'}")

        if not ok:
            # 呼叫 agent 分析
            response = call_agent(data, error, readings, contents, config)
            print(f"[Agent] {response.text}")

            # compaction 檢查
            token_count = count_tokens(contents)
            if token_count > TOKEN_LIMIT:
                contents = compact_conversation(contents)

        time.sleep(POLL_INTERVAL)
```

## 沿用自 Example 07

- `count_tokens()` — token 計算
- `compact_conversation()` — 對話壓縮
- `process_tool_calls()` — 工具呼叫處理
- Gemini client 設定

## 不包含（後續擴充）

- 真實 Modbus 連線（pymodbus）
- 通知系統（email、LINE）
- 資料持久化（DB、CSV log）
- Web dashboard
