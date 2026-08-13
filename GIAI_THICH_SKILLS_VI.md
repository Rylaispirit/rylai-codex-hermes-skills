# Giải thích bộ Rylai Codex-Hermes-Claude Skills

Tài liệu này giải thích ngắn gọn 35 skill trong bộ cài, dành cho người dùng Codex, Hermes và Claude.

Tác giả bộ đóng gói, người duy trì và người chuyển đổi: **Rylai**

Một số skill được thích nghi từ repo GitHub có giấy phép mở. Tác giả, revision
và giấy phép gốc được giữ trong `THIRD_PARTY_NOTICES.md` và `PROVENANCE.yml`.

## Ý nghĩa trạng thái

- **Sẵn sàng (`ready`)**: skill có đủ hướng dẫn và tài nguyên nội bộ để sử dụng. Một số tác vụ vẫn có thể cần Internet hoặc thư viện phù hợp.
- **Có điều kiện (`conditional`)**: skill hoạt động khi máy có đủ chương trình, thư viện, tài khoản, API hoặc công cụ render cần thiết.
- **Lõi đã thích nghi (`adapted-core`)**: luồng công việc chính đã dùng được trên Codex, Hermes và Claude, nhưng một số tính năng nâng cao của bản nguồn không có trong gói này.

## Cài đặt cho Claude

Mọi skill trong bộ này chỉ là thư mục chứa `SKILL.md`, không phụ thuộc runtime
riêng, nên cùng một bộ file dùng được cho Codex, Hermes và Claude. Chỉ khác nơi
đặt file.

### Cách 1: cài cả bộ bằng script

Trên macOS hoặc Linux:

```bash
bash install-claude.sh
```

Trên Windows:

```powershell
.\install-claude.ps1
```

- Thêm `--force` (PowerShell dùng `-Force`) để ghi đè skill đã có. Bản cũ được
  sao lưu trước khi ghi đè.
- Thêm `--project` (`-Project`) để cài vào `.claude/skills` của riêng dự án hiện
  tại thay vì cài cho toàn máy.
- Thêm `--target <thư-mục>` (`-Target <thư-mục>`) nếu muốn tự chọn nơi cài.

Mặc định script cài vào thư mục skill cá nhân, nghĩa là mọi phiên Claude đều
dùng được. Claude quét skill lúc bắt đầu phiên, nên sau khi cài hãy mở một phiên
Claude mới.

### Cách 2: tải từng file ZIP lên Claude.ai hoặc Cowork

Thư mục `packages/` chứa sẵn 35 file `.zip`, mỗi skill một file. Bên trong mỗi
file ZIP là thư mục skill cùng `SKILL.md` và các tài nguyên đi kèm.

Cách này dành cho Claude.ai hoặc Cowork: mở phần quản lý skill, tải file ZIP
tương ứng lên và bật skill. Claude Code nên dùng script cài đặt hoặc chép thư
mục skill vào `~/.claude/skills`.

Sau khi sửa bất kỳ skill nào, dựng lại các file ZIP:

```bash
python build_claude_packages.py --clean
```

File nén được dựng ổn định, nên skill không đổi thì mã băm cũng không đổi. Mã
băm của từng file nằm trong `packages/checksums.sha256`.

### Cách 3: chép tay một skill

Chép một thư mục con trong `skills/` vào đúng chỗ:

```text
Claude cho toàn máy:  ~/.claude/skills/<tên-skill>
Claude cho một dự án: <thư-mục-dự-án>/.claude/skills/<tên-skill>
```

Claude đọc đúng phần frontmatter `name` và `description` trong `SKILL.md` giống
các runtime còn lại. File `agents/openai.yaml` trong mỗi skill bị Claude bỏ qua,
được giữ lại chỉ để một bản checkout dùng chung cho cả ba agent.

## 1. academic-paper-polish

**Trạng thái:** Sẵn sàng
**Nhóm:** Học thuật

