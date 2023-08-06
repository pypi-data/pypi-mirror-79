from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'A D&D Charecter Random Generator'

setup(
		name ='dndchar',
		version ='1.0.0',
		author ='Coder Kearns',
		author_email ='coder.kearns@gmail.com',
		url ='https://github.com/coderkearns',
		description ='A D&D random Charecter Generator',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'dndchar=dndchar.command_line:main'
			]
		},
		classifiers =[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		],
		keywords ='dnd d&d random generators',
		install_requires = requirements,
		zip_safe = False
)
