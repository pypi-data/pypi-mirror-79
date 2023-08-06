[![](https://img.shields.io/pypi/v/foliantcontrib.archeme.svg)](https://pypi.org/project/foliantcontrib.archeme/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.archeme.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.archeme)

# Archeme

Archeme preprocessor allows to integrate Foliant with [Archeme](https://github.com/foliant-docs/archeme/), a tool for describing and visualizing schemes and diagrams, primarily architectural. Archeme requires [Graphviz](https://www.graphviz.org/) to be installed.

Archeme preprocessor finds diagram definitions that are described with Archeme DSL, in source Markdown content, then calls Archeme and Graphviz to draw diagrams, and then replaces the diagram definitions with image references.

## Installation

```bash
$ pip install foliantcontrib.archeme
```

## Config

To enable the preprocessor, add `archeme` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - archeme
```

The preprocessor has a number of options with the following default values:

```yaml
preprocessors:
    - archeme:
        cache_dir: !path .archemecache
        graphviz_paths:
            dot: dot
            neato: neato
            fdp: fdp
        config_concat: false
        config_file: null
        action: generate
        format: png
        targets: []
```

Some values of options specified in the project config may be overridden by tag attributes, see below.

`cache_dir`
:   Directory to store generated Graphviz sources and drawn diagram images.

`graphviz_paths`
:   Paths to binaries of Graphviz engines to be used in external commands: `dot`, `neato`, and `fdp`.

`config_concat`
:   Flag that tells the preprocessor to read the config file and the diagram definition as YAML strings, concatenate these strings, and then load the concatenation result, i.e. single YAML string, as an object. If this option is not set (by default), config and diagram definition will be loaded as separate objects, and then merged. This option may be useful when some aliases are defined in the config, and you would like to use their values in the diagram definition.

`config_file`
:   Path to default config file. May be overridden with the value of the respective `config_file` tag attribute, see below. Config file usually defines common settings of multiple diagrams, it’s recommended but not strictly required. By default, no config file is used.

`action`
:   Default action. Used when the respective `action` tag attribute is not specified explicitly, see below. Available values are: `generate` (default), and `merge` ([see descriptions in Archeme documentation](https://github.com/foliant-docs/archeme/#cli-usage)). 

`format`
:   Format of the output image. May take any value supported by Graphviz, but note that drawn images are used within Markdown content that will be rendered by one or another backend. Preferred values are: `png` (default), and `svg`. The value of this option may be overridden by the respective `format` tag attribute.

`targets`
:   Allowed targets for the preprocessor. If not specified (by default), the preprocessor applies to all targets. Limitation of available targets may be useful when it’s needed to build a certain Foliant project in different ways with various settings, e.g. as a stand-alone documentation (for example, with the `site` target), and as a part of a documentation that combines several Foliant projects (in this case the `pre` target is usually used).

## Usage

To insert an Archeme diagram definition into your Markdown source, enclose it between `<archeme>...</archeme>` tags:

```markdown
<archeme>
structure:
    - node:
        id: first
    - node:
        id: second
edges:
    -   tail: first
        head: second
</archeme>
```

You may use optional tag attributes:

* `caption`—to set an alternative text description of the diagram that may be rendered as image caption by some backends;
* `module_id`—to specify an unique ID of the diagram that may be used for merging multiple diagram definitions;
* `action`—action that should be applied to the diagram definition; the available values are `generate` and `merge`; this attribute overrides the respective `action` config option;
* `config_file`—path to a specific config file for the certain diagram definition; this attribute overrides the respective `config_file` config option;
* `format`—output image format for the certain diagram definition; this attribute overrides the respective `format` config option.

### Examples

Diagram definition with explicitly specified ID, config file, and output format:

```markdown
<archeme module_id="one" caption="Module 1" config_file="!project_path another_config.yml" format="svg">
structure:
    - node:
        id: first
    - node:
        id: second
edges:
    -   tail: first
        head: second
</archeme>
```

Archeme DSL definition that prescribes to combine two modules with explicitly specified IDs:

```markdown
<archeme action="merge">
structure:
    - module:
        id: one
    - module:
        id: two
</archeme>
```

Note that the `file` and `description` module parameters in Archeme DSL work as usual. If you need to combine the diagrams that are identified within the current Foliant project by using `<archeme module_id="...">` tags, you should to omit the `file` and `description` module parameters in your combined diagrams definitions.
