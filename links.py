# Name: Ahmad Al-Dajani

# Filename: links.py

# Description: Contains two classes: Scraper class and Download class.
# Scraper class automates link collections from given webpage.
# Download class downloads and converts documents in webpages as text files

# Dependencies: os, re, urllib.parse, io, urllib.requests, bs4, requests, pdfminer.six

# Time: WAY MORE THAN 30 HOURS. UNICODE AND MEMORY ERRORS WERE A NIGHTMARE IN DOWNLOADING AND CONVERTING TO TEXT.
# import pip
# def import_or_install(package):
#     try:
#         __import__(package)
#     except ImportError:
#         install = pip.main(['install', package])
# packages = ['os', 're', 'urllib.parse', 'io', 'urllib.requests', 'bs4', 'requests', 'pdfminer.six']
# for package in packages:
#     import_or_install(package)

import os
import re
import urllib.parse
import urllib.request
from io import BytesIO, StringIO
from urllib.request import urlopen

import bs4
import html2text
import requests
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class Scraper:
	def __init__(self, url, **kwargs):
		# special=False, extension=False, keywords=False, condition=False):
		self.url = url
		# To get links on a page, you must set links=True
		if 'links' in kwargs:
			if 'special' not in kwargs:
				self.links = [urllib.parse.urljoin(self.url, link) for link in self.all_links()]
			# To get special links, you must include special=True
			elif 'special' in kwargs:
				# You must then specify what is special about the links you want to get.
				# It could be that the links have special extensions or keywords. both can be either strings or list
				# types
				if 'extension' in kwargs and 'keywords' not in kwargs:
					self.links = [urllib.parse.urljoin(self.url, link) for link in
								  self.special_links(extension=kwargs['extension'])]
				elif 'keywords' in kwargs and 'extension' not in kwargs:
					self.links = [urllib.parse.urljoin(self.url, link) for link in
								  self.special_links(keywords=kwargs['keywords'], condition=kwargs['condition'])]
				elif 'extension' in kwargs and 'keywords' in kwargs:
					self.links = [urllib.parse.urljoin(self.url, link) for link in
								  self.special_links(extension=kwargs['extension'], keywords=kwargs['keywords'],
													 condition=kwargs['condition'])]
				elif not ('extension' in kwargs and not 'keywords' in kwargs):
					print("Error: You must specify either link extensions or keywords in link.")
					exit()

	def get_soup(self):
		# Method to Soup Given URL
		html = requests.get(self.url)
		# Get the right encoding.
		encoding = html.encoding if 'charset' in html.headers.get('Content-Type', '') else None
		soup: object = bs4.BeautifulSoup(html.text, 'html5lib', from_encoding=encoding)
		return soup

	def all_links(self):
		# Method to get all links from url
		relative_links = [link.get('href') for link in self.get_soup().find_all('a')]
		return relative_links

	def special_links(self, extension=False, keywords=False, condition=False):
		# Method for selecting certain links with extensions or keywords.
		special_links = []
		if extension and not keywords:
			hrefs = [link.get('href') for link in self.get_soup().select('a')]
			if isinstance(extension, str):
				special_links += [href for href in hrefs if href.endswith(extension) if href not in special_links]
			elif isinstance(extension, list):
				for href in hrefs:
					special_links += [href for ext in extension if (href.endswith(ext) and href not in special_links)]
		elif keywords and not extension:
			hrefs = [link.get('href') for link in self.get_soup().select('a')]
			if isinstance(keywords, str):
				special_links += [href for href in hrefs if keywords in href and href not in special_links]
			elif isinstance(keywords, list):
				while condition is False:
					print(
						"You must provide a condition when using keywords.\n You can type \'and\' to require that all "
						"keywords are in the link. Alternatively, you type 'or' which will return links containing "
						"any "
						"one of the keywords provided")
					condition = input('Condition: ')
					continue
				if 'and' in condition:
					# check if all the words in the list are in the href, and if so, append it to the specified_list
					for href in hrefs:
						if all(word in href for word in keywords):
							if href not in special_links:
								special_links.append(href)
				elif 'or' in condition:
					for href in hrefs:
						for word in keywords:
							if word in href:
								if href not in special_links:
									special_links.append(href)
		if extension and keywords:
			hrefs = [link.get('href') for link in self.get_soup().select('a')]
			if isinstance(extension, str):
				if isinstance(keywords, str):
					# go through each href, check i fit ends with the extension, then check if it has the keyword,
					# then check if the href is not already in the list, then append
					special_links += [href for href in hrefs if href.endswith(extension) if keywords in href if
									  href not in special_links]
				if isinstance(keywords, list):
					# go through each href, if the href ends with the extension, then go through each keyword,
					# if the condition is 'and', then check if all keywords are in the href, then check if the href is
					# not already in the list, and append.
					selected_hrefs = [href for href in hrefs if href if href.endswith(extension)]
					while condition is False:
						print(
							"You must provide a condition when using keywords.\n You can type \'and\' to require that "
							"all keywords are in the link. Alternatively, you type 'or' which will return links "
							"containing any one of the keywords provided")
						condition = input('Condition: ')
						continue
					if 'and' in condition:
						for href in selected_hrefs:
							if all(word in href for word in keywords):
								if href not in special_links:
									special_links.append(href)
					# if or is the condition, go through each href that ends with the extension, go through each
					# word inthe keywords, if you find a match between the word and the href, and the href is not
					# already in the list, then append it to the list.
					if 'or' in condition:
						for href in selected_hrefs:
							for word in keywords:
								if word in href:
									if href not in special_links:
										special_links.append(href)
			if isinstance(extension, list):
				for ext in extension:
					selected_hrefs = [href for href in hrefs if href if href.endswith(ext)]
					if isinstance(keywords, str):
						special_links += [href for href in selected_hrefs if keywords in href if
										  href not in special_links]
					if isinstance(keywords, list):
						while condition is False:
							print(
								"You must provide a condition when using keywords.\n You can type \'and\' to require "
								"that all keywords are in the link. Alternatively, you type 'or' which will return "
								"links containing any one of the keywords provided")
							condition = input('Condition: ')
							continue
						if 'and' in condition:
							for href in selected_hrefs:
								if all(word in href for word in keywords):
									if href not in special_links:
										special_links.append(href)
						if 'or' in condition:
							for href in selected_hrefs:
								for word in keywords:
									if (word in href) and (href not in special_links):
										special_links.append(href)
		return special_links


