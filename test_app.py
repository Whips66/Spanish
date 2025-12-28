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
                self.assertIn('perfecto', verb_data)
                self.assertIn('pluscuamperfecto', verb_data)
                self.assertIn('futuro perfecto', verb_data)
                self.assertIn('presente subjuntivo', verb_data)
                self.assertIn('imperfecto subjuntivo', verb_data)
    
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
    
    def test_compound_tenses_structure(self):
        """Test that compound tenses have correct structure"""
        for verb_name, verb_data in VERBS.items():
            with self.subTest(verb=verb_name):
                # Check perfecto has "haber" conjugations
                perfecto = verb_data['perfecto']
                for pronoun in PRONOUNS:
                    self.assertIn(pronoun, perfecto)
                    # Should contain a space (haber + participle)
                    self.assertIn(' ', perfecto[pronoun], 
                                f"{verb_name} perfecto should be compound")
                
                # Check pluscuamperfecto has "haber" conjugations
                pluscuamperfecto = verb_data['pluscuamperfecto']
                for pronoun in PRONOUNS:
                    self.assertIn(pronoun, pluscuamperfecto)
                    # Should contain a space (haber + participle)
                    self.assertIn(' ', pluscuamperfecto[pronoun],
                                f"{verb_name} pluscuamperfecto should be compound")
                
                # Check futuro perfecto has "haber" conjugations
                futuro_perfecto = verb_data['futuro perfecto']
                for pronoun in PRONOUNS:
                    self.assertIn(pronoun, futuro_perfecto)
                    # Should contain a space (haber + participle)
                    self.assertIn(' ', futuro_perfecto[pronoun],
                                f"{verb_name} futuro perfecto should be compound")
    
    def test_compound_tenses_use_haber(self):
        """Test that compound tenses use correct forms of haber"""
        for verb_name, verb_data in VERBS.items():
            with self.subTest(verb=verb_name):
                # Perfecto should start with present tense of haber
                perfecto_yo = verb_data['perfecto']['yo']
                self.assertTrue(perfecto_yo.startswith('he '))
                
                # Pluscuamperfecto should start with imperfect tense of haber
                pluscuamperfecto_yo = verb_data['pluscuamperfecto']['yo']
                self.assertTrue(pluscuamperfecto_yo.startswith('había '))
                
                # Futuro perfecto should start with future tense of haber
                futuro_perfecto_yo = verb_data['futuro perfecto']['yo']
                self.assertTrue(futuro_perfecto_yo.startswith('habré '))


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
        self.assertIn(data['question_type'], ['conjugation', 'identify-tense', 'identify-pronoun', 'identify-infinitive'])
        
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
        
        elif data['question_type'] == 'identify-infinitive':
            # Identify infinitive question checks
            self.assertIn('conjugated_form', data)
            self.assertIn(data['tense'], TENSES)
            self.assertIn(data['pronoun'], PRONOUNS)
            
            # Correct answer should be a verb infinitive
            self.assertIn(data['correct_answer'], VERBS.keys())
            
            # Options should be verb infinitives
            for option in data['options']:
                self.assertIn(option, VERBS.keys())
    
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
    
    def test_check_answer_with_tense_description(self):
        """Test that tense description is returned when tense is provided"""
        # Get a question first
        response = self.client.get('/api/question')
        question_data = json.loads(response.data)
        
        # Submit answer with tense (mimicking conjugation question)
        if 'tense' in question_data:
            check_response = self.client.post('/api/check',
                                            json={
                                                'answer': question_data['correct_answer'],
                                                'correct_answer': question_data['correct_answer'],
                                                'tense': question_data['tense']
                                            },
                                            content_type='application/json')
            
            check_data = json.loads(check_response.data)
            
            # Should include tense description
            self.assertIn('tense_description', check_data)
            self.assertIn('tense_name', check_data)
            self.assertIsInstance(check_data['tense_description'], str)
            self.assertGreater(len(check_data['tense_description']), 0)
    
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
        """Test that all question types appear"""
        question_types = set()
        for _ in range(150):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            question_types.add(data['question_type'])
        
        # All four question types should appear
        self.assertIn('conjugation', question_types)
        self.assertIn('identify-tense', question_types)
        self.assertIn('identify-pronoun', question_types)
        self.assertIn('identify-infinitive', question_types)
    
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
        """Test that each question type appears approximately 25% of the time"""
        iterations = 400
        identify_tense_count = 0
        identify_pronoun_count = 0
        identify_infinitive_count = 0
        conjugation_count = 0
        
        for _ in range(iterations):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            if data['question_type'] == 'identify-tense':
                identify_tense_count += 1
            elif data['question_type'] == 'identify-pronoun':
                identify_pronoun_count += 1
            elif data['question_type'] == 'identify-infinitive':
                identify_infinitive_count += 1
            else:
                conjugation_count += 1
        
        tense_freq = identify_tense_count / iterations
        pronoun_freq = identify_pronoun_count / iterations
        infinitive_freq = identify_infinitive_count / iterations
        conjugation_freq = conjugation_count / iterations
        
        # Each should be around 25% (allow 15-35% due to randomness)
        self.assertGreater(tense_freq, 0.15)
        self.assertLess(tense_freq, 0.35)
        self.assertGreater(pronoun_freq, 0.15)
        self.assertLess(pronoun_freq, 0.35)
        self.assertGreater(infinitive_freq, 0.15)
        self.assertLess(infinitive_freq, 0.35)
        self.assertGreater(conjugation_freq, 0.15)
        self.assertLess(conjugation_freq, 0.35)


