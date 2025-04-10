<!-- -*- eval:(visual-line-mode 1) -*- -->

# Runs

<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

In [the previous section](project:/pages/start/optimize.md) you generate runs to find optimal hyperparameters for the `train.py` script. When developing models, it's not uncommon to run dozens or hundreds of experiments as you try different approaches, data sets, and hyperparameters.

In this section, you learn techniques for managing runs.

## Show Runs

Use [`guild runs`](project:/pages/commands/runs.md) to show current runs. By default, Guild only shows the latest 20 runs.

``` bash
guild runs
```

You can show 20 additional runs using `--more` or `-m` option.

``` bash
guild runs -m
```

Specify `m` multiple times as needed in increase the number of runs shown --- e.g. `-mm` shows 40 additional runs.

To show all runs, use `--all` or `-a`.

``` bash
guild runs -a
```

## Delete Runs

Use [`guild runs rm`](project:/pages/commands/runs-rm.md) or [`guild runs delete`](project:/pages/commands/runs-delete.md) to delete one or more runs. Provided you omit the `--permanent` option, you can restore deleted runs if you make a mistake.

Delete all of the runs (you restore them later):

``` bash
guild runs rm
```

Guild shows the list of runs to delete. Press **Enter** to confirm.

Verify that the runs list is empty:

``` bash
guild runs
```

Guild moves deleted runs to [*trash*](project:/pages/docs/environments.md#guild-home) where they can be viewed, restored, or purged (permanently deleted).

Show deleted runs by including the `--deleted` option with [`guild runs`](project:/pages/commands/runs.md):

``` bash
guild runs --deleted
```

## Restore Runs

To restore a deleted run, use [`guild runs restore`](project:/pages/commands/runs-restore.md).

Restore all of the deleted runs:

``` bash
guild runs restore
```

Guild shows the runs to restore. Press **Enter** to confirm.

Verify that the runs appear in the runs list:

``` bash
guild runs
```

## Label a Run

A label is a short description associated with a run. Guild shows labels when listing and comparing runs.

By default, Guild generates a default label for each run containing flag values. Specify a different label using the `--label` options with [`guild run`](project:/pages/commands/run.md).

After a run is started, you can modify its label using [`guild label`](project:/pages/commands/label.md).

To see how labels are used, let's tag the "best" run. First, find the run with the lowest *`loss`* using [`guild select`](project:/pages/commands/select.md):

``` bash
guild select -Fo train.py --min loss
```

Guild shows the run ID with the lowest loss. Confirm this by running:

``` bash
guild compare -Fo train.py --min loss --top 1 --table
```

Guild shows the `train.py` run with the lowest loss.

You can append or prepand text to existing labels using the `--append`
or `--prepend` options respectively.

For example, use the `--prepend` option with [`guild label`](project:/pages/commands/label.md) to prepend "best" to the run label:

``` bash
guild label --prepend best <run ID from previous command>
```

Guild prompts you with the proposed change. Press **Enter** to modify the run label.

> <span data-guild-class="callout tip">Tip</span> If you're running Linux, macOS, or another POSIX environment, you can use [command substitution](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html) and [`guild select`](project:/pages/commands/select.md) to specify a run ID argument. For example, `guild run --tag best $(guild select -Fo train.py --min loss)` tags the run with the lowest *`loss`* as "best".

Show runs with "best" in their label:

``` bash
guild runs -l best
```

``` output
[1:c4a48fb8]  train.py  2020-01-20 18:39:03  completed  best noise=0.1 x=-0.28771
```

Due to random effects, the selected run in your case may have a different value for *`x`*. The optimal value of *`x`* is around `-0.3`.

## Tag Runs

Tags are short text values that describe a run. Tags are like labels in that they describe runs. Tags are similarly used to filter runs. Tags provide more provide more precise control over filtering because they must match completely, whereas labels match in part.

You can specify tags when when starting an operation with [`guild run`](project:/pages/commands/run.md) using one or more `--tag` option. Tags specified with the `run` command are automatically included in the run label.

To tag an existing run, use [`guild tag`](project:/pages/commands/tag.md) with the `--add` option. Here we use a tag to mark a "best" run:

``` bash
guild tag --add best <run ID from above>
```

> <span data-guild-class="callout note">Note</span> Tags are not automatically applied to run labels. They are independent values. You can apply tag changes to a run label by specifying the `--sync-labels` option.

View tags associated with a run using [`guild runs info`](project:/pages/commands/runs-info.md).

## Filter Runs

Run-related commands support a common interface for filtering runs affected by the command.

Runs can be filtered by:

- Operation name
- Label
- Tags
- Run status
- Marked status
- When the run was started
- Source code digest

To show "best" runs (via tags), run:

``` bash
guild runs --tag best
```

To show runs that were started within the last 15 minutes, run:

``` bash
guild runs --started 'last 15 minutes'
```

For help filtering runs, refer to the applicable command in [Guild AI Commands](project:/pages/commands.md) or use `--help` with the command.

## Export Runs

Export runs to a directory for backup or to move runs out of your environment.

Export all runs to a local `archived-runs` directory:

``` bash
guild export --move archived-runs
```

Guild shows the list of runs to export. In this case runs are moved because you specify the `--move` option. Press **Enter** to confirm.

Guild moves your runs into a local `archived-runs` directory. The `guild-start` project directory should look like this:

> <span data-guild-class="ls-dir-open">guild-start</span>
<span data-guild-class="ls-dir ls-1">archived-run</span>
<span data-guild-class="ls-file ls-1">train.py</span>

Verify that your runs list is empty:

``` bash
guild runs
```

List runs in an archive directory by specifying the `--archive` option with [`guild runs`](project:/pages/commands/runs.md):

``` bash
guild runs --archive archived-runs
```

Guild shows the list of runs in the directory.

If you want to import any runs back into your list, use [`guild import`](project:/pages/commands/import.md). For this guide, we keep the runs list empty for the next section.

> <span data-guild-class="callout tip">Tip</span> Use [`guild export`](project:/pages/commands/export.md) to keep your list clear of runs you're no longer working with. Use different export directories to categorize your runs as needed. If you want to move runs to a remote location, use [`guild push`](project:/pages/commands/push.md) with a [remote configuration](project:/pages/reference/user-config.md#remotes).

## Summary

In this section you use various commands to manage your runs:

- Delete runs
- Restore deleted runs
- Label a run
- Export runs to a local directory

> <span data-guild-class="callout highlight">Highlights</span>
> - Focus on the most promising results without losing information from other experiments.
> - Generate experiments confidentaly knowing that you can archive and restore runs as needed.

In the next section, you use a *Guild file* to explicitly define operations your project.

<span data-guild-class="next btn">[Next: Create a Guild File](project:/pages/start/guildfile.md)</span>
