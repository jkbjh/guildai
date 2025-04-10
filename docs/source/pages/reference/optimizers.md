<!-- -*- eval:(visual-line-mode 1) -*- -->
# Optimizers
<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

An *optimizer* is a Guild operation that runs a [*batch*](project:/pages/docs/runs.md#batches). A batch generates one or more *trial runs* or *trials*. Optimizers are able to suggest flag values to minimize or maximize an objective.

Below is a list of supported optimizers.

|                   |                                                               |
|-------------------|---------------------------------------------------------------|
| [gp](#gp)         | Sequential optimizer using Gaussian processes.                |
| [forest](#forest) | Sequential optimizer using decision trees.                    |
| [gbrt](#gbrt)     | Sequential optimizer using gradient boosted regression trees. |
| [random](#random) | Batch processor using randomly selected values.               |

Use the default optimizer for an operation by specifying the `--optimize` option with [`guild run`](project:/pages/commands/run.md). The default optimizer can be defined for an operation using the [`optimizers`](project:/pages/reference/guildfile.md#operation-optimizers) attribute. Guild uses the [`gp`](#gp) optimizer if one is not otherwise defined for an operation.

Specify a named optimizer with the `--optimizer` option to [`guild run`](project:/pages/commands/run.md). A name may be one of the optimizers below or may be the name of an optimizer defined for the operation.

Optimizer flags are set using `--opt-flag` or `-Fo`. Optimizer flags are specified like other flags using the format `NAME=VALUE`.

To run the default optimizer for `train`:

``` bash
guild run train --optimize
```

To use the `forest` optimizer:

``` bash
guild run train --optimizer forest
```

For more examples, see [*Guild File Cheatsheet*](project:/pages/cheatsheets/guildfile.md#optimizers).

## gp

Bayesian optimizer using Gaussian processes.

Refer to [skopt API documentation](https://scikit-optimize.github.io/stable/modules/generated/skopt.gp_minimize.html) for details on this algorithm and its flags.

Aliases: `gaussian`, `bayesian`

### gp Flags

(gp-acq-func)=
#### acq-func 

*Function to minimize over the gaussian prior (default is `gp_hedge`)*

Choices:

|            |                                                         |
|------------|---------------------------------------------------------|
| `LCB`      | Lower confidence bound                                  |
| `EI`       | Negative expected improvement                           |
| `PI`       | Negative probability of improvement                     |
| `gp_hedge` | Probabilistically use LCB, EI, or PI at every iteration |
| `EIps`     | Negative expected improvement per second                |
| `PIps`     | Negative probability of improvement per second          |

(gp-kappa)=
#### kappa 

*Degree to which variance in the predicted values is taken into account (default is `1.96`)*

(gp-noise)=
#### noise 

*Level of noise associated with the objective (default is `gaussian`)*

Use `gaussian` if the objective returns noisy observations, otherwise specify the expected variance of the noise.

(gp-random-starts)=
#### random-starts 

*Number of trials using random values before optimizing (default is `3`)*

(gp-xi)=
#### xi 

*Improvement to seek over the previous best values (default is `0.05`)*

## forest

Sequential optimization using decision trees. Refer to [skopt API documentation](https://scikit-optimize.github.io/stable/modules/generated/skopt.forest_minimize.html) for details on this algorithm and its flags.

### forest Flags

(forest-kappa)=
#### kappa 

*Degree to which variance in the predicted values is taken into account (default is `1.96`)*

(forest-random-starts)=
#### random-starts 

*Number of trials using random values before optimizing (default is `3`)*

(forest-xi)=
#### xi 

*Improvement to seek over the previous best values (default is `0.05`)*

## gbrt

Sequential optimization using gradient boosted regression trees.

Refer to [skopt API documentation](https://scikit-optimize.github.io/stable/modules/generated/skopt.gbrt_minimize.html) for details on this algorithm and its flags.

### gbrt Flags

(gbrt-kappa)=
#### kappa 

*Degree to which variance in the predicted values is taken into account (default is `1.96`)*

(gbrt-random-starts)=
#### random-starts 

*Number of trials using random values before optimizing (default is `3`)*

(gbrt-xi)=
#### xi 

*Improvement to seek over the previous best values (default is `0.05`)*

## random

Batch processor supporting random flag value generation.

Values are selected from the search space distribution specified for each flag value.

This optimizer does not attempt to optimize an objective.

The random optimizers does not support any flags.
