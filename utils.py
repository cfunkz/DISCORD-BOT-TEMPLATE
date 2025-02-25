import discord

def get_time(error):
    remaining_time = error.retry_after
    minutes, seconds = divmod(remaining_time, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds