from source.context import Context
from source.interpreter import Interpreter
from source.lexer import Lexer
from source.parser import Parser


def run(fn, text, global_symbol_table):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<prog>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error