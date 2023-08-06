# %%
import subprocess

import pandas as pd

 # %%


res = subprocess.run(
    ["vulture", "--help"], 
    capture_output=True, 
    shell=False,
    text=True
)

# %%
bla = {"a": 1, "b": 2}
blu = {"1": 11, "2": 22}

# %%

bla = "test_code/diff/prediction/test_code/bla.py"

# %%

if bla.startswith("test_code"):
    bli = bla[len("test_code"):]

bli

# %%

text = "test_code/diff/prediction/__init__.py\ntest_code/diff/embedding/__init__.py\nanother_code/hey.py"

prefix = ""

blu = "\n".join(map(lambda s: s[len(prefix):] if s.startswith(prefix) else s, text.splitlines()))
print(blu)


# %%
