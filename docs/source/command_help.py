import json
import os
import re
import subprocess

#from .api import init as init_api
#from .api import DiscourseClientError
#from .log_util import get_logger

# from . import cache
#from . import util
try:
    from sphinx.util import logging
except ImportError:
    import logging

log = logging.getLogger(__name__)
#log = get_logger()

COMMAND_HELP_POST_TEMPLATE = """
<!-- -*- eval: (visual-line-mode 1) -*- -->

<div data-theme-toc="true"></div>
<div data-guild-cmd="true"></div>

### Usage

``` command
{usage[prog]} {usage[args]}
```

{formatted_help}

{formatted_options}{formatted_subcommands}

<span data-guild-class="guild-cmd-version">Guild AI version {version}</span>
"""

COMMAND_INDEX_TEMPLATE = """
{header}

{formatted_commands}

<span data-guild-class="guild-cmd-version">Guild AI version {version}</span>
"""


class NoSuchCommand(Exception):
    pass


###################################################################
# Publish commands
###################################################################


def generate_command_help():
    log.info("querying guild for command help")
    cmds = _guild_commands()
    for cmd, help_data in cmds:
        filename = _command_permalink(cmd)  # + ".md")
        print(filename)
        with open(filename, "w") as manpage:
            formatted_help = _format_command_help_post(cmd, help_data)
            manpage.write(formatted_help)


def _guild_commands(cmd_names=None):
    cmds = []
    if cmd_names:
        _acc_command_data(cmd_names, cmds)
    else:
        _acc_recurse_command_data("", cmds)
    return cmds


def _acc_command_data(cmd_names, cmds):
    for cmd in cmd_names:
        try:
            data = _get_cmd_help_data(cmd)
        except NoSuchCommand:
            log.error("No such command '%s'", cmd)
        else:
            cmds.append((cmd, data))


def _acc_recurse_command_data(base_cmd, acc):
    (help_data, subcommands) = _cmd_help(base_cmd)
    if base_cmd:
        acc.append((base_cmd, help_data))
    for cmd in subcommands:
        _acc_recurse_command_data(cmd, acc)


def _cmd_help(cmd):
    help_data = _get_cmd_help_data(cmd)
    log.debug("Help data for %s: %r", cmd, help_data)
    subcommands = _subcommands_for_help_data(help_data, cmd)
    return help_data, subcommands


