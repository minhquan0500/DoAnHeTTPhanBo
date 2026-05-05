from fastapi import FastAPI, Request
import subprocess

app = FastAPI()

@app.post("/webhook")
async def handle_alert(request: Request):
    
    data = await request.json()
    print(f"📥 Đã nhận tín hiệu Webhook! Trạng thái: {data.get('status')}")
    
    for alert in data.get("alerts", []):
        
        if alert.get("status") == "firing" and alert["labels"].get("alertname") == "BackendDown":
            
            
            instance = alert["labels"].get("instance", "")
            server_name = instance.split(":")[0] if ":" in instance else instance
            
            if server_name:
                print(f"\n[{server_name}] CẢNH BÁO: Phát hiện máy chủ sập!")
                print(f"[{server_name}] Đang gọi Docker để khởi động lại container...")
                
                try:
                    # Lệnh ma thuật cứu sống server
                    subprocess.run(["docker", "start", server_name], check=True)
                    print(f"[{server_name}] CẤP CỨU THÀNH CÔNG! Hệ thống đã phục hồi.\n")
                except Exception as e:
                    print(f"[{server_name}] Chạy lệnh Docker thất bại: {e}\n")
                    
    return {"message": "Đã xử lý xong"}