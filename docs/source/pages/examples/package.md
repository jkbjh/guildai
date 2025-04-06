# Package
<!-- -*- eval:(visual-line-mode 1) -*- -->

<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

This [example](https://github.com/guildai/guildai/tree/master/examples/hello-package) illustrates basic package configuration. It's a modification of [Hello](/pages/examples/hello) to include support for packaging.

Project files:

|||
|-|-|
| [guild.yml](https://github.com/guildai/guildai/blob/master/examples/hello-package/guild.yml) | Project Guild file |
| [say.py](https://github.com/guildai/guildai/blob/master/examples/hello-package/say.py) | Prints a greeting |
| [cat.py](https://github.com/guildai/guildai/blob/master/examples/hello-package/cat.py) | Prints contents of a file |
| [hello.txt](https://github.com/guildai/guildai/blob/master/examples/hello-package/hello.txt), [hello-2.txt](https://github.com/guildai/guildai/blob/master/examples/hello-package/hello-2.txt) | Sample files used by `hello-file` operation |

The Guild file is modified to support packaging with modifications:

- Promote the Guild file format from [*operation only format*](/pages/reference/guildfile#operation-only-format) to [*full format*](/pages/reference/guildfile#full-format). This moves the operations under a model definition. We use the anonymous model (named with an empty string) to maintain the original interface.

- Add a `package` top-level object to the Guild file. This defines the package name and defines the data files that should be included in the package.

## Remote Operations

With package support, the `hello-file` operation can be run on remote servers. Without this change, the files `hello.txt` and `hello-2.txt` would not be included in the package installed on remote systems.

All of the steps outlined in [Hello](/pages/examples/hello) can be run with this example on a remote. Include the additional option <code>\-\-remote <em>NAME</em></code> for each command that you want to run remotely.

> <span data-guild-class="callout important">Important</span> The steps that follow are not required for remote operations. You can run operations remotely without packaging or installing packages --- Guild does this for you when you include the `--remote` option with [`guild run`](/pages/commands/run).

## Build a Package

From the `package` example directory, run:

``` bash
guild package
```

Guild uses [setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html) to build a standard Python package using the package configuration in the Guild file. For more information on supported `package` attributes, see [*Guild File Reference*](/pages/reference/guildfile#packages).

## Create a Virtual Environment

To ensure that this example does not affect your system Python environments, create a virtual environment.

You can use [`guild init`](/pages/commands/init), *virtualenv*, or *conda*. This example below uses `guild init`.

From the `package` example directory, run:

``` bash
guild init -y
```

Activate the environment:

``` bash
source guild-env
```

If you use virtual or conda to create a virtual environment, activate the environment as directed.

## Install the Package

Use `pip` to install the package.

``` bash
pip install dist/*
```

List installed Guild packages:

``` bash
guild packages
```

``` output
hello  0.1  Sample package
```

You can also see the installed packages when running `pip list` and `pip info` (Guild packages are standard Python packages).

## Use the Package

Once installed, operations defined in the package are available anywhere on the system --- even if the project director is removed.

``` bash
guild run gpkg.hello/hello
```

By default, Guild does not include package operations when listing operations from a project directory.

From the `package` directory, show available operations:

``` bash
guild operations
```

``` output
hello       Say hello to my friends
hello-file  Shows a message from a file
hello-op    Show a message from a hello-file operation
```

Include installed operations in the list by specifying the `--installed` option:

``` bash
guild operations --installed
```

``` output
gpkg.hello/hello       Say hello to my friends
gpkg.hello/hello-file  Shows a message from a file
gpkg.hello/hello-op    Show a message from a hello-file operation
hello                  Say hello to my friends
hello-file             Shows a message from a file
hello-op               Show a message from a hello-file operation
```

Change to the parent directory:

``` bash
cd ..
```

From the parent directory, show operations:

``` bash
guild operations
```

``` output
gpkg.hello/hello       Say hello to my friends
gpkg.hello/hello-file  Shows a message from a file
gpkg.hello/hello-op    Show a message from a hello-file operation
```

Guild shows installed operations because the parent directory does not contain a Guild file.

Run a packaged operation from the parent directory:

``` bash
guild run hello msg="hi from a packaged operation"
```
