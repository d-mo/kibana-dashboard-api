from setuptools import setup

setup(name='kibana_dashboard_api',
      version='0.0.3',
      description='Manages Kiabana visualizations and dashboards.',
      long_description='List/create/delete Kibana visualizations and dashboards manipulating Elasticsearch index.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
      ],
      keywords='kibana elasticsearch',
      url='https://github.com/harabchuk/kibana-dashboard-api',
      author='Aliaksei Harabchuk',
      author_email='aliaksei.harabchuk@gmail.com',
      license='MIT',
      packages=['kibana_dashboard_api'],
      install_requires=[
          'elasticsearch',
      ],
      include_package_data=True,
      zip_safe=False)