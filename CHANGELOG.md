# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [x.y.z] - yyyy-mm-dd
### Added
* Added GitHub Publish Workflow

### Changed
* Changed topological_sort as method of DirectedGraph class
* Changed backdoor adjustement sets to all adjustment sets and minimal adjustment sets

### Removed
### Fixed
* Fixed all simple paths return type

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
