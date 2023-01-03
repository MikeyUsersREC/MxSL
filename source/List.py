########################################
# List Class
########################################
from source.Number import Number
from source.Value import Value
from source.errors import RTError


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            try:
                new_list = self.copy()
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def divided_by(self, index):
        if isinstance(index, Number):
            try:
                return self.elements[index.value], None
            except:
                return None, RTError(
                    index.pos_start,
                    index.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        elif isinstance(index, List):
            for element in index.elements:
                try:
                    return self.elements[element.value], None
                except:
                    return None, RTError(
                        element.pos_start,
                        element.pos_end,
                        'Element at this index could not be retrieved from list because index is out of bounds',
                        self.context
                    )
        else:
            return None, Value.illegal_operation(self, index)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"[{', '.join([str(x) for x in self.elements])}]"
