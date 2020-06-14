# fioo - Python FileIO and folder Opertation utility package
A Helper package for basic file and folder opetions. For example, determine file format(carriage return),Getting a file size, file extension, file delimeter, compare file, etcs.

## Installation

Install fioo on your system using: [pip](https://pip.pypa.io/en/stable/)

```bash
pip install fioo
```
## Usage

```python
import fioo

# example file path: r'C:\Users\username\Desktop\test.txt'
# example folder path: r'C:\Users\username\Desktop'

fioo.fformat(path)  # return 'Window'    -> based on the file return carriage, get file format, set parm check_all=True to check all lines in file.
fioo.is_empty_file(path)  # return True  -> check if giving file is empty
fioo.size(path)  # return '16B'          -> check the size of a file or folder
fioo.deli(path) # return ','             -> get file delimeter
fioo.ext(path) # return '.txt'           -> get file exention, set parm dot=False to remove dot -> 'txt'
fioo.compare(path1,path2) #		 -> note:path1 and path2 are folder path, will produce all diff files with csv format in the folder2 path location


beta, working in progress:
------using FIOO class-----
f = fioo.FIOO()
f.set_file_path(path) # set path
f.fformat       	          -> same as fioo.fformat(path)
f.is_empty_file 	          -> same as fioo.is_empty_file(path)
f.size          	          -> same as fioo.size(path)
f.deli          	          -> same as fioo.deli(path)
f.ext                             -> same as fioo.ext(path)
f.compare(path1,path2)            -> same as fioo.compare(path1,path2)

```


## License
[MIT](https://choosealicense.com/licenses/mit/)