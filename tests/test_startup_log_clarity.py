# -*- coding: utf-8 -*-
"""Startup and LLM log lines must describe what this run actually does."""
from types import SimpleNamespace

import main
from src.analyzer import _describe_llm_result_model
from src.config import ConfigIssue


def _config():
    issues = [
        ConfigIssue(severity="error", message="no stocks", field="STOCK_LIST"),
        ConfigIssue(severity="warning", message="no notify", field="WECHAT_WEBHOOK_URL"),
        ConfigIssue(severity="error", message="no llm", field="LITELLM_MODEL"),
    ]
    return SimpleNamespace(validate_structured=lambda: issues)


def test_all_warnings_kept_without_overriding_args():
    args = SimpleNamespace(stocks=None, portfolio=None, no_notify=False)
    assert main._startup_config_warnings(_config(), args) == ["no stocks", "no notify", "no llm"]


def test_cli_stocks_and_no_notify_resolve_their_warnings_only():
    args = SimpleNamespace(stocks="600519", portfolio=None, no_notify=True)
    assert main._startup_config_warnings(_config(), args) == ["no llm"]


def test_portfolio_resolves_missing_stock_list():
    args = SimpleNamespace(stocks=None, portfolio="futu", no_notify=False)
    assert main._startup_config_warnings(_config(), args) == ["no notify", "no llm"]


def test_llm_log_names_fallback_model():
    assert _describe_llm_result_model("deepseek/deepseek-chat", "gemini/x") == (
        "gemini/x（配置模型 deepseek/deepseek-chat，已回退）"
    )


def test_llm_log_unchanged_when_configured_model_answers():
    assert _describe_llm_result_model("gemini/x", "gemini/x") == "gemini/x"
    assert _describe_llm_result_model("gemini/x", None) == "gemini/x"
