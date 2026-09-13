# Environment record

The arithmetic QA ran on Python 3.12.14 / Windows, with NumPy 2.3.5, pandas 2.2.3 and SciPy 1.17.0. These library versions match the recovered arithmetic environment. [requirements-analysis.txt](../requirements-analysis.txt) pins the executed stack including its transitive versions.

The original training record specifies Python 3.13.5 / Linux, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0 and LightGBM 4.6.0. The original later QA record adds SciPy 1.17.0, matplotlib 3.10.8 and python-docx 1.2.0. No training, matplotlib rendering or document generation was rerun here.

**Full historical environment closure remains HOLD.** No exact statsmodels version or import was found in recovered scientific code; the original document requirements give only `lxml>=5`. Neither package was used for checkpoint arithmetic. Original transitive versions were not recorded. No missing version has been guessed. See [machine-readable environment and source hashes](../verification/environment.json).

The shell launcher set `PYTHONPATH=.local/analysis_dependencies` for the isolated pinned libraries and invoked `scripts/verify_science.py --evidence-root .local/evidence --output verification/scientific_checks.json`. The portable equivalent is installation into a fresh virtual environment. Absolute host paths are deliberately excluded.
