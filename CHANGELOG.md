# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed


## [0.0.4] - 2020-01-16
### Added
* Added Back-door and Front-door paths discover function
* Added ACE confidence interval with bootstrap
* Added conditional independence tests
* Added PC algorithm


## [0.0.3] - 2020-01-11
### Added
* Added CausalModel abstract superclass
* Added initial implementation of estimation using G-formula with tests
* Added initial implementation of estimation using Propensity Score and IPW with tests
* Added initial implementation of generic sampling algorithm for SCM with at least one real feasible solution


## [0.0.2] - 2020-01-09
### Added
* Added GitHub Publish Workflow
* Added Primer Figures 3.10a and 3.10b and relative tests
* Added moral graph function
* Added has_path method
* Added frontdoor criterion implementation

### Changed
* Changed backdoor adjustement sets to all adjustment sets and minimal adjustment sets
* Changed backdoor criterion implementation

### Fixed
* Fixed all simple paths return type
* Fixed d-separation


## [0.0.1] - 2020-01-06
### Added
* Added setup.py
* Added CHANGELOG.md
* Added requirements.txt
* Added Graph and DirectedGraph wrappers for NetworkX
* Added initial support DirectedMarkovGraph class for Markov Graphs interface
* Added initial support for StructuralCausalModel class for SCM (SEM)
* Added initial d-separation wrapper
* Added initial back-door criterion check and back-door adjustement sets
* Added initial examples from Pearl's "Causal Inference in Statistic" Primer
* Added initial tests based on said examples
* Added powerset utils