class TestIdentifyPronounQuestions(unittest.TestCase):
    """Test the identify-pronoun question type"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_identify_pronoun_structure(self):
        """Test identify-pronoun question has correct structure"""
        # Get multiple questions until we find an identify-pronoun one
        for _ in range(50):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-pronoun':
                # Check required fields
                self.assertIn('verb', data)
                self.assertIn('english', data)
                self.assertIn('tense', data)
                self.assertIn('tense_name', data)
                self.assertIn('conjugated_form', data)
                self.assertIn('pronoun', data)
                self.assertIn('options', data)
                self.assertIn('correct_answer', data)
                
                # Check that conjugated form is valid
                verb_data = VERBS[data['verb']]
                expected_form = verb_data[data['tense']][data['pronoun']]
                self.assertEqual(data['conjugated_form'], expected_form)
                
                # Check options are pronouns
                for option in data['options']:
                    self.assertIn(option, PRONOUNS)
                
                # Check correct answer matches the pronoun
                self.assertEqual(data['correct_answer'], data['pronoun'])
                self.assertIn(data['correct_answer'], PRONOUNS)
                
                # Check we have 4 unique pronoun options
                self.assertEqual(len(data['options']), 4)
                self.assertEqual(len(set(data['options'])), 4)
                
                break
    
    def test_identify_pronoun_coverage(self):
        """Test that all pronouns can appear as correct answers"""
        pronouns_seen = set()
        
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-pronoun':
                pronouns_seen.add(data['correct_answer'])
        
        # Should see multiple different pronouns
        self.assertGreater(len(pronouns_seen), 3)
    
    def test_identify_pronoun_multiple_correct_answers(self):
        """Test that ambiguous conjugations return all correct answers"""
        # Find a question with ambiguous conjugation (same form for multiple pronouns)
        found_ambiguous = False
        
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-pronoun':
                # Check if all_correct_answers exists and has multiple values
                if 'all_correct_answers' in data and len(data['all_correct_answers']) > 1:
                    found_ambiguous = True
                    
                    # Verify all correct answers have the same conjugation
                    verb_data = VERBS[data['verb']]
                    tense = data['tense']
                    conjugated_form = data['conjugated_form']
                    
                    for pronoun in data['all_correct_answers']:
                        self.assertEqual(verb_data[tense][pronoun], conjugated_form,
                                       f"All pronouns in all_correct_answers should have the same conjugation")
                    
                    # Verify the main correct_answer is in the list
                    self.assertIn(data['correct_answer'], data['all_correct_answers'])
                    
                    break
        
        # We should find at least one ambiguous case (common in imperfecto, condicional)
        self.assertTrue(found_ambiguous, "Should find at least one case with multiple correct answers")
    
    def test_identify_pronoun_accepts_any_valid_answer(self):
        """Test that any of the multiple correct answers is accepted"""
        # Find an ambiguous question
        for _ in range(100):
            response = self.client.get('/api/question')
            question_data = json.loads(response.data)
            
            if (question_data['question_type'] == 'identify-pronoun' and 
                'all_correct_answers' in question_data and 
                len(question_data['all_correct_answers']) > 1):
                
                # Test that each correct answer is accepted
                for correct_pronoun in question_data['all_correct_answers']:
                    check_response = self.client.post('/api/check',
                                                     json={
                                                         'answer': correct_pronoun,
                                                         'correct_answer': question_data['correct_answer'],
                                                         'all_correct_answers': question_data['all_correct_answers'],
                                                         'question_type': 'identify-pronoun'
                                                     },
                                                     content_type='application/json')
                    
                    check_data = json.loads(check_response.data)
                    self.assertTrue(check_data['correct'],
                                  f"{correct_pronoun} should be accepted as correct")
                
                break


class TestIdentifyInfinitiveQuestions(unittest.TestCase):
    """Test the identify-infinitive question type"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_identify_infinitive_structure(self):
        """Test identify-infinitive question has correct structure"""
        # Get multiple questions until we find an identify-infinitive one
        for _ in range(50):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-infinitive':
                # Check required fields
                self.assertIn('verb', data)
                self.assertIn('english', data)
                self.assertIn('tense', data)
                self.assertIn('tense_name', data)
                self.assertIn('pronoun', data)
                self.assertIn('conjugated_form', data)
                self.assertIn('options', data)
                self.assertIn('correct_answer', data)
                
                # Check that conjugated form is valid
                verb_data = VERBS[data['verb']]
                expected_form = verb_data[data['tense']][data['pronoun']]
                self.assertEqual(data['conjugated_form'], expected_form)
                
                # Check options are verb infinitives
                for option in data['options']:
                    self.assertIn(option, VERBS.keys())
                
                # Check correct answer is the verb
                self.assertEqual(data['correct_answer'], data['verb'])
                self.assertIn(data['correct_answer'], VERBS.keys())
                
                # Check we have 4 unique verb options
                self.assertEqual(len(data['options']), 4)
                self.assertEqual(len(set(data['options'])), 4)
                
                break
    
    def test_identify_infinitive_coverage(self):
        """Test that multiple verbs can appear as correct answers"""
        verbs_seen = set()
        
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data['question_type'] == 'identify-infinitive':
                verbs_seen.add(data['correct_answer'])
        
        # Should see multiple different verbs
        self.assertGreater(len(verbs_seen), 5)


