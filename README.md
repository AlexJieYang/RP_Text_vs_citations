# Text vs. citations

Research code for **Text vs. citations: a comparative analysis of breakthrough
and disruption metrics in patent innovation**, by Alex J. Yang. The notebooks
compare text-based KI and citation-based CD metrics in USPTO patent data.

## Workflow

The notebooks in `Codes for paper/` can be run independently with the study-data
directory configured in `config.json`.

| Notebook | Analysis |
| --- | --- |
| `Relation between CD and KI.ipynb` | KI–CD relationships |
| `Relation with cit and eco value.ipynb` | Citation and economic-value relationships |
| `Relation with novelty and ref.ipynb` | Novelty and reference relationships |
| `Team.ipynb` | Team size and geographic distance |
| `Trend.ipynb` | Temporal and field trends |

Each notebook writes its figures to a separate subdirectory of `output_dir`.
ZIP tables are read directly by pandas. Lookup tables use `patent_id`, with
`patent_num` in the KPSS economic-value table; CPC tables support multiple
section assignments per patent.

## Measures

`KI5 = log(fsim5 / bsim5)` uses positive forward and backward similarities.
`CD5 = (D5 - C5) / (D5 + C5 + R5)` uses a positive denominator. Undefined
observations retain their NaN representation. The notebook cohorts
use filing years 1980–2017.

The shared bootstrap function returns separate lower and upper 95% percentile
bounds for each group mean. Its defaults are 2,000 resamples and seed 1, with
one resample per processing batch. Geographic-distance and team-size analyses
retain NaN values. `project.py` contains the path and bootstrap
utilities.

## Installation and configuration

Use Python 3.10 or 3.11. Create and activate a virtual environment with the command
for your operating system, then install the packages:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Copy `config.example.json` to `config.json`. Set `data_dir` to the study-data
directory and `output_dir` to the figure destination. Relative paths resolve
from the repository root; absolute paths are accepted. `RESEARCH_CONFIG` selects
another configuration file.

Start `jupyter lab` inside the repository and open the desired notebook. Each
Python notebook includes its own initialization and data loading. The output
directories are created automatically.

## Source validation

```bash
python scripts/check_sources.py
```

This command validates Python syntax, notebook JSON, configuration JSON, and
empty notebook execution state. The GitHub Actions workflow performs the same
static checks.

## Citation and license

See `CITATION.cff` for repository metadata and cite the associated research.
The MIT license covers code and documentation. Data, publications, and
third-party materials retain their respective source rights.

## Research abstract

This study examines two dynamic metrics for assessing technological innovation— the text-based breakthrough index (KI index) and the citation-based disruption index (CD index)—both of which integrate ex-ante (novelty) and ex-post (impact) information. The KI index identifies breakthrough inventions by measuring their novelty (low similarity to prior patents) and impact (high similarity to future patents), whereas the CD index quantifies technological disruption by analyzing shifts in citation patterns. Using a dataset of over six million patents filed with the USPTO between 1980 and 2017, this paper finds that KI and CD indices are highly correlated and both effectively capture technological breakthroughs. Patents with high KI or CD scores typically originate from original and narrowly focused knowledge bases. However, the two indices exhibit distinct patterns: (1) the KI index fluctuates with economic cycles, while the CD index has experienced a steady decline over time; (2) the KI index positively correlates with future patent citation impact, whereas the CD index follows a U-shaped relationship with patent citation impact; and (3) small and remote teams produce higher KI but lower CD scores, potentially because larger teams cite newer, widely recognized references. I discuss innovation concepts—breakthroughs, disruptions, and beyond—to contextualize these findings and explore their implications for understanding technological advancement. These results contribute to the discourse on measuring innovation and underscore the complementary strengths of text-based and citation-based approaches in assessing technological progress.
