from .Number import Number
from .builtins import BuiltInFunction
from .context import Context
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from .symbols import SymbolTable
from source.runner import run as execute

########################################
# EXECUTION
########################################

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


def run(fn, text):
    return execute(fn, text, global_symbol_table)
