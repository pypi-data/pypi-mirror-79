# -*- coding: utf-8 -*-
import os
from io import open
import click
import yaml
import copy
import logging.config
from .login import LogInput
from .logout import LogOutput
from .logparser import LogParser

DEFAULT_LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s\t%(process)d\t%(thread)d\t%(levelname)s\t%(pathname)s\t%(lineno)d\t%(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "server.log",
            "maxBytes": 1024*1024*128,
            "backupCount": 36,
            "encoding": "utf-8",
        }
    },
    "loggers": {
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "logfile"],
        "propagate": True,
    }
}

logger = logging.getLogger(__name__)

def deep_merge(data1, data2):
    for key2, value2 in data2.items():
        value1 = data1.get(key2, None)
        if isinstance(value1, dict) and isinstance(value2, dict):
            deep_merge(value1, value2)
        else:
            data1[key2] = value2
        

def load_input_object(settings):
    input_settings = settings.get("input", {}) or {}
    try:
        input_object = LogInput.init(input_settings)
        if not input_object:
            logger.error(u"Error: input data type error.")
            os.sys.exit(1)
        return input_object
    except RuntimeError as err:
        logger.error(u"Error: init input failed, message={message}.".format(str(err)))
        os.sys.exit(2)

def load_output_object(settings):
    output_settings = settings.get("output", {}) or {}
    try:
        output_object = LogOutput.init(output_settings)
        if not output_object:
            logger.error(u"Error: output data type error.")
            os.sys.exit(1)
        return output_object
    except RuntimeError as err:
        logger.error(u"Error: init output failed, message={message}.".format(str(err)))
        os.sys.exit(2)

def load_parser_object(settings):
    parser_object = {}
    parser_settings = settings.get("parser", {}) or {}
    if parser_settings:
        try:
            parser_object = LogParser.init(parser_settings)
            if not parser_object:
                logger.error(u"Error: parser data type error.")
            return parser_object
        except RuntimeError as err:
            logger.error(u"Error: init parser failed, message={message}。".format(str(err)))
            os.sys.exit(1)
    else:
        return None

@click.group()
@click.option("-c", "--config", required=True, help=u"Config file path. The config file must in yaml format.")
@click.pass_context
def main(ctx, config):
    """Parse log file as input and export the data to database as output.
    """
    # read settings from config file
    with open(config, "r", encoding="utf-8") as fobj:
        settings = yaml.safe_load(fobj)
    if not settings:
        settings = {}
    
    # setup logging
    logging_settings = copy.copy(DEFAULT_LOGGING_SETTINGS)
    deep_merge(logging_settings, settings.get("logging", {}) or {})
    logging.config.dictConfig(logging_settings)

    # other settings
    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    ctx.obj["settings"] = settings

@main.command()
@click.pass_context
def server(ctx):
    """Start log handler server.
    """
    settings = ctx.obj["settings"]
    input_object = load_input_object(settings)
    output_object = load_output_object(settings)
    parser_object = load_parser_object(settings)
    input_object.set_handlers(output_object, parser_object)
    input_object.loop()

@main.command()
@click.argument("text", nargs=1, required=True)
@click.pass_context
def test(ctx, text):
    """Parse the example text and print out parse result.
    """
    settings = ctx.obj["settings"]
    parser_object = load_parser_object(settings)
    info = parser_object.parse_line(text, keep_not_matched_lines=False)
    text = yaml.dump(info, allow_unicode=True)
    print(text)

@main.command()
@click.option("-i", "--include-blank-lines", is_flag=True, help="Parse empty lines or not. Default to NO parse.")
@click.option("-e", "--encoding", default="utf-8", help="Encoding of the input. Default to UTF-8.")
@click.argument("filename", nargs=1, required=False)
@click.pass_context
def scan(ctx, include_blank_lines, encoding, filename):
    """Try example settings on a test file.
    """
    settings = ctx.obj["settings"]
    scan_input_settings = {
        "type": "file",
        "ignore-blank-lines": not include_blank_lines,
        "filename": filename,
        "encoding": encoding,
    }
    settings["input"] = scan_input_settings
    input_object = load_input_object(settings)
    output_object = load_output_object(settings)
    parser_object = load_parser_object(settings)
    input_object.set_handlers(output_object, parser_object)
    input_object.loop()

if __name__ == "__main__":
    main()
