from setuptools import setup

setup(
    name='clitellum',
    version='5.2.2',
    packages=['clitellum', 'clitellum.channels'],
    package_dir={'clitellum': 'clitellum'},
    url='https://clitellum.hotaka.io',
    license='GPL',
    author='Sergio.Bermudez',
    author_email='sergio@hotaka.io',
    description='Clitellum Microservice Framework',
    extras_require={},
    install_requires=['pika'])
