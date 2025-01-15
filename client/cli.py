import argparse
import sys
from os.path import exists

import requests

from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
from datetime import datetime

from openpyxl.styles import PatternFill, Font


def get_color_code(hu):
    hu_not_older_than_three_months = "007500" # Green
    hu_not_older_than_twelve_months = "FFA500" # Orange
    hu_older_than_twelve_months = "b30000" # Red
    hu_time = datetime.strptime(hu, "%Y-%M-%d")
    now = datetime.now()
    if now + relativedelta(months=-3) < hu_time:
        return PatternFill(
            start_color=hu_not_older_than_three_months,
            end_color=hu_not_older_than_three_months,
            fill_type="solid"
        )
    elif now + relativedelta(months=-12) < hu_time:
        return PatternFill(
            start_color=hu_not_older_than_twelve_months,
            end_color=hu_not_older_than_twelve_months,
            fill_type="solid"
        )
    else:
        return PatternFill(
            start_color=hu_older_than_twelve_months,
            end_color=hu_older_than_twelve_months,
            fill_type="solid"
        )


def upload_csv(csv_path):
    print(f"Uploading {csv_path}...")
    res = requests.post("http://127.0.0.1:8000/upload", files={"file": open(csv_path, "rb")})
    res.raise_for_status()
    return res.json()


def generate_xlsx(merged_list, keys, is_colored=True):
    wb = Workbook()
    ws = wb.active
    ws.title = "Merged"
    ws.append(list(keys))
    for item in merged_list:
        ws.append([item[key] for key in keys])
        if is_colored:
            for cell in ws[ws.max_row]:
                cell.fill = get_color_code(item.get("hu"))
                # FIXME: fill cell font color
                if cell == 'labelIds':
                    cell.font = Font(color=item.get('labelIds'))
    wb.save(f"vehicles_{datetime.now().isoformat()}.xlsx")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI with one required and two optional arguments.")
    parser.add_argument("csv_path", type=str, help="A required argument.")
    parser.add_argument("-k", "--keys", type=str, help="An optional argument with a default value.")
    parser.add_argument("-c", "--colored", type=bool, default=True, help="Another optional argument with a default value.")
    args = parser.parse_args()
    csv_path = args.csv_path

    if not (csv_path.endswith(".csv") and exists(csv_path)):
        print("Invalid CSV path.")
        sys.exit(1)

    keys = {'gruppe', 'rnr'}
    if args.keys:
        keys = keys | set(args.keys.split(','))
    merged_list = upload_csv(csv_path)
    sorted_list = sorted(merged_list, key=lambda x: x['gruppe'])
    generate_xlsx(sorted_list, keys, args.colored)