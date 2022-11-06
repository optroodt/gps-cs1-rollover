import argparse
import csv
import datetime
import pathlib
import typing


def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--folder", default=None, help="Folder that contains log files you want to update")
	parser.add_argument("--file", default=None, help="Log file you want to update")

	return parser.parse_args()

class GpsRollover:
	FILE_FORMAT = "WG%Y%m%d%H%M%S.log"
	GPS_SENTENCE_CODE = "$GPRMC" # the code we need to look for to modify the date
	OFFSET_DAYS = 7168

	@classmethod
	def date_to_str(cls, date: datetime.date) -> str:
		return date.strftime("%0d%0m") + date.strftime("%Y")[2:]

	@classmethod
	def str_to_date(cls, date_string: str) -> datetime.date:
		assert len(date_string) == 6, "Incorrect length for date_string"
		day, month, year = date_string[0:2], date_string[2:4], date_string[4:6]
		return datetime.date(int("20"+year), int(month), int(day))

	@classmethod
	def add_offset(cls, date_obj: datetime.date) -> datetime.date:
		return date_obj + datetime.timedelta(days=cls.OFFSET_DAYS)

	@classmethod
	def fix_files_in_folder(cls, folder: str) -> None:
		path = pathlib.Path(folder).expanduser()
		for entry in path.iterdir():
			if not entry.is_file() or entry.suffix != ".log":
				continue
			if entry.name[:6] > "WG2021":  # We shouldn't have to touch these files
				continue

			cls.fix_file(entry)

	@classmethod
	def fix_file(cls, file: typing.Union[pathlib.Path, str]) -> None:
		if isinstance(file, str):
			filepath = pathlib.Path(file).expanduser()
		elif isinstance(file, pathlib.Path):
			filepath = file
		else:
			raise ValueError("File must be a Path or str")

		file_datetime = datetime.datetime.strptime(filepath.name, cls.FILE_FORMAT)

		target_path = pathlib.Path(filepath.with_name((cls.add_offset(file_datetime).strftime(cls.FILE_FORMAT))))

		writer = csv.writer(target_path.open("w"), delimiter=",", quoting=csv.QUOTE_NONE)
		reader = csv.reader(filepath.open("r"), delimiter=",")

		for row in reader:
			if row[0] == cls.GPS_SENTENCE_CODE:
				row[-4] = cls.date_to_str(cls.add_offset(cls.str_to_date(row[-4])))
			writer.writerow(row)


if __name__ == "__main__":
	args = get_arguments()
	if args.file:
		GpsRollover.fix_file(args.file)
	elif args.folder:
		GpsRollover.fix_files_in_folder(args.folder)