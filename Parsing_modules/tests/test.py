"""
Tests the functions with two example inputs and makes sure the function returns something other than none
"""
import sys 
sys.path.append('../')
import Bsoup_response as br


def test_is_Normal():
    assert br.is_normal("5A") == True
    assert br.is_normal("236A") == False
    
def test_find_normal():
    assert br.find_normal(br.get_HTML_requests("http://wiki.mizuumi.net/w/Under_Night_In-Birth/UNIST/Hyde"), "5A") != None
    
def test_find_special():
    assert br.find_special(br.get_HTML_requests("http://wiki.mizuumi.net/w/Under_Night_In-Birth/UNIST/Hyde"), "236A") != None