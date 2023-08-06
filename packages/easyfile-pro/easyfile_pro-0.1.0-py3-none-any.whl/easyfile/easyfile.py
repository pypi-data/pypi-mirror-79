import json
import os
import shutil
from threading import Thread


def async_func(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()

	return wrapper


class EasyFilePro:
	def __init__(self, path):
		self.path = path

	def read_json(self):
		with open(self.path, 'r', encoding='utf8')as f:
			json_data = json.load(f)
			return json_data

	@async_func
	def write_json(self, data):
		with open(self.path, 'w', encoding='utf8')as f:
			json.dump(data, f)
		print(f'写入json,{self.get_filesize()}mb,{self.path}')

	def read_txt(self):
		with open(self.path, 'r', encoding='utf8')as f:
			return f.read()

	@async_func
	def write_txt(self, data):
		with open(self.path, 'w', encoding='utf8')as f:
			f.write(str(data))

	def make_dir(self):
		path = self.path.strip()  # 去除首位空格
		path = path.rstrip("\\")  # 去除尾部 \ 符号
		is_exists = os.path.exists(path)
		# 判断结果
		if not is_exists:
			os.makedirs(path)
			return True
		else:
			return False

	def move_file(self, to_path):
		if not os.path.isfile(self.path):
			print("%s not exist!" % (self.path))
		else:
			fpath, fname = os.path.split(to_path)  # 分离文件名和路径
			if not os.path.exists(fpath):
				os.makedirs(fpath)  # 创建路径
			shutil.move(self.path, to_path)  # 移动文件
			print(f"移动 {self.path} -> {to_path}")

	def copy_file(self, to_path):
		if not os.path.isfile(self.path):
			print(f"{self.path}不存在!")
		else:
			fpath, fname = os.path.split(to_path)  # 分离文件名和路径
			if not os.path.exists(fpath):
				os.makedirs(fpath)  # 创建路径
			shutil.copyfile(self.path, to_path)  # 复制文件
			print(f"复制 {self.path} -> {to_path}")

	def get_filesize(self, acc: int = 2):
		size = os.path.getsize(self.path)
		size = size / float(1024 * 1024)
		return round(size, acc)  # 精度

	# 检测路径是否存在
	def check_path_is_exist(self) -> bool:
		return os.path.exists(self.path)

	# 检测路径是个文件，还是文件夹
	def check_is_file_or_folder(self) -> str:
		# 先检测路径是否存在
		if not self.check_path_is_exist():
			return 'not exist'
		if os.path.isfile(self.path):
			return 'file'
		else:
			return 'folder'

	# 列出目录文件列表
	def listdir_pro(self):
		filename_list = []
		for i in os.listdir(self.path):
			if i != '.DS_Store':
				filename_list.append(i)
		return filename_list
