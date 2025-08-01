#!/usr/bin/env python3
"""
Comprehensive Backend API Test Suite for Blotato Clone
Tests all endpoints with proper authentication and error handling
"""

import requests
import json
import os
from datetime import datetime
import sys

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    return "http://localhost:8001"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")

class BlotoatoAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_data = None
        self.content_id = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'total': 0
        }
        
        # Test user data
        self.test_user = {
            "name": "Sarah Johnson",
            "email": f"sarah.johnson.{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "SecurePass123!"
        }

    def assert_response(self, response, expected_status, test_name, expected_keys=None):
        """Assert response status and optionally check for expected keys"""
        self.test_results['total'] += 1
        
        try:
            if response.status_code != expected_status:
                print_error(f"{test_name}: Expected status {expected_status}, got {response.status_code}")
                if response.text:
                    print_error(f"Response: {response.text}")
                self.test_results['failed'] += 1
                return False
            
            if expected_keys and response.status_code == 200:
                try:
                    data = response.json()
                    for key in expected_keys:
                        if key not in data:
                            print_error(f"{test_name}: Missing key '{key}' in response")
                            self.test_results['failed'] += 1
                            return False
                except json.JSONDecodeError:
                    print_error(f"{test_name}: Invalid JSON response")
                    self.test_results['failed'] += 1
                    return False
            
            print_success(f"{test_name}: Status {response.status_code}")
            self.test_results['passed'] += 1
            return True
            
        except Exception as e:
            print_error(f"{test_name}: Exception occurred - {str(e)}")
            self.test_results['failed'] += 1
            return False

    def test_health_check(self):
        """Test the health check endpoint"""
        print_header("TESTING HEALTH CHECK ENDPOINT")
        
        try:
            response = self.session.get(f"{API_URL}/")
            if self.assert_response(response, 200, "Health Check", ["message", "status"]):
                data = response.json()
                if data.get("message") == "Blotato Clone API is running!" and data.get("status") == "healthy":
                    print_success("Health check response content is correct")
                else:
                    print_warning("Health check response content differs from expected")
                    print_info(f"Response: {data}")
        except requests.exceptions.RequestException as e:
            print_error(f"Health Check: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print_header("TESTING AUTHENTICATION FLOW")
        
        # Test signup
        print_info("Testing user signup...")
        try:
            response = self.session.post(f"{API_URL}/auth/signup", json=self.test_user)
            if self.assert_response(response, 200, "User Signup", ["success", "user", "token"]):
                data = response.json()
                if data.get("success"):
                    self.auth_token = data.get("token")
                    self.user_data = data.get("user")
                    print_success(f"User created with ID: {self.user_data.get('id')}")
                    
                    # Set authorization header for future requests
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                else:
                    print_error("Signup response indicates failure")
        except requests.exceptions.RequestException as e:
            print_error(f"User Signup: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1
            return

        # Test duplicate signup (should fail)
        print_info("Testing duplicate signup (should fail)...")
        try:
            response = self.session.post(f"{API_URL}/auth/signup", json=self.test_user)
            self.assert_response(response, 400, "Duplicate Signup (Expected Failure)")
        except requests.exceptions.RequestException as e:
            print_error(f"Duplicate Signup Test: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test login
        print_info("Testing user login...")
        try:
            login_data = {
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
            response = self.session.post(f"{API_URL}/auth/login", json=login_data)
            if self.assert_response(response, 200, "User Login", ["success", "user", "token"]):
                data = response.json()
                if data.get("success"):
                    # Update token in case it's different
                    self.auth_token = data.get("token")
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    print_success("Login successful, token updated")
        except requests.exceptions.RequestException as e:
            print_error(f"User Login: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test invalid login
        print_info("Testing invalid login (should fail)...")
        try:
            invalid_login = {
                "email": self.test_user["email"],
                "password": "wrongpassword"
            }
            response = self.session.post(f"{API_URL}/auth/login", json=invalid_login)
            self.assert_response(response, 401, "Invalid Login (Expected Failure)")
        except requests.exceptions.RequestException as e:
            print_error(f"Invalid Login Test: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test get current user
        print_info("Testing get current user...")
        try:
            response = self.session.get(f"{API_URL}/auth/me")
            if self.assert_response(response, 200, "Get Current User", ["id", "name", "email"]):
                data = response.json()
                if data.get("email") == self.test_user["email"]:
                    print_success("Current user data matches expected")
                else:
                    print_warning("Current user data differs from expected")
        except requests.exceptions.RequestException as e:
            print_error(f"Get Current User: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test logout
        print_info("Testing user logout...")
        try:
            response = self.session.post(f"{API_URL}/auth/logout")
            self.assert_response(response, 200, "User Logout", ["success", "message"])
        except requests.exceptions.RequestException as e:
            print_error(f"User Logout: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

    def test_public_endpoints(self):
        """Test public data endpoints"""
        print_header("TESTING PUBLIC DATA ENDPOINTS")
        
        # Test testimonials
        print_info("Testing get testimonials...")
        try:
            response = self.session.get(f"{API_URL}/public/testimonials")
            if self.assert_response(response, 200, "Get Testimonials"):
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print_success(f"Retrieved {len(data)} testimonials")
                    # Check first testimonial structure
                    if data[0].get("name") and data[0].get("content"):
                        print_success("Testimonial structure is correct")
                    else:
                        print_warning("Testimonial structure may be incomplete")
                else:
                    print_warning("No testimonials found or invalid format")
        except requests.exceptions.RequestException as e:
            print_error(f"Get Testimonials: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test features
        print_info("Testing get features...")
        try:
            response = self.session.get(f"{API_URL}/public/features")
            if self.assert_response(response, 200, "Get Features"):
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print_success(f"Retrieved {len(data)} features")
                    # Check first feature structure
                    if data[0].get("title") and data[0].get("description"):
                        print_success("Feature structure is correct")
                    else:
                        print_warning("Feature structure may be incomplete")
                else:
                    print_warning("No features found or invalid format")
        except requests.exceptions.RequestException as e:
            print_error(f"Get Features: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test FAQs
        print_info("Testing get FAQs...")
        try:
            response = self.session.get(f"{API_URL}/public/faqs")
            if self.assert_response(response, 200, "Get FAQs"):
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print_success(f"Retrieved {len(data)} FAQs")
                    # Check first FAQ structure
                    if data[0].get("question") and data[0].get("answer"):
                        print_success("FAQ structure is correct")
                    else:
                        print_warning("FAQ structure may be incomplete")
                else:
                    print_warning("No FAQs found or invalid format")
        except requests.exceptions.RequestException as e:
            print_error(f"Get FAQs: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

    def test_content_management(self):
        """Test content management endpoints"""
        print_header("TESTING CONTENT MANAGEMENT")
        
        if not self.auth_token:
            print_error("No auth token available, skipping content management tests")
            return

        # Test get empty content list
        print_info("Testing get user content (should be empty)...")
        try:
            response = self.session.get(f"{API_URL}/content")
            if self.assert_response(response, 200, "Get User Content (Empty)"):
                data = response.json()
                if isinstance(data, list):
                    print_success(f"Retrieved content list with {len(data)} items")
                else:
                    print_warning("Content response is not a list")
        except requests.exceptions.RequestException as e:
            print_error(f"Get User Content: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test create content
        print_info("Testing create content...")
        content_data = {
            "title": "My First LinkedIn Post",
            "type": "post",
            "platform": "LinkedIn",
            "content": "Excited to share my journey in content creation! 🚀 Using AI tools to scale my social media presence has been a game-changer. #ContentCreation #AI #LinkedIn"
        }
        
        try:
            response = self.session.post(f"{API_URL}/content", json=content_data)
            if self.assert_response(response, 200, "Create Content", ["id", "title", "type", "platform", "content"]):
                data = response.json()
                self.content_id = data.get("id")
                print_success(f"Content created with ID: {self.content_id}")
                
                # Verify content data
                if (data.get("title") == content_data["title"] and 
                    data.get("type") == content_data["type"] and
                    data.get("platform") == content_data["platform"]):
                    print_success("Content data matches input")
                else:
                    print_warning("Content data differs from input")
        except requests.exceptions.RequestException as e:
            print_error(f"Create Content: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test get content list again (should have 1 item)
        print_info("Testing get user content (should have 1 item)...")
        try:
            response = self.session.get(f"{API_URL}/content")
            if self.assert_response(response, 200, "Get User Content (With Items)"):
                data = response.json()
                if isinstance(data, list) and len(data) == 1:
                    print_success("Content list now contains 1 item")
                    if data[0].get("id") == self.content_id:
                        print_success("Content ID matches created content")
                else:
                    print_warning(f"Expected 1 content item, got {len(data) if isinstance(data, list) else 'non-list'}")
        except requests.exceptions.RequestException as e:
            print_error(f"Get User Content (With Items): Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test update content
        if self.content_id:
            print_info("Testing update content...")
            update_data = {
                "status": "published",
                "title": "My Updated LinkedIn Post"
            }
            
            try:
                response = self.session.put(f"{API_URL}/content/{self.content_id}", json=update_data)
                if self.assert_response(response, 200, "Update Content", ["id", "title", "status"]):
                    data = response.json()
                    if (data.get("status") == "published" and 
                        data.get("title") == "My Updated LinkedIn Post"):
                        print_success("Content updated successfully")
                    else:
                        print_warning("Content update may not have applied correctly")
            except requests.exceptions.RequestException as e:
                print_error(f"Update Content: Connection error - {str(e)}")
                self.test_results['total'] += 1
                self.test_results['failed'] += 1

        # Test delete content
        if self.content_id:
            print_info("Testing delete content...")
            try:
                response = self.session.delete(f"{API_URL}/content/{self.content_id}")
                if self.assert_response(response, 200, "Delete Content", ["success", "message"]):
                    data = response.json()
                    if data.get("success"):
                        print_success("Content deleted successfully")
                    else:
                        print_warning("Delete response indicates failure")
            except requests.exceptions.RequestException as e:
                print_error(f"Delete Content: Connection error - {str(e)}")
                self.test_results['total'] += 1
                self.test_results['failed'] += 1

        # Test get content list after deletion (should be empty)
        print_info("Testing get user content after deletion (should be empty)...")
        try:
            response = self.session.get(f"{API_URL}/content")
            if self.assert_response(response, 200, "Get User Content (After Deletion)"):
                data = response.json()
                if isinstance(data, list) and len(data) == 0:
                    print_success("Content list is empty after deletion")
                else:
                    print_warning(f"Expected empty content list, got {len(data) if isinstance(data, list) else 'non-list'} items")
        except requests.exceptions.RequestException as e:
            print_error(f"Get User Content (After Deletion): Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

    def test_analytics_endpoints(self):
        """Test analytics endpoints"""
        print_header("TESTING ANALYTICS ENDPOINTS")
        
        if not self.auth_token:
            print_error("No auth token available, skipping analytics tests")
            return

        # Test get user stats
        print_info("Testing get user stats...")
        try:
            response = self.session.get(f"{API_URL}/analytics/stats")
            if self.assert_response(response, 200, "Get User Stats", ["posts_created", "videos_generated", "total_engagement", "followers_growth"]):
                data = response.json()
                print_success(f"Stats: {data.get('posts_created')} posts, {data.get('videos_generated')} videos, {data.get('total_engagement')} engagement, {data.get('followers_growth')} followers growth")
        except requests.exceptions.RequestException as e:
            print_error(f"Get User Stats: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

        # Test get recent content
        print_info("Testing get recent content...")
        try:
            response = self.session.get(f"{API_URL}/analytics/recent-content")
            if self.assert_response(response, 200, "Get Recent Content"):
                data = response.json()
                if isinstance(data, list):
                    print_success(f"Retrieved {len(data)} recent content items")
                else:
                    print_warning("Recent content response is not a list")
        except requests.exceptions.RequestException as e:
            print_error(f"Get Recent Content: Connection error - {str(e)}")
            self.test_results['total'] += 1
            self.test_results['failed'] += 1

    def test_authentication_protection(self):
        """Test that protected endpoints require authentication"""
        print_header("TESTING AUTHENTICATION PROTECTION")
        
        # Create a session without auth token
        unauth_session = requests.Session()
        
        protected_endpoints = [
            ("GET", f"{API_URL}/auth/me", "Get Current User"),
            ("POST", f"{API_URL}/auth/logout", "Logout"),
            ("GET", f"{API_URL}/content", "Get Content"),
            ("POST", f"{API_URL}/content", "Create Content"),
            ("GET", f"{API_URL}/analytics/stats", "Get Stats"),
            ("GET", f"{API_URL}/analytics/recent-content", "Get Recent Content")
        ]
        
        for method, url, name in protected_endpoints:
            print_info(f"Testing {name} without authentication...")
            try:
                if method == "GET":
                    response = unauth_session.get(url)
                elif method == "POST":
                    response = unauth_session.post(url, json={})
                
                self.assert_response(response, 401, f"{name} (Unauthorized - Expected)")
            except requests.exceptions.RequestException as e:
                print_error(f"{name} (Unauthorized Test): Connection error - {str(e)}")
                self.test_results['total'] += 1
                self.test_results['failed'] += 1

    def run_all_tests(self):
        """Run all test suites"""
        print_header(f"STARTING BLOTATO CLONE BACKEND API TESTS")
        print_info(f"Testing against: {API_URL}")
        print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run test suites
        self.test_health_check()
        self.test_public_endpoints()
        self.test_authentication_flow()
        self.test_content_management()
        self.test_analytics_endpoints()
        self.test_authentication_protection()
        
        # Print final results
        print_header("TEST RESULTS SUMMARY")
        print_info(f"Total Tests: {self.test_results['total']}")
        print_success(f"Passed: {self.test_results['passed']}")
        print_error(f"Failed: {self.test_results['failed']}")
        
        if self.test_results['failed'] == 0:
            print_success("🎉 ALL TESTS PASSED!")
            return True
        else:
            success_rate = (self.test_results['passed'] / self.test_results['total']) * 100
            print_warning(f"Success Rate: {success_rate:.1f}%")
            if success_rate >= 80:
                print_warning("⚠️  Most tests passed, but some issues found")
            else:
                print_error("❌ Multiple test failures detected")
            return False

if __name__ == "__main__":
    tester = BlotoatoAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)