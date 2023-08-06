import _conceptual as c
import _graph as graph

def parse(space, string):
    vocab = space.vocabulary

    detected = [l.id for l in space.objects()]
    objects = [o for (o, t) in vocab if t == c.Type.Object]
    attributes = [o for (o, t) in vocab if t == c.Type.Attribute]
    relations = [o for (o, t) in vocab if t == c.Type.Relation]

    tokens = string.split(" ")
    tokens = [c.Identifier(s) for s in tokens]
    if len(tokens) == 2:
        if (tokens[0] in relations) and ((tokens[1] in objects) or (str(tokens[1]) in detected)):
            return graph.Relation(tokens[0], graph.Object(tokens[1]))

    if len(tokens) == 1:
        if tokens[0] in attributes:
            return graph.Attribute(string[0])

    return None
