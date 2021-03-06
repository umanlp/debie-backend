import json
import logging

from flask import jsonify

import JSONFormatter
import calculation
from debiasing import bam, gbdd


# Debiasing with full vector size, computes the results with the selected models
def return_full_debiasing(models, arguments, content):
    logging.info("APP-DE: Forwarding to related definitions")
    database = 'fasttext'
    augment_flag = 'false'
    vector_flag = 'false'
    if 'space' in arguments.keys():
        database = arguments['space']
    if 'augments' in arguments.keys():
        augment_flag = arguments['augments']
    if 'vectors' in arguments.keys():
        vector_flag = arguments['vectors']
    if vector_flag == 'false':
        target1, target2, attr1, attr2, augments1, augments2, augments3, augments4 = JSONFormatter.retrieve_vectors_debiasing(
            content, database, augment_flag)
    else:
        target1, target2, attr1, attr2, augments1, augments2, augments3, augments4 = JSONFormatter.retrieve_vectors_from_json_debiasing(
            content)
    target1, target2 = calculation.check_sizes(target1, target2)
    attr1, attr2 = calculation.check_sizes(attr1, attr2)
    logging.info("APP: Final retrieved set sizes: T1=" + str(len(target1)) + " T2=" + str(len(target2)) + " A1=" + str(
        len(attr1)) + " A2=" + str(len(attr2)))
    if len(target1) == 0 or len(target2) == 0 or len(attr1) == 0 or len(attr2) == 0:
        logging.info("APP: Stopped, no values found in database")
        return jsonify(message="ERROR: No values found in database."), 404
    logging.info("APP: Debiasing process started")
    res1, res2, res3, res4 = {}, {}, {}, {}
    try:
        if models is None:
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
        if models == 'gbdd':
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
        if models == 'bam':
            res1, res2, res3, res4 = bam.bias_alignment_model(target1, target2, attr1, attr2, augments1, augments2,
                                                              augments3, augments4)
        if models == 'gbddxbam':
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
            res1, res2, res3, res4 = bam.bias_alignment_model(res1, res2, res3, res4, augments1, augments2, augments3,
                                                              augments4)
        if models == 'bamxgbdd':
            res1, res2, res3, res4 = bam.bias_alignment_model(target1, target2, attr1, attr2, augments1, augments2,
                                                              augments3, augments4)
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(res1, res2, res3, res4, augments1,
                                                                               augments2, augments3, augments4)
        biased_terms = calculation.concatenate_dicts(target1, target2, attr1, attr2)
        debiased_terms = calculation.concatenate_dicts(res1, res2, res3, res4)
        response = json.dumps(
            {"EmbeddingSpace": database, "Model": models,
             "BiasedVecs:": JSONFormatter.dict_to_json(biased_terms),
             "DebiasedVecs": JSONFormatter.dict_to_json(debiased_terms)})
    except:
        return jsonify(message="DEBIASING ERROR"), 500
    logging.info("APP: Debiasing process finished")
    return response, 200


# Debiasing with compressed vector size, computes the results with the selected models and a PCA
def return_pca_debiasing(models, arguments, content):
    logging.info("APP-DE: Forwarding to related definitions")
    database = arguments['space']
    augment_flag = arguments['augments']
    target1, target2, attr1, attr2, augments1, augments2, augments3, augments4 = JSONFormatter.retrieve_vectors_debiasing(
        content, database,
        augment_flag)
    target1, target2 = calculation.check_sizes(target1, target2)
    attr1, attr2 = calculation.check_sizes(attr1, attr2)
    logging.info("APP: Final retrieved set sizes: T1=" + str(len(target1)) + " T2=" + str(len(target2)) + " A1=" + str(
        len(attr1)) + " A2=" + str(len(attr2)))
    if len(target1) == 0 or len(target2) == 0 or len(attr1) == 0 or len(attr2) == 0:
        logging.info("APP: Stopped, no values found in database")
        return jsonify(message="ERROR: No values found in database."), 404
    logging.info("APP: Debiasing process started")
    res1, res2, res3, res4 = {}, {}, {}, {}
    try:
        if models is None:
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
        if models == 'gbdd':
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
        if models == 'bam':
            res1, res2, res3, res4 = bam.bias_alignment_model(target1, target2, attr1, attr2, augments1, augments2,
                                                              augments3, augments4)
        if models == 'gbddxbam':
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(target1, target2, attr1, attr2,
                                                                               augments1, augments2, augments3,
                                                                               augments4)
            res1, res2, res3, res4 = bam.bias_alignment_model(res1, res2, res3, res4, augments1, augments2, augments3,
                                                              augments4)
        if models == 'bamxgbdd':
            res1, res2, res3, res4 = bam.bias_alignment_model(target1, target2, attr1, attr2, augments1, augments2,
                                                              augments3, augments4)
            res1, res2, res3, res4 = gbdd.generalized_bias_direction_debiasing(res1, res2, res3, res4, augments1,
                                                                               augments2, augments3, augments4)
        target1_copy, target2_copy = calculation.create_duplicates(target1, target2)
        attr1_copy, attr2_copy = calculation.create_duplicates(attr1, attr2)
        res1_copy, res2_copy, res3_copy, res4_copy = calculation.create_duplicates(res1, res2, res3, res4)
        biased_terms = calculation.concatenate_dicts(target1_copy, target2_copy, attr1_copy, attr2_copy)
        debiased_terms = calculation.concatenate_dicts(res1_copy, res2_copy, res3_copy, res4_copy)
        biased_pca = calculation.principal_componant_analysis(target1, target2, attr1, attr2)
        debiased_pca = calculation.principal_componant_analysis(res1, res2, res3, res4)
        response = json.dumps(
            {"EmbeddingSpace": database, "Model": models,
             "BiasedVectorsPCA": JSONFormatter.dict_to_json(biased_pca),
             "DebiasedVectorsPCA": JSONFormatter.dict_to_json(debiased_pca),
             "BiasedVecs:": JSONFormatter.dict_to_json(biased_terms),
             "DebiasedVecs": JSONFormatter.dict_to_json(debiased_terms)})
    except:
        return jsonify(message="DEBIASING ERROR"), 500
    logging.info("APP: Debiasing process finished")
    return response, 200
