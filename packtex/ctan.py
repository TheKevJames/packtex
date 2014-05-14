import re
import urllib

from bs4 import BeautifulSoup

from . import (error, locations)


def get_data(package, parent=None):
    def get_rows(ctan):
        rows = []
        tables = ctan.find_all('table')
        for table in tables:
            if not str(table).startswith('<table class="entry"'):
                rows.extend(table.find_all('tr')[1:])

        for row in rows:
            if 'class' in row.td and 'i_directory' in row.td['class']:
                if row.td.get_text() not in {'testfiles'}:
                    html = urllib.urlopen('http://www.ctan.org' + row.a.get('href')).read()
                    rows.extend(get_rows(BeautifulSoup(html)))

        return rows

    def get_version(soup):
        rows = soup.find_all('table')[-1].find_all('tr')
        for row in rows:
            if re.search(r'Ver.*sion', str(row)):
                version = row.find_all('td')[-1].get_text().strip()
                return re.sub(r'(SVN)|(\s\d{4}-\d{2}-\d{2})', '', version).strip()

    html = urllib.urlopen('http://www.ctan.org/pkg/' + package).read()
    cover = BeautifulSoup(html)

    try:
        url = 'http://www.ctan.org/tex-archive' + cover.table.tr.code.get_text()
    except AttributeError:
        if 'Apache Tomcat' in cover or '503 Service Temporarily Unavailable' in cover:
            error.msg_ctan_down(fail=True)
        else:
            error.msg_not_on_ctan(package, fail=False)
            return None, -1
    if 'tex-archive/macros/latex/base' in url or 'tex-archive/macros/latex/required' in url:
        error.msg_satisfied(package, parent, fail=False)
        return None, None
    elif 'tex-archive/systems' in url:
        error.msg_not_package(package, fail=False)
        return None, None

    if url[-4] == '.' and url[-3:] in locations.get_valid_filetypes():
        return get_version(cover) or 'unversioned', [url]
    elif url[-3] == '.' and url[-2:] in locations.get_valid_filetypes():
        return get_version(cover) or 'unversioned', [url]

    html = urllib.urlopen(url).read()
    details = BeautifulSoup(html)

    version = get_version(details) or get_version(cover) or 'unversioned'
    rows = get_rows(details)

    return version, rows
