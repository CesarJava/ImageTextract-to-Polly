
import boto3
import json
# Document
documentName = "/Users/filhc/Downloads/unsamples/sample3.jpg"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})


with open("sample-response.json", "w") as target:
    json.dump(response, target)

columns = []
lines = []
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        column_found = False
        for index, column in enumerate(columns):
            bbox_left = item["Geometry"]["BoundingBox"]["Left"]
            bbox_right = item["Geometry"]["BoundingBox"]["Left"] + \
                item["Geometry"]["BoundingBox"]["Width"]
            bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + \
                item["Geometry"]["BoundingBox"]["Width"]/2
            column_centre = column['left'] + column['right']/2
            # print("findingboundingboxcentre")

            if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                # Bbox appears inside the column
                lines.append([index, item["Text"]])
                column_found = True
                break
        if not column_found:
            # print(item["Text"])
            columns.append({'left': item["Geometry"]["BoundingBox"]["Left"], 'right': item["Geometry"]
                            ["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
            lines.append([len(columns)-1, item["Text"]])

lines.sort(key=lambda x: x[0])
print(lines)
for line in lines:
    print(line[1])
