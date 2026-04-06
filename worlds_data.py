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
                "svg_type": "basic"
            },
            {
                "id": "re2",
                "concept": "Độ sâu ảo (Apparent Depth)",
                "statement": "🔴 TÌNH HUỐNG LỖI: Khi bạn nhìn một đồng xu dưới đáy hồ bơi, vị trí bạn nhìn thấy chính là vị trí thực tế của đồng xu đó. Mắt con người luôn nhìn thấy vật thể đúng nơi chúng tọa lạc.",
                "correct_answer": "Sai",
                "explanation": "Do hiện tượng khúc xạ, các tia sáng từ đồng xu dưới nước khi đi ra ngoài không khí sẽ bị lệch xa pháp tuyến hơn. Mắt người có thói quen nội suy ngược tia sáng theo đường thẳng, khiến chúng ta thấy một 'ảnh ảo' của đồng xu nằm nông hơn vị trí thật sự của nó dưới đáy hồ.",
                "ai_context": "Học sinh nhầm lẫn giữa ảnh ảo và vật thật dưới nước. Concept: Ảnh ảo nằm cao hơn (nông hơn) vật thật khi nhìn từ môi trường chiết suất thấp vào môi trường chiết suất cao.",
                "svg_type": "depth"
            },
            {
                "id": "re3",
                "concept": "Phản xạ toàn phần",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một bóng đèn đặt dưới đáy bể bơi có thể chiếu tia sáng thoát ra ngoài không khí theo MỌI HƯỚNG, bất kể bạn chiếu góc nghiêng gắt đến mức nào đi chăng nữa.",
                "correct_answer": "Sai",
                "explanation": "Khi tia sáng truyền từ môi trường chiết suất LỚN (nước) sang môi trường chiết suất NHỎ (không khí), nếu góc tới vượt quá một giá trị gọi là 'góc tới hạn', tia sáng sẽ KHÔNG THỂ thoát ra ngoài mà bị phản xạ ngược trở lại hoàn toàn vào trong nước. Hiện tượng này gọi là Phản xạ toàn phần.",
                "ai_context": "Học sinh chưa biết về góc tới hạn và hiện tượng phản xạ toàn phần. Concept: Phản xạ toàn phần chỉ xảy ra khi ánh sáng đi từ môi trường đặc sang loãng và góc tới vượt ngưỡng.",
                "svg_type": "total_reflection"
            },
            {
                "id": "re4",
                "concept": "Chiết suất và Vận tốc",
                "statement": "🔴 TÌNH HUỐNG LỖI: Chiết suất của kim cương rất lớn (n ≈ 2.4). Điều này có nghĩa là ánh sáng khi bay vào bên trong viên kim cương sẽ tăng tốc và di chuyển nhanh gấp 2.4 lần so với khi bay trong chân không.",
                "correct_answer": "Sai",
                "explanation": "Ngược lại hoàn toàn! Chiết suất của một môi trường tỷ lệ NGHỊCH với tốc độ ánh sáng trong môi trường đó ($n = c/v$). Chiết suất càng lớn, ánh sáng di chuyển càng chậm. Trong kim cương, ánh sáng bị 'hãm' lại chỉ còn khoảng 124.000 km/s (thay vì 300.000 km/s). Sự chậm trễ này khiến nó bị khúc xạ cực mạnh, tạo ra vẻ lấp lánh.",
                "ai_context": "Học sinh nhầm lẫn mối quan hệ giữa chiết suất và vận tốc ánh sáng. Concept: Môi trường có chiết suất n càng lớn thì vận tốc truyền sáng v càng nhỏ.",
                "svg_type": "none"
            },
            {
                "id": "re5",
                "concept": "Sự Tán sắc ánh sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Ánh sáng trắng từ mặt trời là một màu đơn sắc. Khi đi qua một lăng kính thủy tinh, chất liệu thủy tinh đặc biệt của lăng kính đã tự động nhuộm màu cho tia sáng để tạo ra bảy sắc cầu vồng.",
                "correct_answer": "Sai",
                "explanation": "Lăng kính không tự nhuộm màu. Bản thân ánh sáng trắng đã là hỗn hợp của vô số dải màu. Vì mỗi màu có một chiết suất khác nhau đối với thủy tinh (màu tím bị bẻ cong nhiều nhất, màu đỏ ít nhất), lăng kính chỉ làm nhiệm vụ 'tách' các tia màu vốn đã có sẵn này ra thành các góc khác nhau, gọi là hiện tượng tán sắc.",
                "ai_context": "Học sinh hiểu sai bản chất ánh sáng trắng. Concept: Tán sắc là do chiết suất của môi trường phụ thuộc vào màu sắc (bước sóng) của ánh sáng.",
                "svg_type": "prism"
            },
            {
                "id": "re6",
                "concept": "Thấu kính thiên văn",
                "statement": "🔴 TÌNH HUỐNG LỖI: Để kính thiên văn có thể phóng đại những hành tinh xa xôi, vật kính (thấu kính ở đầu kính) đơn thuần là một tấm kính phẳng có đục một lỗ tròn nhỏ để giới hạn lượng ánh sáng đi vào mắt.",
                "correct_answer": "Sai",
                "explanation": "Một kính phẳng không có khả năng tạo ảnh. Vật kính của kính thiên văn phải là một THẤU KÍNH HỘI TỤ (mặt lồi). Lợi dụng hiện tượng khúc xạ, độ cong của thấu kính bẻ cong đồng loạt các tia sáng song song chiếu tới từ các vì sao xa xôi, hội tụ chúng lại tại tiêu điểm để tạo ra một ảnh thật, sau đó dùng thị kính để phóng đại ảnh đó lên.",
                "ai_context": "Học sinh hiểu sai cơ chế tạo ảnh của thấu kính. Concept: Thấu kính hội tụ sử dụng sự khúc xạ qua bề mặt cong để bẻ gãy và gom tia sáng về một điểm.",
                "svg_type": "lens"
            }
        ]
    }
}

