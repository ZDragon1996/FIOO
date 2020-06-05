# fioo - Python FileIO and folder Opertation utility package
A Helper package for basic file and folder opetions. For example, determine file format for differnt operting systems based on the file carriage return or line feed. Getting a file size, file extension, etcs.

## Installation

Install fioo on your system using: [pip](https://pip.pypa.io/en/stable/)

```bash
pip install fioo
```
## Usage

```python
import fioo

fioo.file_format(path)  # returns 'Window'
fioo.is_empty_file(path)  # returns True
fioo.file_size(path)  # returns '16B'
fioo.compare(path1,path2) # will produce diff files
```


## License
[MIT](https://choosealicense.com/licenses/mit/)