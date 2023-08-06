# jupyterlab-translate

![Linux tests](https://github.com/jupyterlab/jupyterlab-translate/workflows/Run%20tests/badge.svg)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Join the chat at https://gitter.im/jupyterlab/jupyterlab](https://badges.gitter.im/jupyterlab/jupyterlab.svg)](https://gitter.im/jupyterlab/jupyterlab)

This package is used to generate [language packs](https://github.com/jupyterlab/language-packs) for the JupyterLab ecosystem.

This pacakge performs the following tasks common on JupyterLab core and external extensions:

* Extract strings from code in `*.py`, `*.ts`, `*.tsx` files.
* Extract strings from JSON schema files.
* Create gettext `*.pot` catalogs.
* Removes duplicate strings from catalogs.
* Create gettext `*.po` catalogs for specific languages.
* Compile catalogs to `*.mo` and `*.json` format to be consumed by the JupyterLab frontent.

## Installation

### Pip

```bash
pip install jupyterlab-translate
```

You will also need to install [gettext-extract](https://www.npmjs.com/package/gettext-extract)
to be able to extract strings from `*.tsx` files.

```bash
npm install gettext-extract -g
```

### Conda

```bash
conda install jupyterlab-translate -c conda-forge
```

## Usage

### Bundle catalogs as part of a language pack

This is the recommended way of distributing your localization catalogs.

Visit the [language packs repository](https://github.com/jupyterlab/language-packs).

### Bundle catalogs with packages

```bash
jlab-trans extract <JLAB-EXTENSION-DIR> <JLAB_EXTENSION_NAME>
jlab-trans update <JLAB-EXTENSION-DIR> <JLAB_EXTENSION_NAME> -l es-ES
jlab-trans compile <JLAB-EXTENSION-DIR> <JLAB_EXTENSION_NAME>
```
