import re
import json
import typer
from enum import Enum
from tabulate import tabulate
from typing import List, Optional
from pathlib import Path, PurePath
from datetime import datetime, timedelta

from bbrecon import BugBountyRecon, Program, ApiResponseError, Domain

from .utils import config, update


bb = BugBountyRecon(token=config.API_TOKEN, base_url=config.BASE_URL)

app = typer.Typer(
    help="""bbrecon

CLI for the Bug Bounty Recon API.

Requires a Bug Bounty Recon API key set in the 'BBRECON_KEY' environment variable or
configured through the CLI.

Head over to https://bugbountyrecon.com to fetch a free key.

Please use https://github.com/bugbountyrecon/bbrecon/issues to report issues.
"""
)
configure = typer.Typer(help="Configure bbrecon.")
get = typer.Typer(help="Fetch resources.")
delete = typer.Typer(help="Delete resources.")
create = typer.Typer(help="Create resources.")
app.add_typer(get, name="get")
app.add_typer(delete, name="delete")
app.add_typer(configure, name="configure")
app.add_typer(create, name="create")


class InvalidDateInputError(Exception):
    pass


class OutputFormat(str, Enum):
    narrow = "narrow"
    wide = "wide"
    json_ = "json"


def get_datetime_from_input(date_input: str) -> datetime:
    if date_input == "yesterday":
        days = 1
    elif date_input == "last-week":
        days = 7
    elif date_input == "last-month":
        days = 31
    elif date_input == "last-year":
        days = 365
    elif matches := re.match(r"last-(\d+)-days", date_input):
        days = int(matches[1])
    else:
        raise InvalidDateInputError()
    return datetime.today() - timedelta(days=days)


def output_json_programs_table(programs: List[Program]):
    typer.echo(json.dumps([program.to_dict() for program in programs], indent=4))


def output_narrow_programs_table(programs: List[Program]):
    headers = ["SLUG", "PLATFORM", "REWARDS", "MAX.BOUNTY", "TYPES"]
    data = []
    for program in programs:
        rewards = ",".join([reward for reward in program.rewards])
        types = ",".join([type_ for type_ in program.types])
        data.append(
            [
                program.slug,
                program.platform,
                rewards,
                f"${program.maximum_bounty}",
                types,
            ]
        )
    typer.echo(tabulate(data, headers, tablefmt="plain"))


def output_wide_programs_table(programs: List[Program]):
    headers = [
        "SLUG",
        "PLATFORM",
        "CREATED",
        "REWARDS",
        "MIN.BOUNTY",
        "AVG.BOUNTY",
        "MAX.BOUNTY",
        "SCOPES",
        "TYPES",
    ]
    data = []
    for program in programs:
        rewards = ",".join([reward for reward in program.rewards])
        types = ",".join([type_ for type_ in program.types])
        created_at = program.bounty_created_at.strftime("%Y-%m-%d")
        data.append(
            [
                program.slug,
                program.platform,
                created_at,
                rewards,
                f"${program.minimum_bounty}",
                f"${program.average_bounty}",
                f"${program.maximum_bounty}",
                len(program.in_scope),
                types,
            ]
        )
    typer.echo(tabulate(data, headers, tablefmt="plain"))


def output_json_scopes_table(scopes: List[dict]):
    typer.echo(json.dumps(scopes, indent=4))


def output_narrow_scopes_table(scopes: List[dict]):
    headers = ["SLUG", "PLATFORM", "TYPE", "VALUE"]
    data = []
    for scope in scopes:
        data.append([scope["slug"], scope["platform"], scope["type"], scope["value"]])
    typer.echo(tabulate(data, headers, tablefmt="plain"))


def output_wide_scopes_table(scopes: List[dict]):
    headers = ["SLUG", "PLATFORM", "TYPE", "VALUE"]
    data = []
    for scope in scopes:
        data.append([scope["slug"], scope["platform"], scope["type"], scope["value"]])
    typer.echo(tabulate(data, headers, tablefmt="plain"))


def output_json_domains_table(domains: List[Domain]):
    typer.echo(json.dumps([domain.to_dict() for domain in domains], indent=4))


