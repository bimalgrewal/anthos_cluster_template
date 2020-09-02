import yaml
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--configFile', required=True, type=str)
parser.add_argument('--templateFile', required=True, type=str)
parser.add_argument('--outputFile', required=True, type=str)

parser.add_argument('--name', required=True, type=str)
parser.add_argument('--vpcID', required=True, type=str)
parser.add_argument('--podAddressCIDRBlocks', required=True, type=str)
parser.add_argument('--serviceAddressCIDRBlocks', required=True, type=str)
parser.add_argument('--serviceLoadBalancerSubnetIDs', nargs='+', required=True, type=str)  # List
parser.add_argument('--instanceType', required=True, type=str)  # List
parser.add_argument('--subnetIDs', required=True, nargs='+', type=str)  # List
parser.add_argument('--securityGroupIDs', nargs='+', required=True, type=str)  # List
parser.add_argument('--rootVolSize', required=True, type=str)
parser.add_argument('--etcdVolSize', required=True, type=str)
parser.add_argument('--hubMembershipName', required=True, type=str)
parser.add_argument('--tag1', required=True, type=str)
parser.add_argument('--tag2', required=True, type=str)
parser.add_argument('--tag3', required=True, type=str)
parser.add_argument('--tag4', required=True, type=str)

# parser.add_argument('--identityARN', required=True, type=str)

args = parser.parse_args()
config_file = args.configFile
template_file = args.templateFile
output_file = args.outputFile

name = args.name
vpc_id = args.vpcID
pod_address_CIDRBlocks = args.podAddressCIDRBlocks
service_address_CIDRBlocks = args.serviceAddressCIDRBlocks
service_loadbalancer_subnetIDs = args.serviceLoadBalancerSubnetIDs
instance_type = args.instanceType
subnetIds = args.subnetIDs
security_groupIDs = args.securityGroupIDs
root_vol_size = args.rootVolSize
etcd_vol_size = args.etcdVolSize
hub_membership_name = args.hubMembershipName
tag1 = args.tag1
tag2 = args.tag2
tag3 = args.tag3
tag4 = args.tag4


# Read the yaml
def read_yaml(yaml_file):
    try:
        config = open(yaml_file)
        parsed_yaml = yaml.load_all(config, Loader=yaml.FullLoader)
        for dic in parsed_yaml:
            if dic["kind"] == "AWSCluster":
                return dic
    except OSError as error:
        print("ERROR: Could not parse file: ", error)
        sys.exit()


# Populate the template file
def merge_data_template(parsed_template, parsed_config):
    parsed_template["metadata"]["name"] = name

    template = parsed_template["spec"]
    cluster0 = parsed_config["spec"]

    template["region"] = cluster0["region"]

    # networking
    template["networking"]["vpcID"] = vpc_id
    template["networking"]["podAddressCIDRBlocks"] = pod_address_CIDRBlocks
    template["networking"]["serviceAddressCIDRBlocks"] = service_address_CIDRBlocks
    template["networking"]["serviceLoadBalancerSubnetIDs"] = service_loadbalancer_subnetIDs

    # Control Plane
    template_control_plane = template["controlPlane"]
    cluster0_control_plane = cluster0["controlPlane"]

    template_control_plane["version"] = cluster0_control_plane["version"]
    template_control_plane["instanceType"] = instance_type
    template_control_plane["keyName"] = cluster0_control_plane["keyName"]
    template_control_plane["subnetIDs"] = subnetIds
    template_control_plane["securityGroupIDs"] = security_groupIDs
    template_control_plane["iamInstanceProfile"] = cluster0_control_plane["iamInstanceProfile"]
    template_control_plane["rootVolume"]["sizeGiB"] = root_vol_size
    template_control_plane["etcd"]["mainVolume.sizeGIB"] = etcd_vol_size
    template_control_plane["databaseEncryption"]["kmsKeyARN"] = cluster0_control_plane["databaseEncryption"][
        "kmsKeyARN"]
    template_control_plane["hub"]["membershipName"] = hub_membership_name

    # tags
    tags_template_control_plane = template_control_plane["tags"]

    tags_template_control_plane["tag1"] = tag1
    tags_template_control_plane["tag2"] = tag2
    tags_template_control_plane["tag3"] = tag3
    tags_template_control_plane["tag4"] = tag4

    template["authentication"]["awsIAM"]["adminIdentityARNs"] = cluster0["authentication"]["awsIAM"][
        "adminIdentityARNs"]

    return parsed_template


if __name__ == "__main__":

    print("Populating the User Cluster template....")
    # Parse Yaml first
    parsed_cluster0_yaml = read_yaml(config_file)
    parsed_template_yaml = read_yaml(template_file)

    # Populate template file
    merged_template = merge_data_template(parsed_template_yaml, parsed_cluster0_yaml)

    # Create the output YAML file
    output = open(output_file, 'w+')
    yaml.dump(merged_template, output, allow_unicode=True, default_flow_style=False)

    print("DONE.... %s CREATED." % output_file)
