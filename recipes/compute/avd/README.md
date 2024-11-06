# Azure Virtual Desktop

## Configuration
* Desktop, Streaming App
* Virtual Desktop Type (Pooled, Personal)
* Session (Multi, Single)
* In-region backup
* Auto-scale

## WAF AVD Assessment
* Pillars (Reliability, Security, Cost, Monitoring, Horizonatal scaling)
* Application Delivery
    * Host Pool (Personal, Pooled)
    * Load-balancing algorithm (Breadth-first, Depth-first, scale-down scenarios)
    * Scaling Plans for session hosts
    * Session Hosts Availability zones or availability sets
    * Compute size target workloads (CPU, GPU, Secure)
    * Storage Solutions
    * HA/Disaster Recovery (Availability zones, Backup)
* Networking and Connectivity
    * Network latency
    * VPN, RDP
    * Hybrid Network performance
    * Network security
    * DNS
    * RDB Short path charges
* Monitoring
    * Service and Resource Health
    * Performance Metrics
    * Security and Compliance
    * Reporting tools
    * Alerts
* ...


## Cost Drivers
* Region
* Service (AVD, AVD HCI)
* Virtual Desktop Type (Pooled, Personal)
* Pooled Session (Multi, Single)
* Pooled Multi-Sesson Workload Type (Light, Medium, Heavy, Power)
* Total Users
* Total Hours
* VM Instance Size
* VM Instance Count
* Savings Plan
* Reservations
* AHUB
* Storage
    * Managed Disks - Tier (Standard HHD, Standard SSD, Premium SSD)
    * Managed Disks - Size (P10-P80)
    * Managed Disk Count
    * File Share - Tier (Standard HHD, Standard SSD, Premium SSD)
    * FSLogix
* Bandwidth
    * Source Region
    * Destination Region
    * Total Data Transfer GB
* Backup
* Log Analytics

## Common Best Practices
* VM Power Management
* Just-in-time provisioning (50% burstable)
* reservations
* OS Disk autoscale
* OS Disk shrink
* FSLogix Shrink

# References
* Workload assessment https://learn.microsoft.com/en-us/assessments/1ef67c4e-b8d1-4193-b850-d192089ae33d//
* https://learn.microsoft.com/en-us/azure/well-architected/azure-virtual-desktop/design-principles#cost-optimization
* Nerdio https://nmmce.getnerdio.com/
