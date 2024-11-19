import json
import os
import re
import struct
import sys
import traceback
import zlib
from collections import namedtuple
from io import BytesIO


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    print("\nError encountered while running Python script.")
    print("Please read arrows >>> above to know what happened.")
    input("")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit

LANGUAGE_CODE_PREFIX = {
    'ENG': '00',
    'CHS': '01',
    'CHT': '02',
    'CZE': '03',
    'DAN': '04',
    'DUT': '05',
    'FIN': '06',
    'FRE': '07',
    'GER': '08',
    'ITA': '0B',
    'JPN': '0C',
    'KOR': '0D',
    'NOR': '0E',
    'POL': '0F',
    'POR': '11',
    'RUS': '12',
    'SPA': '13',
    'SWE': '15',
}

try:
    input_lang = sys.argv[1]
    language_code = LANGUAGE_CODE_PREFIX[input_lang]
except Exception as e:
    print(">>> Error - Language code '{}' does not exist.\n".format(input_lang))
    raise e

language_strings = {}


def _correct_invalid_json_files(json_str):
    # Remove trailing commas in dicts and lists
    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)
    return json_str


for file_name in os.listdir():
    if file_name.endswith('.json'):
        json_file_path = os.path.join(os.getcwd(), file_name)

        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_str = _correct_invalid_json_files(file.read())

            try:
                json_file = json.loads(json_str)
            except Exception as e:
                print(">>> Error - Unable to load '{}' JSON file.".format(file_name))
                print(">>> Verify if the JSON file is valid using any JSON validator website (https://jsonlint.com).\n")
                raise e

            try:
                entries = json_file['Entries'] or ()
            except Exception as e:
                print(">>> Error - Unable to process '{}' JSON file.".format(file_name))
                print(">>> JSON file '{}' is missing string entries.\n".format(file_name))
                raise e

            for entry_count, string_entry in enumerate(entries):
                try:
                    language_strings[int(string_entry['Key'], 16)] = string_entry['Value']
                except Exception as e:
                    print(">>> Error - Unable to process '{}' JSON file.".format(file_name))
                    print(">>> String entry {} (approximately line {}) is invalid.\n".format(entry_count, entry_count * 4))
                    raise e

print("Loaded {} string entries.".format(len(language_strings)))


class BinaryBase():
    def __init__(self, bytes_data=None):
        self.stream = BytesIO(bytes_data)

    def seek(self, position):
        return self.stream.seek(position)

    def tell(self):
        return self.stream.tell()

    def size(self):
        return len(self.stream.getvalue())

    def get_bytes(self):
        self.stream.seek(0)
        return self.stream.read()


class BinaryWriter(BinaryBase):
    def __init__(self, bytes_data=None):
        super().__init__(bytes_data=bytes_data)

    def write(self, data_type, *values):
        self.stream.write(struct.pack(data_type, *values))

    def write_boolean(self, value):
        self.write("?", value)

    def write_8bit_int(self, value):
        self.write("b", value)

    def write_8bit_uint(self, value):
        self.write("B", value)

    def write_16bit_int(self, value):
        self.write("h", value)

    def write_16bit_uint(self, value):
        self.write("H", value)

    def write_32bit_int(self, value):
        self.write("i", value)

    def write_32bit_uint(self, value):
        self.write("I", value)

    def write_64bit_int(self, value):
        self.write("q", value)

    def write_64bit_uint(self, value):
        self.write("Q", value)

    def write_float(self, value):
        self.write("f", value)

    def write_double(self, value):
        self.write("d", value)

    def write_string(self, value, encoding="utf-8"):
        self.stream.write(value.encode(encoding))

    def write_padding(self, size=1):
        self.write("x" * size)

    def write_raw_bytes(self, value):
        self.stream.write(value)

    def delete(self, size):
        current_position = self.tell()
        self.stream = BytesIO(self.stream.getvalue()[:current_position + 1] + self.stream.getvalue()[current_position + size + 1:])
        self.seek(current_position)


