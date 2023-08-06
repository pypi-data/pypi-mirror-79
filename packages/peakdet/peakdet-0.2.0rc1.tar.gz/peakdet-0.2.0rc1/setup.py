import os
import sys

import versioneer


def main():
    from setuptools import setup, find_packages

    if sys.version_info < (3, 5):
        raise SystemError('You need Python >=3.5 or above to use peakdet.')

    # get package information
    ldict = locals()
    curr_path = os.path.dirname(__file__)
    ipath = os.path.join(curr_path, 'peakdet', 'info.py')
    with open(ipath, encoding='utf-8') as infofile:
        exec(infofile.read(), globals(), ldict)

    # get long description from README
    ldpath = os.path.join(curr_path, ldict['LONG_DESCRIPTION'])
    with open(ldpath, encoding='utf-8') as src:
        ldict['LONG_DESCRIPTION'] = src.read()

    setup(
        classifiers=ldict['CLASSIFIERS'],
        description=ldict['DESCRIPTION'],
        download_url=ldict['DOWNLOAD_URL'],
        extras_require=ldict['EXTRAS_REQUIRES'],
        install_requires=ldict['INSTALL_REQUIRES'],
        license=ldict['LICENSE'],
        long_description=ldict['LONG_DESCRIPTION'],
        long_description_content_type=ldict['LONG_DESCRIPTION_CONTENT_TYPE'],
        maintainer=ldict['MAINTAINER'],
        maintainer_email=ldict['EMAIL'],
        name=ldict['NAME'],
        packages=find_packages(exclude=['peakdet/tests']),
        package_data=ldict['PACKAGE_DATA'],
        tests_require=ldict['TESTS_REQUIRES'],
        url=ldict['URL'],
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass()
    )


if __name__ == '__main__':
    main()
