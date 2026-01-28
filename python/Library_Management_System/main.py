from models import Book, Member, Librarian, Library

# 1. 시립 도서관 네트워크 세팅
gangnam = Library("강남 시립 도서관")
hongdae = Library("홍대 시립 도서관")

admin = Librarian("최사서", "E-001")
member = Member("박지성", "M-001")

# 2. 도서 등록
b1 = Book("파이썬 기초", "강작가", "ISBN-001")
b2 = Book("클린 코드", "로버트", "ISBN-002")
b3 = Book("자료구조", "박교수", "ISBN-003")
b4 = Book("인공지능", "최박사", "ISBN-004")

admin.register_book(gangnam, b1)
admin.register_book(gangnam, b2)
admin.register_book(gangnam, b3)
admin.register_book(hongdae, b4)

print("\n" + "="*50)
print("테스트 1: [통합 대출 한도 테스트]")
print("="*50)
gangnam.process_loan(member, b1)
gangnam.process_loan(member, b2)
gangnam.process_loan(member, b3)
gangnam.process_loan(member, b4) # 여기서 한도 초과 메시지가 떠야 함

print("\n" + "="*50)
print("테스트 2: [소프트 딜리트 테스트]")
print("="*50)
gangnam.remove_book(b1) # b1 폐기 처리
gangnam.process_loan(member, b1) # 폐기된 책 대출 시도 (실패해야 함)