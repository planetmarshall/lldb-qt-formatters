from lldb import SBError, SBValue


def format_summary(valobj: SBValue, internal_dict, options):
    """
    Format a summary string for QString values

    :param valobj:
    :param internal_dict: unused
    :param options: unused
    """
    if not valobj.process:
        return "Unknown"

    data_member = valobj.GetChildMemberWithName("d")
    array_member = data_member.deref

    offset_in_bytes = array_member.GetChildMemberWithName("offset").GetValueAsUnsigned()
    string_length = array_member.GetChildMemberWithName("size").GetValueAsUnsigned()
    address = data_member.GetValueAsUnsigned()

    error = SBError()
    character_size = 2
    content = valobj.process.ReadMemory(address + offset_in_bytes, string_length * character_size, error)

    return f'"{bytearray(content).decode("utf-16")}"'
