# logio

Parse log file as input and export the data to database as output.

## Install

```
pip install logio
```

## Installed Command Utils

- logio

## Usage

```
C:\Workspace\logio>logio --help
Usage: logio [OPTIONS] COMMAND [ARGS]...

  Parse log file as input and export the data to database as output.

Options:
  -c, --config TEXT  Config file path. The config file must in yaml format.
                     [required]

  --help             Show this message and exit.

Commands:
  scan    Try example settings on a test file.
  server  Start log handler server.
  test    Parse the example text and print out parse result.
```

## Settings

- input
  - type: stdin, file, tail
  - ignore-blank-lines: true, false
  - encoding: utf-8, gb18030, ...
  - **for type=file**
  - filename
  - **for type=tail**
  - filename
  - offset-file
  - read-from-end
  - backup-patterns
  - sleep-interval
  - non-blocking
  - blocking
- output
  - type: mysql, stdout, print-not-matched-line
  - buffer-size
  - **for type=mysql**
  - ignore-not-matched-lines
  - keep-failed-lines
  - inserts: list<string, string>
    - key: DEFAULT, some other key
    - sql_template
- parser
  - type: regex
  - use-default-rules
  - transforms
  - rules
  - matches: list<string, string>
    - matched_name
    - regex

## Releases

### v0.1.8 2020/09/09

- Translate help informations to english.
- Add License.
- Add LogToStdout.

### v0.1.7

- Some bad old release, ignore them...