class Download:
	def __init__(self, url):
		self.url = url
		self.error_dict = {}
		if url.endswith('pdf'):
			self.DocName = re.sub('pdf', 'txt', self.get_filename())
		if url.endswith('htm'):
			self.DocName = re.sub('htm', 'txt', self.get_filename())
		if url.endswith('txt'):
			self.DocName = self.get_filename()

	def recursive_replace(self, fn, *args):
		# Function to be called by other methods. This is a recursive exception handler
		# designed to handle unicode errors by replacing error characters with empty string.
		try:
			writer = fn(*args)
			return writer
		except UnicodeEncodeError as e:
			# Find the problem character from the Exception string. Isolate it. Then replace it.
			problem_character = re.search(r"(?<=')\\.+(?=')", str(e))
			if not problem_character is None:
				character = problem_character.group(0)
				self.error_dict.setdefault(self.get_filename(), []).append(character)
				text = ''.join(args)
				fix = re.sub(character, '', text)
				return Download.recursive_replace(self, fn, fix)

	def get_filename(self):
		pattern = re.search(r"(?<=[a-z]{3})/(?:.+)", str(self.url))
		if pattern:
			return re.sub('/', '-', pattern.group(0))

	def convert_PDF(self, pages=None):
		# Method for converting PDF Files to TXT files
		DocName = re.sub('pdf', 'txt', self.get_filename())
		# if not os.path.isfile(DocName):
		print('Converting PDF {}'.format(self.get_filename()))
		if not pages:
			pagenums = set()
		else:
			pagenums = set(pages)
		output = StringIO()
		manager = PDFResourceManager()
		converter = TextConverter(manager, output, laparams=LAParams())
		interpreter = PDFPageInterpreter(manager, converter)
		pdf = urlopen(self.url)
		data = pdf.read()
		fp = BytesIO(data)
		for page in PDFPage.get_pages(fp, pagenums):
			interpreter.process_page(page)
		converter.close()
		text = output.getvalue()
		output.close()
		text_file = open(DocName, 'w', encoding='utf-8')
		error = 'No Errors Found'
		try:
			text_file.write(text)
		except BaseException:
			error = Download.recursive_replace(self, text_file.write, text)
		text_file.close()
		return print(error)

	# else:
	# 	return print("{} already exists as txt".format(DocName))

	def convert_HTM(self):
		print("Downloading and Converting HTM Download: {}".format(self.get_filename()))
		DocName = re.sub('htm', 'txt', self.get_filename())
		response = requests.get(self.url).text
		h = html2text.HTML2Text()
		h.unicode_snob = True
		h.ignore_images = True
		h.bypass_tables = True
		text = h.handle(response)
		text = re.sub(r'(?<=Secretary\n).*', '', text, flags=re.DOTALL)
		text = re.sub(r'(\n\))|(\n:)', '', text, flags=re.DOTALL)
		text = re.sub(r'.*(?=UNITED STATES OF AMERICA|United States of America)', '\n', text,
					  flags=re.DOTALL | re.MULTILINE)
		fp = open(DocName, 'w', encoding='utf-8')
		fp.write(text)
		fp.close
		return

	def convert_TXT(self):
		# Method to download and write text files
		DocName = self.get_filename()
		print("Downloading and Converting TXT Download: {}".format(DocName))
		response = urlopen(self.url)
		data = response.read()
		body = data.decode('utf-8', errors='ignore')
		fp = open(DocName, 'w', encoding='utf-8')
		error = 'No Errors Found'
		try:
			fp.write(body)
		except BaseException:
			error = Download.recursive_replace(self, fp.write, body)
		fp.close()
		return print(error)

	def create_dir(self):
		# Method for creating sub-directory to save downloaded files
		dir_path = os.path.dirname(os.path.realpath(__file__))
		# Create a new path from the string by adding it to the current directory where this file is saved
		new_path = str(dir_path) + '\\' + str(self)
		if not os.path.isdir(new_path):
			os.makedirs(new_path)
		return new_path

	def copy_file(self, dir):
		if not os.path.isdir(dir):
			os.makedirs(dir)
		fp = open(self, 'r', encoding='utf-8')
		text = fp.read()
		os.chdir(dir)
		new_file = open(self, 'w', encoding='utf-8')
		new_file.write(text)
		new_file.close()
		fp.close()
		os.chdir('..')
		return "Copied Download to Text Directory"


