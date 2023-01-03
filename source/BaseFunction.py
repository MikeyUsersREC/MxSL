########################################
# BASE FUNCTION CLASS
########################################
from source.Value import Value
from source.context import Context
from source.errors import RTError
from source.runtime_result import RTResult
from source.symbols import SymbolTable


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        if new_context.parent:
            new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        else:
            new_context.symbol_table = SymbolTable()
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()
        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))
        return res.success(None)

    def populate_args(self, arg_names, args, new_context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)
        return new_context

    def check_and_populate_args(self, arg_names, args, new_context):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        new_context = self.populate_args(arg_names, args, new_context)
        return res.success(new_context)

    def copy(self):
        raise Exception("No copy method defined")

    def __repr__(self):
        return f"<function {self.name}>"
