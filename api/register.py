from http.server import BaseHTTPRequestHandler
import json
import urllib.request


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    try:
      content_length = int(self.headers.get("Content-Length", 0))
      post_data = self.rfile.read(content_length)
      request_data = json.loads(post_data.decode("utf-8"))

      name = request_data.get("name")
      phone_number = request_data.get("phone_number")
      business_name = request_data.get("business_name")

      url = "https://api-merchant.carrybee.com/api/v2/merchant/register"
      payload = {
          "name": name,
          "phone_number": phone_number,
          "business_name": business_name,
      }

      headers = {
          "User-Agent": (
              "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML,"
              " like Gecko) Chrome/156.0.0.0 Mobile Safari/537.36"
          ),
          "Accept": "application/json",
          "Content-Type": "application/json",
          "origin": "https://merchant.carrybee.com",
          "referer": "https://merchant.carrybee.com/",
      }

      req = urllib.request.Request(
          url,
          data=json.dumps(payload).encode("utf-8"),
          headers=headers,
          method="POST",
      )

      with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        status_code = response.status

      self.send_response(status_code)
      self.send_header("Content-type", "application/json")
      self.send_header("Access-Control-Allow-Origin", "*")
      self.end_headers()
      self.wfile.write(response_body.encode("utf-8"))

    except Exception as e:
      self.send_response(500)
      self.send_header("Content-type", "application/json")
      self.send_header("Access-Control-Allow-Origin", "*")
      self.end_headers()
      error_res = json.dumps({"error": str(e)})
      self.wfile.write(error_res.encode("utf-8"))

  def do_OPTIONS(self):
    self.send_response(200)
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    self.send_header("Access-Control-Allow-Headers", "Content-Type")
    self.end_headers()
