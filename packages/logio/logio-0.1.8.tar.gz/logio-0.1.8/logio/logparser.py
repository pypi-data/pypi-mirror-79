# -*- coding: utf-8 -*-
from io import open
import re
import copy
import logging
from . import rules as default_rules


logger = logging.getLogger(__name__)


def get_default_rules():
    """Get default rule sets.
    """
    rules = {}
    for key in dir(default_rules):
        if not key.startswith("_"):
            value = getattr(default_rules, key)
            rules[key] = value
    return expend_vars(rules)


def expend_vars(vars):
    """Expand with variables.

    Returns
        return expanded vars.

    Raise exception
        If some variable expand failed.
    """
    vars = copy.copy(vars)
    VAR = "(?P<var>\\{[A-Z_][A-Z_0-9]*\\})"
    while True:
        all_expended_flag = True
        for key in vars.keys():
            value = vars[key]
            names = re.findall(VAR, value)
            if names:
                all_expended_flag = False
                vars[key] = value.format(**vars)
        if all_expended_flag:
            break
    return vars


LOG_PARSER_TYPES = {}

def register_parser_type(name, klass):
    LOG_PARSER_TYPES[name] = klass

def unregister_parser_type(name):
    del LOG_PARSER_TYPES[name]

def get_parser_class(name):
    return LOG_PARSER_TYPES.get(name, None)

class LogParser(object):

    def __init__(self, settings):
        self.settings = settings or {}
        # properties
        self.keep_not_matched_lines = self.settings.get("keeep-not-matched-lines", "") or ""

    def do_keep_not_matched_line(self, info):
        with open(self.keep_not_matched_lines, "a", encoding="utf-8") as fobj:
            fobj.write(u"{0}\n".format(info["_line"]))
        logger.warn(u"Parse line failed: {0}".format(info["_line"]))

    @classmethod
    def init(cls, settings):
        parser_type = settings.get("type", "regex")
        parser_class = get_parser_class(parser_type)
        if not parser_class:
            return None
        return parser_class(settings)

    def parse_line(self, line):
        return {
            "_line": line,
        }

class RegexParser(LogParser):
    
    def __init__(self, settings):
        super(RegexParser, self).__init__(settings)
        # properties
        self.use_default_rules = self.settings.get("use-default-rules", True)
        self.transforms = self.settings.get("transforms", {}) or {}
        self.rules = self.get_rules()
        self.matches = self.get_matches()

    def do_transform(self, data):
        for key, replace_tempalte in self.transforms.items():
            try:
                data[key] = replace_tempalte.format(**data)
            except Exception:
                pass

    def get_rules(self):
        rule_map = {}
        if self.use_default_rules:
            rule_map.update(get_default_rules())
        rule_map.update(self.settings.get("rules", {}) or {})
        return expend_vars(rule_map)

    def get_matches(self):
        raw_matches = self.settings.get("matches", {})
        rule_map = copy.copy(self.rules)
        rule_map.update(raw_matches)
        rule_map = expend_vars(rule_map)
        match_items = []
        for match_name in raw_matches.keys():
            match_pattern = rule_map[match_name]
            match_items.append((match_name, match_pattern))
        return match_items

    def parse_line(self, line, keep_not_matched_lines=None):
        if keep_not_matched_lines is None:
            keep_not_matched_lines = self.keep_not_matched_lines
        data = {
            "_line": line,
        }
        matched = False
        if self.matches:
            for match_name, match_pattern in self.matches:
                try:
                    match = re.match(match_pattern, line)
                    if match:
                        matched = True
                        data["_matched_name"] = match_name
                        data.update(match.groupdict())
                        break
                except Exception as err:
                    msg = u"Error: regex match failed, match_name={0}，match_pattern={1}，error={2}。".format(
                        match_name,
                        match_pattern,
                        str(err),
                    )
                    logger.error(msg)
                    raise err
        data["_matched"] = matched
        self.do_transform(data)
        if not matched and keep_not_matched_lines:
            self.do_keep_not_matched_line(data)
        return data


register_parser_type("regex", RegexParser)
