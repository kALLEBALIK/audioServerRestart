""" Default settings """
SETTINGS = {
    "log":
    {
        "print": False,     # should logger print
        "write": False      # should logger write to file
    },
    "run-style": "once",    # / continuously
    "event-timeout": 10,    # How often to check for weakeup
    "event-time-diff": 180  # How long since the wake up
}