class Order:
	matches = []
	no_matches = []

	def __init__(self, order):
		self.order = order
		self.text = open(order, 'r', encoding='utf-8').read()
		self.filing_date = {}
		self.defendants = {}
		self.file_no = {}
		self.proceeding_type = {}
		self.filing_status = {}
		self.admission = {}
		self.settlement = {}
		self.proceeding_status = {}
		self.proceeding_header = ''

	def get_caption(self, text, part):
		if part == 'left':
			caption_pattern = re.compile(r'^.*?\s(?=(\)|:)\s)', flags=re.MULTILINE)
		elif part == 'right':
			caption_pattern = re.compile(r'(?<=\s(\)|:)\s)\w*.*', flags=re.MULTILINE)
		matches = re.finditer(caption_pattern, text)
		if matches:
			caption = ''
			for match in matches:
				caption += '\n' + match.group(0)
			return caption
		else:
			return print("Could not locate caption")

	def filter_proceeding(self):
		# Filter Proceedings based on Caption Contents
		soup = bs4.BeautifulSoup(self.text, 'html5lib')
		caption_pattern = re.compile(r'(.*?Order|Order).*?(Instituting|of).*?(Proceedings|Proceeding|suspension).+?',
									 flags=re.IGNORECASE | re.DOTALL)
		caption_tags = soup.find('td', text=caption_pattern)
		title = ''
		if caption_tags:
			caption = caption_tags.get_text(strip=True)
			caption = caption.strip()
			caption = caption.replace('\n', ' ').replace('*', '').replace(':', '').replace('-', ' ').replace('<', '')
			title += caption
		if title == '':
			all_tags = soup.find('table')
			if all_tags:
				pattern = re.compile(r"order", flags=re.IGNORECASE)
				final_caption = ' '
				if re.findall(pattern, all_tags.get_text()):
					pattern = re.compile(
						r'(.*)?(Order|Instituting|Public|Administrative|Cease|Decist|Proceeding|Proceedings|Pursuant'
						r'|Securities|Act|Making|Sanctions|Suspension|Forthwith|Findings|Imposing).*',
						flags=re.IGNORECASE)
					caption = all_tags.get_text()
					if re.finditer(pattern, caption):
						for match in re.finditer(pattern, caption):
							text = re.sub('\*(\)|:)', '', match.group(0))
							text = re.sub('\*', '', text)
							text = re.sub('\n', ' ', text)
							final_caption += text
						title += final_caption
				else:
					text = self.text
					pattern = re.compile(r'(order instituting.*?|order of.*?)\n\n', flags=re.DOTALL | re.IGNORECASE)
					match = re.search(pattern, text)
					if match:
						type = re.sub('\n', '', match.group(0))
						if type.endswith('-'):
							caption = self.get_caption(text, 'right')
							caption = re.sub('\n', ' ', caption)
							caption = re.sub('-', ' ', caption)
							title += caption
						else:
							title += type
			if title == '':
				text = self.text
				pattern = re.compile(r'(order instituting.*?|order of.*?)\n\n', flags=re.DOTALL | re.IGNORECASE)
				match = re.search(pattern, text)

				if match:
					match = match.group(0)
					type = re.sub('\n', '-', match)
					if type.endswith('-'):
						caption = self.get_caption(text, 'right')
						if caption:
							caption = re.sub('\n', ' ', caption)
							caption = re.sub('-', ' ', caption)
							title += caption
						else:
							type = re.sub('--', '', type)
							title += type
		self.proceeding_header = title
		one = re.compile(
			r"Order(.+?|\s+)?Instituting(.+?|\s+)?Administrative(.+?|\s+)?and(.+?|\s+)?Cease(.+?|\s+)?and("
			r".+?|\s+)?Desist("
			r".+?|\s+)?(Proceedings|Proceeding).*",
			flags=re.IGNORECASE | re.DOTALL)
		two = re.compile(
			r"Order(.+?|\s+)?Instituting(.+?|\s+)?Public(.+?|\s+)?Administrative(.+?|\s+)?and(.+?|\s+)?Cease("
			r".+?|\s+)?and("
			r".+?|\s+)?Desist(.+?|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		three = re.compile(
			r"Order(.+?|\s+)?Instituting(.+?|\s+)?Cease(.+?|\s+)?and(.+?|\s+)?Desist(.+?|\s+)?("
			r"Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		four = re.compile(
			r"Order(.+?|\s+)?Instituting(.+?|\s+)?Administrative(.+?|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		five = re.compile(
			r"Order(.+?|\s+)?Instituting(.+?|\s+)?Public(.+?|\s+)?Administrative(.+?|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		six = re.compile(r"Order(.+?|\s+)?of(.+?|\s+)?Forthwith(.+?|\s+)?Suspension.+?",
						 flags=re.IGNORECASE | re.DOTALL)
		seven = re.compile(r"Order(.+?|\s+)?of(.+?|\s+)?Suspension.+?", flags=re.IGNORECASE | re.DOTALL)
		if re.search(one, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(two, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(three, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(four, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(five, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(six, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		elif re.search(seven, title):
			Download.copy_file(self.order, '.\\relevant_orders')
		else:
			Order.no_matches.append(self.order)

	### TO DO: Handle Corner Cases where caption is not formatted in html.

	def get_names(self):
		# Return names of defendants from SEC Filing Caption
		soup = bs4.BeautifulSoup(self.text, 'html5lib')
		pattern = re.compile(r'(matter|respondent|respondents).+?(respondent|respondents)?',
							 flags=re.IGNORECASE | re.DOTALL)
		caption_tag = soup.find('td', text=pattern)
		defendants = ''
		if caption_tag:
			caption = caption_tag.get_text(strip=True)
			new_pattern = re.compile(r'(^.+In.*?of)|(^In.*?of)|(Respondents|Respondent).+',
									 flags=re.IGNORECASE | re.DOTALL)
			caption = re.sub(new_pattern, '', caption).replace(r'Respondent', '').replace('Respondant', '').replace(
				'Respondents', '')
			name = caption.replace('*', '').replace('>', '').replace(':', '').replace('\xa0', '').replace('\n',
																										  ' ').strip()
			no_spaces = re.compile(r"\s+(?=\s[A-Z|a-z])")
			name = re.sub(no_spaces, '', name)
			defendants += name
		elif caption_tag is None:
			caption = self.get_caption(self.text, 'left')
			clean_pattern = re.compile(r"(In the Matter of|Respondent|Respondents|Respondant|Respondants)\.?",
									   flags=re.IGNORECASE)
			name = re.sub(clean_pattern, '', caption)
			name = re.sub('\n', ' ', name)
			no_spaces = re.compile(r"\s+(?=\s[A-Z|a-z])")
			name = re.sub(no_spaces, '', name)
			defendants += name
		if defendants == '':
			text = self.text
			pattern = re.compile(r'^The.+?(announced|deems).*?\n{2,}', flags=re.DOTALL | re.MULTILINE)
			para_1 = re.search(pattern, text)
			if para_1:
				para = re.sub('\n', ' ', para_1.group(0))
				names_line = re.search(r'(?<=against).*?("\)\.|\))', para, flags=re.MULTILINE | re.DOTALL)
				if names_line:
					clean_pattern = re.compile(r'(pursuant.+|respondent|\("?.+?"\))', flags=re.IGNORECASE)
					names = re.sub(clean_pattern, '', names_line.group(0))
					defendants += names.strip('"').strip('.').strip()
		if defendants == '':
			print("Could not identify defendants in ", self.order)
			Order.no_matches.append(self.order)
			Download.copy_file(self.order, "NO NAME MATCH")
		else:
			self.defendants.setdefault("Defendants", defendants)

	def get_filing_date(self):
		# Returns filing date from SEC Administrative Proceeding
		pattern = ".?.?(UNITED STATES OF AMERICA|before the|securities and exchange commission).*?(File No\.|File)"
		match = re.search(pattern, self.text, flags=re.DOTALL | re.IGNORECASE)
		if match:
			date = "\w* \d{1,2}(,|\.)? \d{4}"
			date_match = re.search(date, match.group(0))
			if date_match:
				result = date_match.group(0)
				self.filing_date.setdefault("Filing Date", str(result))
			else:
				Order.no_matches.append(self.order)
				print(
					"Error: Missed filing date for this file: {0}\nYou can find it in the 'Files with No Filing "
					"Dates' "
					"folder".format(
						Order.no_matches))
				Download.copy_file(self.order, 'Files with No Filing Dates')
		else:
			Order.no_matches.append(self.order)
			Download.copy_file(self.order, 'Files with No Filing Dates')
			print(
				"Error: Missed filing date for this file: {0}\nYou can find it in the 'Files with No Filing Dates' "
				"folder".format(
					Order.no_matches))

	def get_file_number(self):
		pattern = r".?.?(UNITED STATES OF AMERICA|before the|securities and exchange commission).*?(File " \
				  r"No\..+\n|File.+\n)"
		match = re.search(pattern, self.text, flags=re.DOTALL | re.IGNORECASE)
		if match:
			fn_pattern = r"\s{0,}File (No\.)?\s{0,}\*{0,}\s{0,}\d{0,}(-)?\d{0,}"
			if re.finditer(fn_pattern, match.group(0), flags=re.IGNORECASE):
				for fn_match in re.finditer(fn_pattern, match.group(0), flags=re.IGNORECASE):
					result = fn_match.group(0)
					no = re.sub(r'File (No\.)?', '', result, flags=re.IGNORECASE)
					filenumber = re.sub(r'\*\*', '', no).strip()
					self.file_no.setdefault("File No", str(filenumber))
			else:
				Order.no_matches.append(self.order)
		else:
			Order.no_matches.append(self.order)
			Download.copy_file(self.order, 'Files with No File No.')
			print(
				"Error: Missed File No. for this file: {0}\nYou can find it in the 'Files with No File No.' "
				"folder".format(
					Order.no_matches))

	def get_proceeding_type(self):
		stand_alone_1 = re.compile(
			r"Order(.|\s+)?Instituting(.|\s+)?Administrative(.|\s+)?and(.|\s+)?Cease(.|\s+)?and(.|\s+)?Desist("
			r".|\s+)?(Proceedings|Proceeding).*",
			flags=re.IGNORECASE | re.DOTALL)

		stand_alone_2 = re.compile(
			r"Order(.|\s+)?Instituting(.|\s+)?Public(.|\s+)?Administrative(.|\s+)?and(.|\s+)?Cease(.|\s+)?and("
			r".|\s+)?Desist(.|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		stand_alone_3 = re.compile(
			r"Order(.|\s+)?Instituting(.|\s+)?Cease(.|\s+)?and(.|\s+)?Desist(.|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		follow_on_1 = re.compile(r"Order(.|\s+)?Instituting(.|\s+)?Administrative(.|\s+)?(Proceedings|Proceeding).+?",
								 flags=re.IGNORECASE | re.DOTALL)
		follow_on_2 = re.compile(
			r"Order(.|\s+)?Instituting(.|\s+)?Public(.|\s+)?Administrative(.|\s+)?(Proceedings|Proceeding).+?",
			flags=re.IGNORECASE | re.DOTALL)
		follow_on_3 = re.compile(r"Order(.|\s+)?of(.|\s+)?Forthwith(.|\s+)?Suspension.+?",
								 flags=re.IGNORECASE | re.DOTALL)
		follow_on_4 = re.compile(r"Order(.|\s+)?of(.|\s+)?Suspension.+?", flags=re.IGNORECASE | re.DOTALL)
		soup = bs4.BeautifulSoup(self.text, 'html5lib')
		caption_pattern = re.compile(r'(.*?Order|Order).*?(Instituting|of).*?(Proceedings|Proceeding|suspension).+?',
									 flags=re.IGNORECASE | re.DOTALL)
		caption_tags = soup.find('td', text=caption_pattern)
		title = ''
		if caption_tags:
			caption = caption_tags.get_text(strip=True)
			caption = caption.strip()
			caption = caption.replace('\n', ' ').replace('*', '').replace(':', '').replace('-', ' ').replace('<', '')
			title += caption
		if title == '':
			all_tags = soup.find('table')
			if all_tags:
				pattern = re.compile(r"order", flags=re.IGNORECASE)
				final_caption = ' '
				if re.findall(pattern, all_tags.get_text()):
					pattern = re.compile(
						r'(.*)?(Order|Instituting|Public|Administrative|Cease|Decist|Proceeding|Proceedings|Pursuant'
						r'|Securities|Act|Making|Sanctions|Suspension|Forthwith|Findings|Imposing).*',
						flags=re.IGNORECASE)
					caption = all_tags.get_text()
					if re.finditer(pattern, caption):
						for match in re.finditer(pattern, caption):
							text = re.sub('\*(\)|:)', '', match.group(0))
							text = re.sub('\*', '', text)
							text = re.sub('\n', ' ', text)
							final_caption += text
						title += final_caption
				else:
					text = self.text
					pattern = re.compile(r'(order instituting.*?|order of.*?)\n\n', flags=re.DOTALL | re.IGNORECASE)
					match = re.search(pattern, text)
					type = re.sub('\n', '', match.group(0))
					if type.endswith('-'):
						caption = self.get_caption(text, 'right')
						caption = re.sub('\n', ' ', caption)
						caption = re.sub('-', ' ', caption)
						title += caption
					else:
						title += type
			if title == '':
				text = self.text
				pattern = re.compile(r'(order instituting.*?|order of.*?)\n\n', flags=re.DOTALL | re.IGNORECASE)
				match = re.search(pattern, text)
				match = match.group(0)

				type = re.sub('\n', '-', match)
				if type.endswith('-'):
					caption = self.get_caption(text, 'right')
					if caption:
						caption = re.sub('\n', ' ', caption)
						caption = re.sub('-', ' ', caption)
						title += caption
					else:
						type = re.sub('--', '', type)
						title += type
			elif title == '':
				Order.no_matches.append(self.order)
		if title == '':
			Download.copy_file(self.order, '.\\No Type')
			print("Could not identify proceeding type.\nProceeding moved to folder 'No Type' folder.")
			Order.no_matches.append(self.order)
		# Is the action contested
		if re.search(r"Notice(.+|\s+)of(.+|\s+)Hearing", title, flags=re.IGNORECASE):
			self.filing_status.setdefault("Filing Status", "Contested")
			if re.search("(Offer|Offers)(.+|\s+)of(.+|\s+)Settlement", self.text):
				self.settlement.setdefault("Settlement Offered", "Yes")
			else:
				self.settlement.setdefault("Settlement Offered", "No")

		else:
			self.filing_status.setdefault("Filing Status", "Settled")
			self.settlement.setdefault("Settlement Offered", "Not Applicable. Proceeding Uncontested")
		# Was there an admission?
		if re.search(r"without(.+|\s+)admitting(.+|\s+)or(.+|\s+)denying", self.text, flags=re.IGNORECASE):
			self.admission.setdefault("Admission", 'No')
		else:
			self.admission.setdefault("Admission", "Yes")
		# Is the proceeding stand alone, follow-on or delinquen?
		if re.search(stand_alone_1, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Stand-alone"
			else:
				Order.no_matches.append(self.order)
		elif re.search(stand_alone_2, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Stand-alone"
			else:
				Order.no_matches.append(self.order)
		elif re.search(stand_alone_3, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Stand-alone"
			else:
				Order.no_matches.append(self.order)
		elif re.search(follow_on_1, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Follow-on"
			else:
				Order.no_matches.append(self.order)
		elif re.search(follow_on_2, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Follow-on"
			else:
				Order.no_matches.append(self.order)
		elif re.search(follow_on_3, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Follow-on"
			else:
				Order.no_matches.append(self.order)
		elif re.search(follow_on_4, title):
			if '12(j)' in title:
				self.proceeding_type['Proceeding Type'] = 'Delinquent Filing'
			elif '12(j)' not in title:
				self.proceeding_type['Proceeding Type'] = "Follow-on"
			else:
				Order.no_matches.append(self.order)


if __name__ == '__main__':
	years = Scraper('https://www.sec.gov/litigation/admin.shtml', links=True, special=True, extension='shtml',
					keywords=['litigation', 'admin'], condition='and').links
	proceedings = []
	for year in years:
		proceedings_in_year = Scraper(year, links=True, special=True, extension=['pdf', 'txt', 'htm'],
									  keywords=['litigation', 'admin'], condition='and').links
		proceedings += proceedings_in_year
	errors = []
	htm_dir = Download.create_dir('htm files')
	print(htm_dir)
	txt_dir = Download.create_dir('txt files')
	print(txt_dir)
	pdf_dir = Download.create_dir('pdfs')

	for proceeding in proceedings:
		document = Download(proceeding).DocName
		if proceeding.endswith('htm'):
			os.chdir(htm_dir)
			if os.path.isfile(document):
				print("{} already exists.".format(document))
				continue
			Download(proceeding).convert_HTM()
		elif proceeding.endswith('txt'):
			os.chdir(txt_dir)
			if os.path.isfile(document):
				print("{} already exists.".format(document))
				continue
			Download(proceeding).convert_TXT()
		elif proceeding.endswith('pdf'):
			os.chdir(pdf_dir)
			# print(os.getcwd())
			# print(document)
			if os.path.isfile(document):
				print("{} already exists.".format(document))
				continue
			Download(proceeding).convert_PDF()
