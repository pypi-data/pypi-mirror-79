
import termcolor
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def plain_txt(self, s):
        raise NotImplementedError

    @abstractmethod
    def error_txt(self, s: str):
        raise NotImplementedError

    @abstractmethod
    def path_txt(self, s: str):
        raise NotImplementedError

    @abstractmethod
    def info_txt(self, s: str):
        raise NotImplementedError

    @abstractmethod
    def bold_txt(self, s: str):
        raise NotImplementedError


class PlainFormatter(Formatter):
    def plain_txt(self, s):
        return s

    def error_txt(self, s: str):
        return s

    def path_txt(self, s: str):
        return s

    def info_txt(self, s: str):
        return s

    def bold_txt(self, s: str):
        return s


class ColoredConsoleFormatter(Formatter):
    def plain_txt(self, s):
        return s

    def error_txt(self, s: str):
        return termcolor.colored(s, "red")

    def path_txt(self, s: str):
        return termcolor.colored(s, "cyan")

    def info_txt(self, s: str):
        return termcolor.colored(s, "blue")

    def bold_txt(self, s: str):
        return termcolor.colored(s, attrs=["bold"])


class HtmlFormatter:
    def plain_txt(self, s):
        return "<span>{s}</span>"

    def error_txt(self, s: str):
        return termcolor.colored(s, "red")

    def path_txt(self, s: str):
        return termcolor.colored(s, "cyan")

    def info_txt(self, s: str):
        return termcolor.colored(s, "blue")

    def bold_txt(self, s: str):
        return termcolor.colored(s, attrs=["bold"])
