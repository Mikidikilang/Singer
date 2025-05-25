import FileRead
from Singer import Singer, ConcertOrganizer
from config import INPUT_FILE_NAME


adatok = FileRead.read_file_content(INPUT_FILE_NAME)

if adatok is None:
    raise ValueError("Could not read the file.")

singer_list = []

lines = adatok.strip().split('\n')
lines[:] = [line.strip() for line in lines if line.strip()]

if not lines:
    raise ValueError(f"Error: File '{INPUT_FILE_NAME}' is empty or contains only whitespace. Exiting.")

try:
    n = int(lines[0]) 
    if n < 0:
        raise ValueError("Number of singers cannot be negative.")
except ValueError:
    raise ValueError('The 1st line of the file must be an integer.')

if len(lines) != n + 1:
    raise ValueError(f"File format error: Expected {n} singer data lines (plus the first line with the count), but found {len(lines) - 1} data lines.")

for i in range(1, n+1):
    parts = lines[i].split(',')

    if len(parts) < 2:
        print(f"Warning: Skipping line {i+1} due to incomplete data: '{lines[i]}'.")
        continue

    name = parts[0].strip()
    genre = parts[1].strip()

    if not name:
        print(f"Warning: Skipping the {i+1}th line because the singer's name is missing: '{lines[i]}'")
        continue
    if not genre:
        print(f"Warning: Skipping the {i+1}th line because the singer's genre is missing: '{lines[i]}'")
        continue

    performances = []

    if len(parts) > 2:
        for show in parts[2:]:
            show_list = show.strip().split(';')
            if len(show_list) == 2 and all(item.strip() for item in show_list):
                performances.append(tuple(show_list))

    singer_list.append(Singer(name, genre, performances))

if not singer_list:
    print("No valid singer data found in the file.")
else:
    concert_organizer = ConcertOrganizer(singer_list)

    try:
        singers_with_most = concert_organizer.find_singers_with_most_performances()

        print("\nSinger(s) with the most performances:")
        print("-" * 40)

        if not singers_with_most:
            print("No singer found (this shouldn't happen if there are singers).")
        else:
            for singer in singers_with_most:  
                print(f"Name: {singer.name}")
                print(f"Genre: {singer.genre}")
                print(f"Number of performances: {len(singer.performances)}")
                print("-" * 20)

    except ValueError as e:
        print(f"\nCould not determine the singer with the most performances: {e}")



singer1 = Singer('alma', 'rock', [('bp','1999'),('bp','1998')])