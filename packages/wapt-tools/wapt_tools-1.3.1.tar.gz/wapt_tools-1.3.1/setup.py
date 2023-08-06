from setuptools import setup, find_packages

setup(
    name='wapt_tools',
    url='https://github.com/lrobinot/wapt-tools',
    author='Ludovic ROBINOT',
    author_email='lrobinot@gmail.com',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'python_gitlab'],
    version='1.3.1',
    license='Apache 2.0',
    description='WAPT packaging utilities.',
    include_package_data=True,
    package_data={'': ['data/*.*']},
)
