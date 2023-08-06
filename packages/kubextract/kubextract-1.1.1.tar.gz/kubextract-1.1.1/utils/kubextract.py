from utils import pipeline, watcher
from PyInquirer import prompt
import click
import ruamel.yaml
import os
import time

QUES = [
    {
        'type': 'input',
        'name': 'location',
        'message': 'Where\'s path will be generated:'
    },
    {
        'type': 'input',
        'name': 'gitlab_pers_token',
        'message': 'Your gitlab personal token (https://gitlab.warungpintar.co/profile/personal_access_tokens):'
    },
    {
        'type': 'input',
        'name': 'workchat_id',
        'message': 'Your workchat id:'
    },
    {
        'type': 'input',
        'name': 'workchat_type',
        'message': 'Your type of workchat:'
    },
    {
        'type': 'input',
        'name': 'pipe_name',
        'message': 'Your kubeflow pipeline name:'
    },
    {
        'type': 'input',
        'name': 'pipe_desc',
        'message': 'Your kubeflow pipeline description:'
    },
    {
        'type': 'input',
        'name': 'exp_name',
        'message': 'Your kubeflow experiment name:'
    },
    {
        'type': 'input',
        'name': 'exp_desc',
        'message': 'Your kubeflow experiment description:'
    },
    {
        'type': 'input',
        'name': 'node_key',
        'message': 'Your node key for running your experiment:'
    },
    {
        'type': 'input',
        'name': 'node_val',
        'message': 'Your node value for running your experiment:'
    },
    {
        'type': 'input',
        'name': 'use_gpu',
        'message': 'Using gpu or not (true/false):'
    },
    {
        'type': 'input',
        'name': 'n_comps',
        'message': 'How many components will be generated:'
    }
]

