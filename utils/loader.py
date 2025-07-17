## utils/loader.py
```python
import markdown


def load_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return markdown.markdown(text)
