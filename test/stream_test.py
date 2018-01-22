'''
Created on Jan 4, 2018

@author: Salim
'''

import unittest
from httpoutputsteam.stream import HttpBufferedOutstream


class FakeHttp():
    
    def __init__(self):
        self.buffer = ''
    
    def send(self,data):
        self.buffer =  self.buffer + data
        
    def __str__(self):
        return self.buffer
    
    
class TestExtFormats(unittest.TestCase):
    
    
        
    def test_simple(self):
        http = FakeHttp()
        out = HttpBufferedOutstream(http)
        
        out.write('test string')
        self.assertEqual('', http.buffer)
        out.flush()
        self.assertEqual('b\r\ntest string\r\n', http.buffer)
        out.close()
        self.assertEqual('b\r\ntest string\r\n0\r\n\r\n', http.buffer)
         
    def test_simple_fit_buffer(self):
        http = FakeHttp()
        out = HttpBufferedOutstream(http,11)
        
        out.write('test string')
        self.assertEqual('b\r\ntest string\r\n', http.buffer)
        out.flush()
        self.assertEqual('b\r\ntest string\r\n', http.buffer)
        out.close()
        self.assertEqual('b\r\ntest string\r\n0\r\n\r\n', http.buffer)  
    
    def test_simple_smaller_flush_needed_buffer(self):
        http = FakeHttp()
        out = HttpBufferedOutstream(http,5)
        
        out.write('test string')
        self.assertEqual('5\r\ntest \r\n5\r\nstrin\r\n', http.buffer)
        out.flush()
        self.assertEqual('5\r\ntest \r\n5\r\nstrin\r\n1\r\ng\r\n', http.buffer)
        out.close()
        self.assertEqual('5\r\ntest \r\n5\r\nstrin\r\n1\r\ng\r\n0\r\n\r\n', http.buffer)    
        
    
    def test_simple_smaller_buffer(self):
        http = FakeHttp()
        out = HttpBufferedOutstream(http,6)
        
        out.write('test string*')
        self.assertEqual('6\r\ntest s\r\n6\r\ntring*\r\n', http.buffer)
        out.flush()
        self.assertEqual('6\r\ntest s\r\n6\r\ntring*\r\n', http.buffer)
        out.close()
        self.assertEqual('6\r\ntest s\r\n6\r\ntring*\r\n0\r\n\r\n', http.buffer)    
    
    
if __name__ == '__main__':
    unittest.main()
    
    
