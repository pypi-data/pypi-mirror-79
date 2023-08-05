"""
Documentation
-------------
nothing

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="GxCsvToJson",
        description="Convert Csv to Json",
        keywords="json csv",
        long_description=long_description,
        version="1.0.1",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=find_packages(),
        package_data={},
        entry_points={
            'console_scripts':[
                'csvtojson=GxCsvToJson.main:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
