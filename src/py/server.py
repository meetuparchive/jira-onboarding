from klein import Klein

import json

class JiraOnboardingWebImpl(object):
  app = Klein()

  @app.route('/')
  def land(self, request):
      request.setHeader('Content-Type', 'application/json')
      return json.dumps({"key": "Hello World"})

if __name__ == "__main__":
  web = JiraOnboardingWebImpl()
  web.app.run('localhost', 8080)

