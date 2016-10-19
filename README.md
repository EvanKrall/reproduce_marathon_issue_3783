# Reproduction of [Marathon issue 3783](https://github.com/mesosphere/marathon/issues/3783)

Is the bug fixed yet?: [![Build Status](https://travis-ci.org/EvanKrall/reproduce_marathon_issue_3783.svg?branch=master)](https://travis-ci.org/EvanKrall/reproduce_marathon_issue_3783)

This repo reproduces mesosphere/marathon#3783.

The conditions of failure seem to be:

- A deploy is in progress
- Leadership fails over twice

The behavior observed is that Marathon will kill the already-running tasks belonging to the app being deployed.

## How to run

If you have [`tox`](https://tox.readthedocs.io/en/latest/) installed, simply run `tox`.

If you don't have tox, you can use docker-compose directly:

```
docker-compose run --rm behave tox -e inside_container -- --no-capture
```

## How to read the code in this repo

We use [behave](http://pythonhosted.org/behave/) to encode the reproduction case.
You can see the overall structure of the test in `behave/issue_3783.feature`.
The details of how each step is implemented are in `behave/steps/marathon_steps.py`.


## Credits

A lot of this code was adapted from [Yelp/paasta](https://github.com/Yelp/paasta)'s integration test suite.
