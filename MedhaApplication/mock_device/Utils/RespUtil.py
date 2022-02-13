
def resp_format(resp_data):
  return {
    "status": resp_data['status'],
    "message": resp_data['message'],
    "data": resp_data['data']
  }