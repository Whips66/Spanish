import unittest
import json
import os
from app import app, load_verbs, VERBS, PRONOUNS, TENSES

class TestVerbDatabase(unittest.TestCase):
    """Test verb database loading and structure"""
    
    def test_load_verbs(self):
        """Test that verbs.json loads correctly"""
        verbs = load_verbs()
        self.assertIsInstance(verbs, dict)
        self.assertGreater(len(verbs), 0)
    
    def test_verb_structure(self):
        """Test that each verb has required fields"""
        for verb_name, verb_data in VERBS.items():
            with self.subTest(verb=verb_name):
                self.assertIn('english', verb_data)
                self.assertIn('type', verb_data)
                self.assertIn('presente', verb_data)
                self.assertIn('pretérito', verb_data)
                self.assertIn('imperfecto', verb_data)
                self.assertIn('futuro', verb_data)
                self.assertIn('condicional', verb_data)
    
    def test_verb_conjugations(self):
        """Test that each tense has all pronouns"""
        for verb_name, verb_data in VERBS.items():
            for tense in TENSES:
                with self.subTest(verb=verb_name, tense=tense):
                    self.assertIn(tense, verb_data)
                    conjugations = verb_data[tense]
                    for pronoun in PRONOUNS:
                        self.assertIn(pronoun, conjugations)
                        self.assertIsInstance(conjugations[pronoun], str)
                        self.assertGreater(len(conjugations[pronoun]), 0)
    
    def test_minimum_verb_count(self):
        """Test that we have at least 25 verbs"""
        self.assertGreaterEqual(len(VERBS), 25)
    
    def test_verb_types(self):
        """Test that verb types are valid"""
        valid_types = ['regular', 'irregular']
        for verb_name, verb_data in VERBS.items():
            with self.subTest(verb=verb_name):
                self.assertIn(verb_data['type'], valid_types)


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test that the index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Spanish Verb Practice', response.data)
    
    def test_get_question_route(self):
        """Test the /api/question endpoint"""
        response = self.client.get('/api/question')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('verb', data)
        self.assertIn('english', data)
        self.assertIn('pronoun', data)
        self.assertIn('tense', data)
        self.assertIn('options', data)
        self.assertIn('correct_answer', data)
        
        # tense_english only appears in conjugation questions
        if data.get('question_type') == 'conjugation':
            self.assertIn('tense_english', data)
    
    def test_question_structure(self):
        """Test that question data is valid"""
        response = self.client.get('/api/question')
        data = json.loads(response.data)
        
        # Check question type exists
        self.assertIn('question_type', data)
        self.assertIn(data['question_type'], ['conjugation', 'identify-tense', 'identify-pronoun'])
        
        # Check verb is from our database
        self.assertIn(data['verb'], VERBS)
        
        # Check common fields
        self.assertIn('options', data)
        self.assertIsInstance(data['options'], list)
        self.assertEqual(len(data['options']), 4)
        self.assertIn(data['correct_answer'], data['options'])
        
        if data['question_type'] == 'conjugation':
            # Standard conjugation question checks
            self.assertIn(data['pronoun'], PRONOUNS)
            self.assertIn(data['tense'], TENSES)
            
            # Check correct answer matches the verb conjugation
            verb_data = VERBS[data['verb']]
            expected_answer = verb_data[data['tense']][data['pronoun']]
            self.assertEqual(data['correct_answer'], expected_answer)
        
        elif data['question_type'] == 'identify-tense':
            # Identify tense question checks
            self.assertIn('conjugated_form', data)
            self.assertIn(data['pronoun'], PRONOUNS)
            
            # Correct answer should be a tense name in English
            from app import TENSE_NAMES
            self.assertIn(data['correct_answer'], TENSE_NAMES.values())
            
            # Options should be tense names
            for option in data['options']:
                self.assertIn(option, TENSE_NAMES.values())
        
        elif data['question_type'] == 'identify-pronoun':
            # Identify pronoun question checks
            self.assertIn('conjugated_form', data)
            self.assertIn(data['tense'], TENSES)
            
            # Correct answer should be a pronoun
            self.assertIn(data['correct_answer'], PRONOUNS)
            
            # Options should be pronouns
            for option in data['options']:
                self.assertIn(option, PRONOUNS)
    
    def test_question_randomness(self):
        """Test that questions are randomized"""
        questions = []
        for _ in range(10):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            questions.append((data['verb'], data['pronoun'], data['tense']))
        
        # Check that we get different questions (not all the same)
        unique_questions = set(questions)
        self.assertGreater(len(unique_questions), 1)
    
    def test_check_answer_correct(self):
        """Test checking a correct answer"""
        # Get a question first
        response = self.client.get('/api/question')
        question_data = json.loads(response.data)
        
        # Submit the correct answer
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': question_data['correct_answer'],
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        self.assertEqual(check_response.status_code, 200)
        check_data = json.loads(check_response.data)
        self.assertTrue(check_data['correct'])
        self.assertEqual(check_data['correct_answer'], question_data['correct_answer'])
    
    def test_check_answer_incorrect(self):
        """Test checking an incorrect answer"""
        # Get a question first
        response = self.client.get('/api/question')
        question_data = json.loads(response.data)
        
        # Submit a wrong answer
        wrong_answer = 'wronganswer123'
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': wrong_answer,
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        self.assertEqual(check_response.status_code, 200)
        check_data = json.loads(check_response.data)
        self.assertFalse(check_data['correct'])
        self.assertEqual(check_data['correct_answer'], question_data['correct_answer'])
    
    def test_check_answer_case_insensitive(self):
        """Test that answer checking is case-insensitive"""
        response = self.client.get('/api/question')
        question_data = json.loads(response.data)
        
        # Submit answer with different case
        upper_answer = question_data['correct_answer'].upper()
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': upper_answer,
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        check_data = json.loads(check_response.data)
        self.assertTrue(check_data['correct'])


