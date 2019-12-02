import subprocess
import sys

sudo = len(sys.argv) >= 2 and sys.argv[1] == '--admin'
prefix = 'sudo -H ' if sudo else ''
postfix = ' --user' if not sudo else ''

cmd = prefix + 'pip list --outdated' + postfix
outdated = subprocess.run(
    cmd,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    encoding='utf-8'
)
print(cmd)

packages = [line.split()[0] if len(line.split())
            else None for line in outdated.stdout.split('\n')][2:]
print('Upgrading these packages: ' + str(packages))


for idx, package in enumerate(packages):
    if package:
        cmd = prefix + 'pip install --upgrade ' + package + postfix
        output = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )
        print(cmd)
    else:
        continue
    [print(line) for line in output.stdout.split('\n')]

    percent = round(idx / len(packages) * 100, 2)
    numerical = ('Progress: ' + str(percent) + '%').ljust(20)

    num = int(percent // 10)
    visual = '[' + num * '█' + (10 - num) * ' ' + ']'

    print(numerical + visual)

print('Done! => 100.00%'.ljust(20) + '[██████████]')
