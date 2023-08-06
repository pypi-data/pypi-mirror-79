[![Build Status](https://travis-ci.org/job/rpki-vrp-checker.svg?branch=master)](https://travis-ci.org/job/rpki-vrp-checker)
[![Requirements Status](https://requires.io/github/job/rpki-vrp-checker/requirements.svg?branch=master)](https://requires.io/github/job/rpki-vrp-checker/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/job/rpki-vrp-checker/badge.svg?branch=master)](https://coveralls.io/github/job/rpki-vrp-checker?branch=master)

RPKI VRP Checker
================

The `rpki-vrp-checker` utility takes a set of VRPs (in JSON format)
and applies a number of tests to the VRP set to assess whether
the set conforms to the Network Operator's expectations.

Features
--------

* Canary checking (assert whether expected ROAs are part of the VRP set)
* ...

Usage
-----

```
$ pip3 install rpki-vrp-checker
$ rpki-vrp-checker -i ./export.json -c canaries.yaml -b blessed-vrp-set.json
$
```

Purpose
-------

There are various types of human error, operational failures, or attack
scenarios related to RPKI pipeline operations imaginable. This utility is
intended to be a verification tool between an internal ROA administration and
the RPKI data as published on the Internet.

Comparing "ROAs that are expected to exist" with Validated ROA Payloads as
observed from RPKI data can help in cases such as:

* Resource holder has ARIN IP prefixes, and ARIN CA has [encoding issues](https://www.arin.net/announcements/20200813/)
* Compromise of RIR systems (sudden appareance of ROAs covering an operator's resources under the wrong Trust Anchor)
* Fat fingering during ROA creation process (too many or too little ROAs were actually created compared to the internal administration)
