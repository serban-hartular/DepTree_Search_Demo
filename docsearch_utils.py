from __future__ import annotations

import os
from typing import List

import tree_path as tp
from tree_path import ParsedDoc, Search, Match
import pyperclip

def excel_safe(text : str) -> str:
    if text and text[0] in ('+-='):
        text = "'" + text  # because of excel
    return text

def display_search_results(doc : ParsedDoc|List[ParsedDoc], search_expr : str):
    doclist = [doc] if isinstance(doc, ParsedDoc) else doc
    copy_text = ''
    for d in doclist:
        for match in d.search(search_expr):
            root : tp.ParsedSentence = match.node.root()
            # header = ['Doc', 'Sentence', 'Match']
            data = [d.doc_id, root.sent_id, match.node.sdata('form')]
            next_nodes = match.next_nodes
            match_count = 2
            while next_nodes:
                data.append(','.join([m.node.sdata('form') for m in next_nodes]))
                # header.append('Match%d' % match_count)
                match_count += 1
                new_next = []
                for m in next_nodes:
                    new_next.extend(m.next_nodes)
                next_nodes = new_next
            sent_text = str(root)
            data.append(sent_text)
            # header.append('Text')
            print('\t'.join(data))
            data = [excel_safe(t) for t in data]
            copy_text += '\t'.join(data) + '\n'
    pyperclip.copy(copy_text)
    
def load_parsed_docs(dir : str = '', skip = ('cancan2020', 'craii')):
    if not dir: dir = './parsed_docs/'
    filenames = os.listdir(dir)
    filenames = [f for f in filenames if f.endswith('.jz')]
    all_docs = []
    for f in filenames:
        var_name = f.rstrip('.jz')
        print(var_name)
        if var_name in skip:
            continue
        fname = dir + f
        print('Loading... ' + fname)
        globals()[var_name] = ParsedDoc.from_json_zip(fname)
        all_docs.append(globals()[var_name])
    print('Done loading')
    globals()['all_docs'] = all_docs
    
