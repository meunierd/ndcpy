from setuptools import setup

setup(
    name='ndcpy',
    version='0.3.0',
    description='A Python wrapper for NDC',
    url='https://github.com/meunierd/ndcpy',
    author='Devon Meunier',
    author_email='devon.meunier@gmail.com',
    license='MIT',
    packages=["ndc"],
    install_requires=[
        'python-dateutil',
    ],
    extras_require={
        'dev': [
            'pytest',
        ]
    },
)
