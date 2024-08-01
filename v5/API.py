from fastapi import FastAPI, Depends, HTTPException, Header,UploadFile
from fastapi.responses import FileResponse
import os
import concurrent.futures
import asyncio
import datetime
from main import main as logo_detection
app = FastAPI()

# Define a directory to store uploaded images
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

# Define a list of valid API keys (replace with your actual API keys)
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}

def process_file(file: UploadFile):
    try:
        # Read the uploaded video file into memory
        video_content = file.file.read()

        # Create a temporary file to save the uploaded video
        video_file_path = os.path.join(upload_dir, file.filename)
        with open(video_file_path, "wb") as temp_video_file:
            temp_video_file.write(video_content)
   
        try:
            detected_logo=logo_detection(source=video_file_path)
        except Exception as e:
            return {"error": f"Transcription error: {str(e)}"}

        try:
            os.remove(video_file_path)
            # from pathlib import Path
            # import mimetypes
            #   # Replace the placeholder with the actual path to your file
            # file_path = Path(detected_logo)

            # # Determine the MIME type of the file
            # mime_type, _ = mimetypes.guess_type(file_path)

            # Use the appropriate media type in FileResponse
            response=FileResponse(detected_logo,filename=os.path.basename(detected_logo))
            # os.remove(f"{video_name}.zip")
            return response
            # return FileResponse(file_path, media_type=mime_type)
            # return FileResponse(detected_logo)
            # return {"detected_logo":detected_logo}
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

    except Exception as e:
        return {"error": str(e)}



# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@app.post("/Logo_Detection/")
async def logo_detection_endpoint(
    file: UploadFile,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_file(file)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1011, reload=True)
# uvicorn API:app --host 0.0.0.0 --port 1011 --reload