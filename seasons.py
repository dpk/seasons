from datetime import date
import math


def true_colour_value(colour):
    return tuple(c ** 2 for c in colour)
def rgb_colour_value(colour):
    return tuple(math.sqrt(c) for c in colour)

def subtract_colours(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def divide_coords(colour, divisor):
    return tuple(c / divisor for c in colour)

class SeasonColour:
    def __init__(self, spring=(0x00, 0x64, 0xB5), summer=(0x2C, 0xA7, 0x20), autumn=(0xFF, 0xE1, 0x0B), winter=(0xE1, 0x5B, 0x2A)):
        # self.spring, self.summer, self.autumn, self.winter = spring, summer, autumn, winter
        self.seasons = (spring, summer, autumn, winter)
    
    def colour_for_day(self, day=None):
        if not day:
            day = date.today()
        
        season_length = 92
        day_of_year = day.timetuple().tm_yday
        
        season = day_of_year // season_length
        season_day = day_of_year % season_length
        next_season = (season + 1) % 4
        
        true_season_start_colour = true_colour_value(self.seasons[season])
        true_season_end_colour = true_colour_value(self.seasons[next_season])
        
        coord_diffs = subtract_colours(true_season_end_colour, true_season_start_colour)
        day_value = divide_coords(coord_diffs, 92)
        
        return rgb_colour_value((
            true_season_start_colour[0] + (day_value[0] * season_day),
            true_season_start_colour[1] + (day_value[1] * season_day),
            true_season_start_colour[2] + (day_value[2] * season_day),
        ))

if __name__ == '__main__':
    print("""
    <title>Seasons Colour Cycle</title>
    <style>
      body {
        margin: 0;
      }
      div {
        font-family: Helvetica, sans-serif;
        font-weight: bold;
        padding: 0.5em;
      }
    </style>
    """)
    
    from datetime import timedelta
    day = date(date.today().year, 1, 1)
    one_day = timedelta(days=1)
    sc = SeasonColour()
    
    while day <= date(date.today().year + 1, 1, 1):
        print('<div style="background-color: rgb%r; color: #eee;">%s</div>' % (tuple(map(round, sc.colour_for_day(day))), day.strftime('%e %B')))
        day += one_day
