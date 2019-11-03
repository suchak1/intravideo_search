import subprocess
import sys

sudo = len(sys.argv) >= 3 and sys.argv[2] == '--admin'
prefix = 'sudo ' if sudo else ''
postfix = ' --user' if not sudo else ''

outdated = subprocess.run(
                          prefix + 'pip list --outdated' + postfix,
                          shell = True,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT,
                          encoding = 'utf-8'
                          )

packages = [line.split()[0] if len(line.split()) else None for line in outdated.stdout.split('\n')][2:]
print('Upgrading these packages: ' + str(packages))


for idx, package in enumerate(packages):
    if package:
        output = subprocess.run(
                                prefix + 'pip install ' + package + ' --upgrade' + postfix,
                                shell = True,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.STDOUT,
                                encoding = 'utf-8'
                                )
    else:
        continue
    [print(line) for line in output.stdout.split('\n')]

    percent = round(idx / len(packages))
    numerical = ('Progress: ' + str(percent) + '%').ljust(20)

    num = int(percent // 10)
    visual = '[' + num * '█' + (10 - num) * ' ' + ']'

    print(numerical + visual)

print('Done! => 100.00%'.ljust(20) + '[██████████]')
