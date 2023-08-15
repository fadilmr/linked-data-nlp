import spacy
from spacy import displacy
from spacy.util import minibatch, compounding
from spacy.util import decaying
from thinc.api import Adam
import random
from matplotlib import pyplot as plt

def custom_optimizer(optimizer, learn_rate=0.0001, beta1=0.9, beta2=0.999, eps=1e-8, L2=1e-6, max_grad_norm=1.0):
    
    optimizer.learn_rate = learn_rate
    optimizer.beta1 = beta1
    optimizer.beta2 = beta2
    optimizer.eps = eps
    optimizer.L2 = L2
    optimizer.max_grad_norm = max_grad_norm
    
    return optimizer

def train_spacy(data, 
                iterations, 
                learn_rate=0.001, 
                beta1=0.9, 
                beta2=0.999, 
                eps=1e-8, 
                L2=1e-4, 
                max_grad_norm=1.0):
    
    TRAIN_DATA = data
    nlp = spacy.blank('id') 
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner')
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        
        # additional lines
        optimizer = nlp.begin_training()
        # Define decaying dropout
#         dropout = decaying(0.8, 0.2, 1e-6)
        
#         optimizer = nlp.begin_training()
        loss_list = []
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 64.0, 1.001))
            
            for batch in batches:
                texts, annotations = zip(*batch)
                examples = []
                for text, annots in batch:
                    examples.append(spacy.training.Example.from_dict(nlp.make_doc(text), annots))

                nlp.update(examples, sgd=optimizer, drop=0.35, losses=losses)
            
#             for text, annotations in TRAIN_DATA:
#                 nlp.update(
#                     [text],  # batch of texts
#                     [annotations],  # batch of annotations
#                     drop=next(dropout),  # dropout - make it harder to memorise data
#                     sgd=optimizer,  # callable to update weights
#                     losses=losses)

            print(losses)
            loss_list.append(losses)
        
    return nlp, loss_list