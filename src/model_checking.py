"""
model_checking.py

Este modulo contiene las funciones de model checking proposicional.

Hint: Usa las funciones get_atoms() y evaluate() de logic_core.py.
"""

from __future__ import annotations

from src.logic_core import Formula


def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
    """
    Genera todos los modelos posibles (asignaciones de verdad).
    Para n atomos, genera 2^n modelos.

    Args:
        atoms: Conjunto de nombres de atomos proposicionales.

    Returns:
        Lista de diccionarios, cada uno mapeando atomos a valores booleanos.

    Ejemplo:
        >>> get_all_models({'p', 'q'})
        [{'p': True, 'q': True}, {'p': True, 'q': False},
         {'p': False, 'q': True}, {'p': False, 'q': False}]

    Hint: Piensa en como representar los numeros del 0 al 2^n - 1 en binario.
          Cada bit corresponde al valor de verdad de un atomo.
    """
    atom_list = sorted(atoms)
    num_atoms = len(atom_list)
    total_models = 2**num_atoms

    models: list[dict[str, bool]] = []

    for number in range(total_models):
        model: dict[str, bool] = {}

        for index, atom in enumerate(atom_list):
            # Bit mas significativo para el primer atomo,
            # para mantener una salida estable y legible.
            shift = num_atoms - 1 - index
            bit = (number >> shift) & 1
            model[atom] = bit == 1

        models.append(model)

    return models


def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
    """
    Determina si una formula es satisfacible.

    Args:
        formula: Formula logica a verificar.

    Returns:
        (True, modelo) si encuentra un modelo que la satisface.
        (False, None) si es insatisfacible.

    Ejemplo:
        >>> check_satisfiable(And(Atom('p'), Not(Atom('p'))))
        (False, None)

    Hint: Genera todos los modelos con get_all_models(), luego evalua
          la formula en cada uno usando evaluate().
    """
    atoms = set(formula.get_atoms())
    models = get_all_models(atoms)

    for model in models:
        if formula.evaluate(model):
            return True, model

    return False, None


def check_valid(formula: Formula) -> bool:
    """
    Determina si una formula es una tautologia (valida en todo modelo).

    Args:
        formula: Formula logica a verificar.

    Returns:
        True si la formula es verdadera en todos los modelos posibles.

    Ejemplo:
        >>> check_valid(Or(Atom('p'), Not(Atom('p'))))
        True

    Hint: Una formula es valida si y solo si su negacion es insatisfacible.
          Alternativamente, verifica que sea verdadera en TODOS los modelos.
    """
    atoms = set(formula.get_atoms())
    models = get_all_models(atoms)

    for model in models:
        if not formula.evaluate(model):
            return False

    return True


def check_entailment(kb: list[Formula], query: Formula) -> bool:
    """
    Determina si KB |= query (la base de conocimiento implica la consulta).

    Args:
        kb: Lista de formulas que forman la base de conocimiento.
        query: Formula que queremos verificar si se sigue de la KB.

    Returns:
        True si la query es verdadera en todos los modelos donde la KB es verdadera.

    Ejemplo:
        >>> kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
        >>> check_entailment(kb, Atom('q'))
        True

    Hint: KB |= q  si y solo si  KB ^ ~q es insatisfacible.
          Es decir, no existe un modelo donde toda la KB sea verdadera
          y la query sea falsa.
    """
    atoms: set[str] = set(query.get_atoms())
    for formula in kb:
        atoms.update(formula.get_atoms())

    models = get_all_models(atoms)

    for model in models:
        kb_true = True
        for formula in kb:
            if not formula.evaluate(model):
                kb_true = False
                break

        # Solo revisamos la query en modelos donde KB es verdadera.
        if kb_true and not query.evaluate(model):
            return False

    return True


def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de una formula.

    Args:
        formula: Formula logica.

    Returns:
        Lista de tuplas (modelo, resultado) para cada modelo posible.

    Ejemplo:
        >>> truth_table(And(Atom('p'), Atom('q')))
        [({'p': True, 'q': True}, True),
         ({'p': True, 'q': False}, False),
         ({'p': False, 'q': True}, False),
         ({'p': False, 'q': False}, False)]

    Hint: Combina get_all_models() y evaluate().
    """
    atoms = set(formula.get_atoms())
    models = get_all_models(atoms)

    table: list[tuple[dict[str, bool], bool]] = []
    for model in models:
        result = formula.evaluate(model)
        table.append((model, result))

    return table
