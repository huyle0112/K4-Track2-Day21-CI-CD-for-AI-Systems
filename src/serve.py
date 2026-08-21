from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ["ARTIFACT_BUCKET"]
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """
    Tai file model.joblib tu AWS S3 ve may khi server khoi dong.

    Ham nay duoc goi mot lan khi module duoc import.
    Xac thuc AWS nen su dung IAM Role gan truc tiep vao EC2.
    """

    # TODO 1: Tao S3 client
    s3 = boto3.client("s3")

    # TODO 2 + 3: Tai model tu S3 xuong may
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    s3.download_file(
        ARTIFACT_BUCKET,
        MODEL_KEY,
        MODEL_PATH,
    )

    # TODO 4: In thong bao thanh cong
    print(
        f"Model da duoc tai tu "
        f"s3://{ARTIFACT_BUCKET}/{MODEL_KEY}"
    )


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """
    Endpoint kiem tra suc khoe server.
    GitHub Actions goi endpoint nay sau khi deploy de xac nhan server dang chay.

    Tra ve: {"status": "ok"}
    """

    # TODO 5
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luan chinh.

    Dau vao:
        JSON {"features": [f1, f2, ..., f10]}

    Dau ra:
        JSON {
            "prediction": <0|1>,
            "label": <"thu_nhap_thap"|"thu_nhap_cao">
        }

    Thu tu 10 dac trung:
        age,
        workclass,
        education_num,
        marital_status,
        occupation,
        relationship,
        sex,
        capital_gain,
        capital_loss,
        hours_per_week
    """

    # TODO 6: Kiem tra so luong dac trung
    if len(req.features) != 10:
        raise HTTPException(
            status_code=400,
            detail="Can cung cap dung 10 dac trung.",
        )

    # TODO 7: Du doan
    pred = model.predict([req.features])[0]

    # Chuyen numpy integer -> Python int
    pred = int(pred)

    # TODO 8: Tao label
    label = (
        "thu_nhap_cao"
        if pred == 1
        else "thu_nhap_thap"
    )

    return {
        "prediction": pred,
        "label": label,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )