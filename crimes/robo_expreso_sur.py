"""
robo_expreso_sur.py — El Robo en el Expreso del Sur

El collar de esmeraldas de la Marquesa desapareció del vagón privado del tren nocturno.
Elena fue vista en el vagón privado durante el robo; sus huellas están en el estuche de joyas.
Don Rodrigo fue grabado por la cámara de seguridad en el vagón de equipaje durante toda la noche.
El vagón de equipaje es el extremo opuesto al vagón privado; es imposible haber estado en ambos a la vez.
La Marquesa es la víctima directa del robo y presenció el incidente.
La Marquesa acusa a Elena.
Victor declara que Elena estuvo con él en el vagón comedor toda la noche.
Elena declara que Victor estuvo con ella en el vagón comedor toda la noche.

Como detective, he llegado a las siguientes conclusiones:
Quien fue grabado en cámara en un lugar alejado de la escena durante el crimen está descartado.
La víctima del crimen no tiene razón para mentir; es testigo imparcial.
La acusación de un testigo imparcial es creíble.
Quien estaba en la escena y es acusado de forma creíble es culpable.
Quien da coartada a un culpable lo está defendiendo.
Si dos personas se dan coartada mutuamente, tienen una alianza de coartadas entre sí.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    elena          = Term("elena")
    victor         = Term("victor")
    don_rodrigo    = Term("don_rodrigo")
    marquesa       = Term("marquesa")
    estuche_joyas  = Term("estuche_joyas")
    vagon_equipaje = Term("vagon_equipaje")
    vagon_privado  = Term("vagon_privado")

    # === YOUR CODE HERE ===

    kb.add_fact(Predicate("grabado_en_camara", (don_rodrigo,vagon_equipaje)))
    kb.add_fact(Predicate("lugar_alejado_escena", (vagon_equipaje, vagon_privado)))
    kb.add_fact(Predicate("vista_en_escena", (elena, vagon_privado)))
    kb.add_fact(Predicate("huellas_en_objeto", (elena, estuche_joyas)))
    kb.add_fact(Predicate("victima_del_crimen", (marquesa,)))
    kb.add_fact(Predicate("acusa", (marquesa,elena)))
    kb.add_fact(Predicate("da_coartada", (victor,elena)))
    kb.add_fact(Predicate("da_coartada", (elena, victor)))

    # grabado_en_camara(X,Y) ∧ lugar_alejado_escena(Y,Z) -> descartado(X)
    kb.add_rule(Rule(
        Predicate("descartado", (Term("$X"),)),
        [
            Predicate("grabado_en_camara", (Term("$X"), Term("$Y"))),
            Predicate("lugar_alejado_escena", (Term("$Y"), vagon_privado))
        ]
    ))

    # victima_del_crimen(X) -> testigo_imparcial(X)
    kb.add_rule(Rule(
        Predicate("testigo_imparcial", (Term("$X"),)),
        [Predicate("victima_del_crimen", (Term("$X")))]
    ))

    #testigo_imparcial(X) ∧ acusa(X,Y) -> acusacion_creible(X,Y)
    kb.add_rule(Rule(
        Predicate("acusasion_creible", (Term("$X"), Term("$Y"))),
        [
            Predicate("testigo_imparcial", (Term("$X"),)),
            Predicate("acusa", (Term("$X"), Term("$Y")))
        ]
    ))

    # vista_en_escena(X,Y) ∧ acusacion_creible(Z,X) -> culpable(X)
    kb.add_rule(Rule(
        Predicate("culpable", (Term("$X"),)),
        [
            Predicate("vista_en_escena", (Term("$X"), Term("$Y"))),
            Predicate("acusacion_creible", (Term("$Z"), Term("$X")))
        ]
    ))

    # da_coartada(X,Y) ∧ culpable(Y) -> defiende_al_culpable(X)
    kb.add_rule(Rule(
        Predicate("defiende_al_culpable", (Term("$X"),)),
        [
            Predicate("culpable", (Term("$Y"),)),
            Predicate("da_coartada", (Term("$X"), Term("%Y")))
        ]
    ))

    # da_coartada(X,Y) ∧ da_coartada(Y,X) -> alianza_coartadas(X,Y)
    kb.add_rule(Rule(
        Predicate("alianza_coartadas", (Term("$X"), Term("$Y"))),
        [
            Predicate("da_coartada", (Term("$X"), Term("$Y"))),
            Predicate("de_coartada", (Term("$Y"), Term("$X")))
        ]
    ))


    # === END YOUR CODE ===

    return kb


CASE = CrimeCase(
    id="robo_expreso_sur",
    title="El Robo en el Expreso del Sur",
    suspects=("elena", "victor", "don_rodrigo"),
    narrative=__doc__,
    description=(
        "El collar de la Marquesa desapareció en un tren nocturno. "
        "Don Rodrigo tiene coartada de cámara. Elena estaba en la escena con huellas en el estuche. "
        "La víctima la acusa. Victor y Elena se cubren mutuamente."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Don Rodrigo está descartado?",
            goal=Predicate("descartado", (Term("don_rodrigo"),)),
        ),
        QuerySpec(
            description="¿La acusación de la Marquesa contra Elena es creíble?",
            goal=Predicate("acusacion_creible", (Term("marquesa"), Term("elena"))),
        ),
        QuerySpec(
            description="¿Elena es culpable?",
            goal=Predicate("culpable", (Term("elena"),)),
        ),
        QuerySpec(
            description="¿Victor defiende al culpable?",
            goal=Predicate("defiende_al_culpable", (Term("victor"),)),
        ),
        QuerySpec(
            description="¿Existe alianza de coartadas entre Elena y Victor?",
            goal=ExistsGoal("$X", Predicate("alianza_coartadas", (Term("$X"), Term("victor")))),
        ),
    ),
)
