#!/usr/bin/env python3
"""
模型选择器
从 sys-root/config/models.json 读取模型配置，支持按场景路由到不同模型

使用方式：
    from model_selector import ModelSelector
    selector = ModelSelector()
    config = selector.get_model_config("prd_review")
"""

import json
import os
from pathlib import Path
from typing import Optional


class ModelSelector:
    def __init__(self, models_config_path: Optional[str] = None, gate_config_path: Optional[str] = None):
        if models_config_path is None:
            models_config_path = "/Users/billhu/agentsystem/sys-root/config/models.json"
        if gate_config_path is None:
            gate_config_path = Path(__file__).parent / "config.yaml"

        self.models_config = self._load_json(models_config_path)
        self.gate_config = self._load_yaml(gate_config_path)

    def _load_json(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 配置文件 {path} 未找到")
            return {}

    def _load_yaml(self, path) -> dict:
        try:
            import yaml
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def get_model_config(self, model_id: str) -> Optional[dict]:
        models = self.models_config.get("models", {})
        return models.get(model_id)

    def get_routing(self, task_type: str) -> str:
        routing = self.gate_config.get("models", {}).get("routing", {})
        return routing.get(task_type, routing.get("default"))

    def resolve_model_for_task(self, task_type: str) -> dict:
        model_id = self.get_routing(task_type)
        model_config = self.get_model_config(model_id)

        if not model_config:
            return {
                "error": f"模型 {model_id} 未找到",
                "model_id": model_id
            }

        api_key_env = model_config.get("api_key_env")
        api_key = os.environ.get(api_key_env) if api_key_env else None

        return {
            "model_id": model_id,
            "model_name_in_api": model_config.get("model_id"),
            "provider": model_config.get("provider"),
            "base_url": model_config.get("base_url"),
            "api_key": api_key,
            "api_key_configured": api_key is not None
        }

    def list_available_models(self) -> list:
        models = self.models_config.get("models", {})
        return list(models.keys())

    def list_tasks(self) -> list:
        routing = self.gate_config.get("models", {}).get("routing", {})
        return [k for k in routing.keys() if k != "default"]


if __name__ == "__main__":
    selector = ModelSelector()

    print("可用模型:", selector.list_available_models())
    print("可用任务:", selector.list_tasks())

    for task in selector.list_tasks():
        config = selector.resolve_model_for_task(task)
        print(f"\n{task}:")
        print(f"  模型ID: {config['model_id']}")
        print(f"  API模型名: {config.get('model_name_in_api')}")
        print(f"  Provider: {config.get('provider')}")
        print(f"  Base URL: {config.get('base_url')}")
        print(f"  API Key: {'已配置' if config.get('api_key_configured') else '未配置'}")
