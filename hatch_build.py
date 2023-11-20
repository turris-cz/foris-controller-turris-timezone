import os
import pathlib
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

BASE_DIR = pathlib.Path(os.environ.get("ZONEINFO_DIR", "/usr/share/zoneinfo"))


def timezones():
    """ reads /usr/share/zoneinfo/zone.tab and extracts zone names """
    with (BASE_DIR / "zone.tab").open() as f:
        line = f.readline()
        while line:
            stripped = line.strip()
            line = f.readline()
            if stripped.startswith("#") or not stripped:
                continue  # comments or empty lines
            yield [e for e in stripped.split() if e][2]


def extract_gnu_tz(timezone):
    with (BASE_DIR / timezone).open("rb") as f:
        data = f.read()[:-1]  # remove last newline
        last_new_line = data.rindex(b"\n")
        return data[last_new_line + 1 :].decode()


class CompileTimezones(BuildHookInterface):

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        import l18n
        import l18n.utils

        l18n.set_language("en")  # base language is English

        with open("turris_timezone.py", "w") as f:
            f.write("_tzdata = [\n")
            for timezone in timezones():
                country_code = l18n.utils.get_country_code_from_tz(timezone.replace(" ", "_"))
                country_name = l18n.territories.get(country_code)
                city = l18n.tz_cities.get(timezone.replace(" ", "_"), None)
                if not city:
                    # latest version of l18n doesn't know the timezone yet
                    continue
                gnu = extract_gnu_tz(timezone)
                f.write(f'    ("{timezone}", "{country_code}", "{country_name}", "{city}", "{gnu}"),\n')
            f.write("]\n")
            f.write("\n\n")
            f.write('TZ_GNU = {e[0]: e[4] for e in _tzdata}\n')
            f.write('COUNTRIES = {e[1]: e[2] for e in _tzdata}\n')

        return super().initialize(version, build_data)

    def clean(self, versions: list[str]) -> None:
        os.unlink("turris_timezone.py")
