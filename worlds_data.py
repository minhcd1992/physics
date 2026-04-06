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
                "statement": "Một tia sáng khi đi từ không khí vào mặt nước phẳng lặng sẽ luôn giữ nguyên đường thẳng ban đầu vì ánh sáng có tính chất truyền thẳng tuyệt đối trong mọi tình huống.",
                "correct_answer": "Sai",
                "explanation": "Ánh sáng chỉ truyền thẳng trong môi trường ĐỒNG TÍNH. Khi đi qua mặt phân cách giữa hai môi trường có chiết suất khác nhau (như không khí và nước), tốc độ ánh sáng thay đổi khiến tia sáng bị bẻ cong. Hiện tượng này gọi là khúc xạ.",
                "ai_context": "Học sinh hiểu sai về tính truyền thẳng của ánh sáng khi qua mặt phân cách. Concept: Khúc xạ là sự thay đổi phương truyền do thay đổi tốc độ ánh sáng giữa 2 môi trường.",
                "misconception_msg": "concept_confusion: Bỏ qua sự thay đổi tốc độ ánh sáng giữa 2 môi trường, tin rằng ánh sáng không bao giờ bị bẻ cong.",
                "svg_code": """
                <div style="text-align: center; margin-bottom: 1rem;">
                  <svg viewBox="0 0 400 220" width="100%" style="max-width: 500px;">
                    <rect x="0" y="100" width="400" height="120" fill="#00d4ff33" />
                    <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
                    <line x1="200" y1="20" x2="200" y2="200" stroke="#ffffff55" stroke-dasharray="5,5" />
                    
                    <line x1="50" y1="20" x2="200" y2="100" stroke="#ffca28" stroke-width="3" class="ray" />
                    <text x="50" y="45" fill="#ffca28" font-size="12" font-family="sans-serif">Tia Tới</text>
                    
                    <line x1="200" y1="100" x2="350" y2="180" stroke="#ffffff22" stroke-width="1" stroke-dasharray="3,3" />
                    <text x="250" y="180" fill="#ffffff22" font-size="10" font-family="sans-serif">Dự đoán: Truyền thẳng?</text>
                    
                    <line x1="200" y1="100" x2="260" y2="200" stroke="#00ff88" stroke-width="3" class="ray pulse" />
                    <text x="270" y="195" fill="#00ff88" font-size="12" font-family="sans-serif">Tia khúc xạ Thực tế!</text>
                    
                    <path d="M 180 89 A 20 20 0 0 1 200 80" fill="none" stroke="#ffca28" stroke-width="1"/>
                    <text x="175" y="75" fill="#ffca28" font-size="10">i</text>
                    
                    <path d="M 200 120 A 20 20 0 0 1 215 120" fill="none" stroke="#00ff88" stroke-width="1"/>
                    <text x="220" y="125" fill="#00ff88" font-size="10">r</text>
                    
                    <text x="10" y="90" fill="#ffffff" font-size="12" font-family="sans-serif">KHÔNG KHÍ (n loãng)</text>
                    <text x="10" y="120" fill="#00d4ff" font-size="12" font-family="sans-serif">NƯỚC (n đặc hơn)</text>
                  </svg>
                </div>
                """
            }
        ]
    }
}
