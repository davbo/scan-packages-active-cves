import os
import re
import csv
import click
from collections import defaultdict

@click.command()
@click.argument('packages_listing', type=click.File('rb'))
@click.argument('active_cve_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def scan_packages(packages_listing, active_cve_directory):
    cves = load_cves(active_cve_directory)
    next(packages_listing) # remove header
    for package_line in packages_listing:
        package, _, _ = package_line.partition(b'/')
        package = package.decode('utf-8')
        if package in cves:
            print(package_line)
            print(cves[package])


CVE_REGEX = re.compile('Patches_([\w_-]*):')
def load_cves(active_cve_directory):
    cves = defaultdict(list)
    for filename in os.listdir(active_cve_directory):
        if filename.startswith('CVE'):
            with open(os.path.join(active_cve_directory, filename)) as f:
                m = CVE_REGEX.search(f.read())
                if m:
                    for p in m.groups():
                        cves[p].append(filename)
    return cves


if __name__=='__main__':
    scan_packages()
