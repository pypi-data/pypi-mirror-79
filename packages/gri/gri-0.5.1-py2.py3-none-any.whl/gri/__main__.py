#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys

import click
import rich
import yaml
from click_help_colors import HelpColorsGroup
from click_option_group import optgroup
from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.theme import Theme

from gri.console import TERMINAL_THEME
from gri.gerrit import GerritServer
from gri.review import Review

theme = Theme(
    {
        "normal": "",  # No or minor danger
        "moderate": "yellow",  # Moderate danger
        "considerable": "dark_orange",  # Considerable danger
        "high": "red",  # High danger
        "veryhigh": "dim red",  # Very high danger
        "branch": "magenta",
        "wip": "bold yellow",
    }
)
term = Console(theme=theme, highlighter=rich.highlighter.ReprHighlighter(), record=True)

LOG = logging.getLogger(__name__)


class Config(dict):
    def __init__(self):
        super().__init__()
        self.update(self.load_config("~/.gertty.yaml"))

    @staticmethod
    def load_config(config_file):
        config_file = os.path.expanduser(config_file)
        with open(config_file, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                LOG.error(exc)
                sys.exit(2)


# pylint: disable=too-few-public-methods
class GRI:
    def __init__(self, query=None, server=None):
        self.cfg = Config()
        self.servers = []
        for srv in (
            self.cfg["servers"]
            if server is None
            else [self.cfg["servers"][int(server)]]
        ):
            try:
                self.servers.append(GerritServer(url=srv["url"], name=srv["name"]))
            except SystemError as exc:
                LOG.error(exc)
        if not self.servers:
            sys.exit(1)

        self.reviews = list()
        for item in self.servers:

            for record in item.query(query=query):
                self.reviews.append(Review(record, item))

    def header(self):
        srv_list = " ".join(s.name for s in self.servers)
        return f"[dim]GRI using {len(self.servers)} servers: {srv_list}[/]"


def click_group_ex():
    """Return extended version of click.group()."""
    # Color coding used to group command types, documented only here as we may
    # decide to change them later.
    # green : (default) as sequence step
    # blue : molecule own command, not dependent on scenario
    # yellow : special commands, like full test sequence, or login
    return click.group(
        cls=HelpColorsGroup,
        # Workaround to disable click help line truncation to ~80 chars
        # https://github.com/pallets/click/issues/486
        context_settings=dict(max_content_width=9999),
        help_headers_color="yellow",
        help_options_color="green",
        help_options_custom_colors={
            "drivers": "blue",
            "init": "blue",
            "list": "blue",
            "matrix": "blue",
            "login": "bright_yellow",
            "reset": "blue",
            "test": "bright_yellow",
        },
    )


@click_group_ex()  # type: ignore
@click.option(
    "--incoming", "-i", default=False, help="Incoming reviews (not mine)", is_flag=True
)
@click.option(
    "--merged", "-m", default=None, type=int, help="merged in the last number of days"
)
@click.option(
    "--abandon",
    "-a",
    default=False,
    help="Abandon changes (delete for drafts) when they are >90 days old "
    "and with negative score. Requires -f to perform the action.",
    is_flag=True,
)
@click.option(
    "--abandon-age",
    "-z",
    default=90,
    help="default=90, number of days for which changes are subject to abandon",
)
@optgroup.group("General options")
@optgroup.option("--user", "-u", default="self", help="Query another user than self")
@optgroup.option(
    "--server",
    "-s",
    default=None,
    help="[0,1,2] key in list of servers, Query a single server instead of all",
)
@optgroup.option(
    "--output",
    "-o",
    default=None,
    help="Filename to dump the result in, currently only HTML is supported",
)
@optgroup.option(
    "--force",
    "-f",
    default=False,
    help="Perform potentially destructive actions.",
    is_flag=True,
)
@optgroup.option("--debug", "-d", default=False, help="Debug mode", is_flag=True)
@click.pass_context
# pylint: disable=unused-argument,too-many-arguments,too-many-locals
def main(
    ctx, debug, incoming, server, abandon, force, abandon_age, user, merged, output
):
    query = None
    handler = RichHandler(show_time=False, show_path=False)
    LOG.addHandler(handler)

    LOG.warning("Called with %s", ctx.params)
    if debug:
        LOG.setLevel(level=logging.DEBUG)
    # msg =""
    # gradient = [22, 58, 94, 130, 166, 196, 124]
    # for g in gradient:
    #     msg += term.on_color(g) + "A"
    # print(msg)
    # # return

    if " " in user:
        user = f'"{user}"'

    query = ""
    if incoming:
        query += f"reviewer:{user}"
    else:
        query += f"owner:{user}"
    if merged:
        query += f" status:merged -age:{merged}d"
    else:
        query += " status:open"

    logging.info("Query used: %s", query)
    gri = GRI(query=query, server=server)
    term.print(gri.header())
    cnt = 0

    table = Table(title="Reviews", border_style="grey15", box=box.MINIMAL)
    table.add_column("Review", justify="right")
    table.add_column("Age")
    table.add_column("Project/Subject")
    table.add_column("Meta")
    table.add_column("Score", justify="right")

    for review in sorted(gri.reviews):
        table.add_row(*review.as_columns())
        if ctx.params["abandon"] and review.score < 1:
            if review.age() > ctx.params["abandon_age"] and query != "incoming":
                review.abandon(dry=ctx.params["force"])
        LOG.debug(review.data)
        cnt += 1
    term.print(table)
    term.print(f"[dim]-- {cnt} changes listed[/]")

    if output:
        term.save_html(path=output, theme=TERMINAL_THEME)


if __name__ == "__main__":

    main()  # pylint: disable=no-value-for-parameter
