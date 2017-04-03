from setuptools import setup

setup(name='pysocialwatcher',
      version='0.1c',
      description='pySocialWatcher : Social Watcher through Facebook Marketing API',
      url='https://github.com/maraujo/pySocialWatcher',
      long_description="""
            This package tries to get the full potencial of the Facebook Marketing API for Social Analysis research.
            Recent works show that online social media has a huge potencial to provide interesting insights on trends of across demographic groups.
      """,
      author='Matheus Araujo - QCRI-HBKU',
      author_email='maraujo@hbku.edu.qa',
      license='MIT',
      packages=['pysocialwatcher'],
      classifiers=[
            "Topic :: Sociology",
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      zip_safe=False)