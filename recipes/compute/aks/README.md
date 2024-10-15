# Azure Kubernetes Service (AKS)

Questions to review when first evaluating and AKS cluster:
* TBD

# General

* Adding Pod is easier that adding a VM to the pool
* Leave 20% head room between VM instance resource vs Pod Pool Utilization
* Add a new node(VM Instance) if no more head room
* Adding a new Node (mins) takes more time than adding a new pod (Seconds)
* Split workloads into multiple node pools
* Run System Node Pools on Lower SKUs (VM Scale Set - 3 by default)
* Have at least 1 User Node Pool running smaller VMs
* Split out High Compute workloads for smaller High Compute Node Pool
