import json
from math import floor, ceil
import getData

def lambda_handler(event, context):
    # return 1
    # TODO implement
    category = str(json.dumps(event['queryStringParameters'].get('cat')))
    category = category.strip('\"')
    db_strings = getData.sa(str(category))
    
    try:
        avgJaroSim = 0
        totalJaroSim = 0
        
        s1 = str(json.dumps(event['queryStringParameters']['name']))
        s1 = s1.strip('\"')
        
        max_similarity = {"point": 0, "string": "", "name": s1, "cat": category, "inner_similarity": 0 }
        # for i in range(len(db_strings)*len(db_strings)):
        for i in range(len(db_strings) - 1):
            s2 = db_strings[i]
            # If the s are equal
            if (s1 == s2):
                max_similarity = {
                    "point": 1,
                    "string": s2,
                    "nam": s1
                    # "event": event
                    # "event": json.dumps(event.get("body").get("name"))
                }
         
            # Length of two s
            len1 = len(s1)
            len2 = len(s2)
         
            # Maximum distance upto which matching
            # is allowed
            max_dist = floor(max(len1, len2) / 2) - 1
         
            # Count of matches
            match = 0
         
            # Hash for matches
            hash_s1 = [0] * len(s1)
            hash_s2 = [0] * len(s2)
         
            # Traverse through the first
            for i in range(len1):
         
                # Check if there is any matches
                for j in range(max(0, i - max_dist),
                               min(len2, i + max_dist + 1)):
                     
                    # If there is a match
                    if (s1[i] == s2[j] and hash_s2[j] == 0):
                        hash_s1[i] = 1
                        hash_s2[j] = 1
                        match += 1
                        break
            # print(s1, s2)
            # print(match)
            # If there is no match
            if (match == 0):
                max_similarity = {
                    "point": match,
                    "string": s2
                    # "event": event
                    # "event": json.dumps(event.get("body").get("name"))
                }
                continue
         
            # Number of transpositions
            t = 0
            point = 0
         
            # Count number of occurrences
            # where two characters match but
            # there is a third matched character
            # in between the indices
            for i in range(len1):
                if (hash_s1[i]):
         
                    # Find the next matched character
                    # in second
                    while (hash_s2[point] == 0):
                        point += 1
         
                    if (s1[i] != s2[point]):
                        t += 1
                    point += 1
            t = t//2
         
            # Return the Jaro Similarity
            result = (match/ len1 + match / len2 +
                    (match - t) / match)/ 3.0
            if result > max_similarity["point"]:
                max_similarity = {
                    "point": result,
                    "string": s2,
                    "name": s1
                    # "event": event
                    # "event": json.dumps(event.get("body").get("name"))
                }
                
                
        return {
            'statusCode': 200,
            'body': json.dumps(max_similarity)
        }
    except Exception as e:
        max_similarity = {
            "point": 0.1,
            "string": str(json.dumps(event['queryStringParameters']['name'])),
        }
        return {
            'statusCode': 200,
            'body': json.dumps(max_similarity)
        }
    
