# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Pet_shop',
    version='1.0',
    packages=['Pet_shop'],
    package_data={'Pet_shop': ['*.py', '*.json', '*.pkl', '*.pptx', '*.txt']},
    entry_points={
        'console_scripts': [
            'pet_shop = Pet_shop.Pet_shop_customers:main',
        ],
    },
    install_requires=[
        'requests',
        'numpy',
        # Добавьте здесь другие зависимости, если они необходимы
    ],
    author='5 Element',
    author_email='webmastak2016@gmail.com.com',
    description='A package for Pet_shop',
)
