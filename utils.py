import discord

def get_time(time):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds