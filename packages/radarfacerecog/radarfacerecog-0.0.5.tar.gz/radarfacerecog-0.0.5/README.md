Radar Face Recognition
======

About
-----

Radar Face Recognition is Python library that recognize Brazilian politicians face's based on our dataset.


Requirements
------------

-   Python3.5+

Usage
-----

via Python Module

``` {.sourceCode .python}
from radarfacerecog import Radarfacerecog

predictor = Radarfacerecog()
result = predictor.predict(<Array Image>)

Result can be True or False

```