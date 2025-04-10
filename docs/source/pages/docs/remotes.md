<!-- -*- eval:(visual-line-mode 1) -*- -->
# Remotes
<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

Guild supports training on remote system by way of a *remote* facility.

- Define a remote in [user configuration](project:/pages/reference/user-config.md)
- Specify the remote name using the `--remote` option when running an operation

For a complete reference on remote configuration, see [*Remotes Reference*](project:/pages/reference/remotes.md).

## Define a Remote

Remotes are defined in [user configuration](project:/pages/reference/user-config.md). Below is an example of an SSH remote named `remote-gpu`:

``` yaml
remotes:
  remote-gpu:
    type: ssh
    host: gpu001.mydomain.com
    user: ubuntu
    private-key: ~/.ssh/gpu001.pem
```

Guild supports the following remote types:

<div data-guild-class="terns">

|||
|-|-|
| [ssh](project:/pages/reference/remotes.md#ssh) | Connect to a remote server over [SSH](https://en.wikipedia.org/wiki/Secure_Shell). Use this type to train on remote servers on-premises or on any cloud vendor. Guild does not support support starting of `ssh` remote types. |
| [ec2](project:/pages/reference/remotes.md#ec2) | Connect to a remote EC2 host over [SSH](https://en.wikipedia.org/wiki/Secure_Shell). This remote type supports [`start`](project:/pages/commands/remote-start.md) and [`stop`](project:/pages/commands/remote-stop.md) remote commands given EC2 specific configuration for the remote. |
| [s3](project:/pages/reference/remotes.md#s3) | Copy runs to and from S3. This remote type does not support runs but can be used for backup and  restore. |
| [azure-vm](project:/pages/reference/remotes.md#azure-vm) | Connect to a remote Azure host over SSH. |
| [azure-blob](project:/pages/reference/remotes.md#azure-blob) | Copy runs to and from Azure blob storage. This remote type does not support runs but can be used for backup and restore. |
| [gist](project:/pages/reference/remotes.md#gist) | Copy runs to and from GitHub gists. This remote type does not support runs but can be used for backup and restore. |
</div>

For a complete list of remote types, including examples, see [*Remotes Reference*](project:/pages/reference/remotes.md).

## Manage Remotes

Remotes can be listed, checked for status, and, if supported by the remote type, started and stopped.

Remote management commands:

|                                                  |                                                      |
|--------------------------------------------------|------------------------------------------------------|
| [`guild remotes`](project:/pages/commands/remotes.md)             | List available remotes.                              |
| [`guild remote status`](project:/pages/commands/remote-status.md) | Show status for a remote.                            |
| [`guild remote start`](project:/pages/commands/remote-start.md)   | Start a remote. Not all remote types can be started. |
| [`guild remote stop`](project:/pages/commands/remote-start.md)    | Stop a remote. Not all remote types can be stopped.  |

A remote must be available before it can be used in a remote command. Check a remote using [`guild remote status`](project:/pages/commands/remote-status.md). If a remote is not available and can be started, use [`guild remote start`](project:/pages/commands/remote-start.md) to start it first. Note that some remote types cannot be started or stopped. Refer to [*Remotes Reference*](project:/pages/reference/remotes.md) for detail on each remote type.

## Remote Commands

To run apply a command to a remote, use the `--remote` option. For example, to run [`guild check`](project:/pages/commands/check.md) on a remote named `remote-gpu` (see example above), run:

``` bash
guild check --remote remote-gpu
```

Not all remote types support every command. For example, the `s3` remote type does not support the `run` command. Refer to [*Remotes Reference*](project:/pages/reference/remotes.md) for details on which remote commands are support for a particular remote type.

Guild commands that support remotes:

|||
|-|-|
| [`check`](project:/pages/commands/check.md) | *Check Guild on the remote* |
| [`run`](project:/pages/commands/run.md) | *Run an operation on a remote* |
| [`stop`](project:/pages/commands/runs-stop.md) | *Stop runs in progress on a remote* |
| [`watch`](project:/pages/commands/watch.md) | *Connect to a remote run in progress and watch its output* |
| [`runs`](project:/pages/commands/runs-list.md)| *List runs on a remote* |
| [`runs info`](project:/pages/commands/runs-info.md) | *Show information about a remote run* |
| [`ls`](project:/pages/commands/ls.md) | *List remote run files* |
| [`diff`](project:/pages/commands/diff.md) | *Diff remote runs* |
| [`cat`](project:/pages/commands/cat.md) | *Show remote run file or output* |
| [`label`](project:/pages/commands/label.md) | *Apply a label to one or more remote runs* |
| [`runs delete`](project:/pages/commands/runs-delete.md) | *Delete remote runs* |
| [`runs restore`](project:/pages/commands/runs-restore.md) | *Restore deleted remote runs on a remote* |
| [`runs purge`](project:/pages/commands/runs-purge.md) | *Purge deleted remote runs on a remote* |
| [`pull`](project:/pages/commands/pull.md) | *Copy remote runs to the local environment* |
| [`push`](project:/pages/commands/push.md) | *Copy local runs to the remote* |
