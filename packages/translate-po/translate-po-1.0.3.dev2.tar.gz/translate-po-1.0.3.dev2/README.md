# translate-po

Simple quick script for automatically translating .po files using Google. In attempt to give translators a quick baseline to correct and work off from. Which speeds up and simplifies the internationalization process.

## Usage

```python
from translate_po.main import run

run(fro="en" to="et" src="./untranslated" dest="./translated")
```
