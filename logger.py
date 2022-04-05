import csv
import os
config = {
    "path": "/home/kakushigoto/cards/logs",
    "fieldsname": ["User", "Data"]
}

async def addLogfile(match):
    with open(f"{config['path']}/{match.id}.csv", 'w') as logFile:
        processing = csv.DictWriter(logFile, delimiter = "$", lineterminator="\r", fieldnames=config['fieldsname'])
        processing.writeheader()
        logFile.close()


async def logMsg(match, user, text):
    data = {"User": user, "Data": text}
    with open(f"{config['path']}/{match.id}.csv", 'a', newline='') as logFile:
        processing = csv.DictWriter(logFile, delimiter = "$", lineterminator="\r", fieldnames=config['fieldsname'])
        processing.writerow(data)
        logFile.close()

async def write(match, user, text):
    if not os.path.exists(f"{config['path']}/{match.id}.csv"): await addLogfile(match)
    await logMsg(match, user, text)