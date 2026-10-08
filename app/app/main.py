from io import BytesIO

import pandas as pd

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from app.cleaner import clean_dataframe
from app.validators import count_invalid_emails


app = FastAPI(
    title="CleanCSV API",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "name": "CleanCSV",
        "version": "0.1.0",
        "status": "running"
    }


@app.post("/clean")
async def clean_csv(file: UploadFile):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    content = await file.read()

    try:
        df = pd.read_csv(BytesIO(content))
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV: {error}"
        )

    if len(df) > 1000:
        raise HTTPException(
            status_code=403,
            detail="Free plan limited to 1,000 rows"
        )

    cleaned_df, stats = clean_dataframe(df)

    stats["invalid_emails"] = count_invalid_emails(
        cleaned_df
    )

    output = BytesIO()

    cleaned_df.to_csv(
        output,
        index=False
    )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=cleaned.csv"
        }
    )
