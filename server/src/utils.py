import random
import os
import hashlib
import time

from annotation import Annotations
from expandLogger import Logger
from tokenise import whitespace_token_boundary_gen

GLOBAL_LOGGER = Logger()

def generate_color_config(name, entities):
    md5_obj = hashlib.md5()
    entity_color_items = []
    for entity in entities:
        md5_obj.update("{}_{}".format(name, entity).encode('utf-8'))
        hash_code = md5_obj.hexdigest()
        color = '#{}'.format(str(hash_code)[0:6])
        color = list(color)
        for i in range(1, 6, 2):
            if '7' >= color[i] >= '0':
                color[i] = str(hex(int(color[i]) + 8)).replace('0x', '') 
        color = ''.join(color)
        entity_color_items.append('\n{}_{}\tbgColor:{}'.format(name, entity, color))
    entity_color_items.append('\n{}_unlabeled\tbgColor:#000000'.format(name))
    if not os.path.exists('./data/visualConfigs/drawings.conf'):
        with open('./data/visualConfigs/drawings.conf', 'w') as color_config:
            with open('./data/visualConfigs/drawing.conf', 'r') as drawing_content:
                color_config.write(drawing_content.read())
                color_config.write(''.join(entity_color_items))
    else:
       with open('./data/visualConfigs/drawings.conf', 'a') as color_config:
            color_config.write(''.join(entity_color_items)) 
    os.system('sh ./data/build_visual_conf.sh')

def get_entity_index():
    index = 0
    while 1:
        index += 1
        yield index


def get_entity_index_exist(indexNo):
    index = indexNo
    while 1:
        index += 1
        yield index

def clean_cached_config():
    os.system('rm ./data/visualConfigs/drawings.conf')

def add_common_info(text, res):
    res["text"] = text
    res["token_offsets"] = [o for o in whitespace_token_boundary_gen(text)]
    res["ctime"] = time.time()
    res["source_files"] = ["ann", "txt"]
    return res

def get_entity_index_exist(indexNo):
    index = indexNo
    while 1:
        index += 1
        yield index

def annotation_file_generate(res, file_path, text, mode='w'):
    anno_content = ""
    for entity in res["entities"]:
        anno_content += (
            str(entity[0])
            + "\t"
            + str(entity[1])
            + " "
            + str(entity[2][0][0])
            + " "
            + str(entity[2][0][1])
            + "\t"
            + str(text[entity[2][0][0]: entity[2][0][1]])
            + "\n"
        )
    with open(file_path, mode) as f:
        f.write(anno_content)

def fetch_all_annotations(**kwargs):
    collection = kwargs['collection']
    document = kwargs['document']
    res = dict()
    res['entities'] = merge_ann_files(collection, document)
    txt_file_path = "data" + collection + '/' + document + '.txt'
    with open(txt_file_path, 'r') as f:
        txt = f.read()
        res = add_common_info(txt, res)
    return res

def parse_annotation_file(ann_path):
    anns = Annotations(document=ann_path[:-4])
    anns._parse_ann_file()
    return anns._lines

def merge_ann_files(collection, document):
    file_path = "data" + collection + '/' + document
    manual_anno_file_path = file_path + ".ann"
    label_function_anno_file_path = file_path + "_func.ann"
    if not os.path.exists(label_function_anno_file_path):
        os.system("touch " + label_function_anno_file_path)
    label_func_anno = parse_annotation_file(label_function_anno_file_path)
    label_func_entities = []
    for ann in label_func_anno:
        try:
            if ann:
                label_func_entities.append([ann.id, ann.type, ann.spans])
        except AttributeError:
            pass
    manual_anno = parse_annotation_file(manual_anno_file_path)
    manual_entities = []
    for ann in manual_anno:
        try:
            if ann:
                manual_entities.append([ann.id, ann.type, ann.spans])
        except AttributeError:
            pass
    ann_entities = []
    ann_entities.extend(manual_entities)
    ann_entities.extend(label_func_entities)
    return ann_entities
    
if __name__ == "__main__":
    merge_ann_files('/Local', 'test')