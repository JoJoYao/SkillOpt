# skillopt/model/cli_backend.py
import os
import subprocess
import sys

def _run_local_cli(command_name: str, system: str, user: str) -> str:
    """在後台執行本地的 CLI 工具（如 claude 或 agy）並抓取文字輸出"""
    # 將 System Prompt 與 User Prompt 合併成單一文字送給 CLI
    full_prompt = f"System Instruction:\n{system}\n\nUser Request:\n{user}"
    
    try:
        # 使用 subprocess 呼叫本地 CLI
        # 這裡以 standard input 或是直接帶入參數的方式，可依特定 CLI 調整
        # 預設以 `command_name "prompt text"` 的形式執行
        cmd = [command_name, full_prompt]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"本地 CLI [{command_name}] 執行失敗: {e.stderr}", file=sys.stderr)
        return f"Error from local CLI: {e.stderr}"

def chat_optimizer(system: str, user: str, **kwargs) -> tuple[str, dict]:
    # 透過環境變數 CLI_OPTIMIZER 指定要用的指令（例如 claude 或 agy），預設為 claude
    cli_cmd = os.getenv("CLI_OPTIMIZER", "claude")
    output = _run_local_cli(cli_cmd, system, user)
    # 模擬 Token 計數回傳（本地 CLI 無法直接取得 token，故設為 0）
    return output, {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

def chat_target(system: str, user: str, **kwargs) -> tuple[str, dict]:
    cli_cmd = os.getenv("CLI_TARGET", "claude")
    output = _run_local_cli(cli_cmd, system, user)
    return output, {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