def output_narrow_domains_table(domains: List[Domain]):
    headers = ["SLUG", "DOMAIN", "CREATED"]
    data = []
    for domain in domains:
        created_at = domain.created_at.strftime("%Y-%m-%d")
        data.append([domain.program, domain.name, created_at])
    typer.echo(tabulate(data, headers, tablefmt="plain"))


output_wide_domains_table = output_narrow_domains_table


def output_json_notifications_table(notifications: List[Domain]):
    typer.echo(
        json.dumps([notification.to_dict() for notification in notifications], indent=4)
    )


def output_narrow_notifications_table(notifications: List[Domain]):
    headers = ["ID", "RESOURCES", "PROGRAM"]
    data = []
    for notification in notifications:
        data.append(
            [notification.id, notification.resources, notification.program]
        )
    typer.echo(tabulate(data, headers, tablefmt="plain"))


def output_wide_notifications_table(notifications: List[Domain]):
    headers = ["ID", "RESOURCES", "PROGRAM", "WEBHOOK"]
    data = []
    for notification in notifications:
        data.append(
            [
                notification.id,
                notification.resources,
                notification.program,
                notification.webhook,
            ]
        )
    typer.echo(tabulate(data, headers, tablefmt="plain"))


@get.command("programs")
def programs_get(
    program_slugs: Optional[List[str]] = typer.Argument(None),
    output: OutputFormat = typer.Option(
        OutputFormat.wide, "--output", "-o", help="Output format."
    ),
    name: str = typer.Option(None, "--name", "-n", help="Filter by name."),
    types: List[str] = typer.Option(
        None, "--type", "-t", help="Filter by scope type. Can be used multiple times."
    ),
    rewards: List[str] = typer.Option(
        None,
        "--reward",
        "-r",
        help="Filter by reward type. Can be used multiple times.",
    ),
    platforms: List[str] = typer.Option(
        None,
        "--platform",
        "-p",
        help="Filter by platform. Can be used multiple times.",
    ),
    exclude_platforms: List[str] = typer.Option(
        None,
        "--exclude-platform",
        help="""Exclude specific platform. Ignored if --platform was passed. Can be
used multiple times.""",
    ),
    created_since: str = typer.Option(
        None,
        "--since",
        "-s",
        help="""
Filter by bounties created after a certain date. A specific date in the
format '%Y-%m-%d' can be supplied. Alternatively, the following keywords are supported:
'yesterday', 'last-week', 'last-month', 'last-year' as well as 'last-X-days'
(where 'X' is an integer).
    """,
    ),
):
    """
    Display one or many bug bounty programs, in a table or as JSON.

    If a list of slugs is provided as CLI arguments, the command will fetch the
    specified programs. Alternatively, the command will search through all programs
    using the supplied options.

    CLI filter options are ignored if slugs are provided.
    """

    if created_since:
        try:
            created_since = get_datetime_from_input(created_since)
        except InvalidDateInputError:
            typer.echo(f"Invalid date input '{created_since}', see '--help'.")
            exit(1)

    try:
        if program_slugs:
            programs = list(bb.program(slug) for slug in program_slugs)
        else:
            programs = list(
                bb.programs(
                    name=name,
                    types=types,
                    platforms=platforms,
                    exclude_platforms=exclude_platforms,
                    rewards=rewards,
                    created_since=created_since,
                )
            )
    except ApiResponseError as e:
        typer.echo(e)
        exit()

    globals()[f"output_{output}_programs_table"](programs)


@get.command("scopes")
def scopes_get(
    program_slugs: Optional[List[str]] = typer.Argument(None),
    output: OutputFormat = typer.Option(
        OutputFormat.wide, "--output", "-o", help="Output format."
    ),
    types: List[str] = typer.Option(
        None, "--type", "-t", help="Filter by scope type. Can be used multiple times."
    ),
    platforms: List[str] = typer.Option(
        None,
        "--platform",
        "-p",
        help="Filter by platform. Can be used multiple times.",
    ),
):
    """
    Display many scopes, in a table or as JSON.

    If a list of slugs is provided as CLI arguments, the command will fetch scopes for
    the specified programs. Scopes can be narrowed down by type and platform.
    """

    try:
        if program_slugs:
            programs = list(bb.program(slug) for slug in program_slugs)
        else:
            programs = list(bb.programs(types=types, platforms=platforms,))
    except ApiResponseError as e:
        typer.echo(e)
        exit()

    scopes = []
    for program in programs:
        for scope in program.in_scope:
            if types and scope.type not in types:
                continue
            scopes.append(
                {
                    "type": scope.type,
                    "value": scope.value,
                    "slug": program.slug,
                    "platform": program.platform,
                }
            )

    globals()[f"output_{output}_scopes_table"](scopes)


