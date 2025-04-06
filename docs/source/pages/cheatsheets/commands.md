<!-- -*- eval:(visual-line-mode 1) -*- -->
# Commands
<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

The command examples below generally use the placeholder `train` operation and related sample flags like `lr`, `dropout`, etc. Replace these values with your own.

Short-form options are used for Guild commands when available. Refer to command help for long form.

## Install Guild

Latest release:

``` bash
pip install guildai --upgrade
```

Latest pre-release:

``` bash
pip install guildai --upgrade --pre
```

Check Guild after install:

``` bash
guild check
```

## Run an Operation

Run a script:

``` bash
guild run train.py
```

Run an operation defined in a [Guild file](/pages/docs/guildfiles):

``` bash
guild run train
```

Run with flag values:

``` bash
guild run train lr=0.1 dropout=0.2
```

Run without prompting:

``` bash
guild run train -y
```

Stage an operation without running it:

``` bash
guild run train --stage
```

Start a staged run:

``` bash
guild run --start RUN-ID
```

Use command indirection (Bash compatible shells only) to start the latest staged run:

``` bash
guild run --stage `guild select -G`
```

Restart a run:

``` bash
guild run --restart RUN-ID
```

Restart the lastest run using command indirection (Bash compatible shells only):

``` bash
guild run --restart `guild select`
```

Start a new run using another run as a prototype:

``` bash
guild run --proto RUN-ID
```

Start a new run using the latest as a prototype (Bash compatible shells only):

``` bash
guild run --proto `guild select`
```

## Run a Batch

Run four trials given two values for two flags:

``` bash
guild run train lr=[0.01,0.1] dropout=[0.1,0.2]
```

Run 20 random trials using flag values from a uniform and log-uniform distribution:

``` bash
guild run train lr=loguniform[1e-5:1e-1] dropout=[0.1:0.9] -m 20
```

Run 20 random trials but use Bayesan optimization instead of random:

``` bash
guild run train lr=loguniform[1e-5:1e-1] dropout=[0.1:0.9] -Fo gp -m 20
```

## Evaluate Runs

Get general run info:

``` bash
guild runs info
```

List run files:

``` bash
guild ls
```

List source code files:

``` bash
guild ls --sourcecode
```

List all run files, including Guild files and source code:

``` bash
guild ls -a
```

Compare runs:

``` bash
guild compare
```

Compare runs for an operation:

``` bash
guild compare -Fo train
```

Save compare data to a CSV file:

``` bash
guild compare --csv runs.csv
```

Print compare data in CSV format:

``` bash
guild compare --csv -
```

View runs in TensorBoard:

``` bash
guild tensorboard
```

View runs in Guild View:

``` bash
guild view
```

## Manage Runs

### List Runs

List the latest 20 runs:

``` bash
guild runs
```

List the latest 40 runs:

``` bash
guild runs -m
```

List all runs:

``` bash
guild runs -a
```

List runs for an operation:

``` bash
guild runs -Fo train
```

List completed runs for an operation:

``` bash
guild runs -Fo train -C
```

List the latest 20 deleted runs:

``` bash
guild runs -d
```

List all deleted runs:

``` bash
guild runs -da
```

List terminated and error runs:

``` bash
guild runs -ET
```

List runs started within the last hour:

``` bash
guild runs -S "last hour"
```

List runs started today:

``` bash
guild runs -S today
```

List runs that are older than 30 days:

``` bash
guild runs -S "before 30 days ago"
```

### Delete Runs

Delete all runs:

``` bash
guild runs rm
```

Delete all failed runs (status `error`):

``` bash
guild runs rm -E
```

Delete all staged runs:

``` bash
guild runs rm -S
```

### Restore Runs

Restore all deleted runs:

``` bash
guild runs restore
```

Restore the latest five deleted runs:

``` bash
guild runs restore :5
```

## Get Help

General Guild help:

``` bash
guild --help
```

Help for a command:

``` bash
guild COMMAND --help
```

Help for an operation:

``` bash
guild run OPERATION --help-op
```

Help for the current project:

``` bash
guild help
```

Help for an installed package:

``` bash
guild help PACKAGE
```

## Debug an Operation

Test source code rules:

``` bash
guild run train --test-sourcecode
```

Test output scalar rules on the latest run output:

``` bash
guild cat --output | guild run train --test-output-scalars -
```

Test output scalar rules interactively (i.e. type sample output to evaluate and press **Enter**):

``` bash
guild run train --test-output-scalars -
```

Test flag imports:

``` bash
guild run train --test-flags
```

Stage a run to examine its file layout:

``` bash
guild run train --stage --run-dir /tmp/staged-run
```
