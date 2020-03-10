import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='customio',  
     version='0.1',
     scripts=['customio.py'] ,
     author="Jialong Zhang",
     author_email="BubbleEcho@protonmail.com",
     description="file and folder utility packages",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/ZDragon1996/CustomFileIO",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )