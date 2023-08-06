import setuptools

setuptools.setup(
    name="sqlalchemy_uuidstr",
    version="0.0.2",
    description="Library to autoconvert string <> uuid to/from DB",
    url="https://github.com/shuttl-tech/sqlalchemy_uuidstr",
    author="Sherub Thakur",
    author_email="sherub.thakur@shuttl.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["SQLAlchemy"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "psycopg2-binary"]
    },
)
