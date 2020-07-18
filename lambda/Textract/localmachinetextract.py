
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

# print(response)

# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print('\033[94m' + item["Text"] + '\033[0m')
