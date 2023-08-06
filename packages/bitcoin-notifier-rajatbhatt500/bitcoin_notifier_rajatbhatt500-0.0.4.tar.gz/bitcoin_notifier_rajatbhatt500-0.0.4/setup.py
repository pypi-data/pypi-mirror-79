from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()


setup(
    name="bitcoin_notifier_rajatbhatt500",
    version="0.0.4",
    description="A Python package to get Bitcoin price on various platform.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Rajat Bhatt",
    author_email="rajatbhatt500@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=['bitcoin_notifier_rajatbhatt500'],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "bitcoin-notification = bitcoin_notifier_rajatbhatt500.bitcoin_price:main",
        ]
    },
)