- **Công dụng:** Chỉnh sửa bài báo, luận văn và nội dung nghiên cứu để câu chữ rõ ràng, lập luận chặt chẽ và thuật ngữ nhất quán.
- **Nên dùng khi:** Cần làm mượt phần tóm tắt, mở đầu, phương pháp, kết quả, thảo luận hoặc phản hồi phản biện.
- **Đầu vào:** Bản thảo học thuật, yêu cầu của tạp chí, quy tắc thuật ngữ hoặc đoạn văn cần chỉnh.
- **Kết quả:** Bản sửa có văn phong học thuật hơn, kèm cảnh báo về chỗ thiếu bằng chứng hoặc diễn đạt quá mức.
- **Lưu ý:** Skill không tự tạo số liệu, thí nghiệm, kết quả hay tài liệu tham khảo.

## 2. academic-pptx

**Trạng thái:** Có điều kiện
**Nhóm:** Trình chiếu

- **Công dụng:** Quyết định nội dung và cấu trúc cho bài thuyết trình học thuật.
- **Nên dùng khi:** Làm slide hội thảo, seminar, bảo vệ luận văn, báo cáo phòng thí nghiệm hoặc thuyết trình đề tài nghiên cứu.
- **Đầu vào:** Bài báo, luận văn, dữ liệu, thời lượng trình bày, đối tượng người nghe và số slide dự kiến.
- **Kết quả:** Dàn ý theo từng slide, tiêu đề mang thông điệp, thứ tự lập luận và đề xuất loại hình minh họa.
- **Lưu ý:** Muốn tạo file `.pptx` hoàn chỉnh cần dùng thêm skill `pptx` và công cụ render.

## 3. academic-slides

**Trạng thái:** Có điều kiện
**Nhóm:** Trình chiếu

- **Công dụng:** Lập kế hoạch, xây dựng và kiểm tra một bài nói học thuật từ đầu đến cuối.
- **Nên dùng khi:** Cần chuyển bài nghiên cứu thành bài nói có thời lượng cụ thể và chuẩn bị phần hỏi đáp.
- **Đầu vào:** Nội dung nghiên cứu, bối cảnh buổi nói, thời lượng, mẫu trình chiếu và yêu cầu của đơn vị tổ chức.
- **Kết quả:** Cấu trúc bài nói, outline slide, quy tắc thiết kế, kế hoạch diễn tập và slide dự phòng.
- **Lưu ý:** Cần công cụ tạo và render PowerPoint để kiểm tra hình ảnh thực tế.

## 4. academic-writing-style

**Trạng thái:** Sẵn sàng
**Nhóm:** Học thuật

- **Công dụng:** Hướng dẫn cách viết luận văn và bài nghiên cứu theo văn phong học thuật.
- **Nên dùng khi:** Cần kiểm tra cấu trúc luận văn, cách lập luận, giọng văn, trích dẫn hoặc định dạng APA 7.
- **Đầu vào:** Dàn ý, chương luận văn, đoạn văn, danh mục tài liệu tham khảo hoặc yêu cầu định dạng.
- **Kết quả:** Nhận xét và bản chỉnh sửa theo quy tắc học thuật, kèm các điểm chưa đúng chuẩn.
- **Lưu ý:** Không thay thế phần mềm kiểm tra đạo văn và không tự gửi bài lên tạp chí.

## 5. analytics-data-analysis

**Trạng thái:** Sẵn sàng
**Nhóm:** Dữ liệu

- **Công dụng:** Hướng dẫn thực hiện phân tích dữ liệu bằng Python, Jupyter và các thư viện phổ biến.
- **Nên dùng khi:** Cần xây dựng notebook, làm sạch dữ liệu, thống kê, trực quan hóa hoặc mô hình phân tích.
- **Đầu vào:** Dataset, mô tả cột, câu hỏi phân tích và định dạng đầu ra mong muốn.
- **Kết quả:** Quy trình phân tích có thể tái chạy, mã nguồn, bảng thống kê và biểu đồ.
- **Lưu ý:** Từng bài toán có thể cần cài thêm `pandas`, `numpy`, `matplotlib`, `scipy` hoặc thư viện chuyên ngành.

## 6. chart-image

**Trạng thái:** Sẵn sàng
**Nhóm:** Dữ liệu

