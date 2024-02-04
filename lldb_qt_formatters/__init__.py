# We need to import the formatters like this - no other method will work
from .qstring import *
from .qmap import *


def __lldb_init_module(debugger, internal_dict):
    init_commands = [
        'type summary add --python-function lldb_qt_formatters.qstring.format_summary "QString"',
        'type summary add --summary-string "\{${var.key}: ${var.value}\}" -x "QMapNode<.+>$"',  # noqa: W605
        'type synthetic add --python-class lldb_qt_formatters.qmap.SyntheticChildrenProvider -x "QMap<.+>$"',
        'type summary add --expand --python-function lldb_qt_formatters.qmap.format_summary -x "QMap<.+>$"'
    ]
    for command in init_commands:
        debugger.HandleCommand(command)
