from jobs import job, jobs
import time

job('test', 100, 'url', 'https://dev-cdn.studenttenant.com/uploads/Untitled.png', False).send()
job('test', 200, 'base64', open('/code/var/temp/base64img.txt').read(), True).send()
job('test', 300, 'stream', 'http://192.168.100.67:8000/stream.mjpg', False).send()

while True:
    result = jobs.result()

    if result != None:
        print('client', result.client, 'jobId', result.jobId, 'data', result.data)

    time.sleep(0.1)