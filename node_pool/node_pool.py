import yaml
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--configFile', required=True, type=str)
parser.add_argument('--templateFile', required=True, type=str)
parser.add_argument('--outputFile', required=True, type=str)

parser.add_argument('--name', required=True, type=str)
parser.add_argument('--clusterName', required=True, type=str)
parser.add_argument('--subnetID', required=True, type=str)
parser.add_argument('--minNodeCount', required=True, type=str)
parser.add_argument('--maxNodeCount', required=True, type=str)
parser.add_argument('--maxPodsPerNode', required=True, type=str)
parser.add_argument('--instanceType', required=True, type=str)
parser.add_argument('--rootVolSize', required=True, type=str)

# tags
parser.add_argument('--CostCentre', required=True, type=str)
parser.add_argument('--ProjectCode', required=True, type=str)
parser.add_argument('--ApplicationName', required=True, type=str)
parser.add_argument('--BusinessEntity', required=True, type=str)
parser.add_argument('--Region', required=True, type=str)
parser.add_argument('--Environment', required=True, type=str)
parser.add_argument('--AWSResourceType', required=True, type=str)
parser.add_argument('--BusinessUnit', required=True, type=str)
parser.add_argument('--ApplicationID', required=True, type=str)
parser.add_argument('--Reason', required=True, type=str)
parser.add_argument('--Owner', required=True, type=str)
parser.add_argument('--ManagedBy', required=True, type=str)
parser.add_argument('--Automation', required=True, type=str)

args = parser.parse_args()
config_file = args.configFile
template_file = args.templateFile
output_file = args.outputFile

node_pool_name = args.name
cluster_name = args.clusterName
subnet_id = args.subnetID
min_node_count = args.minNodeCount
max_node_count = args.maxNodeCount
max_pods_node = args.maxPodsPerNode
instance_type = args.instanceType
root_vol_size = args.rootVolSize

tag_cost_centre = args.CostCentre
tag_project_code = args.ProjectCode
tag_application_name = args.ApplicationName
tag_business_entity = args.BusinessEntity
tag_region = args.Region
tag_environment = args.Environment
tag_aws_resourcetype = args.AWSResourceType
tag_business_unit = args.BusinessUnit
tag_applicationId = args.ApplicationID
tag_reason = args.Reason
tag_owner = args.Owner
tag_managedBy = args.ManagedBy
tag_automation = args.Automation


# Read the yaml
def read_nodepool_yaml(yaml_file):
    try:
        config = open(yaml_file)
        parsed_yaml = yaml.load_all(config, Loader=yaml.FullLoader)
        for dic in parsed_yaml:
            if dic["kind"] == "AWSNodePool":
                return dic
    except OSError as error:
        print("ERROR: Could not parse file: ", error)
        sys.exit()


# Populate the template file
def merge_data_template(parsed_template, parsed_config):
    parsed_template["metadata"]["name"] = node_pool_name

    template = parsed_template["spec"]
    cluster0 = parsed_config["spec"]

    template["clusterName"] = cluster_name
    template["version"] = cluster0["version"]
    template["region"] = cluster0["region"]
    template["subnetID"] = subnet_id
    template["minNodeCount"] = min_node_count
    template["maxNodeCount"] = max_node_count
    template["maxPodsPerNode"] = max_pods_node
    template["instanceType"] = instance_type
    template["keyName"] = cluster0["keyName"]
    template["iamInstanceProfile"] = cluster0["iamInstanceProfile"]

    template["rootVolume"]["sizeGiB"] = root_vol_size

    template_tags = template["tags"]
    template_tags["CostCentre"] = tag_cost_centre
    template_tags["ProjectCode"] = tag_project_code
    template_tags["ApplicationName"] = tag_application_name
    template_tags["BusinessEntity"] = tag_business_entity
    template_tags["Region"] = tag_region
    template_tags["Environment"] = tag_environment
    template_tags["AWSResourceType"] = tag_aws_resourcetype
    template_tags["BusinessUnit"] = tag_business_unit
    template_tags["ApplicationID"] = tag_applicationId
    template_tags["Reason"] = tag_reason
    template_tags["Owner"] = tag_owner
    template_tags["ManagedBy"] = tag_managedBy
    template_tags["Automation"] = tag_automation

    return parsed_template


if __name__ == "__main__":

    print("Populating the Node Pool template....")
    # Parse Yaml first
    parsed_cluster0_yaml = read_nodepool_yaml(config_file)
    parsed_template_yaml = read_nodepool_yaml(template_file)

    # Populate template file
    merged_template = merge_data_template(parsed_template_yaml, parsed_cluster0_yaml)

    # Create the output YAML file
    output = open(output_file, 'w+')
    yaml.dump(merged_template, output, allow_unicode=True, default_flow_style=False)

    print("DONE.... %s CREATED." % output_file)
