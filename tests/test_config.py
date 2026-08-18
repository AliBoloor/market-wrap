from pathlib import Path

from market_wrap.config import load_config


def test_load_example_config() -> None:
    config = load_config(Path("config.example.yaml"))
    assert config.assets
    assert config.report.output_dir.is_absolute()
    assert config.schedule.weekdays == "mon-fri"

