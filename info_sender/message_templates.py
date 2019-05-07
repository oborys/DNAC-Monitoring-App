EMAIL_WELCOME_MSG = """
    Hi team,
    It's Network Health Check Daily:
    
    About network:
    %d devices is reachable
    %d devices is unreachable
    
    The program automatically sent an e-mail to CIO, IT Director, and DevOps.
    
    Your Network Health Check automatically report
"""

EMAIL_MTTR_UPDATED = """
    Hi team,
    It's Network Health Check Daily:
    
    I'd like to update you about MTTR level on current network ({0}).
    
    - MTTR changed from {1} to {2}
    - MTTRi changed from {3} to {4}
    
    Have a nice day!
    
    Your Network Health Check automatically report
"""

EMAIL_SLA_UPDATED = """
    Hi team,
    It's Network Health Check Daily:
    
    I'd like to update you about SLA on current network ({0}).
    
    - Service/device availability is - {1}%
    - Customer Satisfaction by day changed from {2}% to {3}%
    
    Have a nice day!
    
    Your Network Health Check automatically report
"""

WEBEX_WELCOME_MSG = """
    Hi team,
    It's APIC-EM health check Bot:
    I create this space and invite all MDU if you want to add somebody new
    adds this person to program.

    I will publish incident information here, information on metrics,
    MTTR, SLA, and more.

    About network:
    %d devices is reacheble
    %d devices is unreachable

    Sincerely your NP1 bot
"""

ISSUE_CONFIG_CHANGED_MSG = """
    For network %s was added ticked:
    Description: %s
    Issue type: Configuration changed
    
    Your Network Health Check automatically report
"""

ISSUE_TRAFFIC_MSG = """
    For network %s was added ticked:
    Description: %s
    Issue type: Traffic
    
    Your Network Health Check automatically report
"""

ISSUE_UNREACHABLE_MSG = """
    For network %s was added ticked:
    Description: %s
    Issue type: Unreachable

    Your Network Health Check automatically report
"""

ISSUE_UNKNOWN_MSG = """
    For network %s was added ticked:
    Description: %s
    Issue type: Unknown

    Your Network Health Check automatically report
"""

ISSUE_DEVICE_UNREACHABLE_TEXT = 'Device with IP: %s is now unreachable' # % (device_ip)

ISSUE_NAME_CHANGED_TEXT = 'Device name changed (Old: %s, New: %s)' # % (old_hostname, new_hostname)

ISSUE_CONNECTION_PROBLEM_TEXT = 'Flow connection problem between  (device IP: %s and device IP: %s)' # % (src_hostname, src_device_ip, dst_hostname, dst_device_ip)

ISSUE_CONFIG_CHANGED_TEXT = 'Change config  (device: %s, add string: %s and Subtract: %s)'

SLA_INFO_FOR_CIO = """
    Hi {},
    It's Network Health Check Daily:
    
    For this network {} we have next SLA metrics:
    
    Service/device availability {}%
    Average mean time to recover from incidents {}
    Customer Satisfaction {}%
    
    Your Network Health Check automatically report
"""

MTTR_FOR_IT_DIRECTOR = """
    Hi {},
    It's Network Health Check Daily:
    
    For this network {} we have next indicators:
    
    MTTR: {}
    Opened tickets: {}
    
    Your Network Health Check automatically report
"""

NEW_TICKET_ASSIGNED = """
    Hi %s,
    It's Network Health Check Daily:
    
    Ticket with ID #%d was assigned to you.
    
    Please, see details in your account.
    
    Your Network Health Check automatically report
"""