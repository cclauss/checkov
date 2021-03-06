from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
import json


class IAMStarActionPolicyDocument(BaseResourceCheck):

    def __init__(self):
        name = "Ensure no IAM policies documents allow \"*\" as a statement's actions"
        id = "CKV_AWS_63"
        supported_resources = ['aws_iam_role_policy', 'aws_iam_user_policy', 'aws_iam_group_policy', 'aws_iam_policy']
        categories = [CheckCategories.IAM]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'policy' in conf.keys():
            try:
                policy_block = json.loads(conf['policy'][0])
                if 'Statement' in policy_block.keys():
                        if 'Action' in policy_block['Statement'][0] and \
                                policy_block['Statement'][0].get('Effect', ['Allow']) == 'Allow' and \
                                policy_block['Statement'][0]['Action'][0] == "*":
                            return CheckResult.FAILED
            except: # nosec
                pass
        return CheckResult.PASSED


check = IAMStarActionPolicyDocument()
