# 🚀 Serverless AI Resume Analyzer on AWS Using Cloudformation

An AI-powered, event-driven application built with AWS serverless services. Users can upload a PDF resume through a web interface, the application extracts text and sends it to an Amazon Bedrock foundation model for analysis, and the resulting structured output is stored in Amazon DynamoDB.

> **Project status:** Built as a hands-on AWS, Python, and Generative AI portfolio project. Verify each feature in your deployed environment before describing it as fully operational.

 # Problem Statement
 Reviewing resumes manually can be time-consuming for recruiters, especially when they receive a large number of applications. Identifying relevant skills, experience, and qualifications in each resume requires significant effort.

This project aims to simplify the initial resume-screening process by building a serverless application on AWS that accepts PDF resumes, extracts their text, and is designed to use AI to analyze resume content and generate structured results.
 

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture Diagram](#️-architecture-diagram)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Prerequisites](#-prerequisites)
- [Setup and Deployment](#-setup-and-deployment)
- [Configuration Notes](#-configuration-notes)
- [Security](#-security)
- [Cost and Cleanup](#-cost-and-cleanup)
- [Challenges and Learning Outcomes](#-challenges-and-learning-outcomes)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

## 📌 Overview

The Serverless AI Resume Analyzer demonstrates how to combine serverless computing, object storage, event-driven processing, a foundation model, and a NoSQL database into one cloud application.

A user selects a PDF resume in the frontend. The frontend requests a short-lived presigned upload URL from an API endpoint and uploads the PDF directly to a private Amazon S3 bucket. An S3 object-created event invokes a processing Lambda function. That function extracts text from the PDF, requests an analysis from Amazon Bedrock, and saves the result to DynamoDB.

## 🏗️ Architecture Diagram
![image alt](https://github.com/shinderutuja319-afk/aws-project/blob/7d0bebc7214d6b74e9e125631f4b01b1da412450/Serverless%20AI%20Resume%20Analyzer%20Workflow.png)

## ✨ Features

- PDF resume selection through a browser-based interface.
- Presigned S3 upload URL with a short expiry, avoiding sending the PDF body through API Gateway.
- Private S3 bucket for uploaded resumes.
- Event-driven processing initiated by an S3 object-created event.
- PDF text extraction using Python and `pypdf`.
- Generative AI analysis using an accessible, compatible Amazon Bedrock model.
- Analysis persistence in Amazon DynamoDB.
- Infrastructure as Code with AWS SAM and AWS CloudFormation.
- CloudWatch logs for investigating runtime issues.

> Feature availability depends on the deployed code, IAM permissions, model access, and configuration in your AWS account.

## 🧰 Technology used

- **AWS (Amazon Web Services)**: As the cloud provider to host and manage the serverless infrastructure.
- **AWS SAM (Serverless Application Model)**: To define, build, and deploy the serverless application.
- **AWS CloudFormation**: For Infrastructure as Code (IaC), to provision and manage AWS resources.
- **Amazon S3**: To store uploaded PDF resumes securely and host frontend static files.
- **Amazon CloudFront**: To distribute frontend content globally with low latency and HTTPS support.
- **Amazon API Gateway**: To provide HTTP API endpoints for generating secure, presigned resume upload URLs.
- **AWS Lambda**: To execute serverless Python functions for upload URL generation and resume processing.
- **Amazon Textract**: To extract text from uploaded resume documents ,but this is available for paid account thats why i used **pypdf** : to read and extract text from pdf.
- **Amazon Bedrock**: To use generative AI for resume analysis and structured output generation.
- **Amazon DynamoDB**: To store resume analysis results in a NoSQL database.
- **AWS IAM (Identity and Access Management)**: To manage permissions and control access between AWS services.
- **Amazon CloudWatch**: To monitor Lambda execution logs and troubleshoot application errors.
- **Python 3.12**: As the backend programming language for AWS Lambda functions.
- **boto3**: The AWS SDK for Python, used to interact with AWS services.
- **HTML5**: To structure the frontend user interface.
- **CSS3**: To style the frontend interface.
- **JavaScript**: To handle resume uploads and communicate with the backend API.
- **Git**: For version control and tracking code changes.
- **GitHub**: To host the source code and maintain project documentation.

## 📂 Project Structure

```text
ai_resume_analyser/
├── Frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── src/
│   ├── upload_url/
│   │   └── app.py
│   └── processor/
│       └── app.py
├── screenshots/
│   ├── frontend.png
│   └── s3-upload.png
├── template.yaml
├── samconfig.toml        # If generated; do not commit secrets
├── README.md
└── .gitignore
```

The structure above reflects the main folders used in this project. Keep only files and folders that actually exist in your repository. If your project has tests or dependency files, include them here too.

## 🔄 How It Works

1. **Choose a resume:** The user selects a PDF file in the frontend.
2. **Request an upload URL:** The frontend calls the API Gateway endpoint, which invokes the upload URL Lambda function.
3. **Create a presigned URL:** The Lambda function returns a time-limited URL for uploading to S3.
4. **Upload to S3:** The browser uploads the PDF directly to the private S3 bucket, using the required HTTP method and headers.
5. **Trigger processing:** The S3 object-created event invokes the processor Lambda function.
6. **Extract PDF text:** The processor reads the S3 object and extracts its text using `pypdf`.
7. **Analyze with AI:** The processor sends the extracted text to the configured Amazon Bedrock model.
8. **Store the result:** The processor writes the structured analysis to DynamoDB.

## 🧑‍💻 Prerequisites

Install or configure the following before deploying:

- Python 3.12
- AWS CLI
- AWS SAM CLI
- Git
- An AWS account and an IAM identity with permissions to deploy the required resources
- Access to a compatible Amazon Bedrock foundation model in the chosen region
- A modern web browser

**Configured region:** `ap-south-1` (Asia Pacific — Mumbai), unless your deployment configuration specifies another region.

## 🚀 Setup and Deployment

### 1. Clone the repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username and adjust the repository URL if needed.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ai_resume_analyser.git
cd ai_resume_analyser
```

### 2. Configure AWS credentials

```bash
aws configure
```

Set the AWS access credentials for your IAM identity and use `ap-south-1` as the default region if that is where you deploy.

Check the active identity and region:

```bash
aws sts get-caller-identity
aws configure get region
```

Use an IAM role or other secure credential method where appropriate. Never put access keys in source code or commit them to GitHub.

### 3. Validate the SAM template

```bash
sam validate --lint
```

Resolve any validation errors before continuing.

### 4. Build the application

```bash
sam build
```

### 5. Deploy with SAM

```bash
sam deploy --guided
```

Follow the prompts. Choose a valid CloudFormation stack name, confirm the region, and review the permissions and changes before deployment. For later deployments, you can usually run:

```bash
sam build
sam deploy
```

### 6. Find the deployed API endpoint

List the stack outputs (replace the stack name if yours differs):

```bash
aws cloudformation describe-stacks \
  --stack-name YOUR_STACK_NAME \
  --region ap-south-1 \
  --query "Stacks[0].Outputs"
```

Use the API URL returned by your deployment in the frontend configuration. Do not paste credentials or presigned URLs into the README.

### 7. Open the frontend

For local testing, open `Frontend/index.html` with VS Code Live Server or another local static web server. Make sure the API endpoint in `Frontend/app.js` matches the deployed API URL and that the API's CORS configuration allows the frontend origin.

![AWS AI Resume Analyzer Architecture](https://github.com/shinderutuja319-afk/aws-project/blob/344f79b2b47bf9014b08eb41e1999a1dcc2d4626/screenshot/Screenshot%20(286).png)


### 8. Test the complete workflow

- Select a PDF resume.
- Start the upload/analysis process.
- Confirm the PDF appears in the S3 `resumes/` prefix.
 ![AWS AI Resume Analzser Architecture](https://github.com/shinderutuja319-afk/aws-project/blob/4545b41f59de0ab2c3a1adf248f3e0e91acd9457/screenshot/Screenshot%20(287).png)
- Check the processor Lambda's CloudWatch logs.
 ![AWS AI Resume Analyzer Architecture](https://github.com/shinderutuja319-afk/aws-project/blob/4545b41f59de0ab2c3a1adf248f3e0e91acd9457/screenshot/Screenshot%20(290).png)
- Confirm that the expected analysis record appears in DynamoDB.
- Check browser developer tools and Lambda logs if any step fails.
- here is the two created lambda functions
![AWS AI Resume Analyzer Architecture](https://github.com/shinderutuja319-afk/aws-project/blob/962a6057f58ec9dca1c4e5041dbf3c04acf73f78/screenshot/Screenshot%20(288).png)

## ⚙️ Configuration Notes

- **Bedrock model:** The model ID must match a foundation model available to your account and supported in your deployment region. Model access and request formats can vary.
- **Presigned upload:** The HTTP method, object key, content type, and other signed headers used by the browser must match the URL generated by the Lambda function. A mismatch can cause `SignatureDoesNotMatch`.
- **S3 event:** Confirm the bucket event notification targets the processor Lambda and that the Lambda permission allows invocation from the bucket.
- **DynamoDB:** The processor's key names and item format must match the table schema defined in `template.yaml`.
- **Frontend:** Confirm the API URL and CORS settings. A browser `Failed to fetch` error can be caused by an incorrect endpoint, CORS, network issues, or a failed API request.

## 🔐 Security

- Keep the S3 bucket private and block public access.
- Use short-lived presigned URLs and validate file type and size.
- Grant each Lambda function only the IAM permissions it needs.
- Avoid logging resume text, personal data, credentials, or presigned URLs.
- Configure appropriate data retention and deletion for resumes and analysis results.
- Consider authentication and authorization before exposing the application publicly.
- Treat AI-generated resume feedback as informational and review it for accuracy and bias.
- Never commit AWS access keys, secrets, real resumes, or personal data to the repository.

## 💰 Cost and Cleanup

AWS resources and Amazon Bedrock model invocations may incur charges. Costs depend on region, usage, model, logging, storage, and current pricing or free-tier eligibility.

When you have finished testing, review your resources and remove anything no longer required. To delete the SAM-managed stack:

```bash
sam delete --stack-name YOUR_STACK_NAME
```

Check the stack name and deletion prompts carefully. Back up anything you need first. Resources retained by deletion policies, separately created resources, S3 objects, or other dependencies may require manual cleanup. Verify the AWS console and billing dashboard afterward.

## 🎓 Challenges and Learning Outcomes

This project provides hands-on practice with:

- Designing a serverless architecture on AWS.
- Defining infrastructure with AWS SAM and CloudFormation.
- Creating API Gateway endpoints and Lambda functions.
- Using presigned URLs to upload files directly to S3.
- Building event-driven workflows with S3 notifications.
- Extracting PDF text with Python.
- Integrating an LLM through Amazon Bedrock.
- Writing structured records to DynamoDB.
- Debugging IAM permissions, CORS, API requests, and Lambda failures.
- Using CloudWatch logs to investigate application behavior.
- Publishing and documenting a cloud project with GitHub.

## 🔮 Future Improvements

- Add a results API so users can view analysis after processing.
- Match a resume against a job description.
- Provide skill-gap and keyword insights.
- Add authentication and user-specific access controls.
- Add automated unit and integration tests.
- Implement CI/CD with GitHub Actions.
- Improve input validation, retry handling, monitoring, and error messages.
- Add a lifecycle and privacy policy for uploaded resume data.

## 👩‍💻 Author

**Rutuja Shinde**  
MCA Graduate | Aspiring Cloud & DevOps Engineer | Python and Generative AI Enthusiast

- GitHub: [shinderutuja319-afk](https://github.com/shinderutuja319-afk)

---

⭐ If you find this project interesting, feel free to explore the repository and share feedback.
