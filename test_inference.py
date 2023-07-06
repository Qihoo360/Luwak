# -*- coding: utf-8 -*-

import unittest
import numpy
import inference
from inference import predict_text


class InferenceTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_none_object(self):
        o_text, ttps = predict_text(None)
        self.assertIsNone(o_text)
        self.assertIsNone(ttps)
    
    def test_non_string_object(self):
        text = 3
        o_text, ttps = predict_text(text)
        self.assertEqual(o_text, text)
        self.assertIsNone(ttps)
    
    def test_empty_text(self):
        text = ''
        o_text, ttps = predict_text(text)
        self.assertEqual(o_text, text)
        self.assertEqual(ttps, [{
            'sent': text,
            'tts': []
        }])

    def test_tp_text(self):
        text = """ACNSHELL is sideloaded by a legitimate executable. 
It will then create a reverse shell via ncat.exe to the server closed.theworkpc.com"""
        o_text, ttps = predict_text(text)
        self.assertEqual(o_text, text)
        self.assertIsInstance(ttps, list)
        self.assertEqual(len(ttps), 2)
        for ttp in ttps:
            self.assertIsInstance(ttp, dict)
            self.assertIn('sent', ttp)
            sent = ttp['sent']
            self.assertIsInstance(sent, str)
            self.assertGreaterEqual(len(sent), 1)
            self.assertIn('tts', ttp)
            tts = ttp['tts']
            self.assertIsInstance(tts, list)
            self.assertGreaterEqual(len(tts), 1)
            for tt in tts:
                self.assertIsInstance(tt, dict)
                self.assertIn('tactic_name', tt)
                self.assertIsInstance(tt['tactic_name'], str)
                self.assertIn('tactic_id', tt)
                self.assertIsInstance(tt['tactic_id'], str)
                self.assertIn('technique_name', tt)
                self.assertIsInstance(tt['technique_name'], str)
                self.assertIn('technique_id', tt)
                self.assertIsInstance(tt['technique_id'], str)
                self.assertIn('score', tt)
                self.assertIsInstance(tt['score'], numpy.float32)
                self.assertGreater(tt['score'], 0.5)
        
        self.assertEqual(ttps[0]['sent'], 'ACNSHELL is sideloaded by a legitimate executable.')
        self.assertEqual(ttps[0]['tts'][0]['tactic_name'], 'Persistence')
        self.assertEqual(ttps[0]['tts'][0]['tactic_id'], 'TA0003')
        self.assertEqual(ttps[0]['tts'][0]['technique_name'], 'DLLSide-Loading')
        self.assertEqual(ttps[0]['tts'][0]['technique_id'], 'T1574.002')
    
        self.assertEqual(ttps[1]['sent'], 'It will then create a reverse shell via ncat.exe to the server closed.theworkpc.com')
        self.assertEqual(ttps[1]['tts'][0]['tactic_name'], 'Execution')
        self.assertEqual(ttps[1]['tts'][0]['tactic_id'], 'TA0002')
        self.assertEqual(ttps[1]['tts'][0]['technique_name'], 'WindowsCommandShell')
        self.assertEqual(ttps[1]['tts'][0]['technique_id'], 'T1059.003')
    
    def test_tn_text(self):
        text = "The general infection chain of REvil"
        o_text, ttps = predict_text(text)
        self.assertEqual(o_text, text)
        self.assertEqual(ttps, [{
            'sent': text,
            'tts': []
        }])
        

if __name__ == '__main__':
    unittest.main()