def _get_cmd_help_data(cmd):
    cmd_desc = _cmd_desc(cmd)
    # cached = cache.read(_cmd_cache_key(cmd))
    # if cached:
    #     log.info("Reading cached command info for %s", cmd_desc)
    #     return json.loads(cached)
    log.info("Fetching command info for %s", cmd_desc)

    git_root = "cd $(git rev-parse --show-toplevel)"
    help_cmd = """(%s; python -c 'import runpy, sys; sys.argv[0]="guild"; runpy.run_module("guild.main_bootstrap", run_name="__main__")' %s --help)""" % (
        git_root, cmd
    )
    # help_cmd = "guild %s --help" % cmd
    help_env = dict(os.environ)
    help_env["GUILD_HELP_JSON"] = "1"
    p = subprocess.Popen(
        help_cmd,
        env=help_env,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    out, err = p.communicate()
    if p.returncode != 0:
        log.debug("Error reading help for '%s': %s", cmd, err)
        raise NoSuchCommand(cmd)
    # cache.write(_cmd_cache_key(cmd), out)
    return json.loads(out)


def _cmd_desc(cmd):
    if cmd:
        return "'%s'" % cmd
    else:
        return "guild base command"


def _subcommands_for_help_data(help_data, base_cmd):
    subcommands = []
    for cmd in help_data.get("commands", []):
        for term in _split_cmd_term(cmd["term"]):
            subcommands.append(_join_cmd(base_cmd, term))
    return subcommands


def _split_cmd_term(cmd_term):
    """Splits a command term into mutiple parts.

    Command terms may contain aliases, which are included in the
    parts.
    """
    return [part.strip() for part in cmd_term.split(",")]


def _join_cmd(base_cmd, subcmd):
    if not base_cmd:
        return subcmd
    return "%s %s" % (base_cmd, subcmd)


def _command_permalink(cmd):
    return "pages/commands/%s" % cmd.replace(" ", "-") + ".md"


def _command_help_title(cmd):
    return "Command: %s" % cmd


def _format_command_help_post(cmd, help_data):
    post = COMMAND_HELP_POST_TEMPLATE.format(
        title=_command_help_title(cmd),
        formatted_help=_format_command_help(help_data),
        formatted_options=_format_command_help_options(help_data),
        formatted_subcommands=_format_command_subcommands(cmd, help_data),
        **help_data,
    )
    return _apply_command_refs(post).strip()


def _format_command_help(help_data):
    return _remove_paragraph_lfs(help_data["help"])


def _remove_paragraph_lfs(s):
    return re.sub(r"(\S)\n(\S)", r"\1 \2", s)


def _format_command_help_options(help_data):
    lines = ["### Options", "", "| | |", "|-|-|"]
    lines.extend([_format_command_option(option) for option in help_data["options"]])
    return "\n".join(lines)


def _format_command_option(option):
    return "|`%s`|%s|" % (option["term"], option["help"])


def _format_command_subcommands(cmd, help_data):
    subcommands = help_data.get("commands")
    if not subcommands:
        return ""
    lines = [
        "",
        "",
        "### Subcommands",
        "",
        ""
        "| | |",
        "|-|-|",
    ]
    lines.extend([_format_subcommand(cmd, subcmd) for subcmd in subcommands])
    return "\n".join(lines)


def _format_subcommand(cmd, subcmd):
    return "|%s|%s|" % (_format_subcommand_links(cmd, subcmd), subcmd["help"])


def _format_subcommand_links(cmd, subcmd):
    return ", ".join(
        [
            _format_subcommand_link(cmd, term)
            for term in _split_cmd_term(subcmd["term"])
        ]
    )


def _format_subcommand_link(base_cmd, subcmd_term):
    return "[%s](%s)" % (
        subcmd_term,
        _command_permalink(_join_cmd(base_cmd, subcmd_term)),
    )


def _apply_command_refs(s):
    parts = re.split(r"(``guild .+ --help``)", s)
    return "".join([_try_command_ref(part) or part for part in parts])


def _try_command_ref(s):
    m = re.match(r"``guild (.+) --help``", s)
    if m:
        return "[`guild %s`](%s)" % (m.group(1), _command_permalink(m.group(1)))
    return None


def _format_command_index(commands, version):
    return COMMAND_INDEX_TEMPLATE.format(
        header=_format_command_index_header(),
        formatted_commands=_format_command_index_commands(commands),
        version=version,
    ).strip()


def _format_command_index_header():
    return "\n".join(
        [
            "Guild supports the commands listed below. You can get "
            "help for any of these commands by running:",
            "",
            "``` command",
            "guild <command> --help",
            "```"
            "",
        ]
    )


def _format_command_index_commands(commands):
    lines = ["| | |", "|-|-|"]
    lines.extend([_format_command_for_index(name, data) for name, data in commands])
    return "\n".join(lines)


def _format_command_for_index(name, data):
    return "|[%s](%s)|%s|" % (name, _command_permalink(name), _cmd_summary(data))


def _cmd_summary(data):
    return data["help"].split("\n")[0]


def _command_help_slug(cmd):
    return "command-%s" % cmd.replace(" ", "-")


def _check_topic_slug(topic, cmd):
    expected = _command_help_slug(cmd)
    if topic["slug"] != expected:
        log.error(
            "Unexpected slug for topic %s: got '%s' expected '%s'",
            topic["id"],
            topic["slug"],
            expected,
        )


def _check_topic_title(topic, cmd):
    expected = _command_help_title(cmd)
    if topic["title"] != expected:
        log.error(
            "Unexpected title for topic %s: got '%s' expected '%s'",
            topic["id"],
            topic["title"],
            expected,
        )
