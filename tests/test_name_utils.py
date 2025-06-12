import ast
import pathlib


def load_functions():
    path = pathlib.Path(__file__).resolve().parents[1] / 'app' / 'app.py'
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    namespace = {}
    for node in tree.body:
        if isinstance(node, ast.Import) and any(alias.name == 're' for alias in node.names):
            exec(compile(ast.Module([node], []), str(path), 'exec'), namespace)
        elif isinstance(node, ast.FunctionDef) and node.name in {'is_all_caps', 'extract_names_from_response'}:
            exec(compile(ast.Module([node], []), str(path), 'exec'), namespace)
    return namespace['is_all_caps'], namespace['extract_names_from_response']


is_all_caps, extract_names_from_response = load_functions()


def test_is_all_caps_mixed_case():
    assert not is_all_caps('Juan PEREZ')


def test_is_all_caps_with_non_letters():
    assert is_all_caps('JUAN-PEREZ 123')


def test_extract_names_only_bold_uppercase():
    response = (
        'Recomendamos a **JUAN PEREZ** y a **Maria Lopez**. '
        'Otros candidatos: **CARLOS-MARTÍNEZ** y **  LUISA GOMEZ  **. '
        'JOSE SINBOLD no aparece en negritas.'
    )
    names = extract_names_from_response(response)
    assert names == ['JUAN PEREZ', 'CARLOS-MARTÍNEZ', 'LUISA GOMEZ']
