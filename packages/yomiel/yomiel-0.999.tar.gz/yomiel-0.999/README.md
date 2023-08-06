# yomiel

`yomiel` is the pretty printer for [jomiel] messages.

![Example (yomiel)](./docs/demo.svg)

## Features

- Support for different output formats (raw/json/yaml)
- Authentication and encryption ([CURVE] and [SSH])
- Highly configurable

## Getting started

- `yomiel` requires [Python] 3.6+
- Make sure `jomiel` is running

To install from [PyPI]:

```shell
pip install yomiel
```

To run from the repository:

```shell
git clone https://github.com/guendto/jomiel-yomiel.git
cd jomiel-yomiel
pip install -e .
```

## HOWTO

### Authenticate and encrypt using CURVE (or SSH)

See (jomiel) [HOWTO].

## License

`yomiel` is licensed under the [Apache License version 2.0][aplv2].

## Acknowledgements

`yomiel` uses [pre-commit] and its many hooks to lint and format the
project files. See the .pre-commit-config.yaml file for details.

### Subprojects (as git subtrees)

- [src/yomiel/comm/](src/yomiel/comm/) of [jomiel-comm]
- [src/yomiel/kore/](src/yomiel/kore/) of [jomiel-kore]

[python]: https://www.python.org/about/gettingstarted/
[jomiel-comm]: https://github.com/guendto/jomiel-comm/
[jomiel-kore]: https://github.com/guendto/jomiel-kore/
[howto]: https://github.com/guendto/jomiel/#howto
[jomiel]: https://github.com/guendto/jomiel/
[aplv2]: https://www.tldrlegal.com/l/apache2
[ssh]: https://en.wikipedia.org/wiki/Ssh
[pre-commit]: https://pre-commit.com/
[curve]: http://curvezmq.org/
[pypi]: https://pypi.org/
