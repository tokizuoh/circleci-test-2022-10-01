import dotenv
import os
import pprint
import requests
import sys

def get_pipeline_id_list():
    org_slug = os.getenv("ORG_SLUG")
    url = "https://circleci.com/api/v2/pipeline?org-slug={0}&mine={1}".format(org_slug, "true")
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        pipeline_id_list = list(map(lambda item: item['id'], res_dict["items"]))
        return pipeline_id_list
    except requests.exceptions.RequestException as e:
        raise e

def get_workflow_id_list(pipeline_id_list):
    url = "https://circleci.com/api/v2/pipeline/{0}/workflow".format(pipeline_id_list[0])
    headers = {"Circle-Token": os.getenv("CIRCLE_TOKEN")}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_dict = res.json()
        workflow_id_list = list(map(lambda item: item['id'], res_dict["items"]))
        return workflow_id_list
    except requests.exceptions.RequestException as e:
        raise e

def main():
    dotenv.load_dotenv()

    pipeline_id_list = get_pipeline_id_list()
    workflow_id_list = get_workflow_id_list(pipeline_id_list=pipeline_id_list)

if __name__ == "__main__":
    main()