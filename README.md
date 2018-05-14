# py2tex
Interface for easily saving python variables in a tex file.

# Installation

Install using pip:
`pip install py2tex`

# Usage

Example usage in Python
```python
import numpy as np
import py2tex

seed = np.random.randint(9999)

tex_file = py2tex.TeXVariableFile( './variables.tex' )
tex_file.save_variable(
    'seedvalue',
    str( seed ),
)
```
Note that the variable should be saved as the string you want displayed in latex.
This means formatting float variables accordingly, for example `'{:.02f}'.format( 0.12356 )` will save as `'.12'`.

Example usage in LaTex:
```
\include{variables}

Our analysis uses random values.
Our randomly chosen seed is \seedvalue.
```

[![Build Status](https://travis-ci.com/zhafen/py2tex.svg?branch=master)](https://travis-ci.com/zhafen/py2tex)