- **Công dụng:** Tạo biểu đồ SVG từ dữ liệu mà không cần thư viện JavaScript bên ngoài.
- **Nên dùng khi:** Cần biểu đồ đường, cột, vùng hoặc điểm để chèn vào báo cáo, dashboard hay bài viết.
- **Đầu vào:** Mảng JSON chứa trường trục X, trục Y và trường phân nhóm nếu có.
- **Kết quả:** File SVG có tiêu đề, nhãn trục, màu sắc và tùy chọn hiển thị giá trị.
- **Lưu ý:** Xuất PNG cần thêm thư viện `sharp`; SVG hoạt động trực tiếp với Node.js.

## 7. content-analysis

**Trạng thái:** Sẵn sàng
**Nhóm:** Nội dung

- **Công dụng:** Phân tích bài viết, podcast, video, YouTube hoặc transcript để rút ra thông tin quan trọng.
- **Nên dùng khi:** Cần tìm ý chính, luận điểm, bài học, câu trích đáng chú ý hoặc nội dung bị bỏ sót.
- **Đầu vào:** Văn bản, transcript, URL có thể truy cập hoặc file nội dung.
- **Kết quả:** Báo cáo có cấu trúc gồm tóm tắt, insight, bằng chứng, điểm mạnh, điểm yếu và câu hỏi tiếp theo.
- **Lưu ý:** Chất lượng phân tích phụ thuộc vào độ đầy đủ của transcript hoặc nội dung nguồn.

## 8. content-research-writer

**Trạng thái:** Sẵn sàng
**Nhóm:** Nội dung

- **Công dụng:** Hỗ trợ nghiên cứu và viết nội dung có nguồn dẫn.
- **Nên dùng khi:** Viết bài chuyên sâu, bài blog, báo cáo, nội dung giáo dục hoặc tài liệu cần trích dẫn.
- **Đầu vào:** Chủ đề, độc giả, mục tiêu, độ dài, giọng văn và yêu cầu nguồn.
- **Kết quả:** Câu hỏi nghiên cứu, outline, bản nháp từng phần và danh sách nguồn gắn với từng nhận định.
- **Lưu ý:** Thông tin hiện hành phải được kiểm tra từ nguồn trực tiếp tại thời điểm viết.

## 9. copywriting

**Trạng thái:** Sẵn sàng
**Nhóm:** Nội dung

- **Công dụng:** Viết nội dung thuyết phục cho bán hàng và marketing.
- **Nên dùng khi:** Cần headline, CTA, landing page, email bán hàng, mô tả giá trị hoặc nội dung theo AIDA/PAS.
- **Đầu vào:** Sản phẩm, khách hàng mục tiêu, vấn đề cần giải quyết, bằng chứng và hành động mong muốn.
- **Kết quả:** Nhiều phương án copy có hook, lợi ích, bằng chứng và lời kêu gọi hành động rõ ràng.
- **Lưu ý:** Không nên tự bịa số liệu, đánh giá khách hàng, khan hiếm hoặc cam kết kết quả.

## 10. creative-writing

**Trạng thái:** Lõi đã thích nghi
**Nhóm:** Nội dung

- **Công dụng:** Lập kế hoạch, viết mới, sửa và kiểm tra nội dung sáng tạo hoặc bài viết dài.
- **Nên dùng khi:** Viết truyện, tiểu luận, blog, bài nghiên cứu phổ thông, nội dung marketing hoặc landing page.
- **Đầu vào:** Ý tưởng, thể loại, giọng kể, nhân vật, độc giả, độ dài và các chi tiết bắt buộc phải giữ.
- **Kết quả:** Dàn ý, bản nháp và bản sửa có kiểm tra nhịp độ, tính liên tục, giọng văn và logic.
- **Lưu ý:** Luồng viết chính dùng được; các pipeline kiểm toán bản thảo chuyên sâu chưa được đóng gói đầy đủ.

## 11. dashboard-creator

**Trạng thái:** Sẵn sàng
**Nhóm:** Dữ liệu

