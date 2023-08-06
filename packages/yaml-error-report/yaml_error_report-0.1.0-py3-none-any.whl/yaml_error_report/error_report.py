import dataclasses
import io
import typing as t
from .types import Location
from .formatters import ColoredConsoleFormatter, Formatter


def _cleanup_loc(content: str, loc: Location) -> Location:
    """remove trailing newlines and whitespace from the location"""
    ctx = content[loc.pos:loc.end_pos]
    ln_adjust = 0
    for ln in reversed(ctx.splitlines()):
        if len(ln.rstrip()) == 0:
            ln_adjust += 1
        else:
            break

    if ln_adjust > 0:
        new_end_col = len(content.splitlines()[loc.end_ln - 1 - ln_adjust])
        return dataclasses.replace(loc, end_ln=loc.end_ln - ln_adjust, end_col=new_end_col)
    return loc


def _get_indent_and_width(content: str, loc: Location) -> t.Tuple[int, int]:
    if loc.ln == loc.end_ln:
        return loc.col, max(loc.end_col - loc.col, 1)

    ctx = content[loc.pos:loc.end_pos]
    ctx = ctx.rstrip()
    max_col = max(len(ln.rstrip()) for ln in ctx.splitlines())
    return loc.col, (max_col - loc.col)


def error_report(title_msg: str,
                 error_msg: str,
                 loc: Location,
                 lines_before: int = 1,
                 lines_after: int = 3,
                 formatter: Formatter = None) -> str:
    """Create a user error report

    Args:
        title_msg: Title of the error report, displayed as a header
        error_msg: Specific error message, displayed next to the error location
        lines_before: Number of context lines to show before the error
        lines_after: Number of context lines to show after the error
        formatter: The formatter to use on the error report [default: ColoredConsoleFormatter]
    """
    formatter = formatter or ColoredConsoleFormatter()

    with open(loc.filename, "r") as f:
        raw_contents = f.read()

    loc = _cleanup_loc(raw_contents, loc)

    def _error_line(error_msg, indent, width):
        return formatter.error_txt(" "*indent + "^"*width + " " + formatter.bold_txt(error_msg))

    report = []
    written_error = False
    for lineno, line in enumerate(io.StringIO(raw_contents)):
        lineno += 1
        line = line.strip("\n")

        if loc.ln - lines_before <= lineno < loc.end_ln + lines_after:
            # color the error in the source text
            if loc.ln <= lineno <= loc.end_ln:
                if loc.ln == lineno:
                    if loc.ln == loc.end_ln:
                        # single line error
                        line = line[:loc.col] + formatter.error_txt(line[loc.col:loc.end_col]) + line[loc.end_col:]
                    else:
                        # multiline start
                        line = line[:loc.col] + formatter.error_txt(line[loc.col:])
                elif loc.end_ln == lineno:
                    # multiline end
                    line = formatter.error_txt(line[:loc.end_col]) + line[loc.end_col:]
                else:
                    # multiline body
                    line = formatter.error_txt(line)

            report.append("{}   {}".format(formatter.info_txt(f"{lineno:4}|"), line))

            if lineno == loc.end_ln:
                written_error = True
                indent, width = _get_indent_and_width(raw_contents, loc)
                report.append(_error_line(error_msg, indent + 8, width))

    # in the case we got to the end of the file without writting the error
    if not written_error:
        report.append(_error_line(error_msg, 0, 0))

    report = [
        formatter.error_txt(title_msg),
        "   {} {}".format(formatter.info_txt("-->"), formatter.path_txt(f"{loc.filename}:{loc.ln}:{loc.col}"))
    ] + report
    return "\n".join(report)
