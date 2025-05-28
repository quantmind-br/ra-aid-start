from setuptools import setup, find_packages

setup(
    name='ra-aid-start',
    version='0.1.0',
    author='[Seu Nome ou Organização Aqui]',
    author_email='[Seu Email Aqui]',
    description='CLI tool to manage and execute Ra.Aid presets.',
    long_description='', # README.md will be created in a later task
    long_description_content_type='text/markdown',
    url='[URL do Repositório do Projeto Aqui]',
    packages=find_packages(),
    install_requires=[
        'rich>=13.7.1',
        'click>=8.1.7',
        'pydantic>=2.7.1',
        'jsonschema>=4.22.0',
        'pathlib>=1.0.1',
        'typing-extensions>=4.11.0',
    ],
    extras_require={
        'test': [
            'pytest>=8.0.0',
            'pytest-mock>=3.12.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'ra-aid-start=ra_aid_start.main:cli',  # Conforme PLAN.MD
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # Exemplo, ajuste conforme sua licença
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)