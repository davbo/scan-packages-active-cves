# Active CVE Check #

Checks a list of packages against the "active" (not yet patched) CVE's as listed
in the [Ubuntu CVE Tracker](http://people.canonical.com/~ubuntu-security/cve/).

CVE information is fetched from the [cve.circl.lu](https://cve.circl.lu/) API.

## How to use ##

Get the Ubuntu CVE Tracker repository (this will need to be updated periodically)

`bzr branch lp:ubuntu-cve-tracker `

Grab a list of installed packages from your Ubuntu host

`apt list --installed > installed_packages.txt`

Install the dependencies

`pip install -r requirements.txt`

Scan the packages against the known active CVE's

```
python scan_packages.py installed_packages.txt ../ubuntu-cve-tracker/active --ubuntu-version=trusty

CVE: CVE-2017-1000368
Package: sudo
CVSS: 7.2
Published: 2017-06-05T12:29:00.200000
Modified: 2017-06-05T12:29:00.217000
Summary: Todd Miller's sudo version 1.8.20p1 and earlier is vulnerable to an input validation (embedded newlines) in the get_process_ttyname() function resulting in information disclosure and command execution.
References: http://www.securityfocus.com/bid/98838 https://www.sudo.ws/alerts/linux_tty.html


CVE: CVE-2017-13049
Package: tcpdump
CVSS: None
Published: 2017-09-14T02:29:03.030000
Modified: 2017-09-14T02:29:03.030000
Summary: The Rx protocol parser in tcpdump before 4.9.2 has a buffer over-read in print-rx.c:ubik_print().
References: http://www.securitytracker.com/id/1039307 http://www.tcpdump.org/tcpdump-changes.txt https://github.com/the-tcpdump-group/tcpdump/commit/aa0858100096a3490edf93034a80e66a4d61aad5

...
```


