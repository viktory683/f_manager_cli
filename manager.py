#!/usr/bin/env python

import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter

from f_manager import Profile, Mod, logger
from helpers import *

from environs import Env

env = Env()


def enable(args):
    print(f"<func enable args: {args}>")


def list_profile(args):
    print(args, end="\n\n")

    from os import get_terminal_size

    env.read_env("settings.env")
    COLORED = env.bool("COLOR")  # TODO what the fuck?

    if args.VERBOSE or (args.DISABLED and not COLORED):
        args.LIST = True

    # print(f"<func list_profile args: {args}>")

    for mod in Profile(args.PROFILE).mods:
        text = ""

        if not args.DISABLED and not mod.enabled:
            continue

        if not args.LIST:
            if mod.enabled:
                text += f"{mod.name} "
            elif args.DISABLED:
                text += f"#{mod.name} "  # TODO colors
        else:
            field_size = max(
                map(
                    len,
                    [
                        "name",
                        "version",
                        "title",
                        "description",
                        "dependencies",
                        "size",
                    ]
                )
            )

            if args.VERBOSE == 0:
                if mod.enabled:
                    text += f"{mod.name}\n"
                elif args.DISABLED:
                    if COLORED:
                        text += f"#{mod.name}\n"  # TODO colors
                    else:
                        text += f"{'#' if not mod.enabled else ''} {mod.name}\n"

            if args.VERBOSE == 1:
                if mod.enabled:
                    text += f"{mod.name}"
                elif args.DISABLED:
                    if COLORED:
                        text += f"#{mod.name}"  # TODO colors
                    else:
                        text += f"{'#' if not mod.enabled else ''} {mod.name}"
                if COLORED:
                    text += f" {mod.version}\n"  # TODO colors
                else:
                    text += f" {mod.version}\n"

            if args.VERBOSE == 2:
                # print("name".ljust(field_size, " "), end="|")
                text += "name".ljust(field_size, " ") + f"| {mod.name}\n"
                text += "version".ljust(field_size, " ") + f"| {mod.version}\n"
                if mod.name_extended:
                    text += "title".ljust(field_size, " ") + f"| {mod.name_extended}\n"
                if mod.description:
                    description_lines = mod.description.strip().splitlines()

                    line = ("\n"+(" "*(field_size+2))).join(split_by_len(description_lines[0], get_terminal_size().columns - (field_size+2)))
                    text += "description".ljust(field_size, " ") + f"| {line}\n"

                    for description_line in description_lines[1:]:
                        line = ("\n"+(" "*(field_size+2))).join(split_by_len(description_line, get_terminal_size().columns - (field_size+2)))
                        text += " "*(field_size+2) + f"{line}\n"
                text += "\n"

            if args.VERBOSE >= 3:
                # name
                # version
                # title
                # description
                # Depends on
                # Optional Deps
                # Required By
                # Optional For
                # Conflicts with
                # size
                pass

        print(text, end="")

    if not args.LIST:
        print()


profiles_choices = tuple(
    map(
        lambda profile: profile.name,
        Profile.list_profiles
    )
)

mods_choices = tuple(
    map(
        lambda mod: mod.name,
        Mod.downloaded_mods
    )
)

parser = argparse.ArgumentParser(description="Factorio mod manager")

commands = parser.add_subparsers(
    title="commands",
    description="Commands to use",
    help="description"
)


enable_parser = commands.add_parser("enable", help="Enable mod")

enable_parser.add_argument(
    "-p", "--profile",
    help="Profile to use",
    choices=profiles_choices,
    dest="PROFILE",
    default="default"
).completer = ChoicesCompleter(profiles_choices)

enable_parser.add_argument(
    "-m", "--mod",
    help="Mod to use for",
    choices=mods_choices,
    dest="MOD",
    metavar='MOD',
    required=True,
    nargs="+",
).completer = ChoicesCompleter(mods_choices)

enable_parser.set_defaults(func=enable)


list_parser = commands.add_parser("list", help="Print mods in profile")

list_parser.add_argument(
    "-p", "--profile",
    help="Profile to use",
    choices=profiles_choices,
    dest="PROFILE",
    default="default"
).completer = ChoicesCompleter(profiles_choices)

list_parser.add_argument(
    "-d", "--disabled",
    help="Display disabled mods (if you don't use colors prints '#' with the name of disabled mod)",
    dest="DISABLED",
    action="store_true",
)

list_parser.add_argument(
    "-l", "--list",
    help="Display one entry per line (default if you wanna print with disabled mods but not using colors)",
    dest="LIST",
    action="store_true"
)

list_parser.add_argument(
    "-v", "--verbose",
    help="Print more (overwrites -l)",
    dest="VERBOSE",
    action="count",
    default=0
)

list_parser.set_defaults(func=list_profile)
# parser.add_argument(
#     "-p", "--profile",
#     help="Profile to use for",
#     choices=profiles_choices,
#     dest="PROFILE"
# ).completer = ChoicesCompleter(profiles_choices)

# parser.add_argument(
#     "-m", "--mod",
#     help="Mod to use for",
#     choices=mods_choices,
#     dest="MOD",
#     metavar='{mod1, mod2}'
# ).completer = ChoicesCompleter(mods_choices)

argcomplete.autocomplete(parser)
# args = parser.parse_args()

if __name__ == "__main__":
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)

# print(args)

# TODO
# create default config settings
# G_F $HOME/Games/factorio
# and others
# custom config reads from $HOME/.config/f_manager/settings.env

# TODO exception handling if there is error in config

# TODO colored output (using switcher in config)
