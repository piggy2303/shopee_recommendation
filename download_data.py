from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(
    file_id='1HJJ06peMHtdzIGaEvc8bU61XE3ZjpBUL',
    dest_path='./data.zip'
)
print("download done")
