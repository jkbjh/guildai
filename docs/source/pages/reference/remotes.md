<!-- -*- eval:(visual-line-mode 1) -*- -->
# Remotes
<div data-theme-toc="true"></div>
<div data-guild-docs="true"></div>

## Overview

This reference documents remote types, their supported attributes, and provides examples.

A remote type is defined using the `type` attribute. The types below are supported. Refer to the applicable section below for details.

|**type attribute**|
|-|
| [ssh](#ssh) |
| [ec2](#ec2) |
| [s3](#s3) |
| [azure-vm](#azure-vm) |
| [azure-blob](#azure-blob) |
| [gist](#gist) |

## SSH

### SSH Requirements

The following external software is required to use SSH remotes:

- SSH service (remote system)
- `realpath` command (remote system)
- `ssh` command (local system)
- `rsync` command (local system)

### SSH Attributes

(ssh-description)=
#### description 

*Remote description (string)*

(ssh-host)=
#### host 

*Host name to use when connecting to the remote (required string)*

(ssh-port)=
#### port 

*Port for SSH connections (integer)*

(ssh-user)=
#### user 

*User for SSH connections (string)*

(ssh-private-key)=
#### private-key 

*Local path to the private key for SSH connections (string)*

(ssh-proxy)=
#### proxy 

*Proxy to use for the SSH connection (string)*

(ssh-connect-time)=
#### connect-time 

*Number of seconds to wait for an SSH connection before quitting (integer)*

(ssh-guild-home)=
#### guild-home 

*Path to Guild home on the remote host (string)*

If this value is not set explicitly, it's determined from the virtual
environment used for the remote or `~/.guild` if a virtual environment
is not used.

Set this value when Guild home is different from the default location.

(ssh-venv-path)=
#### venv-path 

*Path to a virtual environment on the remote host (string)*

Guild activates the environment for each remote command.

Paths are relative to the remote user home directory.

Virtual environments are standard Python virtual environments that are created with `virtualenv`, `guild init`, or the Python `venv` module.

To strictly control the environment activation, use [`venv-activate`](#ssh-venv-activate) instead.

(ssh-guild-env)=
#### guild-env 

*Alias for [`venv-path`](#ssh-venv-path) (see above)*

(ssh-conda-env)=
#### conda-env 

*Conda environment name on the remote (string)*

Guild activates the Conda environment for each remote command. If [`guild-env`](#ssh-guild-env) is also specified, the Guild environment is activated rather than the Conda environment.

(ssh-venv-activate)=
#### venv-activate 

*Command used to activate an environment on the remote (string)*

Use this to specify the command that Guild uses to activate an environment for remote commands. If this attribute is specified, Guild ignores [`guild-env`](#ssh-guild-env) and [`conda-env`](#ssh-conda-env).

(ssh-use-prerelease)=
#### use-prerelease 

*Whether to use pre-release versions for required packages (boolean)*

When Guild starts a remote run, it installs the run code along with required Python packages that are specified in the project package definition or in `requirements.txt`. Set this flag to `yes` to instruct Guild to install pre-release versions of required packages.

(ssh-init)=
#### init 

*Shell command to run when the remote is reinitialized (string)*

See [SSH Start and Stop](#ssh-start-and-stop) details information on initializing an SSH remote.

### SSH Status

When you run [`guild remote status`](project:/pages/commands/remote-status.md), Guild attempts to connect to the remote host over SSH using the specified connect information. If the connect succeeds, Guild considers the remote to be available.

### SSH Start and Stop

SSH remotes cannot be started or stopped. Guild assumes that the specified host is available using the specified connect information.

SSH remotes can, however, be initialized using the `--reinit` option to [`guild remote start`](project:/pages/commands/remote-start.md). When `--reinit` is specified, Guild runs the shell command defined in the remote [`init`](#ssh-init) attribute.

Consider the following remote configuration:

``` yaml
remotes:
  my-remote:
    type: ssh
    host: remote-hostname
    init: |
      sudo apt update -y
      sudo apt upgrade -y
```

The command `guild remote start my-remote --reinit` runs the `init` command on the remote host. Use this to ensure that the remote is configured correctly before running Guild commands.

### SSH Remote Commands

The commands below can be used with SSH remotes.

<!-- master list copied from 171.md -->

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

### SSH Security

Security is managed by the SSH protocol between the local system (client) and the remote (server). Connection settings are defined as attributes (see above) and by the SSH environment. Refer to the SSH documentation for your system for additional security details.

### SSH Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#ssh) for SSH configuration examples.

## EC2

EC2 provides the same features as SSH remotes. In addition, EC2 remotes can be started and stopped on EC2 by configuring EC2 instance attributes. Refer to [Attributes](#ec2-attributes) below for details.

### EC2 Requirements

The following external software is required to use EC2 remotes:

- [AWS Command Line Interface](https://aws.amazon.com/cli/)

### EC2 Attributes

Any [SSH Attribute](#ssh-attributes) may be used to configure an EC2 remote. Refer to that section for details.

In addition to supporting SSH attributes, EC2 remotes support various EC2-specific settings. These are used when running [`guild remote start`](project:/pages/commands/remote-start.md) to create new EC2 resources to support remote operations.

(ec2-ami)=
#### ami 

*AMI used to create the EC2 instance (required string)*

(ec2-instance-type)=
#### instance-type 

*Type of EC2 instance to create (required string)*

(ec2-region)=
#### region 

*AWS region to create the EC2 instance in (string)*

If this value isn't specified, Guild uses the value defined by the
`AWS_DEFAULT_REGION` environment variable.

(ec2-root-device-size)=
#### root-device-size 

*Size of the root volume created for the server (integer)*

If this value is omitted, the default volume size for the AMI is used.

(ec2-public-key)=
#### public-key 

*The public key used when starting the EC2 instance (string or file path)*

This value may be a path, relative to the user configuration directory (i.e. `~/.guild`) or the base 64 encoded public key.

The public key is installed on the new instance to provide SSH access. This public key must correspond to the private key used to access the instance (see [`private-key`](#ec2-private-key) below).

(ec2-private-key)=
#### private-key 

*The private key used to connect to the VM instance (string or file path)*

This value may be a path, relative to the user configuration directory (i.e. `~/.guild`) or the base 64 encoded private key.

(ec2-init-timeout)=
#### init-timeout 

*The timeout to wait for a connection to the instance to become available (integer or string)*

If this value is an integer, it specifies the timeout in minutes. If the timeout is a string, it myst be a number followed by the letter 's' or 'm', to indicate seconds or minutes respectively.

If a valud is not specified, 5 minutes is assumed.

### EC2 Status

On [`guild remote status`](project:/pages/commands/remote-status.md), Guild attempts to connect to the remote host over SSH using the specified connect information. If the connect succeeds, Guild considers the remote to be available.

### EC2 Start and Stop

On [`guild remote start`](project:/pages/commands/remote-start.md), Guild uses [Terraform](https://terraform.io) to start an EC2 instance using the EC2 remote settings. On [`guild remote stop`](project:/pages/commands/remote-stop.md), Guild similarly terminates the EC2 instance using Terraform.

### EC2 Remote Commands

The commands below can be used with EC2 remotes.

<!-- master list copied from 171.md -->

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

### EC2 Security

The following environment variables must be defined when starting or
stopping an EC2 remote.

| | |
|-|-|
| `AWS_ACCESS_KEY_ID` | The AWS access key ID that has the requisite permissions for starting or terminating the applicable EC2 instance. |
| `AWS_SECRET_ACCESS_KEY` | The AWS secret access key associated with the access key ID. |

The following environment variables may be optionally defined:

| | |
|-|-|
| `AWS_DEFAULT_REGION` | The AWS region the remote instance is created in. This value may alternatively be defined in the EC2 remote configuration. |

Once an EC2 remote is created, security is managed by the SSH protocol
between the local system (client) and the remote (server).

### EC2 Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#ec2) for EC2 configuration examples.

## S3

Use S3 remotes to store runs remotely. S3 buckets support the full set of remote management commands. See [Remote Commands](#s3-remote-commands) below for details.

### S3 Requirements

The following external software is required to use SSH remotes:

- [AWS Command Line Interface](https://aws.amazon.com/cli/)

### S3 Attributes

(s3-description)=
#### description 

*Remote description (string)*

(s3-bucket)=
#### bucket 

*S3 bucket to store runs in (required string)*

(s3-root)=
#### root 

*Path in the S3 bucket to store runs in (string)*

(s3-region)=
#### region 

*AWS region where the bucket was created (string)*

The region may alternatively be specified using the `AWS_DEFAULT_REGION` environment variable when running a remote command for the S3 remote.

### S3 Status

When you run  [`guild remote status`](project:/pages/commands/remote-status.md), Guild checks that the bucket exists and that Guild can read from it. This check does not perform a write test.

### S3 Start and Stop

S3 remotes can be started and stopped. When started, Guild creates the remote bucket as needed. When stopped, Guild deletes the remote bucket if it exists.

> <span data-guild-class="callout important">Important</span> Stopping an S3 remote will delete all contents of the remote bucket, including Guild runs any objects that were copied to the bucket independently of Guild. This operation cannot be undone.

### S3 Remote Commands

The following commands can be used with S3 remotes.

<!-- master list copied from 171.md -->

|||
|-|-|
| [`runs`](project:/pages/commands/runs-list.md)| *List runs on a remote* |
| [`runs info`](project:/pages/commands/runs-info.md) | *Show information about a remote run* |
| [`runs delete`](project:/pages/commands/runs-delete.md) | *Delete remote runs* |
| [`runs restore`](project:/pages/commands/runs-restore.md) | *Restore deleted remote runs on a remote* |
| [`runs purge`](project:/pages/commands/runs-purge.md) | *Purge deleted remote runs on a remote* |
| [`pull`](project:/pages/commands/pull.md) | *Copy remote runs to the local environment* |
| [`push`](project:/pages/commands/push.md) | *Copy local runs to the remote* |

### S3 Security

The following environment variables must be defined when running any command on an S3 remote.

| | |
|-|-|
| `AWS_ACCESS_KEY_ID` | The AWS access key ID that has the requisite permissions on the remote S3 bucket. |
| `AWS_SECRET_ACCESS_KEY` | The AWS secret access key associated with the access key ID. |

The following environment variables may be optionally defined:

| | |
|-|-|
| `AWS_DEFAULT_REGION` | The AWS region associated with the bucket. This value may alternatively be defined in the S3 remote configuration. |

### S3 Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#s3) for S3 configuration examples.

## Azure VM

The Azure VM remote type provides the same features as SSH remotes. In addition, Azure VM remotes
can be started and stopped on Azure by configuring Azure VM instance attributes. Refer to [Attributes](#azure-vm-attributes) below for details.

### Azure VM Requirements

The following external software is required to use Azure VM remotes:

- [Azure Command Line Interface](https:/project:/pages/docs.microsoft.com/en-us/cli/azure/.md)

### Azure VM Attributes

Any [SSH Attribute](#ssh-attributes) may be used to configure an Azure VM remote. Refer to that section for details.

In addition to supporting SSH attributes, EC2 remotes support various EC2-specific settings. These are used when running [`guild remote start`](project:/pages/commands/remote-start.md) to create new EC2 resources to support remote operations.

(azure-vm-image)=
#### image 

*Azure image ID used to create the VM instance (required string)*

(azure-vm-instance-type)=
#### instance-type 

*Type of Azure VM instance to create (required string)*

(azure-vm-root-device-size)=
#### root-device-size 

*Size of the root volume created for the server (integer)*

If this value is omitted, the default volume size for the image is used.

(azure-vm-disk-type)=
#### disk-type 

*The type of storage to use for the managed disk (string)*

If this value is omitted, `Premium_LRS` is used.

For a list of supported values, refer to the Terraform [`storage_account_type`](https://registry.terraform.io/providers/hashicorp/azurerm/latestproject:/pages/docs/resources/managed_disk.md#storage_account_type) attribute.

(azure-vm-public-key)=
#### public-key 

*The public key used when starting the VM instance (string or file path)*

This value may be a path, relative to the user configuration directory (i.e. `~/.guild`) or the base 64 encoded public key.

The public key is installed on the new instance to provide SSH access. This public key must correspond to the private key used to access the instance (see [`private-key`](#azure-vm-private-key) below).

(azure-vm-private-key)=
#### private-key 

*The private key used to connect to the VM instance (string or file path)*

This value may be a path, relative to the user configuration directory (i.e. `~/.guild`) or the base 64 encoded private key.

(azure-vm-init-timeout)=
#### init-timeout 

*The timeout to wait for a connection to the instance to become available (integer or string)*

If this value is an integer, it specifies the timeout in minutes. If the timeout is a string, it myst be a number followed by the letter 's' or 'm', to indicate seconds or minutes respectively.

If a valud is not specified, 5 minutes is assumed.

### Azure VM Status

On [`guild remote status`](project:/pages/commands/remote-status.md), Guild attempts to
connect to the remote host over SSH using the specified connect
information. If the connect succeeds, Guild considers the remote to be
available.

### Azure VM Start and Stop

On [`guild remote start`](project:/pages/commands/remote-start.md), Guild uses
[Terraform](https://terraform.io) to start an Azure VM instance using the
Azure VM remote settings. On [`guild remote stop`](project:/pages/commands/remote-stop.md),
Guild similarly terminates the Azure VM instance using Terraform.

### Azure VM Remote Commands

The commands below can be used with Azure VM remotes.

<!-- master list copied from 171.md -->

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

### Azure VM Security

The following environment variables must be defined when starting or
stopping an Azure VM remote.

| | |
|-|-|
| `AWS_ACCESS_KEY_ID` | The AWS access key ID that has the requisite permissions for starting or terminating the applicable Azure VM instance. |
| `AWS_SECRET_ACCESS_KEY` | The AWS secret access key associated with the access key ID. |

The following environment variables may be optionally defined:

| | |
|-|-|
| `AWS_DEFAULT_REGION` | The AWS region the remote instance is created in. This value may alternatively be defined in the Azure VM remote configuration. |

Once an Azure VM remote is created, security is managed by the SSH protocol
between the local system (client) and the remote (server).

### Azure VM Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#azure-vm) for Azure VM configuration examples.

## Azure Blob

Use Azure Blob remotes to store runs remotely in [Microsoft Azure blob storage](https://azure.microsoft.com/en-us/services/storage/blobs/). The Azure Blob remote supports a subset of remote management commands. See [Remote Commands](#azure-blob-remote-commands) below for details.

### Azure Blob Requirements

The following external software is required to use Azure Blob remotes:

- [AzCopy](https:/project:/pages/docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10.md)

### Azure Blob Attributes

(azure-blob-description)=
#### description 

*Remote description (string)*

(azure-blob-bucket)=
#### container 

*Azure blob container URI to store runs in (required string)*

Refer to [*Resource URI Syntax*](https:/project:/pages/docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata.md#resource-uri-syntax) for Azure resources for information on the URI format.

(azure-blob-root)=
#### root 

*Path in the Azure container to store runs in (string)*

### Azure Blob Status

When you run  [`guild remote status`](project:/pages/commands/remote-status.md), Guild checks that the container exists and that Guild can read from it. This check does not perform a write test.

### Azure Blob Start and Stop

Azure Blob remotes do not currently support [`guild remote start`](project:/pages/commands/remote-start.md) and [`guild remote stop`](project:/pages/commands/remote-stop.md). You must create and delete the applicable containers outside of Guild. Refer to [*Quickstart: Upload, download, and list blobs with the Azure portal*](https:/project:/pages/docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal.md) for more information.

### Azure Blob Remote Commands

The Azure Blob remote does not support all remote management commands. In particular, Azure Blob remotes do not support non-permanent deletes. Therefore, [`runs restore`](project:/pages/commands/runs-restore.md) and [`runs purge`](project:/pages/commands/runs-purge.md) are not supported. Additionally, [`runs delete`](project:/pages/commands/runs-delete.md) requires the `--permanent` option.

The following commands can be used with Azure Blob remotes:

<!-- master list copied from 171.md -->

|||
|-|-|
| [`runs`](project:/pages/commands/runs-list.md)| *List runs on a remote* |
| [`runs info`](project:/pages/commands/runs-info.md) | *Show information about a remote run* |
| [`runs delete`](project:/pages/commands/runs-delete.md) | *Delete remote runs* |
| [`pull`](project:/pages/commands/pull.md) | *Copy remote runs to the local environment* |
| [`push`](project:/pages/commands/push.md) | *Copy local runs to the remote* |

The following commads are not currently supported for Azure Blob remotes:

|||
|-|-|
| [`runs restore`](project:/pages/commands/runs-restore.md) | *Restore deleted remote runs on a remote --- not supported* |
| [`runs purge`](project:/pages/commands/runs-purge.md) | *Purge deleted remote runs on a remote --- not supported* |

### Azure Blob Security

Security is handled via [AzCopy](https:/project:/pages/docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10.md) authorization using Azure Active Directory. You must log in using `azcopy login` before running Guild commands that access the applicable remote container. For more information, see [*Authorize access to blobs with AzCopy and Azure Active Directory (Azure AD)*](https:/project:/pages/docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-authorize-azure-active-directory.md).

Guild does not support Azure SAS access tokens at this time.

### Azure Blob Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#azure-blob) for Azure Blob configuration examples.

## Gist

The Gist remote type is used to store Guild runs in a [GitHub gist](https:/project:/pages/docs.github.com/en/free-pro-team@latest/github/writing-on-github/creating-gists.md). This is most convenient with Guild's inline remote support. Provided you have the required

Guild create gists with public access rights. To make a gist private, you must [change the gist visibility](https://github.blog/2014-05-09-change-the-visibility-of-your-gists/).

### Gist Requirements

The following external software is required to use Gist remotes:

- [git](https://git-scm.com/)

### Gist Attributes Attributes

(gist-description)=
#### description 

*Remote description (string)*

(gist-user)=
#### user 

*Gist owner GitHub user name (required string)*

(gist-gist-name)=
#### gist-name 

*Name to use for the gist (required string)*

This value must be unique for `user`. Guild uses this attribute to generate a README file in the gist to identify it.

### Gist Status

When you run  [`guild remote status`](project:/pages/commands/remote-status.md), Guild checks that gist exists and that Guild can read from it. This check does not perform a write test.

### Gist Start and Stop

Guild implicitly creates the applicable gist in GitHub whenever runs are pushed to it. You may explicitly create a gist using using [`guild remote start`](project:/pages/commands/remote-start.md). Delete a gist using [`guild remote stop`](project:/pages/commands/remote-stop.md). Note that when a gist is deleted, any associated runs cannot be recovered.

### Gist Remote Commands

The Gist remote does not support all remote management commands. In particular, Gist remotes do not support non-permanent deletes. Therefore, [`runs restore`](project:/pages/commands/runs-restore.md) and [`runs purge`](project:/pages/commands/runs-purge.md) are not supported. Additionally, [`runs delete`](project:/pages/commands/runs-delete.md) requires the `--permanent` option.

The following commands can be used with Gist remotes:

<!-- master list copied from 171.md -->

|||
|-|-|
| [`runs`](project:/pages/commands/runs-list.md)| *List runs on a remote* |
| [`runs info`](project:/pages/commands/runs-info.md) | *Show information about a remote run* |
| [`runs delete`](project:/pages/commands/runs-delete.md) | *Delete remote runs* |
| [`pull`](project:/pages/commands/pull.md) | *Copy remote runs to the local environment* |
| [`push`](project:/pages/commands/push.md) | *Copy local runs to the remote* |

The following commads are not currently supported for Gist remotes:

|||
|-|-|
| [`runs restore`](project:/pages/commands/runs-restore.md) | *Restore deleted remote runs on a remote --- not supported* |
| [`runs purge`](project:/pages/commands/runs-purge.md) | *Purge deleted remote runs on a remote --- not supported* |

### Gist Security

Guild creates publicly visible gists. Therefore anyone can read published runs without authorization. You may [make a gist private](https://github.blog/2014-05-09-change-the-visibility-of-your-gists/) after it's created to limit access.

To create or write to a gist, you must provide a gist-authorized [personal access token](https:/project:/pages/docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token.md) using the environment variable `GIST_ACCESS_TOKEN`.

By default, Guild uses the `https` URL type to access gists. If you prefer to to use `ssh` URL types, define the environment variable `GIST_URLTYPE` to be `ssh`.

### Gist Blob Examples

Refer to [*Remotes Cheatsheet*](project:/pages/cheatsheets/remotes.md#gist) for Gist configuration examples.

### Gist Inline Specs

A Gist remote may be specified using an inline specification. The format is:

    gist:USER/GIST_NAME

For example, to push runs to a gist named `shared-runs` for the GitHub user `jack`, run:

``` bash
guild push gist:jack/shared-runs
```

To write to a gist, you must have write access provided by a personal access token specified by the environment variable `GIST_ACCESS_TOKEN`.

You may omit the user from a gist spec by defining the `GIST_USER` environment variable.
