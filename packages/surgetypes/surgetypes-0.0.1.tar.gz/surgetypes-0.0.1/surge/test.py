# @surge.wrap
import surge
surge.trace()
class testClassA:
  def __init__(self,a,c=True):
    pass
  def get(self,b):
    return b
    pass

# @surge.wrap
class testClassB:
  def __init__(self,a,c=True):
    pass
  def get(self,b):
    return False

def testFunction(q,v=5):
  return {"hi":"ho"}

# import surge
# surge.track()

a = testClassA(1,c=False)
b = testClassB("1")
a.get(2)
b.get("2")
testFunction("57")
# import pprint
# pprint.PrettyPrinter(indent=2).pprint(globals())#locals()))