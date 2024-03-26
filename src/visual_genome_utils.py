from annotated_types import Predicate

import neumann
import neumann.fol.logic as logic
from neumann.fol.language import DataType, Language
from neumann.fol.logic import Const


def scene_graph_to_language(scene_graph, text, logic_generator, num_objects=2):
    """Extract a FOL language out of a scene graph to parse rules with later."""
    objects = list(set([str(obj).replace(" ", "") for obj in scene_graph.objects]))
    datatype = DataType("type")
    # obj_datatype = DataType("object")
    constants = [Const(obj, datatype) for obj in objects]

    # # put object constants first
    # const_response = "Constants:\nobject:"
    # for i in range(num_objects):
    #     const_response += "obj{}".format(i)
    #     const_response += ","
    # const_response = const_response[:-1]
    # # prepare type constants
    # const_response += "\ntype:"

    const_response = "Constants:\ntype:"
    for obj in objects:
        const_response += obj
        const_response += ","
    const_response = const_response[:-1]

    # predicates are generated by LLMs because we want to omit inrelevant predicates in the scene graph
    # extracting predicates that appear in the prompt
    predicates, pred_response = logic_generator.generate_predicates(
        text, const_response
    )
    print("Predicate generator response:\n    {}".format(pred_response))
    lang = Language(consts=list(set(constants)), preds=list(set(predicates)), funcs=[])
    return lang


def get_init_language_with_sgg(scene_graph, text, logic_generator):
    """Extract a FOL language out of a predicted scene graph to parse rules with later."""
    objects = list(set([rel["o_str"] for rel in scene_graph]))
    subjects = list(set([rel["s_str"] for rel in scene_graph]))
    datatype = DataType("type")
    constants = [Const(obj, datatype) for obj in objects + subjects]

    const_response = "Constants:\ntype:"
    for obj in objects:
        const_response += obj
        const_response += ","
    const_response = const_response[:-1]

    # predicates are generated by LLMs because we want to omit inrelevant predicates in the scene graph
    # extracting predicates that appear in the prompt
    predicates, pred_response = logic_generator.generate_predicates(
        text, const_response
    )
    print("Predicate generator response:\n    {}".format(pred_response))
    lang = Language(consts=list(set(constants)), preds=list(set(predicates)), funcs=[])
    return lang


def scene_graph_to_language_with_sgg(scene_graph):
    """Extract a complete FOL language out of a scene graph to be used by the semantic unifier."""
    objects = list(set([rel["o_str"] for rel in scene_graph]))
    subjects = list(set([rel["s_str"] for rel in scene_graph]))
    rels = list(set([rel["p_str"] for rel in scene_graph]))
    datatype = DataType("type")
    obj_datatype = DataType("object")
    constants = [Const(obj, datatype) for obj in objects + subjects]

    predicates = [
        logic.Predicate(p.replace(" ", "_").lower(), 2, [obj_datatype, obj_datatype])
        for p in rels
    ]

    lang = Language(consts=list(set(constants)), preds=list(set(predicates)), funcs=[])
    return lang


def objdata_to_box(data):
    x = data["x"]
    y = data["y"]
    w = data["w"]
    h = data["h"]
    return x, y, w, h
