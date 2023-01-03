import os

from source.BaseFunction import BaseFunction
from source.List import List
from source.Number import Number
from source.String import String
from source.errors import RTError
from source.runner import run
from source.runtime_result import RTResult
from source.helper import create
from source.symbols import SymbolTable


@create('print', "print", instify=True)
@create('print_ret', "print_ret", instify=True)
@create('input', "input", instify=True)
@create('input_int', "input_int", instify=True)
@create('clear', "clear", instify=True)
@create('cls', 'clear', instify=True)
@create('is_num', "is_number", instify=True)
@create('is_str', "is_string", instify=True)
@create('is_list', "is_list", instify=True)
@create('is_func', "is_function", instify=True)
@create('append', "append", instify=True)
@create('pop', "pop", instify=True)
@create('extend', "extend", instify=True)
@create('run', "run", instify=True)
@create('len', "len", instify=True)
class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res
        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    ########################################
    # BUILT-IN FUNCTIONS
    ########################################

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))

    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(Number.null)

    def execute_input_int(self, exec_ctx):
        while True:
            try:
                text = input()
                number = int(text)
                break
            except:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get('value'), Number)
        return RTResult().success(Number.true if is_number else Number.false)

    def execute_is_string(self, exec_ctx):
        is_string = isinstance(exec_ctx.symbol_table.get('value'), String)
        return RTResult().success(Number.true if is_string else Number.false)

    def execute_is_list(self, exec_ctx):
        is_list = isinstance(exec_ctx.symbol_table.get('value'), List)
        return RTResult().success(Number.true if is_list else Number.false)

    def execute_is_function(self, exec_ctx):
        is_function = isinstance(exec_ctx.symbol_table.get('value'), BaseFunction)
        return RTResult().success(Number.true if is_function else Number.false)

    def execute_append(self, exec_ctx):
        list = exec_ctx.symbol_table.get('list')
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(list, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list.elements.append(value)
        return RTResult().success(Number.null)

    def execute_pop(self, exec_ctx):
        list = exec_ctx.symbol_table.get('list')
        index = exec_ctx.symbol_table.get('index')

        if not isinstance(list, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        if index.value >= len(list.elements) or index.value < 0:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Element at this index could not be found in list",
                exec_ctx
            ))

        element = list.elements.pop(index.value)
        return RTResult().success(element)

    def execute_extend(self, exec_ctx):
        list_a = exec_ctx.symbol_table.get('list_a')
        list_b = exec_ctx.symbol_table.get('list_b')

        if not isinstance(list_a, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(list_b, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        list_a.elements.extend(list_b.elements)
        return RTResult().success(Number.null)

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get('fn')

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"",
                exec_ctx
            ))

        global_symbol_table = SymbolTable()
        global_symbol_table.set("NULL", Number.null)
        global_symbol_table.set("FALSE", Number.false)
        global_symbol_table.set("TRUE", Number.true)
        global_symbol_table.set("PRINT", BuiltInFunction.print)
        global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
        global_symbol_table.set("INPUT", BuiltInFunction.input)
        global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
        global_symbol_table.set("CLEAR", BuiltInFunction.clear)
        global_symbol_table.set("CLS", BuiltInFunction.clear)
        global_symbol_table.set("IS_NUM", BuiltInFunction.is_num)
        global_symbol_table.set("IS_STR", BuiltInFunction.is_str)
        global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
        global_symbol_table.set("IS_FUNC", BuiltInFunction.is_func)
        global_symbol_table.set("APPEND", BuiltInFunction.append)
        global_symbol_table.set("POP", BuiltInFunction.pop)
        global_symbol_table.set("EXTEND", BuiltInFunction.extend)
        global_symbol_table.set("RUN", BuiltInFunction.run)
        global_symbol_table.set("LEN", BuiltInFunction.len)

        _, error = run(fn, script, global_symbol_table)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"{error.as_string()}\n\nFailed to finish executing script \"{fn}\"",
                exec_ctx
            ))


        return RTResult().success(Number.null)

    def execute_len(self, exec_ctx):
        list = exec_ctx.symbol_table.get('list')

        if not isinstance(list, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        return RTResult().success(Number(len(list.elements)))



    execute_print.arg_names = ['value']
    execute_print_ret.arg_names = ['value']
    execute_input.arg_names = []
    execute_input_int.arg_names = []
    execute_clear.arg_names = []
    execute_is_number.arg_names = ['value']
    execute_is_string.arg_names = ['value']
    execute_is_list.arg_names = ['value']
    execute_is_function.arg_names = ['value']
    execute_append.arg_names = ['list', 'value']
    execute_pop.arg_names = ['list', 'index']
    execute_extend.arg_names = ['list_a', 'list_b']
    execute_run.arg_names = ['fn']
    execute_len.arg_names = ['list']