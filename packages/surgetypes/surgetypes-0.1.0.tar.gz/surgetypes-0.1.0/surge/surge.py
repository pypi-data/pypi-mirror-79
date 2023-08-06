from functools import wraps
import json
import inspect
import opcode
import os, pathlib
import collections
log = collections.defaultdict(dict)
# surge_file =  open('.surgetypes','w+')
def saveSurgeFile():
  with open('.surgetypes','w+') as surge_file:
    surge_file.write(json.dumps(log,indent=4))
# settings = {}
# def updateSettings(newsettings):
#   global settings
#   for k,v in newsettings.items():
#     settings[k] = v
#   settings = settings

BLACKLIST = [
  '__name__',
  '__doc__',
  '__loader__',
  '__spec__',
  '__annotations__',
  '__builtins__',
  '__cached__',
  '__package__',
  'surge'
]
def safe_stringify(string):
  try:
    return str(string)
  except Exception as e:
    return ""
# https://explog.in/notes/settrace.html
def trace():
  def show_trace(frame, event, arg):
    if event not in ["call","return"]: return
    ACTION_ID = f"{frame.f_code.co_filename} {frame.f_code.co_firstlineno}"
    try:
      if event == "return":
        log[ACTION_ID]["return"] = safe_stringify(arg)
      elif event == "call":
        if os.path.isabs(frame.f_code.co_filename): return

        args = {name:frame.f_locals.get(name) for name in frame.f_code.co_varnames}
        log[ACTION_ID].update({

          "file": frame.f_code.co_filename,
          "name": frame.f_code.co_name,
          "lineno": frame.f_code.co_firstlineno,
          "args":safe_stringify(args)
        })
      saveSurgeFile()
    except Exception as e:
      print(f"SurgeError {e}")
    return show_trace
  

  import sys
  sys.settrace(show_trace)
  # sys.settrace(None)


def track():
  import pprint
  import inspect
  frame = inspect.stack()[1][0]
  local_vars = {k:v for (k,v) in inspect.stack()[1][0].f_locals.items() if k not in set(BLACKLIST)}
  file_name = local_vars.pop('__file__')
  for local_var in local_vars.values(): wrap(local_var)
  # print(local_vars,file_name)
  # global_vars = globals()
  # global_var_keys = set(global_vars.keys())
  # global_var_keys -= set(BLACKLIST)
  # pprint.PrettyPrinter(indent=2).pprint(global_var_keys)#locals()))
  # pprint.PrettyPrinter(indent=2).pprint(global_vars)#locals()))

def wrap(f):
  # if 'disabled' in settings and settings['disabled']: return f
  if inspect.isclass(f): 
    return wrapClass(f)
  if inspect.isfunction(f): 
    return wrapFunction(f)
  return f

# def validateTypes(oldTypes,newTypes):
#   if oldTypes['args'] != newTypes['args']:
#     raise AssertionError(f"Surge Error: function took different argument types: {oldTypes['args']} and {newTypes['args']}")
#   elif oldTypes['returnval'] != newTypes['returnval']:
#     raise AssertionError(f"Surge Error: function returned two different types: {oldTypes['returnval']} and {newTypes['returnval']}")
def wrapClass(cls):
  myClassName = cls.__name__
  for attr_name in cls.__dict__: # there's propably a better way to do this
      attr = getattr(cls,attr_name)
      if not inspect.isfunction(attr): continue
      wrapped_attr = wrapFunction(attr,class_name=myClassName,is_method=True)
      setattr(cls, attr_name,wrapped_attr)
  return cls
def wrapFunction(f,class_name="",is_method=False):
  myFunctionName = f"{class_name } {f.__name__}"
  data = {
    "run_count":0
  }
  print(myFunctionName)
  @wraps(f)
  def wrapper(*args, **kwds):
    print(myFunctionName)
    returnVal = f(*args, **kwds)
    if data["run_count"] > 0: return returnVal
    data["run_count"] += 1

    
    # newTypes = {
    # 'args':list(map(getArgType,args)), 
    # 'kwargs':list(map(getArgType,list(kwds.items()))),
    # 'returnval':getArgType(returnVal)
    # }
    if is_method: args = args[1:]
    newValues = {
      'args':str(args), 
      'kwargs':str(kwds),
      'returnval':str(returnVal)
    }
    # if myFunctionName in log:
    #   validateTypes(log[myFunctionName],newTypes)
    log[myFunctionName] = newValues
    # print(log)
    with open('.surgetypes','w+') as surgetypesfile:
      surgetypesfile.write(json.dumps(log,indent=4))
    return returnVal
  return wrapper
  


def getArgType(arg):
  val = type(arg).__name__
  if (isIterable(arg)):
    # val += "<"+type(arg[0]).__name__+">"
    # IMPLEMENT SET SUPPORT, EMPTY LIST SUPPORT
    val += "<TODO>"
  return val

def isIterable(maybe_iterable):
  try:
      iter(maybe_iterable)
      return True
  except TypeError:
    return False