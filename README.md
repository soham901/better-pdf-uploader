# PDF Uploader with Validation

A simple and effective pdf uploader with validations, built using FastAPI and jQuery. Ensures only valid and non encrypted PDF files are accepted.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Running the App

To start the FastAPI development server, use the following command:

```bash
fastapi dev
```

## Opening the App

Once the server is running, you can access the file uploader by opening your web browser and navigating to:

```
http://localhost:8000
```

This will load the file uploader interface, where you can select and upload PDF files. The application will perform client-side validation to ensure the files are valid before allowing the upload to proceed.
