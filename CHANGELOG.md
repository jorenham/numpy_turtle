# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Turtle.save_iamge()`

### Changed

- Require `python >= 3.11`
- Require `numpy >= 1.25`
- Require `skimage >= 0.20`
- Migrated to `uv`

## [0.2] - 2019-09-29

### Added

- The `Turtle` class now has color support.
- The examples work with RGBA images now.

## [0.1] - 2018-06-26

### Added

- The `Turtle` class as wrapper for a two-dimensional (grayscale) NumPy array.
It can draw lines on its array using [turtle graphics].
- Utility function for [L-system] rule iteration.
- Code example of L-system Sierpinski triangle.
- Code example of an L-system fractal plant.
- Unit tests for the `Turtle` class.
- README with installation instructions and pointers to the examples.

[turtle graphics]: https://en.wikipedia.org/wiki/Turtle_graphics
[L-system]: https://en.wikipedia.org/wiki/L-system

[unreleased]: https://github.com/jorenham/numpy_turtle/compare/0.2...HEAD
[0.2]: https://github.com/jorenham/numpy_turtle/compare/0.1...0.2
[0.1]: https://github.com/jorenham/numpy_turtle/releases/tag/0.1
