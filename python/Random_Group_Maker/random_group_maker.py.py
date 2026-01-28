import random
import os

def make_group(member_list, members_per_group=4):
    """
    명단을 받아 무작위로 조를 나누고 딕셔너리 형태로 반환합니다.
    """
    # [1. 예외 처리]: 리스트가 비어 있거나 조 크기가 잘못된 경우 방어
    if not member_list:
        print("에러: 명단이 비어 있습니다.")
        return {}
    
    if members_per_group <= 0:
        print("에러: 조 인원 설정은 1명 이상이어야 합니다.")
        return {}

    # 원본 리스트 복사 및 섞기
    shuffled_members = member_list[:]
    random.shuffle(shuffled_members)

    assigned_groups = {}
    group_number = 1

    # 조 나누기 로직
    for i in range(0, len(shuffled_members), members_per_group):
        group_key = f"{group_number}조"
        group_members = shuffled_members[i:i + members_per_group]
        
        assigned_groups[group_key] = group_members
        
        # 출력 가독성 개선
        print(f"{group_key} : {', '.join(group_members)}")
        group_number += 1
        
    return assigned_groups

def save_to_file(file_name, data):
    """
    [3. 데이터의 영속성]: 결과를 파일로 저장하는 기능
    """
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            for group, members in data.items():
                f.write(f"{group}: {', '.join(members)}\n")
        print(f"\n성공: 결과가 '{file_name}'에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

# --- 메인 실행부 ---

# 기존 명단
candidate_names = [
    '강성신', '김수왕', '김아네스', '김진우', '남건우', 
    '박세형', '박지훈', '배은하', '사비카', '서현석', 
    '이상준', '이상호', '이종혁', '이지선', '이채훈', 
    '주현지', '최유리', '하재연', '한다솔', '황희연'
]

# 실행
print("--- 랜덤 조 구성 결과 ---")
final_result = make_group(candidate_names, members_per_group=4)

# 결과 저장
if final_result:
    save_to_file("group_result.txt", final_result)