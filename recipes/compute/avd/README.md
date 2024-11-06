# Azure Virtual Desktop

## Configuration
* Desktop, Streaming App
* Virtual Desktop Type (Pooled, Personal)
* Session (Multi, Single)
* In-region backup
* Auto-scale


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
* Nerdio https://nmmce.getnerdio.com/
