# -*- coding: utf-8 -*-
"""Manifest bản mẫu Cổng B: 3 cảnh, 4 cue (intro + sơ đồ 4 nhóm + luồng đăng nhập).
S01c1 (chào mừng) chỉ dùng ở bản full để giữ mẫu trong khung 30-45s."""
import json, os

ROOT = "D:/Edit/Baigiang_cacbaactrongduan_web"
CUES = [
    dict(id="S01c2", scene="M1", rate="+5%", pause_after=0.0,
         text="Bạn đã bao giờ tự hỏi: trong một công ty phần mềm, ai lên ý tưởng, ai chia việc cho lập trình viên, và ai kiểm tra website trước khi phát hành?",
         say="Bạn đã bao giờ tự hỏi: trong một công ty phần mềm, ai lên ý tưởng, ai chia việc cho lập trình viên, và ai kiểm tra website trước khi phát hành?",
         subs=["Bạn đã bao giờ tự hỏi: trong một công ty phần mềm, ai lên ý tưởng,",
               "ai chia việc cho lập trình viên, và ai kiểm tra website trước khi phát hành?"]),
    dict(id="S04c1", scene="M2", rate="+5%", pause_after=0.0,
         text="Cơ cấu đội ngũ phần mềm thường gồm bốn nhóm: lãnh đạo và định hướng; quản lý dự án; quản lý chuyên môn; và nhóm trực tiếp phát triển, triển khai sản phẩm.",
         say="Cơ cấu đội ngũ phần mềm thường gồm bốn nhóm: lãnh đạo và định hướng; quản lý dự án; quản lý chuyên môn; và nhóm trực tiếp phát triển, triển khai sản phẩm.",
         subs=["Cơ cấu đội ngũ phần mềm thường gồm bốn nhóm: lãnh đạo và định hướng;",
               "quản lý dự án; quản lý chuyên môn; và nhóm trực tiếp phát triển, triển khai sản phẩm."]),
    dict(id="S10c1", scene="M3", rate="+5%", pause_after=0.4,
         text="Backend Developer xử lý logic phía máy chủ. Ví dụ, khi bạn nhấn đăng nhập:",
         say="Bắc-en Đi-ve-lớp-pờ xử lý logic phía máy chủ. Ví dụ, khi bạn nhấn đăng nhập:",
         subs=["Backend Developer xử lý logic phía máy chủ.",
               "Ví dụ, khi bạn nhấn đăng nhập:"]),
    dict(id="S10c2", scene="M3", rate="+0%", pause_after=0.0,
         text="Frontend gửi email và mật khẩu qua API. Backend kiểm tra, truy vấn cơ sở dữ liệu, xác thực tài khoản, rồi trả kết quả về Frontend. Dữ liệu trả về thường ở dạng JSON.",
         say="Phờ-ront-en gửi email và mật khẩu qua Ây Pi Ai. Bắc-en kiểm tra, truy vấn cơ sở dữ liệu, xác thực tài khoản, rồi trả kết quả về Phờ-ront-en. Dữ liệu trả về thường ở dạng Giây-sần.",
         subs=["Frontend gửi email và mật khẩu qua API. Backend kiểm tra, truy vấn cơ sở dữ liệu,",
               "xác thực tài khoản, rồi trả kết quả về Frontend. Dữ liệu trả về thường ở dạng JSON."]),
]

if __name__ == "__main__":
    os.makedirs(ROOT + "/mau", exist_ok=True)
    json.dump(CUES, open(ROOT + "/mau/manifest.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("manifest", len(CUES), "cues")