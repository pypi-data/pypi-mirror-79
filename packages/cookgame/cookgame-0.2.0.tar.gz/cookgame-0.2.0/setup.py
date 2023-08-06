import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="cookgame",
                 version="0.2.0",
                 author="piglite",
                 author_email="piglite@vip.sina.com",
                 description="kcode tutoring package",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/piglite",
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 python_requires='>3',
                 packages=setuptools.find_namespace_packages(
                     include=["cookgame", "cookgame.*"], ),
                 install_requires=['arcade'],
                 include_package_data=True)
