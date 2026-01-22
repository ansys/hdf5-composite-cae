import json
import os
import re
import subprocess
import sys
import time

from ansys.hdf5_composite_cae import __version__

JSON_FILE = "dependencies.json"

_KNOWN_LICENSE_TYPES = [
    "MIT License",
    "Apache License",
    "Python Software Foundation License",
]

_MANUAL_PACKAGE_LICENSE = {
    "click": {
        "8.2.1": "BSD License",
        "8.3.0": "BSD License",
    },
    "humanize": {
        "4.12.3": "MIT License",
    },
    "more-itertools": {
        "10.8.0": "MIT License",
    },
    "pyparsing": {
        "3.2.5": "MIT License",
    },
}

# these are packages only used to collect OSS info, they're not distributed
_IGNORED_PACKAGES = [
    "pipdeptree",  # only used for internal dependency checking
    "pip-licenses",  # only used to collect license info
    "patchelf",  # used by cx_freeze on Linux to prepare executables, not distributed
]


def get_dependency_info() -> list[dict]:
    """
    Runs pip-licenses and returns a list of package info dicts.
    Each dict contains: Name, Version, License, LicenseFile, URL
    """
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "piplicenses",
            "--format",
            "json",
            "--with-urls",
            "--with-license-file",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("Error running pip-licenses:", result.stderr)
        sys.exit(1)

    packages = json.loads(result.stdout)

    # remove package with url starting with https://github.com/ansys-internal
    packages = [
        pkg
        for pkg in packages
        if not pkg["URL"].startswith("https://github.com/ansys-internal")
    ]

    # remove ignored packages
    packages = [pkg for pkg in packages if pkg["Name"] not in _IGNORED_PACKAGES]

    # try to fill in unknown license info
    for pkg in packages:
        _ = pkg.pop("LicenseFile", None)
        if pkg["License"] == "UNKNOWN":
            for known_license in _KNOWN_LICENSE_TYPES:
                if known_license in pkg["LicenseText"]:
                    pkg["License"] = known_license
                    break

        if pkg["License"] == "UNKNOWN":
            try:
                pkg["License"] = _MANUAL_PACKAGE_LICENSE[pkg["Name"]][pkg["Version"]]
            except KeyError:
                print("Could not find license for", pkg["Name"], pkg["Version"])

    # sort packages by name
    packages.sort(key=lambda pkg: pkg["Name"].lower())

    print(f"Found {len(packages)} packages")
    print("Package details:")

    print(f"{'Name':<40} {'Version':<12} {'License':<35}")
    print("-" * 87)
    for pkg in packages:
        print(f"{pkg['Name']:<40} {pkg['Version']:<12} {pkg['License']:<35}")

    num_unknown_licenses = sum(1 for pkg in packages if pkg["License"] == "UNKNOWN")
    if num_unknown_licenses > 0:
        raise Exception(
            f"!! Found {num_unknown_licenses} packages with unknown licenses !!"
        )

    for pkg in packages:
        pkg["Ansys Release Added"] = __version__
        pkg["Date Added"] = time.strftime("%Y-%m-%d", time.gmtime())
        pkg["PR Added"] = os.environ.get("PR_URL", None)

    return packages


def sanitize_string(value):
    if isinstance(value, str):
        # Remove illegal characters for Excel (control chars except tab, newline, carriage return)
        return re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", value)
    return value


def sanitize_packages(packages):
    sanitized = []
    for pkg in packages:
        sanitized_pkg = {k: sanitize_string(v) for k, v in pkg.items()}
        sanitized.append(sanitized_pkg)
    return sanitized


def write_legal_notices_txt(packages, filename="legal_notices.txt"):
    """
    Write a txt file with legal notices: package name and version.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for pkg in packages:
            f.write(f"Package: {pkg['Name']} {pkg['Version']}\n")
            f.write(f"License: {pkg['License']}\n")
            f.write(f"URL: {pkg['URL']}\n\n")
            f.write(pkg["LicenseText"])
            f.write("-" * 80 + "\n\n")
    print(f"Legal notices written to {filename}")


if __name__ == "__main__":
    packages = get_dependency_info()

    # read dependencies.json
    existing_packages = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, encoding="utf-8") as f:
            existing_packages = json.load(f)

    # if a package (name+version) was already there,
    # we don't want to override it
    def key_of(pkg):
        return f"{pkg['Name']}-{pkg['Version']}"

    existing_packages_dict = {key_of(pkg): pkg for pkg in existing_packages}

    merged_packages = []
    for pkg in packages:
        p = pkg
        name_version = key_of(pkg)
        if name_version in existing_packages_dict:
            p = existing_packages_dict[name_version]

        merged_packages.append(
            {
                "Name": p["Name"],
                "Version": p["Version"],
                "Ansys Release Added": p["Ansys Release Added"],
                "Date Added": p["Date Added"],
                "PR Added": p["PR Added"],
                "License": p["License"],
                "LicenseText": p["LicenseText"],
                "URL": p["URL"],
            }
        )

    # Write to dependencies.json
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_packages, f, indent=2)
    print(f"Dependency information written to {JSON_FILE}")

    write_legal_notices_txt(merged_packages)
