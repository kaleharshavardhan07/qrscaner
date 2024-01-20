import cv2
from pyzbar.pyzbar import decode
import openpyxl
from openpyxl import Workbook
import gspread
from google.oauth2 import service_account

def scan_qr_code_camera():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_to_google_sheet(data, spreadsheet_key='1Zy3x_d4Lrk2v1njIG9LL5-cp3i_a_0PzCVT7Q6NpQls', sheet_name='Sheet1'):
 
    creds = service_account.Credentials.from_service_account_file(
        './psf-data-411811-a451ae390965.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )

    gc = gspread.authorize(creds)

    sheet = gc.open_by_key(spreadsheet_key).worksheet(sheet_name)

   
    name, phone = data.split("\n")[0].split(":")[1], data.split("\n")[1].split(":")[1]

    sheet.append_row([name, phone])

    print(f"Data saved to Google Sheet.")

if __name__ == "__main__":
    print("Scan QR code with the camera.")
    data = scan_qr_code_camera()
    print("QR Code scanned successfully!")

    save_to_google_sheet(data)
