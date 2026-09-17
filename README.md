# WearLab – Thương mại điện tử thời trang có phối biến thể

Website minh hoạ cho chương **xây dựng website thương mại điện tử hỗ trợ phối chọn biến thể sản phẩm thời trang**. Người dùng có thể chọn màu/kích cỡ, thiết kế hai mặt áo với Fabric.js, tải ảnh cá nhân, lưu JSON/PNG và đặt đơn COD.

## Công nghệ

- Backend: Python, Flask, PyMongo
- Database: MongoDB
- Frontend: HTML/CSS/JavaScript, Fabric.js 5 (CDN)

## Cài đặt và chạy

```powershell
cd D:\523100181\fashion_ecommerce
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Mở `http://127.0.0.1:5000`.

Khởi động MongoDB cục bộ, sau đó nạp dữ liệu mẫu:

```powershell
mongosh < mongo-init.js
```

Nếu chưa có MongoDB, giao diện và thao tác phối biến thể vẫn mở được. Các nút **Lưu thiết kế** và **Thêm vào giỏ** cần MongoDB để lưu dữ liệu.

## MongoDB collections

| Collection | Vai trò | Trường chính |
|---|---|---|
| `users` | tài khoản khách hàng | `name`, `email`, `passwordHash`, `role` |
| `products` | thông tin sản phẩm | `slug`, `name`, `variants`, `basePrice` |
| `custom_designs` | thiết kế Fabric.js | `productSlug`, `variantSku`, `fabricJson`, `previewDataUrl` |
| `carts` | sản phẩm được thêm giỏ | `variantSku`, `quantity`, `customDesign` |
| `orders` | đơn hàng hoàn tất | `userId`, `items`, `total`, `status` |

`variants` là mảng con của `products`; mỗi biến thể có `sku`, `color`, `hex`, `size`, `stock`, `price`. Cấu trúc này cho phép cập nhật tồn kho và giá theo từng tổ hợp màu/kích cỡ.

## API

- `GET /api/products/<slug>` – đọc sản phẩm cùng biến thể.
- `POST /api/designs/save` – lưu JSON hai mặt, preview PNG và PNG in độ phân giải cao.
- `POST /api/cart` – thêm biến thể đã chọn vào giỏ.
- `POST /api/orders/create` – tạo đơn hàng COD.
- `GET /api/admin/orders` – lấy danh sách đơn hàng và dữ liệu thiết kế phục vụ in.
