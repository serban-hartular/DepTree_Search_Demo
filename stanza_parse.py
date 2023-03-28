from __future__ import annotations

from typing import Dict, List, Tuple

import stanza
from stanza.utils.conll import CoNLL
import tree_path as tp

# stanza.download('ro') # download Romanian model
nlp : stanza.Pipeline|None = None
def init_nlp():
    global nlp
    nlp = stanza.Pipeline('ro') # initialize Romanian neural pipeline

def text_to_parsed_doc(text : str, outname : str) -> tp.ParsedDoc:
    global nlp
    if not nlp:
        init_nlp()
    stanza_doc = nlp(text)
    conll_text = CoNLL.doc2conll(stanza_doc)
    conll_text = ['\n'.join(l) for l in conll_text]
    conll_text = '\n\n'.join(conll_text)
    conllu_filename = outname + '.conllu'
    with open(conllu_filename, 'w', encoding='utf-8') as handle:
        handle.write(conll_text + '\n')
    parsed_doc = [d for d in tp.iter_docs_from_conll(conllu_filename, '')]
    if not parsed_doc: raise Exception('Error reloading ' + conllu_filename)
    parsed_doc = parsed_doc[0]
    parsed_doc.to_json_zip(outname + '.jz')
    return parsed_doc

def text_file_to_parsed_doc(infile_name : str, outname : str) -> tp.ParsedDoc:
    with open(infile_name, 'r', encoding='utf-8') as handle:
        text = handle.read()
    return text_to_parsed_doc(text, outname)
