# git-history-tools

![](https://github.com/orltom/git-history-tools/workflows/Python%20package/badge.svg)
[![MIT License](https://raw.githubusercontent.com/orltom/git-history-tools/master/.github/license.svg?sanitize=true)](https://github.com/orltom/git-history-tools/blob/master/LICENSE)

Command line tool to group commits by user for a specific time window.

## Installation
```
pip install git-history-tools
```

## Usage
To run the program requires python version 3.6 or higher and a few libraries must be installed (see requirements.txt).

```
>>./githistory --help
githistory

Description:
  Group GIT commits by user and show changes in a compact mode

Usage:
  githistory [-b <name>] [-i <regex>] [-d <number>] [--since date] [--after date] <path>

Options:
  -h --help                     Show this screen.
  -b --branch <name>            GIT branch name [default: master]
  -i --issue <regex>            Regex pattern which correspond the issue ID. [default: ""]
  -d --deep <number>            change file deep [default: 1]
  --since <date>                Start date: format (%Y-%m-%d %H:%M:%S). Default is today -1
  --after <date>                End date: format (%Y-%m-%d %H:%M:%S). Default is today -2
  <path>                        GIT repository path.
```

## Docker
```
docker build . -t githistory
docer run --rm --volume "/my/repo:/tmp/repo" -it githistory --branch master --deep 3 /tmp/rep
```

## Disclaimer
This software is provided as source code under an MIT license (see LICENSE)