- **Công dụng:** Tạo dashboard HTML có KPI, biểu đồ, thanh tiến độ và bảng dữ liệu.
- **Nên dùng khi:** Cần trang theo dõi chỉ số, báo cáo vận hành, dashboard bán hàng hoặc màn hình giám sát.
- **Đầu vào:** Dữ liệu, danh sách KPI, quy tắc tính toán, đối tượng sử dụng và yêu cầu giao diện.
- **Kết quả:** Dashboard HTML có thể mở trong trình duyệt, thường kèm SVG và mã nguồn chỉnh sửa được.
- **Lưu ý:** Cần kiểm tra dữ liệu thật, kích thước màn hình và khả năng đọc trên cả desktop lẫn mobile.

## 12. data-analyzer

**Trạng thái:** Sẵn sàng
**Nhóm:** Dữ liệu

- **Công dụng:** Tìm xu hướng, phân bố, bất thường và insight trong dataset.
- **Nên dùng khi:** Người dùng muốn hiểu dữ liệu đang nói gì thay vì chỉ chuyển đổi định dạng.
- **Đầu vào:** CSV, XLSX, JSON, bảng dữ liệu hoặc mô tả schema cùng câu hỏi cần trả lời.
- **Kết quả:** Thống kê mô tả, phân tích xu hướng, phát hiện ngoại lệ và kết luận gắn với bằng chứng.
- **Lưu ý:** Skill phải phân biệt tương quan với quan hệ nhân quả và ghi rõ dữ liệu thiếu.

## 13. deep-research

**Trạng thái:** Sẵn sàng
**Nhóm:** Nghiên cứu

- **Công dụng:** Thực hiện nghiên cứu nhiều nguồn theo câu hỏi và phạm vi rõ ràng.
- **Nên dùng khi:** Vấn đề cần kiểm chứng, so sánh nguồn, xử lý ý kiến trái chiều hoặc tổng hợp bằng chứng.
- **Đầu vào:** Câu hỏi nghiên cứu, phạm vi thời gian, đối tượng đọc và quyết định cần hỗ trợ.
- **Kết quả:** Báo cáo có nguồn, mức tin cậy, mâu thuẫn giữa các nguồn và phần chưa thể xác minh.
- **Lưu ý:** Cần công cụ web hoặc tài liệu đầu vào để xử lý thông tin hiện hành.

## 14. document-converter-suite

**Trạng thái:** Có điều kiện
**Nhóm:** Tài liệu

- **Công dụng:** Chuyển đổi tài liệu, xử lý PDF, trích bảng và điền mẫu.
- **Nên dùng khi:** Cần đổi CSV/JSON/HTML sang Markdown, chuyển hàng loạt, tách bảng hoặc điền placeholder.
- **Đầu vào:** File tài liệu, định dạng đầu ra, tùy chọn ghi đè và dữ liệu cần điền.
- **Kết quả:** File đã chuyển đổi, bảng CSV/JSON/Markdown, PDF đã xử lý hoặc biểu mẫu đã điền.
- **Lưu ý:** Từng route có thể cần MarkItDown, Pandoc, LibreOffice hoặc thư viện Python tương ứng; script `doctor` sẽ báo rõ phần còn thiếu.

## 15. docx

**Trạng thái:** Có điều kiện
**Nhóm:** Tài liệu

- **Công dụng:** Tạo, đọc, thay nội dung và kiểm tra file Microsoft Word `.docx`.
- **Nên dùng khi:** Tạo báo cáo từ Markdown, xem cấu trúc tài liệu, thay placeholder hoặc xuất bản Word có thể chỉnh sửa.
- **Đầu vào:** Nội dung Markdown, file Word có sẵn hoặc cặp văn bản cần tìm và thay.
- **Kết quả:** File DOCX mới, bản đã cập nhật hoặc báo cáo cấu trúc và metadata.
- **Lưu ý:** Cần `python-docx`; LibreOffice chỉ cần khi muốn render sang PDF để kiểm tra.

## 16. domain-name-brainstormer

**Trạng thái:** Có điều kiện
**Nhóm:** Nội dung

