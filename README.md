# CustomIO - Python FileIO and folder utility package
A Helper package for basic file and folder opetions. For example, determine file format for differnt operting systems based on the file carriage return or line feed. Getting a file size, file extension, etcs.

## Installation

Install customio on your system using: [pip](https://pip.pypa.io/en/stable/)

```bash
pip install customio
```
## Usage

```python
import customio

customio.file_format(path)  # returns 'Window(LF|CR)'
customio.is_empty_file(path)  # returns True
customio.file_size(path)  # returns '16B'
```


## License
[MIT](https://choosealicense.com/licenses/mit/)