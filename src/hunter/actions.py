import sys
import os
import linecache

DEFAULT_MIN_FILENAME_ALIGNMENT = 15


def _safe_getline(filename, lineno, getline=linecache.getline):
    try:
        return getline(filename, lineno)
    except Exception as exc:
        return "??? no source: {} ???".format(exc)


class CodePrinter(object):
    def __init__(self, stream=sys.stderr, filename_alignment=DEFAULT_MIN_FILENAME_ALIGNMENT):
        self.stream = stream
        self.filename_alignment = filename_alignment

    def __call__(self, event, basename=os.path.basename):
        filename = event.filename or "<???>"
        # TODO: support auto-alignment, need a context object for this, eg:
        # alignment = context.filename_alignment = max(getattr(context, 'filename_alignment', self.filename_alignment), len(filename))
        self.stream.write("{:>{align}}:{:<5} {:9} {}\n".format(
            basename(filename),
            event.lineno,
            event.kind,
            _safe_getline(filename, event.lineno).rstrip(),
            align=self.filename_alignment
        ))
        if event.kind in ('return', 'exception'):
            self.stream.write("{:>{align}}       {:9} {} value: {}\n".format(
                "",
                ".",
                event.kind,
                event.arg,
                align=self.filename_alignment
            ))


class VarsDumper(object):
    def __init__(self, name=None, names=(), globals=False, stream=sys.stderr, filename_alignment=DEFAULT_MIN_FILENAME_ALIGNMENT):
        self.stream = stream
        self.filename_alignment = filename_alignment
        self.names = list(names)
        if name:
            self.names.append(name)
        self.globals = globals

    def __call__(self, event):
        first = True
        for key, value in event.locals.items():
            if key in self.names:
                self.stream.write("{:>{align}}       {:9} {} -> {}\n".format(
                    "",
                    "vars" if first else ".",
                    key,
                    value,
                    align=self.filename_alignment
                ))
                first = False
        if self.globals:
            for key, value in event.globals.items():
                if key in self.names:
                    self.stream.write("{:>{align}}       {:9} {} => {}\n".format(
                        "",
                        "vars" if first else ".",
                        key,
                        value,
                        align=self.filename_alignment
                    ))
                    first = False