class TestCompoundTenseQuestions(unittest.TestCase):
    """Test that compound tenses appear in questions"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_compound_tenses_in_questions(self):
        """Test that perfecto, pluscuamperfecto, and futuro perfecto appear in questions"""
        tenses_seen = set()
        
        for _ in range(200):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if 'tense' in data:
                tenses_seen.add(data['tense'])
        
        # Should see all compound tenses
        self.assertIn('perfecto', tenses_seen)
        self.assertIn('pluscuamperfecto', tenses_seen)
        self.assertIn('futuro perfecto', tenses_seen)
    
    def test_compound_tense_conjugation_question(self):
        """Test that compound tenses can be used in conjugation questions"""
        found_compound = False
        
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            if data.get('question_type') == 'conjugation' and data.get('tense') in ['perfecto', 'pluscuamperfecto', 'futuro perfecto']:
                found_compound = True
                
                # Verify the correct answer is a compound form
                self.assertIn(' ', data['correct_answer'], 
                            "Compound tense should have space (haber + participle)")
                break
        
        self.assertTrue(found_compound, "Should find at least one compound tense question")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_all_question_types_have_enough_options(self):
        """Test that all question types can generate 4 unique options"""
        for _ in range(100):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            # Should always have 4 options
            self.assertEqual(len(data['options']), 4)
            
            # All options should be unique
            self.assertEqual(len(set(data['options'])), 4, 
                           f"Duplicate options in {data['question_type']} question")
    
    def test_check_answer_handles_whitespace(self):
        """Test that answer checking handles extra whitespace"""
        response = self.client.get('/api/question')
        question_data = json.loads(response.data)
        
        # Add extra whitespace to answer
        answer_with_space = f"  {question_data['correct_answer']}  "
        
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': answer_with_space,
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        check_data = json.loads(check_response.data)
        self.assertTrue(check_data['correct'])
    
    def test_special_characters_in_conjugations(self):
        """Test that Spanish special characters are handled correctly"""
        found_special_char = False
        special_chars = ['á', 'é', 'í', 'ó', 'ú', 'ñ', 'ü']
        
        for _ in range(50):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            correct_answer = data['correct_answer']
            
            # Check if any special character is in the answer
            if any(char in correct_answer for char in special_chars):
                found_special_char = True
                
                # Verify it's properly encoded
                self.assertIsInstance(correct_answer, str)
                break
        
        self.assertTrue(found_special_char, "Should find conjugations with Spanish characters")
    
    def test_question_type_distribution(self):
        """Test that all 4 question types are reasonably distributed"""
        type_counts = {
            'conjugation': 0,
            'identify-tense': 0,
            'identify-pronoun': 0,
            'identify-infinitive': 0
        }
        
        iterations = 400
        for _ in range(iterations):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            type_counts[data['question_type']] += 1
        
        # Each type should appear at least 15% of the time (allowing for randomness)
        for qtype, count in type_counts.items():
            percentage = count / iterations
            self.assertGreater(percentage, 0.15, 
                             f"{qtype} appeared only {percentage:.1%} of the time")
            self.assertLess(percentage, 0.35,
                          f"{qtype} appeared {percentage:.1%} of the time (too high)")


if __name__ == '__main__':
    unittest.main()
