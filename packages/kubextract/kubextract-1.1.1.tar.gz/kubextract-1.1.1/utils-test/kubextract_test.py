from utils.kubextract import FrameGenerator
import ruamel.yaml as yaml
import pytest
import click
import time
import os
import re

def load_data():
    params = {
        'location': 'gen-frame',
        'gitlab_pers_token': 'foo',
        'workchat_id': 'bar',
        'workchat_type': 'user',
        'pipe_name': 'test',
        'pipe_desc': 'test aja',
        'exp_name': 'test',
        'exp_desc': 'test aja',
        'node_key': 'test',
        'node_val': 'aja',
        'use_gpu': 'true',
        'n_comps': 2
    }

    params['pipeline_path'] = "%s/%s/utils/pipeline.py" % (os.getcwd(), params['location'])
    params['watcher_path'] = "%s/%s/utils/watcher.py" % (os.getcwd(), params['location'])
    params['ci_path'] = "%s/%s/.gitlab-ci.yml" % (os.getcwd(), params['location'])

    for i in range(1, int(params['n_comps'])+1):
        params['comp_name_%i' % i] = 'test %i' % i
        params['comp_desc_%i' % i] = 'test aja %i' % i

        comp_name = params['comp_name_%i' % i]
        params['comp_name_%i' % i] = comp_name.replace(' ', '_')

        params['comp_%i_ci_path' % i] = "%s/%s/%s/_gitlab-ci.yml" % (
            os.getcwd(), params['location'], params['comp_name_%i' % i])
        params['comp_%i_cb_path' % i] = "%s/%s/%s/cloudbuild.yaml" % (
            os.getcwd(), params['location'], params['comp_name_%i' % i])

    return params

params = load_data()

def test_generate_framework():
    if not os.path.exists(params['location']):
        os.makedirs(params['location'])

    gen = FrameGenerator(params)

    with click.progressbar(gen.steps, bar_template='%(label)s [%(bar)s] %(info)s',
                           label='Generate framework to %s' % params['location']) as bar:
        for step, filepath in bar:
            time.sleep(0.5)
            gen.main(step, filepath)

    assert os.path.exists(params['pipeline_path']) == True
    assert os.path.exists(params['watcher_path']) == True
    assert os.path.exists(params['ci_path']) == True

    for i in range(1, int(params['n_comps'])+1):
        assert os.path.exists(params['comp_%i_ci_path' % i]) == True
        assert os.path.exists(params['comp_%i_cb_path' % i]) == True

# @pytest.mark.dependency(depends=["generate_framework"])
def test_check_ci_env():
    with open(params['ci_path'], 'r') as rfile:
        data = yaml.safe_load(rfile.read())

    assert data['variables']['GITLAB_PERS_TOKEN'] == params['gitlab_pers_token']
    assert data['variables']['WORKCHAT_ID'] == params['workchat_id']
    assert data['variables']['WORKCHAT_TYPE'] == params['workchat_type']
    assert data['variables']['PIPE_NAME'] == params['pipe_name']
    assert data['variables']['PIPE_DESC'] == params['pipe_desc']
    assert data['variables']['EXP_NAME'] == params['exp_name']
    assert data['variables']['EXP_DESC'] == params['exp_desc']
    assert data['variables']['NODE_KEY'] == params['node_key']
    assert data['variables']['NODE_VAL'] == params['node_val']
    assert data['variables']['USE_GPU'] == bool(params['use_gpu'])

    for i in range(1, int(params['n_comps'])+1):
        regexp_name = re.compile(params['comp_name_%i' % i])
        regexp_desc = re.compile(params['comp_desc_%i' % i])

        img_name_check = bool(regexp_name.search(data['variables']['IMG_NAME_%i' % i]))
        local_src_check = bool(regexp_name.search(data['variables']['LOCAL_SRC_%i' % i]))
        cloudbuild_check = bool(regexp_name.search(data['variables']['CLOUDBUILD_%i' % i]))
        comp_check = bool(regexp_desc.search(data['variables']['COMPONENTS']))
        ci_include_check = bool(regexp_name.search(str(data['include'])))

        assert img_name_check == True
        assert local_src_check == True
        assert cloudbuild_check == True
        assert comp_check == True
        assert ci_include_check == True

# @pytest.mark.dependency(depends=["generate_framework"])
def test_check_comp_ci_env():
    for i in range(1, int(params['n_comps'])+1):
        with open(params['comp_%i_ci_path' % i], 'r') as rfile:
            data = yaml.safe_load(rfile.read())

        regexp_cb = re.compile("CLOUDBUILD_%i" % i)
        regexp_img = re.compile("IMG_NAME_%i" % i)
        regexp_loc_src = re.compile("LOCAL_SRC_%i" % i)

        build_con = data["%s_build" % params['comp_name_%i' % i]]

        cloudbuild_check = bool(regexp_cb.search(str(build_con['script'])))
        img_name_check = bool(regexp_img.search(str(build_con['script'])))
        local_src_check = bool(regexp_loc_src.search(str(build_con['script'])))

        assert cloudbuild_check == True
        assert img_name_check == True
        assert local_src_check == True
