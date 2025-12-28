import unittest
import json
from app import app, VERBS

class TestIntegration(unittest.TestCase):
    """Integration tests for complete user workflows"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_complete_question_flow(self):
        """Test complete flow: get question -> answer -> check"""
        # Step 1: Get a question
        question_response = self.client.get('/api/question')
        self.assertEqual(question_response.status_code, 200)
        question_data = json.loads(question_response.data)
        
        # Step 2: Answer the question correctly
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': question_data['correct_answer'],
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        self.assertEqual(check_response.status_code, 200)
        check_data = json.loads(check_response.data)
        self.assertTrue(check_data['correct'])
    
    def test_multiple_questions(self):
        """Test answering multiple questions in sequence"""
        correct_count = 0
        total_questions = 5
        
        for _ in range(total_questions):
            # Get question
            question_response = self.client.get('/api/question')
            question_data = json.loads(question_response.data)
            
            # Answer correctly
            check_response = self.client.post('/api/check',
                                             json={
                                                 'answer': question_data['correct_answer'],
                                                 'correct_answer': question_data['correct_answer']
                                             },
                                             content_type='application/json')
            
            check_data = json.loads(check_response.data)
            if check_data['correct']:
                correct_count += 1
        
        # All answers should be correct
        self.assertEqual(correct_count, total_questions)
    
    def test_all_tenses_coverage(self):
        """Test that all tenses appear in questions over time"""
        tenses_seen = set()
        max_attempts = 50
        
        for _ in range(max_attempts):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            tenses_seen.add(data['tense'])
            
            # If we've seen all tenses, break early
            if len(tenses_seen) == 5:
                break
        
        # We should see all 5 tenses
        self.assertEqual(len(tenses_seen), 5)
    
    def test_all_pronouns_coverage(self):
        """Test that all pronouns appear in questions over time"""
        pronouns_seen = set()
        max_attempts = 50
        
        for _ in range(max_attempts):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            pronouns_seen.add(data['pronoun'])
            
            # If we've seen all pronouns, break early
            if len(pronouns_seen) == 6:
                break
        
        # We should see all 6 pronouns
        self.assertEqual(len(pronouns_seen), 6)
    
    def test_options_are_all_different(self):
        """Test that the 4 options in a question are unique"""
        for _ in range(20):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            
            options = data['options']
            unique_options = set(options)
            
            # All options should be unique
            # Note: For identify-pronoun, we have 6 pronouns so can always get 4 unique
            # For identify-tense, we have 7 tenses so can always get 4 unique
            # For conjugation, we have many conjugations so should get 4 unique
            self.assertEqual(len(unique_options), len(options), 
                           f"Duplicate options in {data['question_type']} question")
    
    def test_wrong_answer_shows_correct_one(self):
        """Test that wrong answers return the correct answer"""
        # Get question
        question_response = self.client.get('/api/question')
        question_data = json.loads(question_response.data)
        
        # Submit wrong answer
        check_response = self.client.post('/api/check',
                                         json={
                                             'answer': 'definitivamente_incorrecto',
                                             'correct_answer': question_data['correct_answer']
                                         },
                                         content_type='application/json')
        
        check_data = json.loads(check_response.data)
        
        # Should be marked incorrect
        self.assertFalse(check_data['correct'])
        
        # Should return the correct answer
        self.assertEqual(check_data['correct_answer'], question_data['correct_answer'])


class TestVerbCoverage(unittest.TestCase):
    """Test that all verbs can appear in questions"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_all_verbs_can_appear(self):
        """Test that all verbs in database can appear in questions"""
        verbs_seen = set()
        max_attempts = 200
        
        for _ in range(max_attempts):
            response = self.client.get('/api/question')
            data = json.loads(response.data)
            verbs_seen.add(data['verb'])
            
            # If we've seen all verbs, break early
            if len(verbs_seen) == len(VERBS):
                break
        
        # We should see a good variety of verbs (at least 20 out of 25)
        self.assertGreaterEqual(len(verbs_seen), 20)


if __name__ == '__main__':
    unittest.main()
