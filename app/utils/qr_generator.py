import uuid
import qrcode
import os

def generate_token_and_qr(user_id: int, event_id: int) -> tuple[str, str]:
    token_uuid = str(uuid.uuid4())
    qr_data = f"{user_id}:{event_id}:{token_uuid}"
    # qr_data = f"http://localhost:8000/tokens/validate/{token_uuid}"
    print("the qr data: ", qr_data)

    filename = f"qr_user{user_id}_event{event_id}.png"
    filepath = os.path.join("generated_qrs", filename)
    os.makedirs("generated_qrs", exist_ok=True)

    img = qrcode.make(qr_data)
    img.save(filepath)

    return token_uuid, filepath
