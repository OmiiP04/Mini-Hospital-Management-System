#!/usr/bin/env python3
"""
Local test server for the email handler
Run this and test with Postman
"""
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from handler import send_email

# Set environment variables
os.environ['GMAIL_USER'] = os.getenv('GMAIL_USER', 'omi131004@gmail.com')
os.environ['GMAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD', 'bbag kmnn ixrp gixm')

class EmailHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"\n--- Request received ---")
        print(f"Headers: {dict(self.headers)}")
        
        if self.path == '/send-email':
            content_length = int(self.headers.get('Content-Length', 0))
            print(f"Content-Length: {content_length}")
            
            if content_length > 0:
                body = self.rfile.read(content_length).decode('utf-8')
            else:
                body = '{}'
            
            print(f"Body received: {body}")
            
            # Call the Lambda handler with proper event structure
            event = {'body': body}
            context = None
            try:
                response = send_email(event, context)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Handler error: {e}")
                import traceback
                traceback.print_exc()
                response = {'statusCode': 500, 'body': json.dumps({'error': str(e)}), 'headers': {'Content-Type': 'application/json'}}
            
            # Send response
            self.send_response(response.get('statusCode', 200))
            for header, value in response.get('headers', {}).items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response['body'].encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('localhost', 3000), EmailHandler)
    print("Email service running on http://localhost:3000")
    print("POST to http://localhost:3000/send-email")
    server.serve_forever()
