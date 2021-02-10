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
        # see https://dateutil.readthedocs.io/en/stable/examples.html?highlight=tzstr#tzstr-examples

        with open("turris_timezone.py", "w") as f:
            f.write("TZ_GNU = {\n")
            for timezone in timezones():
                f.write(f'    "{timezone}": "{extract_gnu_tz(timezone)}",\n')
            f.write("}\n")

        # run original build cmd
        build_py.run(self)


setup(
    name="turris-timezone",
    version="0.1.0",
    description=open("README.md").read(),
    author="CZ.NIC, z. s. p. o.",
    author_email="packaging@turris.cz",
    url="https://gitlab.nic.cz/turris/foris-controller/turris-timezone",
    license="GPL-3.0",
    install_requires=[],
    setup_requires=[],
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
