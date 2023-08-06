Statisfaction
========================================

A library to unify statistical testing at BlaBlaCar.

# Objectives

* Gather the statistical knowledge and capabilities otherwise scattered in multiple libraries: `scipy`, `numpy`, `statsmodels`, `pandas`
* Provide simple interfaces and sensible default values for the statistical tools most commonly used at BlaBlaCar

# Install

You can install the public package with the following command:
```bash
pip3 install https://storage.googleapis.com/bbc-datascience-libraries/python/statisfaction-latest.tar.gz
```

Here we're installing the `latest` version, but you could replace `latest` with a release id (e.g. `0.3.1`).

# Supported functionalities

* Loading data from BigQuery, CSV, Vertica and Pandas
* Binomial test to verify assignment of observations
* Normality tests
* F-test for equal variance check
* T-test and U-test to assess uplifts
* Power calculations for T-test
* Confidence intervals for T-test
* Bonferonni corrections for multiple variables
* Corrections for multiple peeking
* Multinormality test
* Hotelling's T2-test for mean vector equality
* Difference-in-difference estimation

# Structure

The library is organized in modules that group related functionalities:

* `core` contains the base data structure of the library (see below)
* `io` contains facilities to load data from data sources commonly used at BlaBlaCar (ex: loading from Vertica)
* `univariate` and `multivariate` contain common statistical functions (ex: T test)
* `duration` enables power calculations (ex: duration of a T test, minimum detectable effect)
* `suite` is for common workflows and experiment designs that we use internally (ex: diff-in-diff)

# Usage

Have a look at this [tutorial](docs/USAGE.md) on the application of the T-test to learn how to use the library.

# Contributing

[Here](docs/CONTRIBUTING.md) you can learn about the contribution workflow.