class FrameGenerator():
    def __init__(self, params):
        self.yaml = ruamel.yaml
        self.params = params
        self.steps = [
            ('utils', 'utils'),
            ('.gitlab-ci', '.gitlab-ci.yml'),
            ('_gitlab-ci', '_gitlab-ci.yml'),
            ('cloudbuild', 'cloudbuild.yaml')
        ]

    def utils_generator(self, filepath):
        os.system('mkdir -p %s/%s' % (self.params['location'], filepath))

        os.system('cp -r %s %s/%s/watcher.py' % (
            watcher.__file__, self.params['location'], filepath))
        os.system('cp -r %s %s/%s/pipeline.py' % (
            pipeline.__file__, self.params['location'], filepath))

        click.echo("\ncopying watcher.py to %s/%s/watcher.py..." % (self.params['location'], filepath))
        click.echo("\ncopying pipeline.py to %s/%s/pipeline.py..." % (self.params['location'], filepath))

    def main_ci_generator(self, filepath):
        image_name = ""
        local_build = ""
        cloud_build = ""
        comp_str = ""
        gitlab_inc = ""

        for i in range(1, int(self.params['n_comps'])+1):
            if i == 1:
                image_name = "IMG_NAME_%i: %s" % (i, self.params['comp_name_%i' % i])
                local_build = "LOCAL_SRC_%i: %s" % (i, self.params['comp_name_%i' % i])
                cloud_build = "CLOUDBUILD_%i: %s/cloudbuild.yaml" % (i, self.params['comp_name_%i' % i])
                comp_str = '[\"%s\", \"$IMAGE_REGISTRY/$IMG_NAME_%i:$CI_COMMIT_REF_NAME\"]' % (
                    self.params['comp_desc_%i' % i], i)
                gitlab_inc = "- \'%s/_gitlab-ci.yaml\'" % (self.params['comp_name_%i' % i])
            else:
                image_name = """%s
                IMG_NAME_%i: %s""" % (
                    image_name, i, self.params['comp_name_%i' % i])

                local_build = """%s
                LOCAL_SRC_%i: %s""" % (
                    local_build, i, self.params['comp_name_%i' % i])

                cloud_build = """%s
                CLOUDBUILD_%i: %s/cloudbuild.yaml""" % (
                    cloud_build, i, self.params['comp_name_%i' % i])

                comp_str = """%s,
                        [\"%s\", \"$IMAGE_REGISTRY/$IMG_NAME_%i:$CI_COMMIT_REF_NAME\"]""" % (
                    comp_str, self.params['comp_desc_%i' % i], i)

                gitlab_inc = """%s
                - \'%s/_gitlab-ci.yaml\'""" % (
                    gitlab_inc, self.params['comp_name_%i' % i])

        content = """
            stages:
                - test
                - build
                - deploy-pipe
                - deploy

            variables:
                GITLAB_PERS_TOKEN: %s
                WORKCHAT_ID: %s
                WORKCHAT_TYPE: %s
                PIPE_NAME: %s
                PIPE_DESC: %s
                EXP_NAME: %s
                EXP_DESC: %s
                JOB_NAME: $EXP_NAME experiment $CI_COMMIT_SHA
                PIPE_VER_NAME: $PIPE_NAME-$CI_COMMIT_SHA
                NODE_KEY: %s
                NODE_VAL: %s
                USE_GPU: %s
                %s
                %s
                %s
                IMAGE_REGISTRY: asia.gcr.io/warung-support
                COMPONENTS: |
                    [
                        %s
                    ]

            include:
                %s
        """ % (self.params['gitlab_pers_token'], self.params['workchat_id'],
               self.params['workchat_type'], self.params['pipe_name'],
               self.params['pipe_desc'], self.params['exp_name'],
               self.params['exp_desc'], self.params['node_key'],
               self.params['node_val'], self.params['use_gpu'],
               image_name, local_build,
               cloud_build, comp_str, gitlab_inc)

        ci_path = "%s/%s" % (self.params['location'], filepath)
        with open(ci_path, 'w') as wfile:
            data = self.yaml.round_trip_load(content)
            self.yaml.round_trip_dump(
                data, wfile, indent=4,
                block_seq_indent=3)

        click.echo("\ncreating %s to %s/%s..." % (filepath, self.params['location'], filepath))

    def comp_ci_generator(self, filepath):
        for i in range(1, int(self.params['n_comps'])+1):
            if i != 1:
                content = """
                    %s_build:
                        stage: build
                        image: asia.gcr.io/warung-support/google-sdk:latest
                        only:
                            - master
                        tags:
                            - gke-ml
                        script:
                            - |
                              gcloud builds submit \\
                              --config $CLOUDBUILD_%i \\
                              --substitutions _IMAGE_TAG=$IMAGE_REGISTRY/$IMG_NAME_%i:$CI_COMMIT_REF_NAME,\\
                              _LOCAL_SRC=$LOCAL_SRC_%i
                """ % (self.params['comp_name_%i' % i], i, i, i)
            else:
                content = """
                    %s_build:
                        stage: build
                        image: asia.gcr.io/warung-support/google-sdk:latest
                        only:
                            - master
                        tags:
                            - gke-ml
                        script:
                            - |
                              gcloud builds submit \\
                              --config $CLOUDBUILD_%i \\
                              --substitutions _IMAGE_TAG=$IMAGE_REGISTRY/$IMG_NAME_%i:$CI_COMMIT_REF_NAME,\\
                              _LOCAL_SRC=$LOCAL_SRC_%i

                    kubepipe:
                        stage: deploy-pipe
                        image: asia.gcr.io/warung-support/google-sdk:latest
                        only:
                            - master
                        tags:
                            - gke-ml
                        before_script:
                            - kubectl version --client
                            - apk add python3-dev
                            - apk add py3-pip
                            - pip3 install requests
                            - pip3 install kfp --upgrade
                            - export PATH=$PATH:~/.local/bin
                            - which dsl-compile
                        script:
                            - python3 -m utils.pipeline
                """ % (self.params['comp_name_%i' % i], i, i, i)

            directory = "%s/%s" % (
                self.params['location'], self.params['comp_name_%i' % i])
            if not os.path.exists(directory):
                os.makedirs(directory)

            ci_path = "%s/%s" % (directory, filepath)
            with open(ci_path, 'w') as wfile:
                data = self.yaml.round_trip_load(content)
                self.yaml.round_trip_dump(
                    data, wfile, indent=4,
                    block_seq_indent=3)

            click.echo("\ncreating %s to %s/%s..." % (filepath, directory, filepath))

    def cloudbuild_generator(self, filepath):
        for i in range(1, int(self.params['n_comps'])+1):
            content = """
                steps:
                  - name: 'gcr.io/cloud-builders/docker'
                    args: ['build', '-t', '${_IMAGE_TAG}', '${_LOCAL_SRC}']
                substitutions:
                    _IMAGE_TAG: IMAGE_TAG
                    _LOCAL_SRC: LOCAL_SRC
                images:
                  - '${_IMAGE_TAG}'
            """

            directory = "%s/%s" % (
                self.params['location'], self.params['comp_name_%i' % i])
            if not os.path.exists(directory):
                os.makedirs(directory)

            ci_path = "%s/%s" % (directory, filepath)
            with open(ci_path, 'w') as wfile:
                data = self.yaml.round_trip_load(content)
                self.yaml.round_trip_dump(
                    data, wfile, indent=4,
                    block_seq_indent=3)

            click.echo("\ncreating %s to %s/%s..." % (filepath, directory, filepath))

    def main(self, step, filepath):
        if step == 'utils':
            self.utils_generator(filepath)
        elif step == 'pipeline':
            self.pipeline_generator(filepath)
        elif step == '.gitlab-ci':
            self.main_ci_generator(filepath)
        elif step == '_gitlab-ci':
            self.comp_ci_generator(filepath)
        elif step == 'cloudbuild':
            self.cloudbuild_generator(filepath)

@click.command()
def main():
    params = prompt(QUES)
    COMP_QUES = []

    for i in range(1, int(params['n_comps'])+1):
        comp_q = [
        {
            'type': 'input',
            'name': 'comp_name_%i' % i,
            'message': 'What\'s your component %i name:' % i},
        {
            'type': 'input',
            'name': 'comp_desc_%i' % i,
            'message': 'What\'s your component %i description:' % i}]

        COMP_QUES += comp_q

    comp_params = prompt(COMP_QUES)

    for i in range(1, int(params['n_comps'])+1):
        comp_name = comp_params['comp_name_%i' % i]
        comp_params['comp_name_%i' % i] = comp_name.replace(' ', '_')

    params.update(comp_params)
    gen = FrameGenerator(params)

    with click.progressbar(gen.steps, bar_template='%(label)s [%(bar)s] %(info)s',
                           label='Generate framework to %s' % params['location']) as bar:
        for step, filepath in bar:
            time.sleep(0.5)
            gen.main(step, filepath)

if __name__ == '__main__':
    main(prog_name='kubextract')
