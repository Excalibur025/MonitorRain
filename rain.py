import curses
import psutil
import random
import time

def generate_rain_data(processes, columns):
    """Generate process data mapped to rain columns."""
    rain_data = [[] for _ in range(columns)]
    
    for proc in processes:
        try:
            pid = str(proc.pid)
            name = proc.name()[:10]
            cpu = f"{proc.cpu_percent():.1f}%"
            mem = f"{proc.memory_percent():.1f}%"
            entry = f"{pid} {name} {cpu} {mem}"
            random.choice(rain_data).append(entry)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return rain_data

def matrix_rain(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    stdscr.clear()
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()
    columns = width // 20  # Each column is 20 characters wide
    positions = [0] * columns

    while True:
        processes = psutil.process_iter(attrs=None, ad_value=None)
        rain_data = generate_rain_data(processes, columns)
        
        stdscr.clear()
        for col, pos in enumerate(positions):
            data = rain_data[col] if col < len(rain_data) else []
            for i, line in enumerate(data):
                y = (pos + i) % height
                x = col * 20
                try:
                    stdscr.addstr(y, x, line.ljust(20), curses.color_pair(1))
                except curses.error:
                    continue
            positions[col] = (positions[col] + 1) % height
        
        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(matrix_rain)
