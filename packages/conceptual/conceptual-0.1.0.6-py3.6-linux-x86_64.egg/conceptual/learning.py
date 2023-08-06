import cv2
import _conceptual as c


def _train_attr(space, word, obj):
    vocab = space.vocabulary
    dims = [o for (o, t) in vocab if t == c.Type.Dimension]

    if 'image' in obj:
        mat = cv2.imread(obj['image'])
        space.update(mat)

    space.addTrainingData(word, dims, obj['x'], obj['y'], obj['w'], obj['h'])

def learn_attr(space, word, obj):
    _train_attr(space,word, obj)
    space.learnGaussian(word, c.Type.Attribute)


def learn_attr_batch(space, word, objs):
    for o in objs:
        _train_attr(space, word, o)
    space.learnGaussian(word, c.Type.Attribute)

def _train_rel(space, word, obj):
    vocab = space.vocabulary
    dims = [o for (o, t) in vocab if t == c.Type.Dimension]
    aug_dims = space.augment(dims)

    if 'image' in obj:
        mat = cv2.imread(obj['image'])
        space.update(mat)

    lm = obj['lm']
    space.attend(lm['x'], lm['y'], lm['w'], lm['h'])

    tr = obj['tr']
    space.addTrainingData(word, aug_dims, tr['x'], tr['y'], tr['w'], tr['h'])

def learn_rel(space, word, obj):
    _train_rel(space, word, obj)
    space.learnGaussian(word, c.Type.Relation)

def learn_rel_batch(space, word, objs):
    for o in objs:
        _train_rel(space, word, o)
    space.learnGaussian(word, c.Type.Relation)
