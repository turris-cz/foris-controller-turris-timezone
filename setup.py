import os
import pathlib

from setuptools import setup
from setuptools.command.build_py import build_py

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


class BuildCmd(build_py):
    def run(self):
        # Should generate mapping between zonename and
        # GNU TZ format based on system timezones
        # Country list, etc
        # see https://dateutil.readthedocs.io/en/stable/examples.html?highlight=tzstr#tzstr-examples

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

        # run original build cmd
        build_py.run(self)


setup(
    name="turris-timezone",
    version="0.2.2",
    description=open("README.md").read(),
    author="CZ.NIC, z. s. p. o.",
    author_email="packaging@turris.cz",
    url="https://gitlab.nic.cz/turris/foris-controller/turris-timezone",
    license="GPL-3.0",
    install_requires=[],
    setup_requires=[
        "l18n",
    ],
    extras_require={
        "test": [
            "pytest",
            "tox",
        ],
    },
    provides=["turris_timezone"],
    py_modules=["turris_timezone"],
    cmdclass={"build_py": BuildCmd},
    entry_points={},
)
