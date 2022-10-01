import dotenv
import os
import pprint
import requests
import sys

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

def get_workflow_id(pipeline_id):
    url = "https://circleci.com/api/v2/pipeline/{0}/workflow".format(pipeline_id)
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        workflow_id_list = list(map(lambda item: item['id'], res_dict["items"]))
        return workflow_id_list
    except requests.exceptions.RequestException as e:
        raise e

def get_workflow_name(id):
    url = "https://circleci.com/api/v2/workflow/{0}".format(id)
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        return res_dict["name"]
    except requests.exceptions.RequestException as e:
        raise e

def main():
    args = sys.argv
    if len(args) != 2:
        sys.exit("error. do `python {THIS_FILE} {COMMIT_REVISION}`")
    revision = args[1]

    dotenv.load_dotenv()

    # TODO: ここに {ワークフロー名:Bool} の辞書を宣言したい
    pipeline_id_list = get_pipeline_id_list(target_revision=revision)
    for pipeline_id in pipeline_id_list:
        workflow_id_list = get_workflow_id(pipeline_id=pipeline_id)
        for workflow_id in workflow_id_list:
            print(get_workflow_name(workflow_id))

if __name__ == "__main__":
    main()