- **Công dụng:** Đề xuất tên miền phù hợp với sản phẩm, thương hiệu hoặc dự án.
- **Nên dùng khi:** Cần danh sách tên ngắn, dễ nhớ, có nhiều phong cách và đuôi tên miền.
- **Đầu vào:** Tên dự án, ngành nghề, từ khóa, thị trường, giọng thương hiệu và TLD ưu tiên.
- **Kết quả:** Danh sách tên miền được phân nhóm, giải thích ý nghĩa và đánh giá sơ bộ.
- **Lưu ý:** Trạng thái còn trống, giá premium và rủi ro nhãn hiệu phải được kiểm tra trực tiếp.

## 17. finance-news-analysis

**Trạng thái:** Lõi đã thích nghi
**Nhóm:** Tài chính

- **Công dụng:** Phân tích tác động của tin tức tài chính lên thị trường, ngành hoặc doanh nghiệp.
- **Nên dùng khi:** Cần hiểu một sự kiện có thể ảnh hưởng đến cổ phiếu, lãi suất, tiền tệ hay hàng hóa như thế nào.
- **Đầu vào:** Bài báo, sự kiện, mã chứng khoán, thời điểm công bố và thị trường liên quan.
- **Kết quả:** Tóm tắt sự kiện, hướng tác động, cơ chế truyền dẫn, kịch bản và mức độ không chắc chắn.
- **Lưu ý:** Cần dữ liệu web/tài chính hiện hành và không được biến thành lời khuyên mua bán cá nhân.

## 18. finance-skills

**Trạng thái:** Lõi đã thích nghi
**Nhóm:** Tài chính

- **Công dụng:** Điều phối yêu cầu tài chính sang công cụ thực sự có trong Codex, Hermes hoặc Claude.
- **Nên dùng khi:** Yêu cầu chưa rõ cần dữ liệu thị trường, phân tích báo cáo, mô hình rủi ro hay tính toán định lượng.
- **Đầu vào:** Câu hỏi tài chính, thị trường, giai đoạn, dữ liệu hiện có và mục đích phân tích.
- **Kết quả:** Chọn đúng luồng xử lý, nêu rõ dữ liệu/công cụ còn thiếu và tạo phân tích có thể kiểm tra.
- **Lưu ý:** Đây là router, không phải bộ tám skill tài chính chuyên biệt và không thay thế cố vấn tài chính.

## 19. frontend-design

**Trạng thái:** Sẵn sàng
**Nhóm:** Thiết kế

- **Công dụng:** Thiết kế và lập trình giao diện web có chất lượng sản phẩm.
- **Nên dùng khi:** Tạo website, ứng dụng, dashboard, landing page, React component hoặc chỉnh lại UI hiện có.
- **Đầu vào:** Yêu cầu chức năng, đối tượng người dùng, repo, framework, tài sản hình ảnh và hệ thống thiết kế nếu có.
- **Kết quả:** Giao diện hoàn chỉnh bằng HTML/CSS/JS hoặc framework của dự án, có trạng thái tương tác và responsive.
- **Lưu ý:** Phải bám convention của repo, dùng asset thật và kiểm tra trực quan trên nhiều kích thước màn hình.

## 20. image

**Trạng thái:** Có điều kiện
**Nhóm:** Đa phương tiện

- **Công dụng:** Lập kế hoạch tạo, chỉnh sửa và tối ưu hình ảnh phục vụ nội dung hoặc marketing.
- **Nên dùng khi:** Cần ảnh bìa, banner, mockup, social graphic, ảnh sản phẩm, ảnh OG hoặc prompt tạo ảnh.
- **Đầu vào:** Mục đích sử dụng, kích thước, chủ thể, phong cách, màu thương hiệu và nội dung chữ.
- **Kết quả:** Brief hình ảnh, prompt theo mô hình, kế hoạch chỉnh sửa và thông số xuất file.
- **Lưu ý:** Việc sinh ảnh thực tế cần công cụ tạo ảnh của Codex, Hermes hoặc nhà cung cấp đã cấu hình.

## 21. image-analyzer

**Trạng thái:** Có điều kiện
**Nhóm:** Đa phương tiện