class StringTableBuilder():
    def __init__(self):
        self.version = 0x05
        self.is_compressed = 0x00
        self.reserved = [0x00, 0x00]
        self.string_length = 0x00
        self.entries = []

    def append(self, text, fnv, flags=0x00):
        self.entries.append((fnv, flags, text))
        self.string_length += len(text.encode("utf-8")) + 1

        return self

    def get_bytes(self):
        stream = BinaryWriter()

        stream.write_32bit_uint(self._get_header("STBL"))
        stream.write_16bit_uint(self.version)
        stream.write_boolean(self.is_compressed)
        stream.write_32bit_uint(len(self.entries))
        stream.write_padding(size=2)
        stream.write_padding(size=4)
        stream.write_32bit_uint(self.string_length)

        for (fnv_hash, flags, text) in self.entries:
            stream.write_32bit_uint(fnv_hash)
            stream.write_8bit_uint(flags)
            stream.write_16bit_uint(len(text.encode("utf-8")))
            stream.write_string(text)

        return stream.get_bytes()

    def _get_header(self, string_header):
        i = 0

        for j in reversed(range(len(string_header))):
            i += ord(string_header[j]) << (j * 8)

        return i


string_table_builder = StringTableBuilder()

for k, v in language_strings.items():
    string_table_builder.append(v, k)

string_table_bytes = string_table_builder.get_bytes()

_PackageResource = namedtuple('_PackageResource', ('resource_type', 'resource_group', 'resource_instance', 'resource_bytes', 'resource_position', 'resource_size_compressed', 'resource_size_uncompressed', 'compression_type'))


class PackageResourceCompressionType:
    UNCOMPRESSED = 0x0000
    STREAMABLE_COMPRESSION = 0xFFFE
    INTERNAL_COMPRESSION = 0xFFFF
    DELETED_RECORD = 0xFFE0
    ZLIB = 0x5A42


class PackageWriter():
    HEADER_SIZE = 96
    INDEX_ENTRY_SIZE = 32

    def __init__(self):
        self.file_version = [2, 1]
        self.user_version = [0, 0]

        self.resources = []
        self.next_resource_position = 0

    def append_resource(self, resource_type, resource_group, resource_instance, resource_bytes, compression_type=PackageResourceCompressionType.ZLIB):
        resource_size_uncompressed = len(resource_bytes)

        if compression_type == PackageResourceCompressionType.ZLIB:
            resource_bytes = zlib.compress(resource_bytes)

        resource_size_compressed = len(resource_bytes)

        self.resources.append(_PackageResource(resource_type, resource_group, resource_instance, resource_bytes, self.next_resource_position, resource_size_compressed, resource_size_uncompressed, compression_type))
        self.next_resource_position += resource_size_compressed

        return self

    def get_bytes(self):
        stream = BinaryWriter()

        stream.write_raw_bytes(b'DBPF')

        stream.write_32bit_uint(self.file_version[0])
        stream.write_32bit_uint(self.file_version[1])
        stream.write_32bit_uint(self.user_version[0])
        stream.write_32bit_uint(self.user_version[1])

        stream.write_32bit_uint(0)

        stream.write_32bit_uint(0)
        stream.write_32bit_uint(0)

        stream.write_32bit_uint(0)

        stream.write_32bit_uint(len(self.resources))
        stream.write_32bit_uint(0)
        stream.write_32bit_uint((self.INDEX_ENTRY_SIZE * len(self.resources)) + 4)

        stream.write_padding(4 * 3)
        stream.write_32bit_uint(3)

        stream.write_64bit_uint(self.next_resource_position + self.HEADER_SIZE)

        stream.write_padding(4 * 6)

        for resource in self.resources:
            stream.write_raw_bytes(resource.resource_bytes)

        stream.write_32bit_uint(0)

        for resource in self.resources:
            stream.write_32bit_uint(resource.resource_type)
            stream.write_32bit_uint(resource.resource_group)

            stream.write_32bit_uint(resource.resource_instance >> 32)
            stream.write_32bit_uint(resource.resource_instance & 0xFFFFFFFF)

            stream.write_32bit_uint(resource.resource_position + self.HEADER_SIZE)

            stream.write_32bit_uint(resource.resource_size_compressed | 0x80000000)
            stream.write_32bit_uint(resource.resource_size_uncompressed)

            stream.write_16bit_uint(resource.compression_type)
            stream.write_16bit_uint(1)

        return stream.get_bytes()


package_builder = PackageWriter()

string_table_resource_instance = 0xCBF29CE484222325

for random_byte in list(os.urandom(64)):
    string_table_resource_instance = (string_table_resource_instance * 0x100000001B3) % 2 ** 64
    string_table_resource_instance = string_table_resource_instance ^ random_byte

package_builder.append_resource(0x220557DA, 0x00000000, int("0x" + language_code + hex(string_table_resource_instance)[4:], 16), string_table_bytes)

print("Saving {} translation package...".format(input_lang))

with open(os.path.join(os.getcwd(), "Translation_{}.PACKAGE".format(input_lang)), 'wb') as file:
    file.write(package_builder.get_bytes())
