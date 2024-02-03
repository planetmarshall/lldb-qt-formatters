from typing import List

from lldb import SBValue


def format_summary(valobj: SBValue, internal_dict, options):
    """
    Format a summary string for QMap values

    :param valobj:
    :param internal_dict: unused
    :param options: unused
    """

    provider = SyntheticChildrenProvider(valobj.GetNonSyntheticValue(), internal_dict)
    return f"Size: {provider.size()}"


def _depth_first_traverse(node: SBValue, nodes: List[int]):
    # We only need the address of each node as we're going to read its
    # value directly from memory later
    nodes.append(node.load_addr)

    # QMaps are Red-Black trees but we don't need to know much about the
    # details to just extract the data.
    left = node.GetChildMemberWithName("left")
    if left.GetValueAsUnsigned() != 0:
        _depth_first_traverse(left.deref, nodes)

    right = node.GetChildMemberWithName("right")
    if right.GetValueAsUnsigned() != 0:
        _depth_first_traverse(right.deref, nodes)


def _derived_node_type(map_obj: SBValue):
    # The actual data in the QMap is in QMapNode<> elements, however QMaps only actually store each node as a
    # pointer to a non-templated base class of QMapNode<>. We need to work out what the derived class is supposed to be
    # so we can get at the data
    map_type = map_obj.type.GetUnqualifiedType()
    key_type = map_type.GetTemplateArgumentType(0)
    value_type = map_type.GetTemplateArgumentType(1)
    node_type = f"QMapNode<{key_type.name}, {value_type.name}>"
    # TODO (andrew) this can fail in unusual circumstances - such as trying to use a GCC-built Qt with a Clang-built
    #  main, but that's only ever going to work by coincidence anyway...
    return map_obj.target.FindFirstType(node_type)


class SyntheticChildrenProvider:
    def __init__(self, valobj, internal_dict):
        self.valobj = valobj
        self.node_type = _derived_node_type(self.valobj)

    def size(self):
        data_member_ptr = self.valobj.GetChildMemberWithName("d")
        data_member = data_member_ptr.deref
        return data_member.GetChildMemberWithName("size").GetValueAsSigned()

    def update(self):
        data_member_ptr = self.valobj.GetChildMemberWithName("d")
        data_member = data_member_ptr.deref
        # The root node is also a QMapNode<> but doesn't contain any
        # data we actually need.
        root = data_member.GetChildMemberWithName("header")
        nodes = []
        _depth_first_traverse(root, nodes)
        self.size = data_member.GetChildMemberWithName("size").GetValueAsSigned()
        self.nodes = [] if self.size == 0 else nodes[1:]

    def num_children(self):
        return self.size

    @staticmethod
    def get_child_index(self, name: str):
        index = name.lstrip("[").rstrip("]")
        return int(index)

    def get_child_at_index(self, index):
        node_addr = self.nodes[index]
        child_node = self.valobj.CreateValueFromAddress(f"[{index}]", node_addr, self.node_type)
        return child_node

    def has_children(self):
        return self.size > 0
