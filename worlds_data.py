# ==========================================
# FILE: worlds_data.py
# Nơi lưu trữ toàn bộ nội dung kịch bản học tập, báo lỗi và đồ họa SVG
# ==========================================

WORLDS = {
    "refraction_world": {
        "name": "Đại Dương Ảo Ảnh",
        "emoji": "🌊",
        "subtitle": "Khúc Xạ Ánh Sáng",
        "color": "#00d4ff",
        "css_class": "refraction",
        "badge_bg": "#00d4ff22",
        "badge_border": "#00d4ff55",
        "description": "Nơi ánh sáng bị bẻ cong khi bước qua ranh giới giữa các môi trường. Hãy cẩn thận, mắt bạn sẽ đánh lừa bạn!",
        "scenarios": [
            {
                "id": "re1",
                "concept": "Sự bẻ cong tia sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một tia sáng khi đi từ không khí vào mặt nước phẳng lặng sẽ luôn giữ nguyên đường thẳng ban đầu vì ánh sáng có tính chất truyền thẳng tuyệt đối trong mọi tình huống.",
                "correct_answer": "Sai",
                "explanation": "Ánh sáng chỉ truyền thẳng trong môi trường ĐỒNG TÍNH. Khi đi qua mặt phân cách giữa hai môi trường có chiết suất khác nhau (như không khí và nước), tốc độ ánh sáng thay đổi khiến tia sáng bị bẻ cong. Hiện tượng này gọi là khúc xạ.",
                "ai_context": "Học sinh hiểu sai về tính truyền thẳng của ánh sáng khi qua mặt phân cách. Concept: Khúc xạ là sự thay đổi phương truyền do thay đổi tốc độ ánh sáng giữa 2 môi trường.",
                "misconception_msg": "concept_confusion: Bỏ qua sự thay đổi tốc độ ánh sáng giữa 2 môi trường, tin rằng ánh sáng không bao giờ bị bẻ cong.",
                "svg_code": """
                <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
                  <rect x="0" y="100" width="400" height="100" fill="#00d4ff33" />
                  <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
                  <line x1="200" y1="20" x2="200" y2="180" stroke="#ffffff55" stroke-dasharray="5,5" />
                  <line x1="50" y1="20" x2="200" y2="100" stroke="#ffca28" stroke-width="3" class="ray" />
                  <line x1="200" y1="100" x2="350" y2="180" stroke="#ffffff33" stroke-width="1" stroke-dasharray="2,2" />
                  <line x1="200" y1="100" x2="260" y2="180" stroke="#ffca28" stroke-width="3" class="ray" />
                  <text x="10" y="90" fill="#ffffff" font-size="12" font-family="sans-serif">KHÔNG KHÍ (n1)</text>
                  <text x="10" y="120" fill="#00d4ff" font-size="12" font-family="sans-serif">NƯỚC (n2 > n1)</text>
                  <path d="M 180 89 A 20 20 0 0 1 200 80" fill="none" stroke="#ffca28" stroke-width="1"/>
                  <path d="M 200 120 A 20 20 0 0 1 215 120" fill="none" stroke="#ffca28" stroke-width="1"/>
                </svg>
                <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Tia sáng bị bẻ cong về phía pháp tuyến khi đi vào môi trường đặc hơn.</div>
                """
            },
            {
                "id": "re2",
                "concept": "Độ sâu ảo (Apparent Depth)",
                "statement": "🔴 TÌNH HUỐNG LỖI: Khi bạn nhìn một đồng xu dưới đáy hồ bơi, vị trí bạn nhìn thấy chính là vị trí thực tế của đồng xu đó. Mắt con người luôn nhìn thấy vật thể đúng nơi chúng tọa lạc.",
                "correct_answer": "Sai",
                "explanation": "Do hiện tượng khúc xạ, các tia sáng từ đồng xu dưới nước khi đi ra ngoài không khí sẽ bị lệch xa pháp tuyến hơn. Mắt người có thói quen nội suy ngược tia sáng theo đường thẳng, khiến chúng ta thấy một 'ảnh ảo' của đồng xu nằm nông hơn vị trí thật sự của nó dưới đáy hồ.",
                "ai_context": "Học sinh nhầm lẫn giữa ảnh ảo và vật thật dưới nước. Concept: Ảnh ảo nằm cao hơn (nông hơn) vật thật khi nhìn từ môi trường chiết suất thấp vào môi trường chiết suất cao.",
                "misconception_msg": "real_vs_virtual: Áp đặt trực giác đời thường, nhầm lẫn ảnh ảo do khúc xạ tạo ra thành vật thật.",
                "svg_code": """
                <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
                  <rect x="0" y="80" width="400" height="120" fill="#00d4ff33" />
                  <line x1="0" y1="80" x2="400" y2="80" stroke="#00d4ff" stroke-width="2" />
                  <circle cx="200" cy="180" r="10" fill="#ffca28" />
                  <text x="220" y="185" fill="#ffffff" font-size="12" font-family="sans-serif">Vị trí thật</text>
                  <circle cx="160" cy="120" r="10" fill="#ffca2855" class="pulse"/>
                  <text x="180" y="125" fill="#00d4ff" font-size="12" font-family="sans-serif">Vị trí ảo (Mắt thấy)</text>
                  <line x1="200" y1="180" x2="140" y2="80" stroke="#ffffff88" stroke-width="2" />
                  <line x1="140" y1="80" x2="100" y2="20" stroke="#ffffff" stroke-width="2" class="ray" />
                  <line x1="140" y1="80" x2="160" y2="120" stroke="#00d4ff88" stroke-dasharray="4,4" />
                  <path d="M 80 10 Q 100 -5 120 10 Q 100 25 80 10 Z" fill="none" stroke="#ffffff" stroke-width="2"/>
                  <circle cx="100" cy="10" r="4" fill="#ffffff" />
                </svg>
                <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Mắt nhìn theo đường thẳng kéo dài của tia khúc xạ tạo ra ảnh ảo.</div>
                """
            },
            {
                "id": "re3",
                "concept": "Phản xạ toàn phần",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một bóng đèn đặt dưới đáy bể bơi có thể chiếu tia sáng thoát ra ngoài không khí theo MỌI HƯỚNG, bất kể bạn chiếu góc nghiêng gắt đến mức nào đi chăng nữa.",
                "correct_answer": "Sai",
                "explanation": "Khi tia sáng truyền từ môi trường chiết suất LỚN (nước) sang môi trường chiết suất NHỎ (không khí), nếu góc tới vượt quá một giá trị gọi là 'góc tới hạn', tia sáng sẽ KHÔNG THỂ thoát ra ngoài mà bị phản xạ ngược trở lại hoàn toàn vào trong nước. Hiện tượng này gọi là Phản xạ toàn phần.",
                "ai_context": "Học sinh chưa biết về góc tới hạn và hiện tượng phản xạ toàn phần. Concept: Phản xạ toàn phần chỉ xảy ra khi ánh sáng đi từ môi trường đặc sang loãng và góc tới vượt ngưỡng.",
                "misconception_msg": "missing_concept: Không biết về hiện tượng Phản xạ toàn phần và giới hạn của góc tới hạn.",
                "svg_code": """
                <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
                  <rect x="0" y="100" width="400" height="100" fill="#00d4ff33" />
                  <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
                  <line x1="200" y1="20" x2="200" y2="180" stroke="#ffffff55" stroke-dasharray="5,5" />
                  <circle cx="200" cy="180" r="6" fill="#ffca28" class="pulse"/>
                  
                  <line x1="200" y1="180" x2="180" y2="100" stroke="#ffffff55" stroke-width="1" />
                  <line x1="180" y1="100" x2="150" y2="20" stroke="#ffffff55" stroke-width="1" />
                  
                  <line x1="200" y1="180" x2="250" y2="100" stroke="#ffffff88" stroke-width="2" />
                  <line x1="250" y1="100" x2="380" y2="100" stroke="#ffffff88" stroke-width="2" />
                  
                  <line x1="200" y1="180" x2="280" y2="100" stroke="#ff4b4b" stroke-width="3" class="ray" />
                  <line x1="280" y1="100" x2="360" y2="180" stroke="#ff4b4b" stroke-width="3" class="ray" />
                  <text x="290" y="140" fill="#ff4b4b" font-size="12" font-family="sans-serif">Phản xạ toàn phần</text>
                </svg>
                <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Khi góc tới quá lớn, tia sáng không thể thoát ra ngoài môi trường.</div>
                """
            },
            {
                "id": "re4",
                "concept": "Chiết suất và Vận tốc",
                "statement": "🔴 TÌNH HUỐNG LỖI: Chiết suất của kim cương rất lớn (n ≈ 2.4). Điều này có nghĩa là ánh sáng khi bay vào bên trong viên kim cương sẽ tăng tốc và di chuyển nhanh gấp 2.4 lần so với khi bay trong chân không.",
                "correct_answer": "Sai",
                "explanation": "Ngược lại hoàn toàn! Chiết suất của một môi trường tỷ lệ NGHỊCH với tốc độ ánh sáng trong môi trường đó ($n = c/v$). Chiết suất càng lớn, ánh sáng di chuyển càng chậm. Trong kim cương, ánh sáng bị 'hãm' lại chỉ còn khoảng 124.000 km/s (thay vì 300.000 km/s). Sự chậm trễ này khiến nó bị khúc xạ cực mạnh, tạo ra vẻ lấp lánh.",
                "ai_context": "Học sinh nhầm lẫn mối quan hệ giữa chiết suất và vận tốc ánh sáng. Concept: Môi trường có chiết suất n càng lớn thì vận tốc truyền sáng v càng nhỏ.",
                "misconception_msg": "inverse_relation_error: Hiểu ngược mối quan hệ tỷ lệ nghịch giữa chiết suất và vận tốc truyền sáng.",
                "svg_code": ""  # Không dùng SVG cho câu này để tránh làm rối
            },
            {
                "id": "re5",
                "concept": "Sự Tán sắc ánh sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Ánh sáng trắng từ mặt trời là một màu đơn sắc. Khi đi qua một lăng kính thủy tinh, chất liệu thủy tinh đặc biệt của lăng kính đã tự động nhuộm màu cho tia sáng để tạo ra bảy sắc cầu vồng.",
                "correct_answer": "Sai",
                "explanation": "Lăng kính không tự nhuộm màu. Bản thân ánh sáng trắng đã là hỗn hợp của vô số dải màu. Vì mỗi màu có một chiết suất khác nhau đối với thủy tinh (màu tím bị bẻ cong nhiều nhất, màu đỏ ít nhất), lăng kính chỉ làm nhiệm vụ 'tách' các tia màu vốn đã có sẵn này ra thành các góc khác nhau, gọi là hiện tượng tán sắc.",
                "ai_context": "Học sinh hiểu sai bản chất ánh sáng trắng. Concept: Tán sắc là do chiết suất của môi trường phụ thuộc vào màu sắc (bước sóng) của ánh sáng.",
                "misconception_msg": "nature_of_light: Hiểu sai bản chất ánh sáng trắng, cho rằng nó là đơn sắc và bị lăng kính nhuộm màu.",
                "svg_code": """
                <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
                  <polygon points="200,40 120,160 280,160" fill="#ffffff11" stroke="#ffffff" stroke-width="2" />
                  <line x1="50" y1="130" x2="160" y2="100" stroke="#ffffff" stroke-width="4" class="ray" />
                  <text x="50" y="120" fill="#ffffff" font-size="10" font-family="sans-serif">Ánh sáng trắng</text>
                  
                  <line x1="160" y1="100" x2="240" y2="100" stroke="#ff4b4b" stroke-width="2" />
                  <line x1="160" y1="100" x2="250" y2="115" stroke="#00ff88" stroke-width="2" />
                  <line x1="160" y1="100" x2="260" y2="130" stroke="#9900ff" stroke-width="2" />
                  
                  <line x1="240" y1="100" x2="350" y2="60" stroke="#ff4b4b" stroke-width="2" class="ray"/>
                  <line x1="250" y1="115" x2="350" y2="100" stroke="#00ff88" stroke-width="2" class="ray"/>
                  <line x1="260" y1="130" x2="350" y2="140" stroke="#9900ff" stroke-width="2" class="ray"/>
                  
                  <text x="360" y="65" fill="#ff4b4b" font-size="10" font-family="sans-serif">ĐỎ (Ít lệch)</text>
                  <text x="360" y="145" fill="#9900ff" font-size="10" font-family="sans-serif">TÍM (Lệch nhiều)</text>
                </svg>
                <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Lăng kính bẻ cong các tia màu khác nhau với mức độ khác nhau.</div>
                """
            },
            {
                "id": "re6",
                "concept": "Thấu kính thiên văn",
                "statement": "🔴 TÌNH HUỐNG LỖI: Để kính thiên văn có thể phóng đại những hành tinh xa xôi, vật kính (thấu kính ở đầu kính) đơn thuần là một tấm kính phẳng có đục một lỗ tròn nhỏ để giới hạn lượng ánh sáng đi vào mắt.",
                "correct_answer": "Sai",
                "explanation": "Một kính phẳng không có khả năng tạo ảnh. Vật kính của kính thiên văn phải là một THẤU KÍNH HỘI TỤ (mặt lồi). Lợi dụng hiện tượng khúc xạ, độ cong của thấu kính bẻ cong đồng loạt các tia sáng song song chiếu tới từ các vì sao xa xôi, hội tụ chúng lại tại tiêu điểm để tạo ra một ảnh thật, sau đó dùng thị kính để phóng đại ảnh đó lên.",
                "ai_context": "Học sinh hiểu sai cơ chế tạo ảnh của thấu kính. Concept: Thấu kính hội tụ sử dụng sự khúc xạ qua bề mặt cong để bẻ gãy và gom tia sáng về một điểm.",
                "misconception_msg": "mechanism_error: Không hiểu cơ chế tạo ảnh bằng sự hội tụ tia sáng qua mặt cong của thấu kính.",
                "svg_code": """
                <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
                  <line x1="0" y1="100" x2="400" y2="100" stroke="#ffffff55" stroke-dasharray="5,5" />
                  <path d="M 200 40 Q 220 100 200 160 Q 180 100 200 40 Z" fill="#00d4ff33" stroke="#00d4ff" stroke-width="2" />
                  
                  <line x1="50" y1="60" x2="195" y2="60" stroke="#ffca28" stroke-width="2" class="ray" />
                  <line x1="50" y1="100" x2="200" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
                  <line x1="50" y1="140" x2="195" y2="140" stroke="#ffca28" stroke-width="2" class="ray" />
                  
                  <line x1="195" y1="60" x2="300" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
                  <line x1="200" y1="100" x2="350" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
                  <line x1="195" y1="140" x2="300" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
                  
                  <circle cx="300" cy="100" r="4" fill="#ff4b4b" class="pulse"/>
                  <text x="290" y="85" fill="#ff4b4b" font-size="12" font-family="sans-serif">Tiêu điểm</text>
                </svg>
                <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Vật kính hội tụ các tia sáng song song để tạo ảnh thật.</div>
                """
            }
        ]
    }
}
