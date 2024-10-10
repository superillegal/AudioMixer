from behave import *
import mixer
import os
import wave


@given('a new mixing session')
def step_impl(context):
    context.segments = []

@given('the audio file "{filename}"')
def step_impl(context, filename):
    #  In a real scenario, ensure the file exists
    pass

@when('I mix "{filename}" from {start} seconds to {end} seconds')
def step_impl(context, filename, start, end):
    context.segments.append({"file": filename, "start": int(start), "end": int(end)})

@when('I mix "{filename}" from {start} seconds to {end} seconds into "{output_file}"')
def step_impl(context, filename, start, end, output_file):
    context.segments.append({"file": filename, "start": int(start), "end": int(end)})
    context.output_file = output_file
    mixer.mix_audio(context.segments, output_file)

@then('the output file "{output_file}" should exist')
def step_impl(context, output_file):
    assert os.path.exists(output_file)

@then('the output file should not be empty')
def step_impl(context):
    with wave.open(context.output_file, 'rb') as outfile:
        assert outfile.getnframes() > 0