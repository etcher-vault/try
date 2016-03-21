"""
    `try` - Awesome cli tool to try out python packages.

    This module contains the command line interface.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""


import re
import sys
import click

from .core import Package, try_packages


def normalize_python_version(ctx, param, value):  # pylint: disable=unused-argument
    """Normalize given python version."""
    if value is None:
        return "python{major}.{minor}".format(
            major=sys.version_info.major,
            minor=sys.version_info.minor)

    if re.match(r"\d\.\d", value):
        return "python{0}".format(value)

    return value


def fix_packages(ctx, param, value):
    """Fix value of given packages."""
    if not value:
        return None

    def fix_package(value):
        """Fix name of package."""
        if re.match("[^/]+?/[^/]+?", value):
            return Package(value.split("/")[-1], "git+git://github.com/{0}".format(value))

        return Package(value, value)

    return [fix_package(x) for x in value]


@click.command()
@click.argument("packages", nargs=-1, callback=fix_packages)
@click.option("-v", "--version", callback=normalize_python_version,
              help="The python version to use.")
@click.option("--ipython", "use_ipython", flag_value=True,
              help="Use ipython instead of python.")
def cli(packages, version, use_ipython):
    """Easily try out python packages."""
    if not packages:
        raise click.BadArgumentUsage("At least one package is required.")

    click.echo("==> Use python {0}".format(click.style(version, bold=True)))
    click.echo("[*] Download {0} from PyPI".format(click.style(",".join(p.name for p in packages), bold=True)))
    if not try_packages(packages, version, use_ipython):
        click.secho("[*] Failed to try package. See logs for more details.", fg="red")
        sys.exit(1)


main = cli

if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter