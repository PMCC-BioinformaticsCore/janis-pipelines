from setuptools import setup, find_packages

######## SHOULDN'T NEED EDITS BELOW THIS LINE ########

vsn = {}
with open("./janis_pipelines/__meta__.py") as fp:
    exec(fp.read(), vsn)
version = vsn["__version__"]
description = vsn["description"]

with open("./README.md") as readme:
    long_description = readme.read()

setup(
    name="janis-pipelines.pipelines",
    version=version,
    description=description,
    url="https://github.com/PMCC-BioinformaticsCore/janis-pipelines",
    author="Michael Franklin",
    author_email="michael.franklin@petermac.org",
    license="GNU",
    packages=["janis_pipelines"]
    + ["janis_pipelines." + p for p in sorted(find_packages("./janis_pipelines"))],
    entry_points={
        "janis.extension": ["pipelines=janis_pipelines"],
        "janis.tools": ["pipelines=janis_pipelines"],
        "janis.pipelines": ["bioinformatics=janis_pipelines"],
    },
    install_requires=["janis-pipelines>=0.6.0"],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