@get.command("domains")
def domains_get(
    program_slugs: List[str] = typer.Argument(None),
    output: OutputFormat = typer.Option(
        OutputFormat.wide, "--output", "-o", help="Output format."
    ),
    created_since: str = typer.Option(
        None,
        "--since",
        "-s",
        help="""
Filter for domains created after a certain date. A specific date in the
format '%Y-%m-%d' can be supplied. Alternatively, the following keywords are supported:
'yesterday', 'last-week', 'last-month', 'last-year' as well as 'last-X-days'
(where 'X' is an integer).
    """,
    ),
):
    """
    Display many domains, in a table or as JSON.

    If a list of slugs is provided as CLI arguments, the command will fetch domains for
    the specified programs.
    """

    if not created_since and not program_slugs:
        typer.echo(
            "You can't query all domains like this. "
            "Specify program slugs or use `--since`."
        )
        exit(1)

    if created_since:
        try:
            created_since = get_datetime_from_input(created_since)
        except InvalidDateInputError:
            typer.echo(f"Invalid date input '{created_since}', see '--help'.")
            exit(1)

    try:
        domains = list(bb.domains(programs=program_slugs, created_since=created_since))
    except ApiResponseError as e:
        typer.echo(e)
        exit()

    globals()[f"output_{output}_domains_table"](domains)


@get.command("notifications")
def notifications_get(
    notification_ids: Optional[List[str]] = typer.Argument(None),
    output: OutputFormat = typer.Option(
        OutputFormat.wide, "--output", "-o", help="Output format."
    ),
):
    """
    Display many notifications, in a table or as JSON.
    """

    try:
        if notification_ids:
            notifications = list(bb.notification(id=id) for id in notification_ids)
        else:
            notifications = list(bb.notifications())
    except ApiResponseError as e:
        typer.echo(e)
        exit()

    globals()[f"output_{output}_notifications_table"](notifications)


@delete.command("notifications")
def notifications_delete(notification_ids: Optional[List[str]] = typer.Argument(None)):
    """
    Delete one or more notifications.
    """

    try:
        for id in notification_ids:
            bb.delete_notification(id=id)
            typer.echo(f"Successfully deleted notification '{id}'.")
    except ApiResponseError as e:
        typer.echo(e)
        exit()


@create.command("notifications")
def notifications_create(
    resources: str = typer.Option(
        ..., "--resources", help="Resources to monitor. Currently supports 'programs'.",
    ),
    program: str = typer.Option(
        ...,
        "--program",
        help="""
Program to monitor. Use 'ALL' for all resources. Must be 'ALL' for 'programs' resources.
""",
    ),
    webhook: str = typer.Option(..., "--webhook", help="Destination webhook URL."),
):
    """
    Create an notification to monitor on new resources, or changes to resources.

    Currently only 'programs' is supported.
    """

    try:
        notification = bb.create_notification(
            resources=resources, program=program, webhook=webhook
        )
        typer.echo(f"Successfully created notification '{notification.id}'.")
    except ApiResponseError as e:
        typer.echo(e)
        exit()


@configure.command("key")
def key_configure():
    path = PurePath.joinpath(Path.home(), ".bbrecon")
    token_path = PurePath.joinpath(path, "token")
    Path(path).mkdir(parents=True, exist_ok=True)
    typer.echo("You can get a free API key from https://console.bugbountyrecon.com/")
    token = typer.prompt("Enter your API key")
    with open(token_path, "w+") as f:
        print(token, file=f)


def main():
    update.check()
    app()


if __name__ == "__main__":
    main()
