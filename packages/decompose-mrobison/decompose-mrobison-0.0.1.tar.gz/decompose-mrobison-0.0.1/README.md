# Decompose
This module provides a method for decomposing strings containing latin diacretics, ligatures, 
and other unusual latin letters into their appropriate ascii counterparts generally for the purpose
of data for submission into systems requiring the usage of the ascii subset.

## Example
```python
from decompose import decompose

decompose('Málaga') # returns 'Malaga'
```

## Comments
decompose.decompose() depends upon unicodedata.normalize() for most of its heavy lifting. 
However, it also contains a lookup table (decompose.charmap) for those unicode characters that are
not necessarily handled by normalize(). Any letter not handled by either normalize or charmap will
be silently dropped.