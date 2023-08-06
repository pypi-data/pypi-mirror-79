import json
import pathlib
import os
import os.path

from conceptual.sources.source import Source
from conceptual import Type

class VRD(Source):

    def __init__(self, location):
        super().__init__(location)

    def preprocess(self):
        files = os.listdir(self.relation_path)
        if len(files) > 10:
            self.lexicon += [(k.split(".")[0], Type.Relation) for k in files]
            return

        # Load annotations
        training_data = json.load(open(self.location + "annotations_train.json"))
        preds = json.load(open(self.location + "predicates.json"))

        lex = {}
        self.lexicon = []

        for k, v in training_data.items():
            for rel in v:
                n = {}
                relname = preds[rel['predicate']]
                n['name'] = relname
                n['image_id'] = k
                lm = {}
                tr = {}
                lm['y'] = rel['object']['bbox'][0]
                lm['h'] = rel['object']['bbox'][1] - lm['y']
                lm['x'] = rel['object']['bbox'][2]
                lm['w'] = rel['object']['bbox'][3] - lm['x']

                tr['y'] = rel['subject']['bbox'][0]
                tr['h'] = rel['subject']['bbox'][1] - tr['y']
                tr['x'] = rel['subject']['bbox'][2]
                tr['w'] = rel['subject']['bbox'][3] - tr['x']

                if tr['h'] < 0:
                   old = tr['y']
                   tr['y'] += tr['h']
                   tr['h'] = old

                if lm['h'] < 0:
                   old = lm['y']
                   lm['y'] += lm['h']
                   lm['h'] = old

                n['lm'] = lm
                n['tr'] = tr

                if relname not in lex:
                    lex[relname] = []

                lex[relname].append(n)

        for k in lex.keys():
            self.lexicon += [(k, Type.Relation)]
            with open(self.relation_path + k + ".json", 'w') as f:
                json.dump(lex[k], f)

    def sample_word(self, word, t, k, rng):
        file = open(self.relation_path + word + ".json")
        objs = json.load(file)
        samples = Source._sample_from(rng, objs, k)
        for obj in samples:
            obj['image'] = self.location + 'sg_dataset/sg_train_images/' + obj['image_id']
        return samples
