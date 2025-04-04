<!-- -*- eval:(visual-line-mode 1) -*- -->

<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

Guild supports training on remote system by way of a *remote* facility.

- Define a remote in [user configuration](/pages/reference/user-config)
- Specify the remote name using the `--remote` option when running an operation

For a complete reference on remote configuration, see [*Remotes Reference*](/pages/reference/remotes).

## Define a Remote

Remotes are defined in [user configuration](/pages/reference/user-config). Below is an example of an SSH remote named `remote-gpu`:

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
| [ssh](/pages/reference/remotes#ssh) | Connect to a remote server over [SSH](https://en.wikipedia.org/wiki/Secure_Shell). Use this type to train on remote servers on-premises or on any cloud vendor. Guild does not support support starting of `ssh` remote types. |
| [ec2](/pages/reference/remotes#ec2) | Connect to a remote EC2 host over [SSH](https://en.wikipedia.org/wiki/Secure_Shell). This remote type supports [`start`](/pages/commands/remote-start) and [`stop`](/pages/commands/remote-stop) remote commands given EC2 specific configuration for the remote. |
| [s3](/pages/reference/remotes#s3) | Copy runs to and from S3. This remote type does not support runs but can be used for backup and  restore. |
| [azure-vm](/pages/reference/remotes#azure-vm) | Connect to a remote Azure host over SSH. |
| [azure-blob](/pages/reference/remotes#azure-blob) | Copy runs to and from Azure blob storage. This remote type does not support runs but can be used for backup and restore. |
| [gist](/pages/reference/remotes#gist) | Copy runs to and from GitHub gists. This remote type does not support runs but can be used for backup and restore. |
</div>

For a complete list of remote types, including examples, see [*Remotes Reference*](/pages/reference/remotes).

## Manage Remotes

Remotes can be listed, checked for status, and, if supported by the remote type, started and stopped.

Remote management commands:

|                                                  |                                                      |
|--------------------------------------------------|------------------------------------------------------|
| [`guild remotes`](/pages/commands/remotes)             | List available remotes.                              |
| [`guild remote status`](/pages/commands/remote-status) | Show status for a remote.                            |
| [`guild remote start`](/pages/commands/remote-start)   | Start a remote. Not all remote types can be started. |
| [`guild remote stop`](/pages/commands/remote-start)    | Stop a remote. Not all remote types can be stopped.  |

A remote must be available before it can be used in a remote command. Check a remote using [`guild remote status`](/pages/commands/remote-status). If a remote is not available and can be started, use [`guild remote start`](/pages/commands/remote-start) to start it first. Note that some remote types cannot be started or stopped. Refer to [*Remotes Reference*](/pages/reference/remotes) for detail on each remote type.

## Remote Commands

To run apply a command to a remote, use the `--remote` option. For example, to run [`guild check`](/pages/commands/check) on a remote named `remote-gpu` (see example above), run:

``` command
guild check --remote remote-gpu
```

Not all remote types support every command. For example, the `s3` remote type does not support the `run` command. Refer to [*Remotes Reference*](/pages/reference/remotes) for details on which remote commands are support for a particular remote type.

Guild commands that support remotes:

|||
|-|-|
| [`check`](/pages/commands/check) | *Check Guild on the remote* |
| [`run`](/pages/commands/run) | *Run an operation on a remote* |
| [`stop`](/pages/commands/runs-stop) | *Stop runs in progress on a remote* |
| [`watch`](/pages/commands/watch) | *Connect to a remote run in progress and watch its output* |
| [`runs`](/pages/commands/runs-list)| *List runs on a remote* |
| [`runs info`](/pages/commands/runs-info) | *Show information about a remote run* |
| [`ls`](/pages/commands/ls) | *List remote run files* |
| [`diff`](/pages/commands/diff) | *Diff remote runs* |
| [`cat`](/pages/commands/cat) | *Show remote run file or output* |
| [`label`](/pages/commands/label) | *Apply a label to one or more remote runs* |
| [`runs delete`](/pages/commands/runs-delete) | *Delete remote runs* |
| [`runs restore`](/pages/commands/runs-restore) | *Restore deleted remote runs on a remote* |
| [`runs purge`](/pages/commands/runs-purge) | *Purge deleted remote runs on a remote* |
| [`pull`](/pages/commands/pull) | *Copy remote runs to the local environment* |
| [`push`](/pages/commands/push) | *Copy local runs to the remote* |
