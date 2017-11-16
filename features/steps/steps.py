import os, fnmatch, re, yaml
from behave import *

@given('the filename in the "{env_name}" environment variable')
def step_impl(context, env_name):
  if not hasattr(context, "filename"):
    context.filename = os.environ.get(env_name)

@given('the threat feature file has been loaded')
def step_impl(context):
  if not hasattr(context, "file_data"):
    process_comments = True
    metadata_lines = []
    story_lines = []
    with open(context.filename) as fh:
      for line in fh.readlines():
        match = re.match(r'^\s*#\s*(.*)$', line)
        if process_comments and match:
          metadata_lines.append(match.group(1))
        else:
          match = re.match(r'^\s*Feature:\s*(.*)$', line)
          if match:
            process_comments = False
            metadata_lines.append("Name: %s" % match.group(1))
            story_lines.append(line)
        if not process_comments:
          story_lines.append(line)

    context.file_data = yaml.load("\n".join(metadata_lines))
    context.file_data["Story"] = "\n".join(story_lines)

@then('the parent directory must be "{parent}"')
def step_impl(context, parent):
  assert os.path.split(os.path.dirname(context.filename))[1] == parent

@then('the file must match the pattern "{pattern}"')
def step_impl(context, pattern):
  basename = os.path.basename(context.filename)
  assert re.match(pattern, basename) 

@then('the file length must be less than or equal to "{length:d}" characters')
def step_impl(context, length):
  basename = os.path.basename(context.filename)
  assert len(basename) <= length

@then('the "{field}" field must exist')
def step_impl(context, field):
  assert field in context.file_data
  
@then('the "{field}" field must be a "{field_type}"')
def step_impl(context, field, field_type):
  type_map = {
    "string": str,
    "str": str,
    "array": list,
    "list": list,
    "hash": dict,
    "dict": dict
  }
  assert isinstance(context.file_data[field], type_map[field_type])

@then('the Id must be the same as the filename Id')
def step_impl(context):
  basename = os.path.basename(context.filename)
  match = re.search(r'^ocst_(\d+)_(\d+)_(\d+)[a-z0-9_]*\.feature$', basename)
  assert match
  ocst_id = "OCST-%s.%s.%s" % (match.group(1), match.group(2), match.group(3))
  assert context.file_data["Id"] == ocst_id

@then('the "{field}" field length must be {operation} "{length:d}" characters')
def step_impl(context, field, operation, length):
  if operation == "less than or equal to":
    assert len(context.file_data[field]) <= length
  elif operation == "greater than or equal to":
    assert len(context.file_data[field]) >= length

@then('the "{field}" field must match the pattern "{pattern}"')
def step_impl(context, field, pattern):
  assert re.match(pattern, context.file_data[field])

@given('the set of allowed values')
def step_impl(context):
  context.allowed_values = []
  for row in context.table:
    context.allowed_values.append(row["value"])

@then('the "{field}" field must be one of the allowed values')
def step_impl(context, field):
  assert context.file_data[field] in context.allowed_values

@then('the "{field}" field must be one or more of the allowed values')
def step_impl(context, field):
  for value in context.file_data[field]:
    assert value in context.allowed_values

@then('each "{field}" value must match the pattern "{pattern}"')
def step_impl(context, field, pattern):
  for value in context.file_data[field]:
    assert re.match(pattern, value)
