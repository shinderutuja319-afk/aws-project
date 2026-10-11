const API_URL =
"https://dj5cwsqap4.execute-api.ap-south-1.amazonaws.com/upload-url";

const fileInput = document.getElementById("resumeFile");
const chooseBtn = document.getElementById("chooseBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const fileName = document.getElementById("fileName");
const status = document.getElementById("status");

let selectedFile = null;

// Choose Resume button
chooseBtn.addEventListener("click", () => {
fileInput.click();
});

// When user selects a file
fileInput.addEventListener("change", () => {
selectedFile = fileInput.files[0];

if (!selectedFile) {
    return;
}

// Check PDF
if (selectedFile.type !== "application/pdf") {
    status.textContent = "Please select a PDF file.";
    selectedFile = null;
    analyzeBtn.disabled = true;
    return;
}

// Display selected file
fileName.textContent = `Selected: ${selectedFile.name}`;

status.textContent = "";

// Enable Analyze button
analyzeBtn.disabled = false;

});

// Analyze Resume button
analyzeBtn.addEventListener("click", async () => {

if (!selectedFile) {
    return;
}

try {

    analyzeBtn.disabled = true;

    // --------------------------------
    // STEP 1: Get Presigned URL
    // --------------------------------

    status.textContent =
        "Getting secure upload URL...";

    const response = await fetch(API_URL, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            file_name: selectedFile.name
        })
    });

    if (!response.ok) {
        throw new Error(
            `API request failed: ${response.status}`
        );
    }

    const data = await response.json();

    console.log("API Response:", data);

    const uploadUrl = data.upload_url;

    if (!uploadUrl) {
        throw new Error(
            "Upload URL was not returned by API."
        );
    }

    // --------------------------------
    // STEP 2: Upload PDF to S3
    // --------------------------------

    status.textContent =
        "Uploading resume to AWS S3...";

    const uploadResponse = await fetch(uploadUrl, {
        method: "PUT",

        headers: {
            "Content-Type": "application/pdf"
        },

        body: selectedFile
    });

    if (!uploadResponse.ok) {
        throw new Error(
            `S3 upload failed: ${uploadResponse.status}`
        );
    }

    // --------------------------------
    // STEP 3: S3 Event → Lambda
    // --------------------------------

    status.textContent =
        "Resume uploaded successfully. Processing started...";

    console.log(
        "Resume uploaded successfully."
    );

    /*
     * S3 ObjectCreated event automatically
     * triggers ProcessorFunction.
     *
     * ProcessorFunction:
     * S3 → Lambda → pypdf → Bedrock → DynamoDB
     */

} catch (error) {

    console.error(
        "Error:",
        error
    );

    status.textContent =
        `Error: ${error.message}`;

    analyzeBtn.disabled = false;
}

});
