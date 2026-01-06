from tasks import run_pipeline 

output = run_pipeline.delay()
while not output.ready():    # until computation is finished
    result = output.get()

print(result)
