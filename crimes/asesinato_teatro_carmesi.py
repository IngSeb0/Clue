"""
asesinato_teatro_carmesi.py — El Asesinato en el Teatro Carmesí

El famoso director de teatro Augusto Valmont fue encontrado muerto en su camerino durante el estreno de su última obra.
La causa de muerte fue un disparo con un revólver antiguo que pertenecía a la colección de utilería del teatro.
Sofía, la actriz principal, fue vista discutiendo acaloradamente con Augusto una hora antes del crimen.
Las huellas dactilares de Sofía están en el revólver que causó la muerte.
Lorenzo, el productor, estaba en el escenario dando un discurso frente a 200 personas durante el momento exacto del disparo.
El escenario está en el extremo opuesto del teatro respecto a los camerinos; es imposible estar en ambos lugares simultáneamente.
Catalina, la asistente de dirección, declara que vio a Sofía salir del camerino de Augusto minutos antes del disparo.
Diego, el técnico de luces, afirma que Sofía estuvo con él en la cabina de control durante toda la noche.
Sofía declara que Diego estuvo con ella en la cabina de control durante toda la noche.
Diego tiene antecedentes de falsificar documentos y mentir bajo juramento.
Catalina es conocida por su honestidad impecable y nunca ha mentido en sus 20 años de carrera.

Como detective, he llegado a las siguientes conclusiones:
Quien estaba frente a múltiples testigos en un lugar alejado durante el crimen tiene una coartada sólida.
Quien tiene coartada sólida está completamente descartado como culpable.
Quien tiene huellas en el arma del crimen tiene evidencia física en su contra.
Un testigo con reputación de honestidad impecable es un testigo confiable.
Si un testigo confiable vio a alguien en la escena del crimen, esa persona estuvo presente en la escena.
Quien tiene evidencia física en su contra y estuvo presente en la escena es el principal sospechoso.
Quien da coartada a un principal sospechoso y tiene antecedentes de mentir es un cómplice potencial.
Si dos personas se dan coartada mutuamente y una tiene antecedentes de mentir, existe una conspiración entre ellas.
Quien es principal sospechoso y tiene un cómplice potencial es culpable del crimen.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    sofia = Term("sofia")
    lorenzo = Term("lorenzo")
    catalina = Term("catalina")
    diego = Term("diego")
    augusto = Term("augusto")
    revolver = Term("revolver")
    camerino = Term("camerino")
    escenario = Term("escenario")
    cabina_control = Term("cabina_control")

    # === HECHOS DEL CASO ===
    
    # Hechos sobre la víctima y el arma
    kb.add_fact(Predicate("victima", (augusto,)))
    kb.add_fact(Predicate("arma_del_crimen", (revolver,)))
    kb.add_fact(Predicate("escena_del_crimen", (camerino,)))
    
    # Evidencia física
    kb.add_fact(Predicate("huellas_en_arma", (sofia, revolver)))
    kb.add_fact(Predicate("discusion_con_victima", (sofia, augusto)))
    
    # Coartadas y ubicaciones
    kb.add_fact(Predicate("frente_a_multiples_testigos", (lorenzo, escenario)))
    kb.add_fact(Predicate("lugar_alejado", (escenario, camerino)))
    
    # Testimonios
    kb.add_fact(Predicate("vio_en_escena", (catalina, sofia, camerino)))
    kb.add_fact(Predicate("reputacion_honesta", (catalina,)))
    
    # Coartadas cruzadas
    kb.add_fact(Predicate("da_coartada", (diego, sofia)))
    kb.add_fact(Predicate("da_coartada", (sofia, diego)))
    
    # Antecedentes
    kb.add_fact(Predicate("antecedentes_mentir", (diego,)))

    # === REGLAS DE INFERENCIA ===
    
    # Regla 1: frente_a_multiples_testigos(X,Y) ∧ lugar_alejado(Y,Z) → coartada_solida(X)
    kb.add_rule(Rule(
        Predicate("coartada_solida", (Term("$X"),)),
        [
            Predicate("frente_a_multiples_testigos", (Term("$X"), Term("$Y"))),
            Predicate("lugar_alejado", (Term("$Y"), Term("$Z")))
        ]
    ))
    
    # Regla 2: coartada_solida(X) → descartado(X)
    kb.add_rule(Rule(
        Predicate("descartado", (Term("$X"),)),
        [Predicate("coartada_solida", (Term("$X"),))]
    ))
    
    # Regla 3: huellas_en_arma(X,Y) → evidencia_fisica(X)
    kb.add_rule(Rule(
        Predicate("evidencia_fisica", (Term("$X"),)),
        [Predicate("huellas_en_arma", (Term("$X"), Term("$Y")))]
    ))
    
    # Regla 4: reputacion_honesta(X) → testigo_confiable(X)
    kb.add_rule(Rule(
        Predicate("testigo_confiable", (Term("$X"),)),
        [Predicate("reputacion_honesta", (Term("$X"),))]
    ))
    
    # Regla 5: testigo_confiable(X) ∧ vio_en_escena(X,Y,Z) → presente_en_escena(Y,Z)
    kb.add_rule(Rule(
        Predicate("presente_en_escena", (Term("$Y"), Term("$Z"))),
        [
            Predicate("testigo_confiable", (Term("$X"),)),
            Predicate("vio_en_escena", (Term("$X"), Term("$Y"), Term("$Z")))
        ]
    ))
    
    # Regla 6: evidencia_fisica(X) ∧ presente_en_escena(X,Y) → principal_sospechoso(X)
    kb.add_rule(Rule(
        Predicate("principal_sospechoso", (Term("$X"),)),
        [
            Predicate("evidencia_fisica", (Term("$X"),)),
            Predicate("presente_en_escena", (Term("$X"), Term("$Y")))
        ]
    ))
    
    # Regla 7: da_coartada(X,Y) ∧ principal_sospechoso(Y) ∧ antecedentes_mentir(X) → complice_potencial(X)
    kb.add_rule(Rule(
        Predicate("complice_potencial", (Term("$X"),)),
        [
            Predicate("da_coartada", (Term("$X"), Term("$Y"))),
            Predicate("principal_sospechoso", (Term("$Y"),)),
            Predicate("antecedentes_mentir", (Term("$X"),))
        ]
    ))
    
    # Regla 8: da_coartada(X,Y) ∧ da_coartada(Y,X) ∧ antecedentes_mentir(X) → conspiracion(X,Y)
    kb.add_rule(Rule(
        Predicate("conspiracion", (Term("$X"), Term("$Y"))),
        [
            Predicate("da_coartada", (Term("$X"), Term("$Y"))),
            Predicate("da_coartada", (Term("$Y"), Term("$X"))),
            Predicate("antecedentes_mentir", (Term("$X"),))
        ]
    ))
    
    # Regla 9: principal_sospechoso(X) ∧ complice_potencial(Y) → culpable(X)
    kb.add_rule(Rule(
        Predicate("culpable", (Term("$X"),)),
        [
            Predicate("principal_sospechoso", (Term("$X"),)),
            Predicate("complice_potencial", (Term("$Y"),))
        ]
    ))

    return kb


CASE = CrimeCase(
    id="asesinato_teatro_carmesi",
    title="El Asesinato en el Teatro Carmesí",
    suspects=("sofia", "lorenzo", "catalina", "diego"),
    narrative=__doc__,
    description=(
        "El director Augusto Valmont fue asesinado en su camerino durante el estreno. "
        "Sofía tiene sus huellas en el arma y fue vista en la escena. Lorenzo tiene coartada sólida. "
        "Diego, con antecedentes de mentir, da coartada a Sofía. Catalina, testigo confiable, "
        "vio a Sofía salir del camerino. Resuelve quién es el culpable usando backward chaining."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Lorenzo está descartado como culpable?",
            goal=Predicate("descartado", (Term("lorenzo"),)),
        ),
        QuerySpec(
            description="¿Catalina es un testigo confiable?",
            goal=Predicate("testigo_confiable", (Term("catalina"),)),
        ),
        QuerySpec(
            description="¿Sofía estuvo presente en la escena del crimen?",
            goal=Predicate("presente_en_escena", (Term("sofia"), Term("camerino"))),
        ),
        QuerySpec(
            description="¿Sofía es la principal sospechosa?",
            goal=Predicate("principal_sospechoso", (Term("sofia"),)),
        ),
        QuerySpec(
            description="¿Diego es un cómplice potencial?",
            goal=Predicate("complice_potencial", (Term("diego"),)),
        ),
        QuerySpec(
            description="¿Sofía es culpable del asesinato?",
            goal=Predicate("culpable", (Term("sofia"),)),
        ),
        QuerySpec(
            description="¿Existe alguien que conspire con Sofía?",
            goal=ExistsGoal("$X", Predicate("conspiracion", (Term("$X"), Term("sofia")))),
        ),
        QuerySpec(
            description="¿Todos los que dan coartada a Sofía tienen antecedentes de mentir?",
            goal=ForallGoal(
                "$X",
                Predicate("da_coartada", (Term("$X"), Term("sofia"))),
                Predicate("antecedentes_mentir", (Term("$X"),))
            ),
        ),
    ),
)
