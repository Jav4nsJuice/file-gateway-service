# Secure Serverless File Gateway (AWS Lab 4)

## Project Overview
This project implements a secure, serverless **File Gateway** using **AWS SAM (Serverless Application Model)**. It allows users to upload and download files to a **private S3 bucket** via **time-limited, cryptographically signed URLs**.

The architecture maintains **100% bucket privacy** while offloading heavy data transfers directly to **Amazon S3**, using **AWS Lambda** only for logic and authorization.

---

## Architecture Diagram
*(Add diagram here if available)*

---

## Key Achievements (Rubric Compliance)

- **Infrastructure as Code (IaC):**  
  100% of resources (S3, Lambda, IAM, API Gateway) are defined in `template.yaml`.

- **Security:**  
  S3 bucket has `PublicAccessBlockConfiguration` enabled. No public access is permitted.

- **Protocol Semantics:**  
  Implements **HTTP 307 Temporary Redirect** for the download flow to preserve request integrity.

- **Regional Robustness:**  
  Specifically configured for **us-east-2 (Ohio)** using **Signature Version 4 (SigV4)**.

---

## Prerequisites

Before deploying, ensure you have the following:

- **AWS Account:** Active credentials configured locally
- **AWS SAM CLI:** Installed and up to date
- **Python 3.9:** Installed (matches the Lambda runtime)
- **Target Region:** Optimized for `us-east-2` to handle specific S3 regional signature requirements

---

## Deployment Instructions

### Step 1: Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/file-gateway-service.git
cd file-gateway-service
```

### Step 2: Build the Application

```bash
sam build
```

### Step 3: Deploy (Guided)

```bash
sam deploy --guided
```

#### Configuration Settings

- **Stack Name:** `file-gateway-service`
- **AWS Region:** `us-east-2`
- **Allow SAM CLI to create IAM roles:** Yes
- **Allow SAM CLI to create API:** Yes
- **Save arguments to configuration file:** Yes

---

## Functionality Verification

### Endpoint A: `POST /files` (Upload)

```bash
curl -X POST <ApiEndpoint>/files \
  -H "Content-Type: application/json" \
  -d '{"filename": "test-file.txt"}'
```

**Expected Result:**  
A JSON response containing `uploadUrl`.

```bash
curl -X PUT -T "test-file.txt" "<UPLOAD_URL>"
```

---

### Endpoint B: `GET /files/{objectKey}` (Download)

```bash
curl -i <ApiEndpoint>/files/test-file.txt
```

**Expected Result:**

- `HTTP/2 307 Temporary Redirect`
- `Location` header contains an S3 pre-signed URL valid for 1 hour

```bash
curl -L <ApiEndpoint>/files/test-file.txt
```

---

## Technical Implementation Notes

- **Redirect Logic:**  
  Uses **HTTP 307** to ensure the client preserves the original HTTP method during redirects.

- **Boto3 Configuration:**  
  Explicitly uses `s3.us-east-2.amazonaws.com` and `signature_version='s3v4'`.

- **Least Privilege:**  
  IAM roles are restricted to `PutObject` and `GetObject`.
