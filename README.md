#### Run it locally

1. `pip install -r requirements.txt`
2. Update the `cluster-0.yaml`, and the template files in the `node_pool/` and `user_cluster/` directory.

#### Execute the following command to populate the user cluster template

``` 
python3 user_cluster/cluster.py --configFile cluster-0.yaml --templateFile user_cluster/cluster_template.yaml --outputFile user_cluster/output.yaml \
            --name cluster1 \
            --vpcID vpcId-123 \
            --podAddressCIDRBlocks 111.111.11 \
            --serviceAddressCIDRBlocks 222.222.22 \
            --serviceLoadBalancerSubnetIDs subnetId-1 subnetId-2 subnetId-3 \
            --instanceType t3.large \
            --subnetIDs subnetId-4 subnetId-5 \
            --securityGroupIDs sg-1 sg-2 sg-3 \
            --rootVolSize 5 --etcdVolSize 10 \
            --hubMembershipName elite \
            --tag1 tes-tag1 \
            --tag2 tes-tag2 \
            --tag3 tes-tag3 \
            --tag4 tes-tag4 \
```

#### Execute the following command to populate the Node Pool template

``` 
python3 node_pool/node_pool.py --configFile cluster-0.yaml --templateFile node_pool/nodepool_template.yaml --outputFile node_pool/output.yaml \
            --name cluster1 \
            --clusterName cluster-123 \
            --subnetID subnet-1 \
            --minNodeCount 1 \
            --maxNodeCount 3 \
            --maxPodsPerNode 10 \
            --instanceType t3.large \
            --rootVolSize 2 \
            --CostCentre London \
            --ProjectCode LSP \
            --ApplicationName LSP \
            --BusinessEntity LSEG \
            --Region europe-west2 \
            --Environment dev \
            --AWSResourceType ec2 \
            --BusinessUnit lseg-london \
            --ApplicationID lsp \
            --Reason deployment \
            --Owner lseg \
            --ManagedBy lseg \
            --Automation abc \
```