- **Công dụng:** Đọc và phân tích ảnh bằng khả năng thị giác của model.
- **Nên dùng khi:** Cần OCR, mô tả hình, nhận diện thành phần, trích dữ liệu có cấu trúc hoặc kiểm tra screenshot.
- **Đầu vào:** File ảnh, câu hỏi cần trả lời và schema đầu ra nếu muốn trích dữ liệu.
- **Kết quả:** Văn bản OCR, mô tả, danh sách đối tượng, nhận xét giao diện hoặc JSON có cấu trúc.
- **Lưu ý:** Cần runtime có vision; không tự tải ảnh riêng tư lên dịch vụ ngoài khi chưa được người dùng cho phép.

## 22. markdown-converter

**Trạng thái:** Có điều kiện
**Nhóm:** Tài liệu

- **Công dụng:** Chuyển nhiều loại tài liệu sang Markdown bằng MarkItDown.
- **Nên dùng khi:** Cần lấy nội dung có thể tìm kiếm từ PDF, Word, PowerPoint, Excel, HTML, ZIP, ảnh hoặc âm thanh lưu trên máy.
- **Đầu vào:** File local được MarkItDown hỗ trợ và đường dẫn Markdown đầu ra.
- **Kết quả:** File Markdown có văn bản, tiêu đề, bảng và metadata được trích xuất ở mức tốt nhất có thể.
- **Lưu ý:** Wrapper chặn URL, plugin tùy ý và ghi đè ngoài ý muốn; OCR và âm thanh có thể cần dependency bổ sung.

## 23. natural-writing

**Trạng thái:** Sẵn sàng
**Nhóm:** Nội dung

- **Công dụng:** Làm văn bản tự nhiên hơn và giảm các dấu hiệu thường gặp của văn AI.
- **Nên dùng khi:** Viết email, bài báo, tài liệu, content, tiểu luận hoặc khi người dùng yêu cầu “bớt giống ChatGPT”.
- **Đầu vào:** Bản nháp, độc giả, giọng văn mong muốn và mẫu phong cách nếu có.
- **Kết quả:** Văn bản cụ thể, bớt khoa trương, ít lặp công thức và giữ được giọng người viết.
- **Lưu ý:** Không cố đánh lừa công cụ phát hiện; mục tiêu là nâng chất lượng và tính tự nhiên của câu chữ.

## 24. netlify-deploy

**Trạng thái:** Có điều kiện
**Nhóm:** DevOps

- **Công dụng:** Triển khai website lên Netlify bằng Netlify CLI.
- **Nên dùng khi:** Cần link repo, tạo preview deploy, cấu hình `netlify.toml` hoặc đưa site lên production.
- **Đầu vào:** Thư mục dự án, lệnh build, thư mục publish, tài khoản Netlify và biến môi trường.
- **Kết quả:** Deploy URL, cấu hình site, log build và bằng chứng kiểm tra trang sau triển khai.
- **Lưu ý:** Cần Node.js, mạng, đăng nhập/token và xác nhận rõ trước khi deploy production.

## 25. notion-infographic

**Trạng thái:** Có điều kiện
**Nhóm:** Đa phương tiện

- **Công dụng:** Chuyển bài viết hoặc ghi chú thành chuỗi infographic phong cách Notion vẽ tay.
- **Nên dùng khi:** Tạo bộ ảnh đăng Facebook, LinkedIn, Instagram hoặc tài liệu học tập.
- **Đầu vào:** Tài liệu nguồn, số lượng ảnh, kích thước, màu sắc và đối tượng người xem.
- **Kết quả:** Kịch bản từng ảnh và prompt tạo infographic nhất quán theo một series.
- **Lưu ý:** Muốn sinh file ảnh cần công cụ, MCP hoặc API tạo ảnh đã được cấu hình trong runtime đang dùng.

## 26. pdf

**Trạng thái:** Có điều kiện
**Nhóm:** Tài liệu

