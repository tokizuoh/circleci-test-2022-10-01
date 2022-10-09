import dotenv
import os
import pprint
import requests
import sys

# https://circleci.com/docs/api/v2/index.html#operation/listPipelines
def get_pipeline_id_list(target_revision):
    org_slug = os.getenv("ORG_SLUG")
    url = "https://circleci.com/api/v2/pipeline?org-slug={0}&mine={1}".format(org_slug, "true")
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        pipeline_id_list = list(
            map(
                lambda item: item['id'] if item['vcs']['revision'] == target_revision else None,
                res_dict["items"]
            )
        )
        return [pipeline_id for pipeline_id in pipeline_id_list if pipeline_id != None ]
    except requests.exceptions.RequestException as e:
        raise e

# https://circleci.com/docs/api/v2/index.html#operation/getPipelineById
def get_workflow_id(pipeline_id, target_workflow_name):
    url = "https://circleci.com/api/v2/pipeline/{0}/workflow".format(pipeline_id)
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        workflow_id_list = list(
            map(
                lambda item: item['id'] if item['name'] == target_workflow_name else None,
                res_dict["items"]
            )
        )
        workflow_id_list = [workflow_id for workflow_id in workflow_id_list if workflow_id != None]
        if len(workflow_id_list) > 0:
            return workflow_id_list[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        raise e

# https://circleci.com/docs/api/v2/index.html#operation/rerunWorkflow
def rerun_workflow(workflow_id):
    url = "https://circleci.com/api/v2/workflow/{0}/rerun".format(workflow_id)
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.post(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        pprint.pprint(res_dict)
    except requests.exceptions.RequestException as e:
        raise e

def main():
    args = sys.argv
    if len(args) != 2:
        sys.exit("error. do `python {THIS_FILE} {COMMIT_REVISION}`")
    revision = args[1]

    dotenv.load_dotenv()

    target_workflow_name = "workflow-status-checks-workflow"
    pipeline_id_list = get_pipeline_id_list(target_revision=revision)
    for pipeline_id in pipeline_id_list:
        workflow_id = get_workflow_id(pipeline_id=pipeline_id, target_workflow_name=target_workflow_name)
        if workflow_id == None:
            continue
        rerun_workflow(workflow_id=workflow_id)
    else:
        print("success")

if __name__ == "__main__":
    main()