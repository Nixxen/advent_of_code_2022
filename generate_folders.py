import shutil
from files_renamer import rename_files


PLACEHOLDER = "XX"
START_DAY = 1
END_DAY = 25
TEMPLATE_DIR = "dayXX"


def main(placeholder, start_day, end_day, template_dir):
    # Make a copy of the template directory and its contents and rename
    # the placeholder in the new directory to the day number
    # Pads the day number with a leading zero if necessary
    for day_num in range(start_day, end_day + 1):
        day_str = str(day_num)
        if len(day_str) == 1:
            day_str = "0" + day_str
        new_dir = template_dir.replace(placeholder, day_str)
        shutil.copytree(template_dir, new_dir)
        rename_files(new_dir, placeholder, day_str)


if __name__ == "__main__":
    main(PLACEHOLDER, START_DAY, END_DAY, TEMPLATE_DIR)
