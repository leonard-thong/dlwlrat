# -*- coding:utf-8 -*-
"""
===========================================
  @author:  lmy
  @time:    2020/8/19 11:03 PM
  @project: brat
  @file:    spam.py
===========================================
"""
import re
from utils import generate_color_config

def spam_get_entities(text, entity_index):
    entity_list = ['quantity', 'money']
    generate_color_config('spam', entity_list)
    entities = [
        ["T" + str(next(entity_index)), "spam_quantity", [(pos.start(), pos.end())]]
        for pos in re.finditer("million", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "spam_quantity", [(pos.start(), pos.end())]]
            for pos in re.finditer("billion", text)
        ]
    )
    entities.extend(
        [
            ["T" + str(next(entity_index)), "spam_money", [(pos.start(), pos.end())]]
            for pos in re.finditer("(\$([1-9|.]*))|(dollars)", text)
        ]
    )
    return entities


def spam_get_realtions(text):
    pass


def spam(text="", entity_index=None):
    res = dict()
    entities = spam_get_entities(text, entity_index)

    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass