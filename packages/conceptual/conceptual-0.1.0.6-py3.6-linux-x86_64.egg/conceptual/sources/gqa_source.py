import json
import pathlib
import os
import os.path

from conceptual.sources.source import Source
from conceptual import Type

def add(v, k, name):
    v[name] = k
    return v

def set_rel(objs, objs_hash, rel):
    res = []
    counter = 0
    for r in objs:
        for rr in r['relations']:
            if rr['name'] == rel:
                counter += 1
                if counter > 10000:
                    continue
                new_obj = {}
                new_obj['image_id'] = r['image_id']
                new_obj['tr'] = r
                new_obj['lm'] = objs_hash[rr['object']]
                res.append(new_obj)
    return res


class GQA(Source):

    def __init__(self, location):
        super().__init__(location)

    def preprocess(self):
        files = os.listdir(self.attribute_path)
        r_files = os.listdir(self.relation_path)
        if len(files) > 10 and len(r_files) > 10:
            self.lexicon += [(k.split(".")[0], Type.Attribute) for k in files]
            self.lexicon += [(k.split(".")[0], Type.Relation) for k in r_files]
            return

        # Load json graphs
        graphs = open(self.location + "train_sceneGraphs.json").read()
        j = json.loads(graphs)
        imgs = [add(v, k, 'image_id') for k, v in j.items()]
        objs = [add(add(v, k, 'object_id'), o['image_id'], 'image_id') for o in imgs for k, v in o['objects'].items()]
        objs_hash = {o['object_id']: o for o in objs}

        # Process attributes
        attrs = set([a for o in objs for a in o['attributes']])
        res = {a: [o for o in objs if a in o['attributes']] for a in attrs}
        self.lexicon += [(k, Type.Attribute) for k in res.keys()]
        for k in res.keys():
            with open(self.attribute_path + k + ".json", 'w') as f:
                json.dump(res[k], f)

        # Process relations
        rels = set([r['name'] for o in objs for r in o['relations']])
        each_rel = {r: set_rel(objs, objs_hash, r) for r in rels}
        self.lexicon += [(k, Type.Relation) for k in each_rel.keys()]
        for k in each_rel.keys():
            with open(self.relation_path + k + ".json", 'w') as f:
                json.dump(each_rel[k], f)


    def sample_word(self, word, t, k, rng):
        loc = self.location
        if t == Type.Attribute:
            loc = self.attribute_path
        elif t == Type.Relation:
            loc = self.relation_path

        file = open(loc + word + ".json")
        objs = json.load(file)
        samples = Source._sample_from(rng, objs, k)
        for obj in samples:
            obj['image'] = self.location + 'images/' + obj['image_id'] + ".jpg"
        return samples
