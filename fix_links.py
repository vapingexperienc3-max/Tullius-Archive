import os

# 모든 하위 폴더를 샅샅이 뒤집니다.
ROOT = "."

print("🚑 초강력 세탁기 가동 시작...")

for root, dirs, files in os.walk(ROOT):
    for file in files:
        if file.lower().endswith(".html"):
            file_path = os.path.join(root, file)
            
            try:
                # 파일을 읽어서 내용 확인
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 'Tullius-ferry' 글자가 하나라도 발견되면 즉시 치환
                if "Tullius-ferry" in content:
                    # BeautifulSoup 대신 직접 문자열 치환을 사용하여 원본 포맷을 최대한 보존합니다.
                    new_content = content.replace("Tullius-ferry", "Tullius-Archive")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ 수술 완료 (화석 복구): {file_path}")
                    
            except Exception as e:
                print(f"❌ 에러 발생 ({file}): {e}")

print("🏁 모든 화석 파일 현대화 완료. 이제 404는 없습니다.")