import yaml
import sys


def update_output_yaml(version):
    major_version = version.split('.')[0]
    with open('browser-matrix.yml', 'r') as file:
        data = yaml.safe_load(file)

    browser = data['matrix']['browser']

    if major_version in browser:
        browser[major_version]['FIREFOX_VERSION'] = f'firefox={version}'
        browser[major_version]['FIREFOX_PACKAGE_VERSION'] = version
        # Preserve any existing FIREFOX_PLATFORMS. The reconcile step in the
        # workflow sets it from the packages actually archived to the release,
        # so we must not downgrade linux/amd64,linux/arm64 back to linux/amd64
        # here just because arm64 has not been archived yet.
        browser[major_version].setdefault('FIREFOX_PLATFORMS', 'linux/amd64')
    else:
        # amd64 is always available; the reconcile step upgrades this to
        # include linux/arm64 once the arm64 package has been archived.
        browser[major_version] = {
            'FIREFOX_VERSION': f'firefox={version}',
            'FIREFOX_PACKAGE_VERSION': version,
            'FIREFOX_PLATFORMS': 'linux/amd64'
        }

    # Sort the dictionary by major_version as a number
    sorted_data = dict(sorted(browser.items(), key=lambda x: int(x[0]), reverse=True))
    data['matrix']['browser'] = sorted_data

    with open('browser-matrix.yml', 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    version = sys.argv[1]
    update_output_yaml(version)
