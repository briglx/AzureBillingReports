# Azure Kubernetes Service (AKS)

## Background
* `deployment.yml` - Defines min and max resources for a container
* Workloads are deployed as containers into Pods
* You can define requests and limits on an image
* A deployment allows limits for workloads
* workload limits set the min and max resources for a container
* resource quotas set the aggregate limits for a namespace
* AKS
    * System node pools are used for system workloads
    * User node pools are used for user workloads
* Monitoring tools will show utilization of the node pools
* Utilization strategies
    * Monitor ave workload per sku / nodepool to scale out
    * Monitor to scale up
* Vertical pool autoscaling (vpa)
* Goal is to have higher computing density per node around 80% utilization
* Most users use persistent volume and persistent volume claims
    * Example: Azure Disk, Azure File, Azure Blob

## Questions
Questions to review when first evaluating and AKS cluster:
* Do you have requests and limits set on your pods?
    * As defined in the `PodSpec` in the `deployment.yml` file or `Pod` object via `kubectl`
* If no limits for workloads, Do you have default limit ranges defined for the namespace?
    * As defined in the `LimitRange` object in the namespace configured by the cluster admin via `kubectl`
    * example: `kubectl create -f limit-range.yml`
* Do you have resource quotas set on the namespace?
    * As defined in the `ResourceQuota` object in the namespace configured by the cluster admin via `kubectl`
    * example: `kubectl create -f resource-quota.yml`
* Workload Questions
    * Have you configured both system node pools and user node pools?
        * Do system workloads run on lower sku VMs?
        * Do user workloads run appropriate sized VMs?
    * Have you split out high compute workloads into a separate node pool?
    * Have you left 20% head room between VM instance resource vs Pod Pool Utilization?
* Do you have a strategy to estimate actual workload(deployment) consumption?
* Monitoring Questions
    * Are you monitoring average workload per sku / nodepool to scale out?
    * Are you monitoring to scale up?
    * Are you using vertical pod autoscaling (vpa)?
* DR Questions
    * Are you using availability zones?
    * Are you configuring Pod Topology Spread constraints?
* Storage Questions
    * Have you reviewed the required storage amount for the workloads disks?

## General

* Adding Pod is easier that adding a VM to the pool
* Leave 20% head room between VM instance resource vs Pod Pool Utilization
* Add a new node(VM Instance) if no more head room
* Adding a new Node (mins) takes more time than adding a new pod (Seconds)
* Split workloads into multiple node pools
* Run System Node Pools on Lower SKUs (VM Scale Set - 3 by default)
* Have at least 1 User Node Pool running smaller VMs
* Split out High Compute workloads for smaller High Compute Node Pool

## AKS Cost Drivers
* Region
* Tier (Free, Standard, Premium)
* OS
* VM Instance Size
* Total VM Compute Hrs
* Savings Plan
* Reservations
* Managed Disks

Example `deployment.yml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3  # Number of pod replicas
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21.6  # Nginx image from Docker Hub
        ports:
        - containerPort: 80
        resources:
          requests:            # Minimum resources required
            memory: "128Mi"
            cpu: "250m"
          limits:              # Maximum resources allowed
            memory: "256Mi"
            cpu: "500m"
```

Example `service.yml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer  # This will provision an Azure Load Balancer
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: nginx  # Match the label from the deployment
```

Example Namespace `limit-range.yml`
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: limit-range
spec:
    limits:
    - default:
        memory: 512Mi
        cpu: 500m
        defaultRequest:
        memory: 256Mi
        cpu: 250m
        type: Container
```

Example `resource-quota.yml`
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: resource-quota
spec:
    hard:
        pods: "10"
        requests.cpu: "1"
        requests.memory: 1Gi
        limits.cpu: "2"
        limits.memory: 2Gi
```

# Resources
* https://learn.microsoft.com/en-us/azure/aks/best-practices-cost
* https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
