"""
Bytearray class extension
"""

class bytearrayex(bytearray):
    def replace_at(self, index, bytes):
        """Perform an in-place replacement with bytes starting at index"""
        self[index:index+len(bytes)] = bytes

if __name__ == '__main__':
    from struct import pack

    ba = bytearrayex('A' * 10)
    ba.replace_at(2, pack('I', 0x700))
    ba.replace_at(9, 'CC')

    print len(ba), ba
