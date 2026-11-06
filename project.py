"""Repository-relative input configuration and figure destinations."""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parent

def settings():
    path = Path(os.environ.get("RESEARCH_CONFIG", ROOT / "config.json"))
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        if "RESEARCH_CONFIG" in os.environ:
            raise FileNotFoundError(f"Configuration file does not exist: {path}")
        path = ROOT / "config.example.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

_FILES = {'TextInnovation.csv.zip': ['data', 'TextInnovation.csv.zip'], 'Disruption.csv.zip': ['data', 'Disruption.csv.zip'], 'cpc.csv.zip': ['data', 'cpc.csv.zip'], 'CitationWindows.csv.zip': ['data', 'CitationWindows.csv.zip'], 'KPSS_2022.csv.zip': ['data', 'KPSS_2022.csv.zip'], 'Firstpair.csv.zip': ['data', 'Firstpair.csv.zip'], 'FirstGroup.csv.zip': ['data', 'FirstGroup.csv.zip'], 'patent_hhi.csv.zip': ['data', 'patent_hhi.csv.zip'], 'patents_RefAge.csv.zip': ['data', 'patents_RefAge.csv.zip'], 'patents_RefPop.csv.zip': ['data', 'patents_RefPop.csv.zip'], 'patent.csv.zip': ['data', 'patent.csv.zip'], 'TeamSize.csv.zip': ['data', 'TeamSize.csv.zip'], 'patentAffDistance2.csv.zip': ['data', 'patentAffDistance2.csv.zip']}

def input_path(key):
    config = settings()
    kind, filename = _FILES[key]
    setting = "regression_dir" if kind == "regression" else "data_dir"
    directory = Path(config.get(setting, "data")).expanduser()
    if not directory.is_absolute():
        directory = ROOT / directory
    path = directory / filename
    if not path.is_file():
        raise FileNotFoundError(f"Input {key!r} is unavailable at {path}. Set {setting} in config.json to the study-data directory.")
    return path

def output_path(name):
    path = Path(settings().get("output_dir", "outputs")).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    destination = path / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination

def bootstrap_interval(data, n_resamples=2000):
    """Return both percentile-bootstrap bounds for the mean of finite values."""
    import numpy as np
    from scipy.stats import bootstrap
    values = np.asarray(data, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return (np.nan, np.nan)
    if values.size == 1:
        return (values[0], values[0])
    result = bootstrap((values,), np.mean, confidence_level=0.95,
                       n_resamples=n_resamples, batch=1,
                       random_state=1, method="percentile")
    return (result.confidence_interval.low, result.confidence_interval.high)

def ci_bound(intervals, side):
    """Extract the lower (0) or upper (1) bound from grouped intervals."""
    return intervals.map(lambda value: value[side]).to_numpy()
