import json
import os
import urllib.parse
import boto3
from pypdf import PdfReader


# AWS clients
s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")
dynamodb = boto3.resource("dynamodb")


# Environment variables
RESULTS_TABLE = os.environ["RESULTS_TABLE"]

table = dynamodb.Table(RESULTS_TABLE)


# Bedrock model
MODEL_ID = os.environ.get(
    "MODEL_ID",
    "amazon.nova-lite-v1:0"
)


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using pypdf.
    """

    reader = PdfReader(pdf_path)

    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)


def analyze_resume_with_bedrock(resume_text):
    """
    Send resume text to Amazon Bedrock
    and get structured analysis.
    """

    prompt = f"""
You are an AI resume analyzer.

Analyze the following resume and return ONLY valid JSON.

Return this structure:

{{
    "candidate_name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "summary": "",
    "strengths": [],
    "missing_skills": [],
    "recommended_roles": [],
    "overall_score": 0
}}

Resume:

{resume_text}
"""

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.2
        }
    )

    result_text = response["output"]["message"]["content"][0]["text"]

    return result_text


def save_result_to_dynamodb(result_id, s3_key, analysis):
    """
    Save resume analysis to DynamoDB.
    """

    table.put_item(
        Item={
            "pk": result_id,
            "s3_key": s3_key,
            "analysis": analysis
        }
    )


def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))

    try:

        # ------------------------------------------------
        # 1. Read S3 event
        # ------------------------------------------------

        record = event["Records"][0]

        bucket = record["s3"]["bucket"]["name"]

        encoded_key = record["s3"]["object"]["key"]

        key = urllib.parse.unquote_plus(encoded_key)

        print(f"Bucket: {bucket}")
        print(f"S3 Key: {key}")


        # ------------------------------------------------
        # 2. Create temporary PDF path
        # ------------------------------------------------

        file_name = os.path.basename(key)

        local_path = f"/tmp/{file_name}"

        print(f"Downloading PDF to: {local_path}")


        # ------------------------------------------------
        # 3. Download PDF from S3
        # ------------------------------------------------

        s3.download_file(
            bucket,
            key,
            local_path
        )

        print("PDF downloaded successfully.")


        # ------------------------------------------------
        # 4. Extract text using pypdf
        # ------------------------------------------------

        print("Extracting text using pypdf...")

        resume_text = extract_text_from_pdf(local_path)

        print(
            f"Extracted text length: {len(resume_text)}"
        )


        if not resume_text.strip():

            print("No text could be extracted from PDF.")

            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Could not extract text from PDF."
                })
            }


        # ------------------------------------------------
        # 5. Limit text size
        # ------------------------------------------------

        # Prevent extremely large resumes from
        # creating an unnecessarily large Bedrock request.

        resume_text = resume_text[:30000]


        # ------------------------------------------------
        # 6. Analyze resume using Bedrock
        # ------------------------------------------------

        print("Sending resume to Bedrock...")

        analysis = analyze_resume_with_bedrock(
            resume_text
        )

        print("Bedrock analysis completed.")


        # ------------------------------------------------
        # 7. Generate result ID
        # ------------------------------------------------

        result_id = os.path.splitext(file_name)[0]


        # ------------------------------------------------
        # 8. Save result to DynamoDB
        # ------------------------------------------------

        save_result_to_dynamodb(
            result_id,
            key,
            analysis
        )

        print("Result saved to DynamoDB.")


        # ------------------------------------------------
        # 9. Return success
        # ------------------------------------------------

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resume processed successfully",
                "result_id": result_id
            })
        }


    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error processing resume",
                "error": str(e)
            })
        }