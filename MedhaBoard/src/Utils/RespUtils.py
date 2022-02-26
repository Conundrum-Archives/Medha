
def format_response(respdata):
  return {
    "status": respdata['status'],
    "message": respdata['message'],
    "data": respdata['data']
  }