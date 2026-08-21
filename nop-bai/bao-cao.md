# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

|             |                                                                   |
| ----------- | ----------------------------------------------------------------- |
| Họ và tên   | Lê Hồ Quang Huy                                                   |
| MSSV        | 2A202602026                                                       |
| Lớp / Khóa  | K4                                                                |
| Repo GitHub | https://github.com/huyle0112/K4-Track2-Day21-CI-CD-for-AI-Systems |
| Ngày nộp    | 21/08/2026                                                        |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
| -------- | -----------: | ------------: | --------: | -------: | -------: |
| 1        |          125 |         0.075 |         4 |   0.7222 |    0.880 |
| 2        |          150 |         0.080 |         4 |   0.7189 |    0.878 |
| 3        |          200 |         0.100 |         5 |   0.7149 |    0.874 |
| 4        |          100 |         0.100 |         3 |   0.7109 |    0.878 |
| 5        |           50 |         0.050 |         2 |   0.6051 |    0.846 |
| 6        |           10 |         0.100 |         2 |   0.2963 |    0.525 |
| 7        |           10 |         0.100 |         2 |   0.2963 |    0.525 |
| 8        |           10 |         0.100 |         2 |   0.2963 |    0.525 |

**Bộ siêu tham số đã chọn:** `n_estimators=125`, `learning_rate=0.075`, `max_depth=4`.

**Lý do:** Trong tất cả các lần thử nghiệm, bộ `n_estimators=125`, `learning_rate=0.075`, `max_depth=4` cho kết quả tốt nhất với `f1_score = 0.7222` và `accuracy = 0.880`. Vì bộ dữ liệu Adult mất cân bằng lớp, F1-score là tiêu chí quan trọng hơn accuracy trong việc lựa chọn mô hình. Bộ được chọn có F1-score cao nhất, cho thấy khả năng cân bằng tốt hơn giữa precision và recall đối với lớp dương.
Trong các lần chạy, mô hình có accuracy cao nhất là mô hình có F1-score cao nhất. Tuy nhiên, sự khác biệt giữa hai metric vẫn đáng chú ý. Cấu hình `n_estimators=100`, `learning_rate=0.1`, `max_depth=3` đạt accuracy 0.878, chỉ thấp hơn 0.002 so với mô hình tốt nhất, nhưng F1-score chỉ khoảng 0.7109. Cho thấy chỉ dựa vào accuracy có thể che giấu sự khác biệt về khả năng dự đoán lớp dương.

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Vì dữ liệu ko cân bằng, mô hình đơn giản luôn dự đoán mọi mẫu là “thu nhập thấp” vẫn có thể đạt accuracy khoảng 75%, mặc dù hoàn toàn không phát hiện được người thuộc lớp thu nhập cao. Khiến accuracy không dánh giá đúng. F1-score của lớp dương kết hợp precision và recall, đánh giá cả khả năng phát hiện đúng người có thu nhập cao và hạn chế dự đoán dương sai. Không sử dụng `average="weighted"` vì kết quả có thể bị bias cho lớp đa số, cũng không dùng `average="macro"` vì sẽ tính trung bình hai lớp. Mục tiêu là đánh giá trực tiếp lớp dương, nên sử dụng `f1_score(y_true, y_pred)` với mặc định `pos_label=1`.

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn               | Nguyên nhân                        | Cách giải quyết                     |
| ---------------------- | ---------------------------------- | ----------------------------------- |
| DVC báo `AccessDenied` | IAM thiếu quyền S3                 | Bổ sung IAM policy                  |
| API EC2 không chạy     | Version thư viện không khớp CI     | Đồng bộ `scikit-learn` và `joblib`  |
| Test CI lỗi MLflow     | Experiment chưa được khởi tạo đúng | Cấu hình tracking URI và experiment |

---

## 4. So Sánh Bước 2 và Bước 3

|                           | f1_score | accuracy |
| ------------------------- | -------: | -------: |
| Bước 2 (`train_batch1`)   |   0.7222 |    0.880 |
| Bước 3 (`+ train_batch2`) |   0.7339 |   0.8840 |

**Nhận xét:** Sau khi thêm `train_batch2`, F1-score tăng từ **0.7222 lên 0.7339** và accuracy tăng từ **0.880 lên 0.884**. Cho thấy dữ liệu mới đã giúp cải thiện model, đặc biệt là khả năng dự đoán lớp thu nhập cao.

## 5. Phần Bonus Đã Thực Hiện (nếu có)

- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: chạy Ci với tham số yếu, làm fail CI
