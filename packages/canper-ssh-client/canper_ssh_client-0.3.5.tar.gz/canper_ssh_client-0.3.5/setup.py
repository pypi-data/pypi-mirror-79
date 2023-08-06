import setuptools

with open('requirements/base.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='canper_ssh_client',
    version='0.3.5',
    description='Perform operations in client',
    author='Diego',
    author_email='diego@test.com',
    license='MIT',
    python_requires='>=3.7.7',
    packages=['ssh_client'],
    include_package_data=True,
    install_requires=required,
)