class TestTenseNames(unittest.TestCase):
    """Test tense name mappings"""
    
    def test_tense_name_mapping(self):
        """Test that all tenses have English names"""
        from app import TENSE_NAMES
        
        for tense in TENSES:
            self.assertIn(tense, TENSE_NAMES)
            self.assertIsInstance(TENSE_NAMES[tense], str)
            self.assertGreater(len(TENSE_NAMES[tense]), 0)


class TestVerbsJSONFile(unittest.TestCase):
    """Test the verbs.json file integrity"""
    
    def test_json_file_exists(self):
        """Test that verbs.json exists"""
        verbs_path = os.path.join(os.path.dirname(__file__), 'verbs.json')
        self.assertTrue(os.path.exists(verbs_path))
    
    def test_json_file_valid(self):
        """Test that verbs.json is valid JSON"""
        verbs_path = os.path.join(os.path.dirname(__file__), 'verbs.json')
        with open(verbs_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, dict)
            except json.JSONDecodeError as e:
                self.fail(f"Invalid JSON: {e}")
    
    def test_json_encoding(self):
        """Test that verbs.json properly handles Spanish characters"""
        verbs_path = os.path.join(os.path.dirname(__file__), 'verbs.json')
        with open(verbs_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for proper Spanish characters (not escaped)
            self.assertIn('á', content)
            self.assertIn('é', content)
            self.assertIn('í', content)


class TestIdentifyTenseQuestions(unittest.TestCase):
    """Test the new identify-tense question type"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_identify_tense_appears(self):
        """Test that identify-tense questions appear"""
        question_types = set()
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            question_types.add(data['question_type'])
        
        # All three question types should appear
        self.assertIn('conjugation', question_types)
        self.assertIn('identify-tense', question_types)
        self.assertIn('identify-pronoun', question_types)
    
    def test_identify_tense_structure(self):
        """Test identify-tense question has correct structure"""
        # Get multiple questions until we find an identify-tense one
        for _ in range(50):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-tense':
                # Check required fields
                self.assertIn('verb', data)
                self.assertIn('english', data)
                self.assertIn('pronoun', data)
                self.assertIn('conjugated_form', data)
                self.assertIn('tense', data)
                self.assertIn('options', data)
                self.assertIn('correct_answer', data)
                
                # Check that conjugated form is valid
                verb_data = VERBS[data['verb']]
                self.assertIn(data['conjugated_form'], 
                            [verb_data[t][data['pronoun']] for t in TENSES])
                
                # Check options are tense names
                from app import TENSE_NAMES
                for option in data['options']:
                    self.assertIn(option, TENSE_NAMES.values())
                
                # Check correct answer matches the tense
                expected_tense_name = TENSE_NAMES[data['tense']]
                self.assertEqual(data['correct_answer'], expected_tense_name)
                
                break
    
    def test_identify_tense_frequency(self):
        """Test that each question type appears approximately 33% of the time"""
        iterations = 300
        identify_tense_count = 0
        identify_pronoun_count = 0
        conjugation_count = 0
        
        for _ in range(iterations):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            if data['question_type'] == 'identify-tense':
                identify_tense_count += 1
            elif data['question_type'] == 'identify-pronoun':
                identify_pronoun_count += 1
            else:
                conjugation_count += 1
        
        tense_freq = identify_tense_count / iterations
        pronoun_freq = identify_pronoun_count / iterations
        conjugation_freq = conjugation_count / iterations
        
        # Each should be around 33% (allow 20-46% due to randomness)
        self.assertGreater(tense_freq, 0.20)
        self.assertLess(tense_freq, 0.46)
        self.assertGreater(pronoun_freq, 0.20)
        self.assertLess(pronoun_freq, 0.46)
        self.assertGreater(conjugation_freq, 0.20)
        self.assertLess(conjugation_freq, 0.46)


if __name__ == '__main__':
    unittest.main()