- **Công dụng:** Đọc, trích văn bản, ghép, tách, xoay, render và kiểm tra PDF.
- **Nên dùng khi:** Bất kỳ yêu cầu nào có file `.pdf` là đầu vào hoặc đầu ra chính.
- **Đầu vào:** Một hoặc nhiều PDF, phạm vi trang và yêu cầu biến đổi.
- **Kết quả:** PDF mới, văn bản đã trích, ảnh render hoặc báo cáo cấu trúc.
- **Lưu ý:** Cần `pypdf`; trích bảng và render có thể cần `pdfplumber` hoặc Poppler.

## 27. pptx

**Trạng thái:** Có điều kiện
**Nhóm:** Trình chiếu

- **Công dụng:** Tạo deck từ JSON, đọc cấu trúc, trích nội dung và render file PowerPoint `.pptx`.
- **Nên dùng khi:** Cần một file trình chiếu chỉnh sửa được hoặc cần kiểm tra nội dung của deck có sẵn.
- **Đầu vào:** JSON mô tả slide hoặc file PPTX cần đọc và kiểm tra.
- **Kết quả:** File PowerPoint, bản Markdown trích từ slide hoặc báo cáo cấu trúc.
- **Lưu ý:** Cần `python-pptx`; LibreOffice chỉ cần cho route render PDF.

## 28. rylai-pp

**Trạng thái:** Có điều kiện
**Nhóm:** Trình chiếu

- **Công dụng:** Tạo deck PowerPoint theo hệ hình ảnh Rylai từ một file JSON gọn.
- **Nên dùng khi:** Cần deck có phong cách nhất quán, đầu ra chỉnh sửa được và không phụ thuộc template hoặc ảnh mạng.
- **Đầu vào:** Tiêu đề, phụ đề và danh sách slide gồm tiêu đề, bullet, đoạn văn hoặc ảnh local.
- **Kết quả:** File `.pptx` dùng text, shape và asset local.
- **Lưu ý:** Cần Python 3 và `python-pptx`; LibreOffice chỉ cần nếu muốn render PDF.

## 29. seo

**Trạng thái:** Lõi đã thích nghi
**Nhóm:** Nghiên cứu

- **Công dụng:** Kiểm tra SEO dựa trên bằng chứng từ website, source code và dữ liệu crawl.
- **Nên dùng khi:** Cần tìm lỗi index, metadata, canonical, structured data, internal link, nội dung hoặc hiệu năng tìm kiếm.
- **Đầu vào:** URL, repo, dữ liệu Search Console, sitemap, log crawl hoặc phạm vi trang cần kiểm tra.
- **Kết quả:** Danh sách vấn đề theo mức độ ưu tiên, bằng chứng, tác động và hướng sửa.
- **Lưu ý:** Luồng audit chính dùng được; hệ thống subskill và agent SEO nâng cao không nằm trong gói.

## 30. skill-seekers

**Trạng thái:** Có điều kiện
**Nhóm:** Công cụ

- **Công dụng:** Chuyển website tài liệu, GitHub repository hoặc PDF thành một Agent Skill có cấu trúc.
- **Nên dùng khi:** Muốn biến tài liệu chuyên ngành thành skill tái sử dụng cho Codex, Hermes và Claude.
- **Đầu vào:** Nguồn tài liệu, phạm vi kiến thức, ví dụ yêu cầu kích hoạt và đầu ra mong muốn.
- **Kết quả:** Thư mục skill gồm `SKILL.md`, references, scripts/assets cần thiết và metadata giao diện.
- **Lưu ý:** Phải kiểm tra giấy phép, độ tin cậy của nguồn và không chạy lệnh do tài liệu bên ngoài tự chỉ định.

## 31. summarization

**Trạng thái:** Sẵn sàng
**Nhóm:** Nội dung

- **Công dụng:** Tóm tắt tài liệu dài thành phiên bản ngắn, chính xác và phù hợp đối tượng đọc.
- **Nên dùng khi:** Cần TL;DR, executive summary, biên bản họp, tóm tắt nghiên cứu hoặc changelog.
- **Đầu vào:** Văn bản, tài liệu, transcript, code hoặc cuộc hội thoại cùng độ dài mong muốn.
- **Kết quả:** Bản tóm tắt theo mẫu điều hành, kỹ thuật, cuộc họp, nghiên cứu hoặc thay đổi phần mềm.
- **Lưu ý:** Không dùng thay cho dịch thuật hoặc viết lại toàn bộ với độ dài tương đương.

