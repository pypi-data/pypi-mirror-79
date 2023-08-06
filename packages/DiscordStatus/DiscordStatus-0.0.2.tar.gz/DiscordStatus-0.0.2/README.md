# PyPi

[Download Here](https://pypi.org/project/DiscordStatus/)

# DiscordStatus
Wrapper for the Discord Status page's API.

https://discordstatus.com/

For output, see https://discordstatus.com/api

Ex:
```python
    from discordstatus import DiscordStatus

    status_obj = DiscordStatus()

    print(str(status_obj.status))
```

Properties:
- summary
- status
- components
- unresolved_incidents
- all_incidents
- upcoming_maintenances
- active_maintenances
- all_maintenances
