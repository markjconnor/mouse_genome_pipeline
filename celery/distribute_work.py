from task import pipeline_script

output = pipeline_script.delay()
while not output.ready():    # until computation is finished
    result = output.get()

print(result)