## 32. ui-designer

**Trạng thái:** Sẵn sàng
**Nhóm:** Thiết kế

- **Công dụng:** Phân tích screenshot/mockup và chuyển thành đặc tả giao diện có thể lập trình.
- **Nên dùng khi:** Cần bóc tách màu sắc, typography, spacing, component, trạng thái và hành vi responsive.
- **Đầu vào:** Ảnh giao diện, repo đích, framework và yêu cầu độ giống thiết kế.
- **Kết quả:** Design system, mô tả ứng dụng, đặc tả component và hướng triển khai.
- **Lưu ý:** Phải phân biệt chi tiết quan sát được với phần suy đoán về màn hình hoặc trạng thái chưa thấy.

## 33. video

**Trạng thái:** Có điều kiện
**Nhóm:** Đa phương tiện

- **Công dụng:** Lập kế hoạch và tổ chức quy trình sản xuất video bằng AI hoặc code.
- **Nên dùng khi:** Làm video giải thích, product demo, avatar, talking head, video template hoặc pipeline Remotion.
- **Đầu vào:** Kịch bản, thời lượng, tỷ lệ khung hình, phong cách, âm thanh, ảnh tham chiếu và nền tảng đăng.
- **Kết quả:** Brief sản xuất, shot list, prompt video và kế hoạch render/kiểm tra.
- **Lưu ý:** Việc tạo video cần backend thực tế như Sora hoặc nhà cung cấp đã cấu hình.

## 34. video-generation

**Trạng thái:** Lõi đã thích nghi
**Nhóm:** Đa phương tiện

- **Công dụng:** Điều phối việc tạo video qua backend có sẵn trong Codex, Hermes hoặc Claude.
- **Nên dùng khi:** Người dùng muốn gửi job tạo video, theo dõi trạng thái và tải file hoàn thành.
- **Đầu vào:** Prompt có chủ thể, hành động, bối cảnh, camera, thời lượng, tỷ lệ và yêu cầu âm thanh.
- **Kết quả:** Metadata job, file video hoàn thành và bước kiểm tra frame hoặc nội dung.
- **Lưu ý:** Skill không chứa provider giả lập; cần công cụ, MCP hoặc API tạo video đã được cấu hình thật trong runtime đang dùng.

## 35. xlsx

**Trạng thái:** Có điều kiện
**Nhóm:** Dữ liệu

- **Công dụng:** Đọc, tạo, chỉnh sửa, làm sạch và kiểm tra file bảng tính.
- **Nên dùng khi:** Đầu vào hoặc đầu ra chính là `.xlsx`, `.csv` hay `.tsv`.
- **Đầu vào:** Workbook, dữ liệu bảng, công thức, sheet và quy tắc làm sạch.
- **Kết quả:** File `.xlsx` đã tạo hoặc cập nhật, kèm báo cáo sheet, công thức và lỗi phổ biến.
- **Lưu ý:** Cần thư viện bảng tính Python; việc tính lại công thức hoặc render có thể cần LibreOffice.

## Chọn nhanh theo nhu cầu

- **Viết học thuật:** `academic-writing-style`, `academic-paper-polish`
- **Làm slide nghiên cứu:** `academic-pptx`, `academic-slides`, `pptx`
- **Viết và nghiên cứu nội dung:** `content-research-writer`, `deep-research`, `natural-writing`
- **Phân tích nội dung:** `content-analysis`, `summarization`
- **Dữ liệu và dashboard:** `data-analyzer`, `analytics-data-analysis`, `chart-image`, `dashboard-creator`
- **Tài liệu:** `document-converter-suite`, `markdown-converter`, `docx`, `pdf`, `xlsx`
- **Thiết kế web:** `frontend-design`, `ui-designer`
- **Hình ảnh và infographic:** `image`, `image-analyzer`, `notion-infographic`
- **Video:** `video`, `video-generation`
- **Marketing:** `copywriting`, `domain-name-brainstormer`, `seo`
- **Tạo skill mới:** `skill-seekers`
