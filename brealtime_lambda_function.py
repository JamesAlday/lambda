import json
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Found event: {}'.format(event))
    
    httpStatusCode = 200

    job_data = {
        'ping': 'OK',
        'name': 'James Alday',
        'email address': 'jim@jamesalday.com',
        'phone': '718-795-7026',
        'position': 'Tech Lead/Engineer',
        'referrer': 'LinkedIn',
        'degree': 'BA',
        'resume': 'http://jamesalday.com/projects/JRA2Resume.pdf',
        'source': 'https://github.com/JamesAlday/lambda/blob/master/brealtime_lambda_function.py',
        'status': 'Yes',
    }
    
    if event['queryStringParameters']:
        if event['queryStringParameters']['q']:
            query = event['queryStringParameters']['q'].lower()
            
            if query == 'years':
                now = datetime.datetime.now()
                responseBody = now.year - 2005
            elif query == 'puzzle':
                # split by new line in question string
                puzzleText = event['queryStringParameters']['d'].splitlines()
                
                # String 'ABCD' split into a list
                keys = list(puzzleText[1].strip())
                
                del(puzzleText[0:2]) # delete question and keys from puzzle text
                
                # create a dict with empty values for each key
                values = {}
                for key in keys:
                    values[key] = None
                
                # set our first key ('A') to 1
                values[keys[0]] = 1
                
                while True:
                    values = evaluateConditions(puzzleText, keys, values)

                    noneCount = 0

                    for val in values:
                        if values[val] is None:
                            noneCount += 1 

                    if noneCount == 0:
                        break;

                solution = []
                
                for idx, key1 in enumerate(values):
                    solution.insert(idx, key1)
                    
                    for key2 in values:
                        if values[key1] == values[key2]:
                            solution[idx] += '='
                        elif values[key1] > values[key2]:
                            solution[idx] += '>'
                        elif values[key1] < values[key2]:
                            solution[idx] += '<'
                
                responseBody = ' ' + str.join('', keys) + '\n' + str.join('\n', solution)
            else:
                responseBody = job_data.get(query, 'Bad Query!')

    return {
        "isBase64Encoded": False,
        "statusCode": httpStatusCode,
        "headers": { "Content-Type": "text/plain" },
        "body": responseBody
    }

def evaluateConditions(puzzleText, keys, values):
    # loop over each line of puzzle text
    for puzzle in puzzleText:
        conditionals = list(puzzle) # the list of conditionals to compare on
        currentKey = conditionals.pop(0) # first value is our current letter, remove it
        
        # loop over conditionals to set the rest of our values
        for idx, condition in enumerate(conditionals):
            idxKey = keys[idx]
            
            if condition == '-':
                continue
            elif condition == '>':
                if values[idxKey] is not None:
                    values[currentKey] = values[idxKey] + 1
                elif values[currentKey] is not None:
                    values[idxKey] = values[currentKey] - 1
            elif condition == '<':
                if values[idxKey] is not None:
                    values[currentKey] = values[keys[idx]] - 1
                elif values[currentKey] is not None:
                    values[idxKey] = values[currentKey] + 1
            elif condition == '=':
                if values[idxKey] is not None:
                    values[currentKey] = values[idxKey]
                elif values[currentKey] is not None:
                    values[idxKey] = values[currentKey]

    return values
