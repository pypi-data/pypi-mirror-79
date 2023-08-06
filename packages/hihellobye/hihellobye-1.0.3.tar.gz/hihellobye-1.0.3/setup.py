from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


if __name__ == '__main__':
    setup(
        name="hihellobye",

        version='1.0.3',

        description='Pakistani chat rooms for FREE',
        long_description_content_type='text/markdown',
        long_description=long_description,


        author='hihellobye',
        author_email='chat_room@hihellobye.com',

        license='BSD2',
        url = 'https://github.com/onlinechatrooms/hihellobye.com',

        classifiers=[

            'Development Status :: 5 - Production/Stable',


            'License :: OSI Approved :: BSD License',

            'Natural Language :: English',

            'Programming Language :: Python :: 3'
        ],

        keywords='chat room, online chat, chat rooms',



        entry_points={
            'console_scripts': [
                'main=main:main'
            ]
        },

    )

