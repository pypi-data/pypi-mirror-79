from setuptools import setup
from os.path import join, dirname

setup(
	name='color_terminal',
	version='1.0',
	description='Color terminal',
	packages=['colorterminal'],
	author_email='easyhelloworld228@gmail.com',
	long_description_content_type='text/markdown',
	long_description=open(join(dirname(__file__), 'README.rst')).read(),
	zip_safe=False
)
