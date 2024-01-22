# COR API INTEGRATION

Tài liệu tích hợp cho hệ thống OCR giấy tờ của VAIP


# REST API tích hợp

REST API tích hợp được mô tả ở dưới

## Get list danh sách tài liệu có trong 1 hồ sơ

### Request

`GET /external/workspaces/:id/documents`

    curl --location '${base_url}/api/v1/external/workspace/1/documents' --header 'x-api-key: vaip_api_key'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2023 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {
        "data" : [
            {
                "id": 327,
                "orgId": 135,
                "document" : {
                    "id": 332,
                    "name": "cccd.png",
                    "rawFile": "file/vaip/phuctv14/cccd.png",
                    "createdAt":"2023-10-26T03:25:06.000Z",
                    "updatedAt":"2021-10-26T03:25:06.000Z",
                },
                "createdAt":"2023-10-26T03:25:06.000Z",
                "updatedAt":"2021-10-26T03:25:06.000Z",
                "status": 1
            },
            {
                "id": 328,
                "orgId": 135,
                "document" : {
                    "id": 336,
                    "name": "cccd.png",
                    "rawFile": "file/vaip/phuctv14/cccd1.png",
                    "createdAt":"2023-10-26T03:25:06.000Z",
                    "updatedAt":"2021-10-26T03:25:06.000Z",
                },
                "createdAt":"2023-10-26T03:25:06.000Z",
                "updatedAt":"2021-10-26T03:25:06.000Z",
                "status": 1
            },
            {
                "id": 329,
                "orgId": 135,
                "document" : {
                    "id": 465,
                    "name": "cccd.png",
                    "rawFile": "file/vaip/phuctv14/cccd2.png",
                    "createdAt":"2023-10-26T03:25:06.000Z",
                    "updatedAt":"2021-10-26T03:25:06.000Z",
                },
                "createdAt":"2023-10-26T03:25:06.000Z",
                "updatedAt":"2021-10-26T03:25:06.000Z",
                "status": 1
            }
        ],
        "meta" : {
            "message": "Success",
            "code": 200
        }
    }

### Các mã HTTP code

| Mã code |                                Mô tả                                 |
|---------|:--------------------------------------------------------------------:|
| 200     |                        Lấy dữ liệu thành công                        |
| 401     | x-api-key không hợp lệ hoặc không có quyền lấy dữ liệu trong thư mục |
| 400     |                  Hồ sơ không tồn tại hoặc đã bị xoá                  |
| 500     |                              Lỗi server                              |

## Upload file

### Request

`POST /external/documents`

    curl --location '${base_url}/api/v1/external/document' --header 'x-api-key: vaip_api_key' --form 'file=@"/Users/mac/Desktop/cmnd.png"'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2023 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {
        "data" : {
            "id": 352,
            "orgId": 173,
            "hashMD5": "938c2cc0dcc05f2b68c4287040cfcf71",
            "name": "cmnd.png",
            "size": 106372,
            "mimetype": "image/png"
        },
        "meta" : {
            "message": "Success",
            "code": 200
        }
    }

### Các mã HTTP code

| Mã code |         Mô tả          |
|---------|:----------------------:|
| 200     | Upload file thành công |
| 401     | x-api-key không hợp lệ |
| 500     |       Lỗi server       |

## Tạo mới văn bản OCR

### Request

`POST /external/application_documents`

    curl --location '${base_url}/api/v1/external/application_documents' --header 'x-api-key: vaip_api_key' --header 'Content-Type: application/json' --data '{"document_id": 256}'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2023 12:36:30 GMT
    Status: 200 OK
    Content-Type: application/json
    
    {
      "data": {
        "id": 782,
        "orgId": 173,
        "applicationId": 163,
        "workspaceId": 194,
        "coreVersion": "idcard-0.0.1",
        "status": 0,
        "createdAt": "2023-10-26T03:25:06.000Z"
      },
      "meta": {
        "message": "Success",
        "code": 200
      }
    }

| Mã code |         Mô tả          |
|---------|:----------------------:|
| 200     | Upload file thành công |
| 401     | x-api-key không hợp lệ |
| 500     |       Lỗi server       |

## Get OCR document data

### Request

`GET /external/application_documents/:id`

    curl --location '${base_url}/api/v1/external/application_documents/196' --header 'x-api-key: vaip_api_key'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2023 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {
      "data": {
        "id": 782,
        "orgId": 173,
        "applicationId": 163,
        "workspace": {
          "id": 326,
          "orgId": 173,
          "name": "So hoa van ban",
          "description": "So hoa tai lieu",
          "createdAt": "2023-10-26T03:25:06.000Z"
        },
        "document": {
          "id": 352,
          "orgId": 173,
          "hashMD5": "938c2cc0dcc05f2b68c4287040cfcf71",
          "rawFile": "file/vaip/phuctv14/cccd.png",
          "name": "cmnd.png",
          "size": 106372,
          "mimetype": "image/png"
        },
        "startTime": "2023-10-26T03:25:06.000Z",
        "startExtractionTime": "2023-10-26T03:25:06.000Z",
        "endExtractionTime": "2023-10-26T03:25:06.000Z",
        "endTime": "2023-10-26T03:25:06.000Z",
        "coreVersion": "idcard-0.0.1",
        "status": 1,
        "createdAt": "2023-10-26T03:25:06.000Z"
      },
      "meta": {
        "message": "Success",
        "code": 200
      }
    }

| Mã code |          Mô tả          |
|---------|:-----------------------:|
| 200     | Upload file thành công  |
| 401     | x-api-key không hợp lệ  |
| 404     | Không tìm thấy tài liệu |
| 500     |       Lỗi server        |
