# MICSV
**MIC**S **S**UR**V**EY: automate MICS dataset download

TODO

- [x] Login and download 
- [ ] Refine popup deflection

# Install

```bash
pip3 install micsv
```

Required libs

```bash
pip3 install bs4
pip3 install selenium
# and install whatever libs missing on your machine...
```

# Run

In terminal 
```bash
python3
```
In python
```python
from micsv import run_mics
run_mics(versions = [], overwrite = False, save_to = ".", sleep = 5)
```

- `versions`: a list of MICS versions to download, empty means download
  all from MICS2 to MICS6
- `overwrite`: overwrite exising file in `save_to` directory
- `save_to`: where to save the file, default to current working directory.
  Perhaps better to do 
  ```python
  import os
  os.chdir('path/to/where/to/save')
  run_mics()
  ```
- `sleep`: required, sometime MICS website load too slow and needed time to
  solve reCaptcha.

- This program will open a new browser window (Firefox in this case).
- Use your username, password, pass the reCaptcha and click login (then make no
  more movement in the browser please). 
- The code will wait until MICS logged in successfully (5 minutes timeout) and
  automatically redirect to surveys site.

# Example outputs

```python
Processing page 1
Processing page 2
Processing page 3
Processing page 4
Processing page 5
Processing page 6
There are 222 file(s) detected.
The-Gambia-MICS6-Datasets.zip is already existed.
Skip downloading The-Gambia-MICS6-Datasets.zip
```
