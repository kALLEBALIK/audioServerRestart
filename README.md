# audioServerRestart
 
Fixing windows 10 bug where audio doesn't work after waking up from sleep.

Restarts windows audio server.   
Run once or run continuously to check if windows just woke up.
```python
""" Default settings """
SETTINGS = {
    "log":
    {
        "print": False,     # should logger print
        "write": False      # should logger write to file
    },
    "run-style": "once",    # / continuously
    "event-timeout": 10,    # How often to check for weakeup (if running continuously)
    "event-time-diff": 180  # How long since the wake up (if running continuously)
}
```
Custom settings is read from ``settings.json``  