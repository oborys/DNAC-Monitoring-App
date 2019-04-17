# DNAC Monitoring App

You can choose one (main) directions:

  - [About this App](#about_this_app)
  - [The main featuresg](#the_main_features)
  - [Install and run locally ](#install_and_run_locally )
  - [Test App using Cisco DevNet sandboxes](#test_app_using_cisco_devnet_sandboxes)

## About this App
DNAC Monitoring App extends the basic features of [DNA-C](https://www.cisco.com/c/en/us/products/cloud-systems-management/dna-center/index.html) (Cisco Digital Network Architecture Center). This App help collect information about devices and manage network issues. This App can be useful for Enterprise and Service Providers who want to collect and store different changes about network devices, calculate and manage different indicators such as:
- Average MTTR (Mean time to repair); 
- Average mean time to recover incident; 

Registration and schedule of the hackathon you can find [here](https://www.cisco.com/c/m/uk_ua/training-events/2018/hackathon/index.html)

## The main features
1. an application that can collect and process data from DNA-C
2. User-friendly interface 

3. You can add and manage different type of roles:
- IT management/CIO reports: gets health report and high-level SLA stats (you can manage or propose your parameters for SLA calculation)
- IT manager: gets opened/closed service requests (ticket) and MTTR stats. 
- Also can assign responsible persons from the Administrator/DevOps list for solving the ticket 
- Administrator/DevOps: can solve a ticket, get WAN availability and average latency reports 

4. Using Redis, Celery and local DataBase App collect and compare different device config changes

5. Ticket management:
- filters by type of problem: 
    - traffic
    - configuration change
- filters by creation date 
- filters by ticket status:
    - open 
    - in progress
    - rejected
    - solved
 
- Notifications module for sending alerts via (Webex Teams)[https://www.webex.com/team-collaboration.html] and Email 
- Collect and display inventory and topology from DNA-C 

## Install and run locally 

You need to install Python 3+, Vue.js

in terminal 

`git clone https://github.com/oborys/DNAC-Monitoring-App.git`

then open file usage.txt and run commands

After deployment, you need to add a network controller (DNA-C) credentials

![](img/DNAC_App_credentials.png)

Ticket management  
![](img/DNAC_App_ticket_management.png)



## Test App using Cisco DevNet sandboxes

Available [sandboxes by Networking category](https://devnetsandbox.cisco.com/RM/Topology?c=14ec7ccf-2988-474e-a135-1e90b9bc6caf)

In this direction you can also use DNA-C (Digital Network Architecture Center) sandboxes

DNA-C 1.2.10 - [https://sandboxdnac2.cisco.com/](https://sandboxdnac2.cisco.com/)

login: devnetuser

password: Cisco123!

DNA-C 1.2.6 - [https://sandboxdnac.cisco.com](https://sandboxdnac.cisco.com)

login: devnetuser

password: Cisco123!


**Other Useful links**

- [Cisco DevNet Modules](https://developer.cisco.com/learning/modules)
- [Discover code repositories related to Cisco technologies](https://developer.cisco.com/codeexchange/)
- [Cisco Ecosystem Exchange](https://developer.cisco.com/ecosystem)
- [Cisco DevNet github](https://github.com/CiscoDevNet)
- [Sandbox Labs](https://devnetsandbox.cisco.com/RM/Topology)

