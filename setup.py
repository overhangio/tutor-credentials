import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorcredentials", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-credentials",
    version=ABOUT["__package_version__"],
    url="https://github.com/overhangio/tutor-credentials.git",
    project_urls={
        "Code": "https://github.com/overhangio/tutor-credentials.git",
        "Issue tracker": "https://github.com/overhangio/tutor-credentials.git/issues",
        "Community": "https://discuss.overhang.io",
    },
    license="AGPLv3",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    description="A Tutor plugin for Open edX Credentials service",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=17.0.0,<18.0.0", "tutor-discovery>=17.0.0,<18.0.0", "tutor-mfe>=17.0.0,<18.0.0"],
    entry_points={"tutor.plugin.v1": ["credentials = tutorcredentials.plugin"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
